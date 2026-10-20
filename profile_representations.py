"""Step 6: reduce every data representation to one canonical description of the entity.

    uv run python profile_representations.py Q7245

For each identifier property it reads the data files under data/<QID>/representations/<key>/ and
writes data/<QID>/analysis/profiles/<P>.json:

    formats          which formats the site served (rdf-xml, json-ld, marcxml, json ...)
    vocabularies     RDF namespaces / MARC / MADS / EAC used, with predicate counts
    elements         canonical elements -> list of {value, lang, via, file}: name_preferred,
                     name_variant, given_name, family_name, birth_date, death_date, birth_place,
                     death_place, gender, occupation, field_of_activity, nationality, language,
                     description, work, related_agent, same_as, identifier, image, source,
                     record_created, record_modified, license
    unmapped         predicates / fields seen on the entity that are not mapped to an element
    json_profiles    for ad-hoc JSON/XML files: key paths, sample values and entity signals
                     (input for the LLM extraction step)

RDF (rdflib), MARC (pymarc), MADS XML and EAC-CPF are handled deterministically.
"""

import collections
import csv
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pymarc
import rdflib
from rdflib.namespace import RDF, RDFS, SKOS

ENTITY_TERMS = ("twain", "clemens", "1835", "1910", "тве", "吐温", "トウェイン", "טוין", "تواين")
ENTITY_NAME_SETS = []   # set in main() from entity.json: one token-set per label/alias ("mark twain" -> {"mark", "twain"})
NAME_TOKENS = set()     # set in main(): entity_name_tokens(entity)


def strong_entity_name(text):
    """True when the text contains one of the entity's labels/aliases in full (all its tokens) - relatives who share the
    surname ('Clara Clemens') do not pass, 'Clemens, Samuel Langhorne, 1835-1910' does."""
    low = (text or "").lower()
    if not ENTITY_NAME_SETS:
        return any(t in low for t in ENTITY_TERMS)
    return any(all(t in low for t in ns) for ns in ENTITY_NAME_SETS)


def mentions_terms(text):
    return mentions_entity(text or "", NAME_TOKENS) if NAME_TOKENS else any(t in (text or "").lower() for t in ENTITY_TERMS)

# predicate local-name -> canonical element (namespace-agnostic; the namespace is recorded separately)
PRED_MAP = {
    "name_preferred": {"prefLabel", "label", "name", "authoritativeLabel", "preferredNameForThePerson", "preferredName",
                       "preferredNameEntityForThePerson", "title", "authorizedAccessPoint", "headline", "fullName", "P50411", "P50385",
                       "preferredLabel", "hasPreferredLabel", "nameOfThePerson"},
    "name_variant": {"altLabel", "variantNameForThePerson", "variantLabel", "hasVariant", "alternateName", "variantName",
                     "alternativeName", "hiddenLabel", "variantAccessPoint", "variantNameEntityForThePerson", "alias", "P50409",
                     "alternativeLabel", "hasAlternativeLabel", "otherName", "nickname"},
    "given_name": {"givenName", "forename", "firstName", "P50392", "prefixOfTheName"},
    "family_name": {"familyName", "surname", "lastName", "P50383"},
    "pseudonym": {"pseudonym", "pseudonymFor", "realIdentity", "P50358"},
    "birth_date": {"birthDate", "dateOfBirth", "birth", "P50121", "born", "yearOfBirth"},
    "death_date": {"deathDate", "dateOfDeath", "death", "P50120", "died", "yearOfDeath"},
    "birth_place": {"birthPlace", "placeOfBirth", "P50119", "bornIn"},
    "death_place": {"deathPlace", "placeOfDeath", "P50118", "diedIn"},
    "activity_place": {"placeOfActivity", "placeOfResidence", "homeLocation", "workLocation", "P50115", "P50109", "location"},
    "gender": {"gender", "sex", "P50116"},
    "occupation": {"hasOccupation", "occupation", "professionOrOccupation", "jobTitle", "P50104", "profession", "activity"},
    "field_of_activity": {"fieldOfActivity", "P50100", "subjectArea"},
    "nationality": {"nationality", "geographicAreaCode", "associatedCountry", "countryOfCitizenship", "country", "P50097", "citizenship"},
    "language": {"languageCode", "language", "knowsLanguage", "P50102", "languageOfThePerson"},
    "description": {"description", "biographicalOrHistoricalInformation", "definition", "note", "abstract", "comment",
                    "biographicalInformation", "bio", "biography", "scopeNote", "editorialNote", "P50113", "hasNote", "text"},
    "work": {"notableWork", "workExample", "author", "creator", "contributor", "mainEntityOfPage", "P50195", "hasWork",
             "isCreatorOf", "isAuthorOf"},
    "subject_of": {"subjectOf", "isSubjectOf", "subject_of", "P50007"},   # works ABOUT the person (schema:subjectOf, LC "Subject Of Works")
    "related_agent": {"relatedTo", "knows", "spouse", "parent", "children", "colleague", "hasCloseRelation", "relationship", "affiliation",
                      "memberOf", "familialRelationship", "relatedPerson", "sibling", "hasRelatedPerson", "hasSeeAlso", "P50316"},
    "same_as": {"sameAs", "exactMatch", "closeMatch", "identifiesRWO", "focus", "wikidata", "isPrimaryTopicOf", "page"},
    "see_also": {"seeAlso", "url", "homepage", "describedby", "isDescribedBy", "relatedLink"},
    "identifier": {"identifier", "gndIdentifier", "identifiedBy", "oldAuthorityNumber", "viafId", "isniId", "lcnaf", "P50006", "id",
                   "controlNumber", "recordIdentifier", "value"},
    "image": {"image", "depiction", "thumbnail", "logo", "photo", "thumbnailUrl"},
    "source": {"source", "citation", "sourceNote", "hasSource", "isBasedOn", "P50001"},
    "record_created": {"created", "dateCreated", "creationDate", "P50028"},
    "record_modified": {"modified", "dateModified", "lastModified", "changed", "P50030"},
    "license": {"license", "rights", "accessRights", "copyright"},
    "type": {"type", "entityType", "typeOfPerson"},
}
# site-specific predicate codes that the local-name map can't guess
PRED_MAP["name_preferred"] |= {"P5001"}            # datos.bne.es
PRED_MAP["birth_date"] |= {"P5010", "P98i_was_born"}   # BNE, CIDOC-CRM
PRED_MAP["death_date"] |= {"P5011", "P100i_died_in"}
PRED_MAP["family_name"] |= {"P5012"}
PRED_MAP["same_as"] |= {"P5024"}
PRED_MAP["related_agent"] |= {"OP5001"}
PRED_MAP["work"] |= {"OP3005"}
PRED_MAP["description"] |= {"P5002", "lifeSpan"}       # "1835-1910"-style life dates
URI_ELEMENTS = {"same_as", "see_also", "image", "identifier"}
PAGE_META_NS = re.compile(r"ogp\.me|twitter|xhtml/vocab|fb:|opengraph", re.I)  # keep the URI, never a label, for these
LOCAL_TO_ELEMENT = {local: el for el, locals_ in PRED_MAP.items() for local in locals_}
LABEL_PREDS = {"prefLabel", "label", "name", "preferredNameForThePlace", "preferredNameForTheSubjectHeading", "preferredNameForTheCorporateBody",
               "preferredName", "authoritativeLabel", "title", "preferredNameForThePerson", "preferredNameForTheWork"}

MARC_MAP = {  # authority tag -> element (subfields that carry the value)
    "100": ("name_preferred", "abcdq"), "400": ("name_variant", "abcdq"), "500": ("related_agent", "abcdqi"),
    "510": ("related_agent", "abi"), "046": None, "370": None, "372": ("field_of_activity", "a"), "374": ("occupation", "a"),
    "375": ("gender", "a"), "377": ("language", "al"), "378": ("given_name", "q"), "670": ("source", "ab"), "678": ("description", "ab"),
    "024": ("identifier", "a2"), "035": ("identifier", "a"), "010": ("identifier", "a"), "016": ("identifier", "a"), "663": ("description", "ab"),
    "665": ("description", "a"), "667": ("description", "a"), "680": ("description", "i"), "368": ("type", "abc"), "040": None, "005": None,
    "043": ("nationality", "a"), "053": ("field_of_activity", "ab"), "856": ("see_also", "u"), "880": None,
}


def local(uri):
    s = str(uri)
    return re.split(r"[#/]", s)[-1] or s


def namespace(uri):
    s = str(uri)
    return s[: max(s.rfind("#"), s.rfind("/")) + 1]


JUNK_IMAGE = re.compile(r"logo|icon|placeholder|default|avatar|badge|sprite|facebook|twitter|instagram|opengraph\.png|share\.png|og-image|social|banner|\.svg$|^data:|^[a-z]{2,4}$", re.I)
TYPE_WORDS = {"place", "person", "thing", "event", "date", "country", "city", "organization", "text", "work", "image", "unknown", "none", "null", "n/a", "-"}


def junk_value(element, value):
    """Values that are never data about a person: a site logo as his image, a schema type name as his birthplace, a
    base64 blob, a template placeholder."""
    low = value.lower()
    if element == "image":
        return bool(JUNK_IMAGE.search(low)) or not (low.startswith("http") or low.startswith("//"))
    if element in ("birth_place", "death_place", "activity_place", "birth_date", "death_date", "gender", "nationality", "occupation", "language"):
        return low in TYPE_WORDS or low.endswith(".html") or "{{" in low or low.startswith("http://schema.org")
    if element in ("name_preferred", "name_variant", "pseudonym"):
        return low in TYPE_WORDS or "{{" in low
    return low.startswith("data:") or "{{" in low


class Profile:
    def __init__(self, prop, label):
        self.prop, self.label = prop, label
        self.formats = collections.Counter()
        self.vocab = collections.Counter()
        self.elements = collections.defaultdict(list)
        self.unmapped = collections.Counter()
        self.files = []
        self.json_profiles = []
        self.llm_notes = None
        self.about_entity = True
        self.chrome_elements = {}
        self._seen = set()

    def add(self, element, value, lang=None, via=None, file=None, is_uri=False):
        value = str(value).strip()
        if not value or junk_value(element, value):
            return
        key = (element, value.lower(), lang)
        if key in self._seen or len(self.elements[element]) >= (2000 if element in ("work", "subject_of") else 400):
            return
        self._seen.add(key)
        self.elements[element].append({"value": value[:500], "lang": lang, "via": via, "file": file, "uri": is_uri})

    def to_json(self):
        return {
            "property": self.prop, "property_label": self.label, "files": self.files, "formats": dict(self.formats),
            "vocabularies": dict(self.vocab.most_common()), "elements": dict(self.elements),
            "element_languages": {el: sorted({v["lang"] for v in vals if v["lang"]}) for el, vals in self.elements.items()},
            "unmapped": dict(self.unmapped.most_common(60)), "json_profiles": self.json_profiles, "llm_notes": self.llm_notes,
            "about_entity": self.about_entity, "chrome_elements": self.chrome_elements,
        }



# ---------- CIDOC-CRM / Linked Art (Yale LUX, Getty...) ----------
CRM = "http://www.cidoc-crm.org/cidoc-crm/"
LA = "https://linked.art/ns/terms/"
CRMDIG = "http://www.ics.forth.gr/isl/CRMdig/"


def profile_cidoc(profile, g, s, fname):
    """Linked Art nests everything (names are Appellation nodes typed 'Primary Name', dates sit in a
    Time-Span under a Birth event, nationality/gender/occupation are all P2_has_type concepts whose own
    type says which). Walk those shapes into the element schema."""
    P = lambda name: rdflib.URIRef(CRM + name)
    LAP = lambda name: rdflib.URIRef(LA + name)

    def label(n):
        return graph_label(g, n)[0]

    def content(n):
        for o in g.objects(n, P("P190_has_symbolic_content")):
            return str(o), o.language
        return graph_label(g, n)

    def type_labels(n):
        return {label(t) for t in g.objects(n, P("P2_has_type")) if label(t)}

    def lang(n):
        for l in g.objects(n, P("P72_has_language")):
            for o in g.objects(l, rdflib.URIRef("http://www.w3.org/2004/02/skos/core#notation")):
                return str(o)
            if label(l):
                return label(l).lower()[:2]
        return None

    def span(n):
        for ts in g.objects(n, P("P4_has_time-span")):
            for idn in g.objects(ts, P("P1_is_identified_by")):
                text, _ = content(idn)
                if text:
                    return text
            begin = next((str(b)[:10] for b in g.objects(ts, P("P82a_begin_of_the_begin"))), None)
            end = next((str(e)[:10] for e in g.objects(ts, P("P82b_end_of_the_end"))), None)
            if begin and end and begin.endswith("-01-01") and end.endswith("-12-31"):
                return begin[:4]   # a year, not 1 January
            if begin:
                return begin
        return None

    def places(n):
        return [label(pl) or str(pl) for pl in g.objects(n, P("P7_took_place_at"))]

    def access_points(n, carrier):
        for d in g.objects(n, LAP(carrier)):
            for ap in g.objects(d, LAP("access_point")):
                yield str(ap)

    for n in g.objects(s, P("P1_is_identified_by")):
        text, _ = content(n)
        if not text:
            continue
        types = type_labels(n)
        if any("Identifier" in local(t) for t in g.objects(n, RDF.type)) or any("identifier" in t.lower() for t in types):
            profile.add("identifier", text, None, "P1_is_identified_by/Identifier", fname)
        elif "Primary Name" in types:
            profile.add("name_preferred", text, lang(n), "P1_is_identified_by/Primary Name", fname)
        elif any("seudonym" in t for t in types):
            profile.add("pseudonym", text, lang(n), "P1_is_identified_by/Pseudonym", fname)
        else:
            profile.add("name_variant", text, lang(n), "P1_is_identified_by/" + ("|".join(sorted(types)) or "Name"), fname)
    for pred, date_el, place_el in (("P98i_was_born", "birth_date", "birth_place"), ("P100i_died_in", "death_date", "death_place")):
        for ev in g.objects(s, P(pred)):
            if span(ev):
                profile.add(date_el, span(ev), None, f"{pred}/P4_has_time-span", fname)
            for pl in places(ev):
                profile.add(place_el, pl, None, f"{pred}/P7_took_place_at", fname)
    for n in g.objects(s, P("P67i_is_referred_to_by")):
        text, l = content(n)
        if not text:
            continue
        types = " ".join(type_labels(n))
        el = "license" if re.search(r"copyright|license|rights", types, re.I) else "source" if re.search(r"citation|source", types, re.I) else "description"
        profile.add(el, text, l or lang(n), f"P67i_is_referred_to_by/{types or 'statement'}", fname)
    for c in g.objects(s, P("P2_has_type")):
        text = label(c)
        if not text:
            continue
        meta = " ".join(type_labels(c))
        el = ("nationality" if re.search(r"nationality|culture", meta, re.I) else "gender" if re.search(r"gender|sex", meta, re.I)
              else "occupation" if re.search(r"occupation|role|profession", meta, re.I) else "type")
        profile.add(el, text, None, f"P2_has_type/{meta or 'Type'}", fname)
    for ev in g.objects(s, P("P14i_performed")):
        for pl in places(ev):
            profile.add("activity_place", pl, None, "P14i_performed/P7_took_place_at", fname)
    for pl in g.objects(s, P("P74_has_current_or_former_residence")):
        profile.add("activity_place", label(pl) or str(pl), None, "P74_has_current_or_former_residence", fname, is_uri=label(pl) is None)
    for grp in g.objects(s, P("P107i_is_current_or_former_member_of")):
        profile.add("related_agent", label(grp) or str(grp), None, "P107i_is_current_or_former_member_of", fname, is_uri=label(grp) is None)
    for l in g.objects(s, P("P72_has_language")):
        profile.add("language", label(l) or str(l), None, "P72_has_language", fname)
    for eq in g.objects(s, LAP("equivalent")):
        profile.add("same_as", str(eq), None, "equivalent", fname, is_uri=True)
    for vi in g.objects(s, P("P138i_has_representation")):
        for url in access_points(vi, "digitally_shown_by"):
            profile.add("image", url, None, "P138i_has_representation/access_point", fname, is_uri=True)
    for lo in g.objects(s, P("P129i_is_subject_of")):
        for url in access_points(lo, "digitally_carried_by"):
            profile.add("see_also", url, None, "P129i_is_subject_of/access_point", fname, is_uri=True)


# ---------- RDF ----------
VOCAB_NS = ("http://www.w3.org/", "https://www.w3.org/", "http://purl.org/dc/", "http://schema.org/", "https://schema.org/", "http://xmlns.com/foaf/",
            "http://vocab.getty.edu/aat/", "http://id.loc.gov/vocabulary/", "http://www.cidoc-crm.org/")

def graph_label(g, node):
    for p, o in g.predicate_objects(node):
        if local(p) in LABEL_PREDS and isinstance(o, rdflib.Literal):
            return str(o), o.language
    return None, None


def profile_rdf(profile, path, fmt, value):
    g = rdflib.Graph()
    g.parse(path, format={"rdf-xml": "xml", "turtle": "turtle", "n-triples": "nt", "json-ld": "json-ld"}[fmt])
    if not len(g):
        return
    counts = collections.Counter(s for s in g.subjects())
    focus = {s for s in counts if isinstance(s, rdflib.URIRef) and value and value.lower() in str(s).lower()}
    if not focus:
        # no entity URI to go by (typical for data embedded in HTML): prefer a Person-typed node,
        # then a node whose literals mention the entity, never the WebSite/WebPage/Organization nodes
        def types(s):
            return {local(o).lower() for o in g.objects(s, RDF.type)}
        persons = [s for s in counts if types(s) & {"person", "agent", "differentiatedperson", "personalname", "authority", "humanbeing", "e21_person", "e21person"}]
        mentions = [s for s in counts if any(isinstance(o, rdflib.Literal) and any(t in str(o).lower() for t in ENTITY_TERMS) for o in g.objects(s))]
        noise = {s for s in counts if types(s) & {"website", "webpage", "organization", "breadcrumblist", "imageobject", "listitem", "searchaction",
                                                   "sitenavigationelement", "collectionpage", "itemlist", "newsarticle", "article", "document", "informationresource",
                                                   "videoobject", "clip", "mediaobject", "musicgroup", "musicevent", "event", "product", "offer", "faqpage", "question",
                                                   "answer", "contactpoint", "postaladdress", "class", "property", "datatype", "webapplication", "softwareapplication",
                                                   "wpheader", "wpfooter", "sitelinkssearchbox", "readaction", "entrypoint", "aggregaterating", "rating", "review", "comment"}}
        noise |= {s for s in counts if str(s).startswith(VOCAB_NS)}
        noise |= {s for s in counts if any(t.endswith(("organization", "page", "site", "action", "list", "object", "element", "rating", "event", "application",
                                                       "album", "recording", "book", "creativework", "movie", "series", "periodical", "specification", "point"))
                                            for t in types(s))}
        strong = [s for s in persons if strong_entity_name(graph_label(g, s)[0] or "")]
        for pool in (strong, mentions):
            pool = [s for s in pool if s not in noise]
            if pool:
                focus = {max(pool, key=lambda s: counts[s])}
                break
        if not focus:
            profile.unmapped["(no node about the entity in this file)"] += 1
            return
    # follow "this record is about" links to the real-world-object node
    for s in list(focus):
        for p, o in g.predicate_objects(s):
            if local(p) in ("identifiesRWO", "focus", "mainEntity", "about", "primaryTopic") and isinstance(o, rdflib.URIRef):
                focus.add(o)
    fname = path.name

    def repair_glued_name(node, literal):
        """VIAF emits 'Samuel LanghorneClemens' (given+family with no space); put the space back."""
        text = str(literal)
        if " " in text and not re.search(r"[a-zà-ÿ][A-ZÀ-Þ]", text):
            return text
        for p2, o2 in g.predicate_objects(node):
            if local(p2) in ("givenName", "forename") and isinstance(o2, rdflib.Literal):
                for p3, o3 in g.predicate_objects(node):
                    if local(p3) in ("familyName", "surname") and isinstance(o3, rdflib.Literal):
                        if text == f"{o2}{o3}":
                            profile.unmapped["(repaired glued given+family name)"] += 1
                            return f"{o2} {o3}"
        return text

    cidoc = any(namespace(p) == CRM for p in set(g.predicates()))
    if cidoc:
        actor_types = {"e21_person", "e39_actor", "e74_group", "person", "group", "actor"}
        focus = {s for s in focus if {local(o).lower() for o in g.objects(s, RDF.type)} & actor_types}
        if not focus:
            profile.unmapped["(CIDOC record whose subject is not a person: concept/place/object)"] += 1
            return
    for s in focus:
        if cidoc:
            profile_cidoc(profile, g, s, fname)
        for p, o in g.predicate_objects(s):
            profile.vocab[namespace(p)] += 1
            if cidoc and (namespace(p) in (CRM, LA, CRMDIG) or local(p) == "label"):
                continue   # walked by profile_cidoc (names come from P1_is_identified_by, not the display label)
            if PAGE_META_NS.search(str(p)):
                # OpenGraph / Twitter-card / XHTML metadata describes the web page, not the entity: keep the description
                # only when it names him (a site tagline does not) and the image only when the card is about him
                og_text = " ".join(str(o2) for p2, o2 in g.predicate_objects(s) if PAGE_META_NS.search(str(p2)) and local(p2) in ("title", "description") and isinstance(o2, rdflib.Literal))
                og_desc = next((str(o2) for p2, o2 in g.predicate_objects(s) if PAGE_META_NS.search(str(p2)) and local(p2) == "description" and isinstance(o2, rdflib.Literal)), "")
                desc_ok = mentions_terms(og_desc) and len(og_desc) >= 80 and not re.search(r"\||·|—|discover|découvr|explore|catalog|biblioth|library|free ebooks|podcast", og_desc, re.I)
                if local(p) == "description" and isinstance(o, rdflib.Literal) and desc_ok:
                    profile.add("description", str(o), o.language, "og:description", fname)
                elif local(p) == "image" and isinstance(o, (rdflib.Literal, rdflib.URIRef)) and desc_ok and strong_entity_name(og_text):
                    profile.add("image", str(o), None, "og:image", fname, is_uri=True)
                elif local(p) in ("description", "image"):
                    profile.unmapped["(og chrome: tagline / site image)"] += 1
                continue
            el = LOCAL_TO_ELEMENT.get(local(p))
            if el is None:
                profile.unmapped[f"{local(p)} ({namespace(p)})"] += 1
                continue
            if isinstance(o, rdflib.Literal):
                text = repair_glued_name(s, o) if el in ("name_preferred", "name_variant") else o
                profile.add(el, text, o.language, f"{local(p)}", fname)
            elif isinstance(o, rdflib.URIRef) and el in URI_ELEMENTS:
                profile.add(el, str(o), None, f"{local(p)}", fname, is_uri=True)
            elif isinstance(o, (rdflib.BNode, rdflib.URIRef)):
                lbl, lang = graph_label(g, o)
                if lbl:
                    profile.add(el, lbl, lang, f"{local(p)}", fname, is_uri=isinstance(o, rdflib.URIRef))
                    if isinstance(o, rdflib.URIRef):
                        profile.add(el, str(o), None, f"{local(p)} (uri)", fname, is_uri=True)
                if isinstance(o, rdflib.URIRef) and not lbl:
                    profile.add(el, str(o), None, f"{local(p)}", fname, is_uri=True)
                if isinstance(o, rdflib.BNode) or (isinstance(o, rdflib.URIRef) and not lbl):
                    # structured value (name entity, variant node, date node...): route its parts
                    for p2, o2 in g.predicate_objects(o):
                        if not isinstance(o2, rdflib.Literal):
                            continue
                        el2 = LOCAL_TO_ELEMENT.get(local(p2))
                        if local(p2) in LABEL_PREDS or el2 in ("name_preferred", "name_variant") or local(p2) in ("variantLabel", "marcKey"):
                            if local(p2) != "marcKey":
                                profile.add(el, o2, o2.language, f"{local(p)}/{local(p2)}", fname)
                        elif el2:
                            profile.add(el2, o2, o2.language, f"{local(p)}/{local(p2)}", fname)
                        else:
                            profile.unmapped[f"{local(p)}/{local(p2)} ({namespace(p2)})"] += 1
    # works: things in the graph that point at the focus as creator/author/contributor
    for s, p, o in g:
        if o in focus and local(p) in ("creator", "author", "contributor", "agent", "byArtist") and s not in focus:
            lbl, lang = graph_label(g, s)
            profile.add("work", lbl or str(s), lang, f"^{local(p)}", fname, is_uri=lbl is None)


# ---------- MARC / MADS / EAC ----------

def marc_json_records(doc):
    """MARC serialised as JSON: VIAF's {"mx:record": {"mx:datafield": [{"tag", "ind1", "ind2", "mx:subfield": [{"code", "content"}]}]}}
    (also without the mx: prefix, as IdRef's export). Returns pymarc Records, or [] when the document is not that shape."""
    def strip(k):
        return k.split(":")[-1]
    def norm(node):
        if isinstance(node, dict):
            return {strip(k): norm(v) for k, v in node.items()}
        if isinstance(node, list):
            return [norm(v) for v in node]
        return node
    doc = norm(doc)
    recs = doc.get("record") if isinstance(doc, dict) else None
    if recs is None and isinstance(doc, dict) and "datafield" in doc:
        recs = doc
    if recs is None:
        return []
    out = []
    for r in (recs if isinstance(recs, list) else [recs]):
        if not isinstance(r, dict) or "datafield" not in r:
            continue
        rec = pymarc.Record()
        for df in (r["datafield"] if isinstance(r["datafield"], list) else [r["datafield"]]):
            if not isinstance(df, dict) or not df.get("tag"):
                continue
            subs = df.get("subfield") or []
            subs = subs if isinstance(subs, list) else [subs]
            pairs = [pymarc.Subfield(code=str(sf.get("code")), value=str(sf.get("content") or sf.get("value") or "")) for sf in subs if isinstance(sf, dict) and sf.get("code")]
            try:
                rec.add_field(pymarc.Field(tag=str(df["tag"]), indicators=[str(df.get("ind1") or " "), str(df.get("ind2") or " ")], subfields=pairs))
            except Exception:
                continue
        if rec.get_fields():
            out.append(maybe_unimarc(rec))
    return out


def maybe_unimarc(rec):
    """UNIMARC authorities (IdRef, BnF) carry the name in 200 and coded data in 100$a; MARC21 ones carry the name in 100."""
    coded = rec["100"]["a"] if rec.get("100") and rec["100"].get("a") else ""
    if rec.get("200") and re.match(r"^\d{8}", coded or ""):
        return unimarc_to_marc21(rec)
    return rec


UNIMARC_TO_MARC21 = {"200": "100", "400": "400", "300": "678", "340": "678", "500": "500", "856": "856", "010": "024", "033": "035", "035": "035"}


def unimarc_to_marc21(rec):
    """Rename the UNIMARC authority fields the element map understands into their MARC21 equivalents; drop the rest."""
    out = pymarc.Record()
    for f in rec.get_fields():
        tag = UNIMARC_TO_MARC21.get(f.tag)
        if not tag:
            continue
        subs = [sf for sf in f.subfields if sf.code in "abcdfgq"] if tag in ("100", "400", "500") else list(f.subfields)
        if tag in ("100", "400", "500"):
            # UNIMARC 200: $a family, $b given, $f dates, $c qualifier -> "family, given, dates"
            parts = [sf.value for sf in subs if sf.code == "a"] + [sf.value for sf in subs if sf.code == "b"] + [sf.value for sf in subs if sf.code in "cf"]
            subs = [pymarc.Subfield(code="a", value=", ".join(p for p in parts if p))]
        out.add_field(pymarc.Field(tag=tag, indicators=f.indicators, subfields=subs))
    return out


def profile_marc(profile, path, fmt, records=None):
    if records is None:
        records = pymarc.parse_xml_to_array(str(path)) if fmt == "marcxml" else list(pymarc.MARCReader(path.read_bytes(), to_unicode=True))
    records = [maybe_unimarc(r) for r in records]
    for rec in records:
        profile.vocab["MARC21 authority"] += 1
        for f in rec.get_fields():
            tag = f.tag
            if tag < "010":
                continue
            profile.vocab[f"MARC {tag}"] += 1
            spec = MARC_MAP.get(tag, "?")
            if spec == "?":
                profile.unmapped[f"MARC {tag}"] += 1
                continue
            if tag == "046":
                if f.get("f"): profile.add("birth_date", f["f"], None, "046$f", path.name)
                if f.get("g"): profile.add("death_date", f["g"], None, "046$g", path.name)
                continue
            if tag == "370":
                if f.get("a"): profile.add("birth_place", f["a"], None, "370$a", path.name)
                if f.get("b"): profile.add("death_place", f["b"], None, "370$b", path.name)
                for e in f.get_subfields("e", "f"): profile.add("activity_place", e, None, "370$e/f", path.name)
                continue
            if tag == "880":
                linked = (f.get("6") or "")[:3]
                el = (MARC_MAP.get(linked) or ("name_variant", "abcdq"))[0]
                profile.add(el, " ".join(f.get_subfields(*"abcdq")), "(880 vernacular)", f"880->{linked}", path.name)
                continue
            if spec is None:
                continue
            el, subs = spec
            val = " ".join(f.get_subfields(*subs)).strip()
            lang = f.get("7") if tag in ("400", "100", "500") else None
            if val:
                profile.add(el, val, lang, f"{tag}", path.name)


def xml_text(e):
    return " ".join(e.itertext()).strip()


def profile_mads(profile, path):
    root = ET.parse(path).getroot()
    ns = {"m": "http://www.loc.gov/mads/v2"}
    profile.vocab["MADS XML"] += 1
    for a in root.iter("{http://www.loc.gov/mads/v2}authority"):
        for n in a.iter("{http://www.loc.gov/mads/v2}name"):
            profile.add("name_preferred", " ".join(xml_text(p) for p in n), n.get("lang"), "mads:authority/name", path.name)
    for v in root.iter("{http://www.loc.gov/mads/v2}variant"):
        for n in v.iter("{http://www.loc.gov/mads/v2}name"):
            profile.add("name_variant", " ".join(xml_text(p) for p in n), n.get("lang"), "mads:variant/name", path.name)
    for n in root.iter("{http://www.loc.gov/mads/v2}note"):
        el = {"history": "description", "source": "source"}.get(n.get("type"), "description")
        profile.add(el, xml_text(n), None, f"mads:note[{n.get('type')}]", path.name)
    for i in root.iter("{http://www.loc.gov/mads/v2}identifier"):
        profile.add("identifier", xml_text(i), None, f"mads:identifier[{i.get('type')}]", path.name)
    for f in root.iter("{http://www.loc.gov/mads/v2}fieldOfActivity"):
        profile.add("field_of_activity", xml_text(f), None, "mads:fieldOfActivity", path.name)
    for f in root.iter("{http://www.loc.gov/mads/v2}occupation"):
        profile.add("occupation", xml_text(f), None, "mads:occupation", path.name)
    for f in root.iter("{http://www.loc.gov/mads/v2}gender"):
        profile.add("gender", xml_text(f), None, "mads:gender", path.name)
    for f in root.iter("{http://www.loc.gov/mads/v2}languageOfCataloging"):
        profile.add("language", xml_text(f), None, "mads:languageOfCataloging", path.name)
    for r in root.iter("{http://www.loc.gov/mads/v2}related"):
        profile.add("related_agent", xml_text(r), None, f"mads:related[{r.get('type')}]", path.name)


def profile_eac(profile, path):
    root = ET.parse(path).getroot()
    profile.vocab["EAC-CPF"] += 1
    strip = lambda tag: tag.split("}")[-1]
    for e in root.iter():
        t = strip(e.tag)
        if t == "nameEntry":
            parts = " ".join(xml_text(p) for p in e if strip(p.tag) == "part")
            kind = "name_preferred" if any(strip(a.tag) == "authorizedForm" for a in e) else "name_variant"
            profile.add(kind, parts, e.get("{http://www.w3.org/XML/1998/namespace}lang"), f"eac:nameEntry", path.name)
        elif t == "existDates":
            for d in e.iter():
                if strip(d.tag) == "fromDate": profile.add("birth_date", d.get("standardDate") or xml_text(d), None, "eac:existDates/fromDate", path.name)
                if strip(d.tag) == "toDate": profile.add("death_date", d.get("standardDate") or xml_text(d), None, "eac:existDates/toDate", path.name)
        elif t == "place":
            role = next((xml_text(c) for c in e if strip(c.tag) == "placeRole"), "")
            name = next((xml_text(c) for c in e if strip(c.tag) == "placeEntry"), "")
            el = "birth_place" if "birth" in role.lower() or "geburt" in role.lower() else "death_place" if "death" in role.lower() or "sterbe" in role.lower() else "activity_place"
            if name: profile.add(el, name, None, f"eac:place[{role}]", path.name)
        elif t == "occupation":
            profile.add("occupation", xml_text(e), None, "eac:occupation", path.name)
        elif t == "biogHist":
            profile.add("description", xml_text(e)[:1000], None, "eac:biogHist", path.name)
        elif t == "cpfRelation":
            profile.add("related_agent", xml_text(e)[:200], None, f"eac:cpfRelation[{e.get('cpfRelationType')}]", path.name)
        elif t == "resourceRelation":
            rt = (e.get("resourceRelationType") or "").lower()
            el = "work" if any(w in rt for w in ("creator", "contributor", "author")) else "subject_of"   # referencedIn / subjectOf: about him
            profile.add(el, xml_text(e)[:200], None, f"eac:resourceRelation[{e.get('resourceRelationType')}]", path.name)
        elif t == "otherRecordId" or t == "recordId":
            profile.add("identifier", xml_text(e), None, f"eac:{t}", path.name)
        elif t == "source":
            profile.add("source", xml_text(e)[:200], None, "eac:source", path.name)


# ---------- ad-hoc JSON / XML: key-path profile ----------

def walk_json(node, path, paths, samples, signals):
    if isinstance(node, dict):
        for k, v in node.items():
            walk_json(v, f"{path}.{k}" if path else k, paths, samples, signals)
    elif isinstance(node, list):
        for v in node[:50]:
            walk_json(v, f"{path}[]", paths, samples, signals)
    else:
        paths[path] += 1
        if path not in samples and node not in (None, "", [], {}):
            samples[path] = str(node)[:120]
        if isinstance(node, str) and any(t in node.lower() for t in ENTITY_TERMS):
            if len(signals) < 60:
                signals.append({"path": path, "value": node[:200]})


JSON_KEY_MAP = {k.lower(): el for el, keys in PRED_MAP.items() for k in keys}
JSON_KEY_MAP.update({
    "birthdate": "birth_date", "birth_date": "birth_date", "date_of_birth": "birth_date", "birthday": "birth_date", "birthyear": "birth_date",
    "deathdate": "death_date", "death_date": "death_date", "date_of_death": "death_date", "deathday": "death_date", "deathyear": "death_date",
    "birthplace": "birth_place", "birth_place": "birth_place", "place_of_birth": "birth_place", "deathplace": "death_place", "death_place": "death_place",
    "place_of_death": "death_place", "occupations": "occupation", "professions": "occupation", "jobs": "occupation", "nationalities": "nationality",
    "languages": "language", "aliases": "name_variant", "alternatenames": "name_variant", "other_names": "name_variant", "othernames": "name_variant",
    "variants": "name_variant", "variant_names": "name_variant", "alsoknownas": "name_variant", "aka": "name_variant", "fullname": "name_preferred",
    "full_name": "name_preferred", "displayname": "name_preferred", "display_name": "name_preferred", "preferred_name": "name_preferred",
    "preferredname": "name_preferred", "summary": "description", "biography": "description", "bio": "description", "about": "description",
    "overview": "description", "intro": "description", "images": "image", "thumbnail": "image", "picture": "image", "avatar": "image",
    "profile_image": "image", "works": "work", "books": "work", "titles": "work", "publications": "work", "wikidata": "same_as", "wikidata_id": "same_as",
    "viaf": "same_as", "isni": "same_as", "lccn": "same_as", "gnd": "same_as", "sex": "gender", "pseudonyms": "pseudonym",
    "created": "record_created", "updated": "record_modified", "last_modified": "record_modified", "modified": "record_modified",
})
JSON_SKIP_PATH = re.compile(r"(^|\.)(meta|_links|links|pagination|facets?|navigation|menu|settings|config|seo|og|twitter|analytics|tracking|ads?|"
                            r"jwplayer|playlist|prebid|bidders?|consent|cookies?|DomainData|geo|geolocation|location|locale|culture|avatar|video|advert\w*|"
                            r"sponsor\w*|widgets?|banner|search|filters?|options|availableSearches|interface|ui|i18n|translations?|labels)(\.|\[|$)", re.I)
RECORD_KEYS = {"naid", "recordtype", "isbn", "issn", "publisher", "publicationdate", "datepublished", "pages", "year", "itemtype", "genre", "edition",
               "format", "medium", "caption", "mimetype", "contributor", "uploaded", "photo", "collection", "series", "volume", "doi", "url"}
NAME_KEYS = {"name", "label", "title", "heading", "fullname", "full_name", "displayname", "display_name", "preferredname", "preferred_name",
             "preflabel", "authorizedform", "nombre", "nom", "naam", "имя", "names", "aliases", "value"}
LANG_SEG = re.compile(r"^[a-z]{2,3}(-[A-Za-z]{2,4})?$")


def object_about_entity(node):
    """For one JSON object: True / False when its own strings decide it, None when it says nothing either way.
    An object with a name-like key is about the entity only if that name is one of the entity's labels in full
    (so a relative's record, a book, an ad or a geo lookup is not); otherwise any string mentioning the entity decides."""
    strs, names = [], []
    for k, v in node.items():
        kl = str(k).lower()
        if isinstance(v, str):
            strs.append(v)
            if kl in NAME_KEYS and kl != "value":
                names.append(v)
        elif isinstance(v, dict):
            for k2, v2 in v.items():
                if isinstance(v2, str):
                    strs.append(v2)
                    if kl in NAME_KEYS and str(k2).lower() in NAME_KEYS:
                        names.append(v2)
        elif isinstance(v, list):
            for v2 in v[:20]:
                if isinstance(v2, str):
                    strs.append(v2)
                    if kl in NAME_KEYS and kl != "value":
                        names.append(v2)
                elif isinstance(v2, dict) and kl in NAME_KEYS:
                    names.extend(x for x in v2.values() if isinstance(x, str))
    if names:
        return any(strong_entity_name(n) for n in names)
    if any(mentions_terms(x) for x in strs):
        return True
    return None


def heuristic_json_elements(profile, doc, fname):
    """Map JSON keys to elements by name; take the language from language-coded path segments. Values are only taken
    from objects that are about the entity (see object_about_entity); a small undecided object inherits its parent's
    decision (birth: {date: ...} inside his record), a big one does not (an ad config, a UI settings block)."""
    def walk(node, segs, about, since, parent=None):
        if isinstance(node, dict):
            d = object_about_entity(node)
            if d is None:
                about2, since2 = (about if (len(node) <= 8 and since < 2) else False), since + 1
            else:
                about2, since2 = d, 0
            for k, v in node.items():
                walk(v, segs + [str(k)], about2, since2, node)
        elif isinstance(node, list):
            for v in node[:100]:
                walk(v, segs, about, since, parent)
        elif node not in (None, "", True, False) and segs:
            if not about:
                return
            if segs[-1].lower() in ("title", "name", "label") and isinstance(parent, dict) and len({k.lower() for k in parent} & RECORD_KEYS) >= 2:
                # a record (photo, census entry, patent, book) whose title names him: a thing about him, not his name
                profile.add("subject_of", str(node), None, f"json:{'.'.join(segs)[-60:]} (record title)", fname)
                return
            path = ".".join(segs)
            if JSON_SKIP_PATH.search(path):
                return
            lang = next((sg for sg in reversed(segs) if LANG_SEG.match(sg) and sg not in ("id", "url", "uri", "src", "key", "ids")), None)
            keys = [sg.lower() for sg in segs if not LANG_SEG.match(sg) or sg.lower() in JSON_KEY_MAP]
            for k in reversed(keys[-2:]):  # the leaf key, else its parent (e.g. birth.date / name.value)
                el = JSON_KEY_MAP.get(k)
                if el:
                    val = str(node)
                    # ad-hoc JSON is full of UI strings: only accept text elements that are visibly about the entity
                    if el in ("name_preferred", "name_variant", "description", "work", "related_agent", "pseudonym", "identifier", "type"):
                        if el in ("name_preferred", "name_variant", "pseudonym") and not strong_entity_name(val):
                            return
                        if el == "description" and not mentions_terms(val):
                            return
                        if el in ("work", "related_agent", "identifier", "type"):
                            return
                    profile.add(el, val, lang, f"json:{path[-60:]}", fname, is_uri=val.startswith("http"))
                    return
    walk(doc, [], False, 0)


def lc_relationships(profile, doc, fname):
    """id.loc.gov's 'Subject Of Works' / 'Contributor To Works' panels: paginated JSON the page loads by XHR."""
    if not (isinstance(doc, dict) and isinstance(doc.get("summary"), dict) and isinstance(doc.get("results"), list)):
        return False
    kind = doc["summary"].get("type")
    el = {"subjectOf": "subject_of", "contributorTo": "work"}.get(kind)
    if not el:
        return False
    for r in doc["results"]:
        if isinstance(r, dict) and r.get("label"):
            profile.add(el, r["label"], None, f"json:results[].label ({kind})", fname)
    return True


def profile_json_file(profile, path, fmt):
    paths, samples, signals = collections.Counter(), {}, []
    if fmt == "json":
        try:
            doc = json.loads(path.read_text(errors="replace"))
        except Exception:
            return
        walk_json(doc, "", paths, samples, signals)
        marc_recs = marc_json_records(doc)
        if marc_recs:
            profile.formats["marc-json"] += 1
            profile_marc(profile, path, "marc-json", records=marc_recs)
        elif not lc_relationships(profile, doc, path.name):
            heuristic_json_elements(profile, doc, path.name)
    else:
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            return
        def walk_xml(e, p):
            tag = e.tag.split("}")[-1]
            p = f"{p}/{tag}" if p else tag
            text = (e.text or "").strip()
            paths[p] += 1
            if text and p not in samples:
                samples[p] = text[:120]
            if text and any(t in text.lower() for t in ENTITY_TERMS) and len(signals) < 60:
                signals.append({"path": p, "value": text[:200]})
            for a, v in e.attrib.items():
                paths[f"{p}@{a}"] += 1
                if f"{p}@{a}" not in samples:
                    samples[f"{p}@{a}"] = v[:120]
            for c in e:
                walk_xml(c, p)
        walk_xml(root, "")
    lang_keys = sorted({p.split(".")[-1] for p in paths if re.fullmatch(r"[a-z]{2,3}(-[A-Za-z]{2,4})?", p.split(".")[-1].split("[]")[0])})
    profile.json_profiles.append({
        "file": path.name, "format": fmt, "size": path.stat().st_size, "path_count": len(paths),
        "paths": [{"path": p, "n": n, "sample": samples.get(p)} for p, n in paths.most_common(120)],
        "entity_signals": signals, "language_like_keys": lang_keys[:40],
    })


# ---------- is the extracted data about the entity at all? ----------

PERSONAL_ELEMENTS = {"name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place",
                     "death_place", "gender", "occupation", "nationality", "work", "related_agent", "same_as", "identifier"}


def entity_name_tokens(entity):
    """Distinctive words from every label/alias of the Wikidata item (all languages), plus birth/death years."""
    tokens = set()
    for group in ("labels", "aliases"):
        for v in entity.get(group, {}).values():
            for item in (v if isinstance(v, list) else [v]):
                for w in re.split(r"[\s,.()\-]+", item["value"]):
                    if len(w) >= 4:
                        tokens.add(w.lower())
    for prop in ("P569", "P570"):
        for claim in entity.get("claims", {}).get(prop, []):
            t = claim.get("mainsnak", {}).get("datavalue", {}).get("value", {}).get("time", "")
            if t[1:5].isdigit():
                tokens.add(t[1:5])
    return tokens


WORDLIKE = re.compile(r"[A-Za-z\u00c0-\u024f\u0370-\u03ff\u0400-\u04ff0-9]+")


def mentions_entity(text, tokens):
    """True when the text names the entity: a distinctive token (5+ chars, or a birth/death year) or two different
    tokens together. Alphabetic tokens must match whole words - 'mark' inside 'marquee'/'bookmark' is not Mark Twain."""
    low = text.lower()
    hits = set()
    for t in tokens:
        if WORDLIKE.fullmatch(t):
            if re.search(r"(?<!\w)" + re.escape(t) + r"(?!\w)", low):
                hits.add(t)
        elif t in low:
            hits.add(t)
    return any(len(t) >= 5 or t.isdigit() for t in hits) or len(hits) >= 2


def about_entity(profile, tokens):
    """A site counts as describing the entity when it has a personal element (name, date, work...) or any
    value that names the entity. Otherwise the values are page chrome (a site tagline as og:description,
    the site's share image) and must not be mistaken for data about the person."""
    if any(profile.elements.get(el) for el in PERSONAL_ELEMENTS):
        return True
    return mentions_entity(" ".join(v["value"] for vals in profile.elements.values() for v in vals), tokens)


# ---------- LLM extractions (Opus subagents, for the ad-hoc JSON/XML the parsers can't read) ----------

def merge_llm_extraction(profile, path, prefix="llm"):
    """prefix 'llm' = extracted from ad-hoc JSON/XML files; 'llm-page' = extracted from the rendered page text."""
    if not path.exists():
        return
    try:
        d = json.loads(path.read_text())
    except ValueError:
        profile.unmapped["(llm extraction unreadable)"] += 1
        return
    if not d.get("about_entity", True) and not d.get("elements"):
        profile.llm_notes = d.get("notes")
        return
    profile.llm_notes = d.get("notes")
    for el, vals in (d.get("elements") or {}).items():
        if el not in PRED_MAP:
            profile.unmapped[f"(llm element {el})"] += 1
            continue
        for v in vals if isinstance(vals, list) else []:
            if isinstance(v, dict) and v.get("value"):
                if el == "same_as" and "996" in str(v.get("via", "")):
                    profile.unmapped["(VIAF 996: not clustered with him, dropped)"] += 1
                    continue
                if re.search(r"\(\s*spirit\s*\)|82045653|0000000077209145", f"{v['value']} {v.get('via', '')}", re.I):
                    profile.unmapped["('(Spirit)' heading via page text, dropped)"] += 1
                    continue
                profile.add(el, v["value"], v.get("lang"), f"{prefix}:{v.get('via', '')}"[:120], path.name, is_uri=str(v["value"]).startswith("http"))
            elif isinstance(v, str):
                profile.add(el, v, None, prefix, path.name)
    profile.vocab["LLM extraction"] += 1


# ---------- driver ----------

def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else "Q7245"
    data_dir = Path("data") / qid
    rep_dir = data_dir / "representations"
    out_dir = data_dir / "analysis" / "profiles"
    out_dir.mkdir(parents=True, exist_ok=True)
    identifiers = {r["property"]: r for r in json.loads((data_dir / "identifiers.json").read_text())}
    entity = json.loads((data_dir / "entity.json").read_text())
    name_tokens = entity_name_tokens(entity)
    global NAME_TOKENS, ENTITY_NAME_SETS
    NAME_TOKENS = name_tokens
    for group in ("labels", "aliases"):
        for v in entity.get(group, {}).values():
            for item in (v if isinstance(v, list) else [v]):
                toks = {w.lower() for w in re.split(r"[\s,.()\-]+", item["value"]) if len(w) >= 3 and not w.isdigit()}
                if toks and (len(toks) > 1 or len(next(iter(toks))) >= 5):
                    ENTITY_NAME_SETS.append(toks)
    chrome_only = []

    wrong_keys = set()
    qr = data_dir / "analysis" / "quality_records.csv"
    if qr.exists():   # from a previous step-8 run: pages that are not his record contribute nothing to the property's profile
        wrong_keys = {r["key"] for r in csv.DictReader(qr.open()) if r.get("status") == "wrong_page"}
    rows = [r for r in csv.DictReader(open(rep_dir / "summary.csv")) if r["file"] and r["file"].split("/")[0] not in wrong_keys]
    by_prop = collections.defaultdict(list)
    for r in rows:
        by_prop[r["property"]].append(r)

    profiles = {}
    for prop, prop_rows in sorted(by_prop.items(), key=lambda kv: int(kv[0][1:])):
        label = prop_rows[0]["property_label"]
        profile = Profile(prop, label)
        seen_bodies = set()
        for r in prop_rows:
            path = rep_dir / r["file"]
            fmt = r["detected"]
            body_hash = hashlib.sha1(path.read_bytes()).hexdigest()
            if body_hash in seen_bodies:
                continue
            seen_bodies.add(body_hash)
            profile.formats[fmt] += 1
            profile.files.append({"file": r["file"], "format": fmt, "kind": r["kind"], "via": r["via"], "url": r["request_url"]})
            try:
                if fmt in ("rdf-xml", "turtle", "n-triples", "json-ld"):
                    profile_rdf(profile, path, fmt, r["value"])
                elif fmt in ("marcxml", "marc-binary"):
                    profile_marc(profile, path, fmt)
                elif fmt == "mads":
                    profile_mads(profile, path)
                elif fmt == "eac-cpf":
                    profile_eac(profile, path)
                elif fmt in ("json", "xml", "feed", "sru-oai-xml", "mods"):
                    profile_json_file(profile, path, "json" if fmt == "json" else "xml")
                elif fmt in ("rdfa", "microdata", "opengraph"):
                    # extruct output is JSON-LD-ish; treat the RDFa as RDF, the rest as JSON
                    if fmt == "rdfa":
                        profile_rdf(profile, path, "json-ld", r["value"])
                    else:
                        profile_json_file(profile, path, "json")
            except Exception as e:
                profile.files[-1]["error"] = f"{type(e).__name__}: {str(e)[:120]}"
        merge_llm_extraction(profile, data_dir / "analysis" / "llm_extractions" / f"{prop}.json")
        merge_llm_extraction(profile, data_dir / "analysis" / "llm_extractions_pages" / f"{prop}.json", "llm-page")  # from the rendered page text
        profile.about_entity = about_entity(profile, name_tokens)
        if not profile.about_entity:
            profile.chrome_elements, profile.elements = dict(profile.elements), collections.defaultdict(list)
            chrome_only.append(prop)
        profiles[prop] = profile
        (out_dir / f"{prop}.json").write_text(json.dumps(profile.to_json(), ensure_ascii=False, indent=1))

    # sites with no representation file at all but a page-text extraction (the record exists only as rendered text)
    for path in sorted((data_dir / "analysis" / "llm_extractions_pages").glob("P*.json")):
        prop = path.stem
        if prop in profiles or prop not in identifiers:
            continue
        profile = Profile(prop, identifiers[prop]["property_label"])
        merge_llm_extraction(profile, path, "llm-page")
        profile.about_entity = about_entity(profile, name_tokens)
        if not profile.about_entity:
            profile.chrome_elements, profile.elements = dict(profile.elements), collections.defaultdict(list)
            chrome_only.append(prop)
        profiles[prop] = profile
        (out_dir / f"{prop}.json").write_text(json.dumps(profile.to_json(), ensure_ascii=False, indent=1))
    profiles = dict(sorted(profiles.items(), key=lambda kv: int(kv[0][1:])))

    # one-line-per-site overview
    elements = list(PRED_MAP.keys())
    with (data_dir / "analysis" / "site_elements.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["property", "label", "formats", "vocabularies", "n_files"] + elements + ["languages", "unmapped_predicates"])
        for prop, p in profiles.items():
            langs = sorted({v["lang"] for vals in p.elements.values() for v in vals if v["lang"]})
            w.writerow([prop, p.label, ", ".join(sorted(p.formats)), ", ".join(k for k, _ in p.vocab.most_common(6)), len(p.files)]
                       + [len(p.elements.get(e, [])) for e in elements] + [", ".join(langs), len(p.unmapped)])

    n_struct = sum(1 for p in profiles.values() if p.elements)
    n_json = sum(1 for p in profiles.values() if p.json_profiles and not p.elements)
    print(f"{len(profiles)} properties profiled: {n_struct} with elements extracted deterministically, {n_json} with only ad-hoc JSON/XML profiles")
    cov = collections.Counter(e for p in profiles.values() for e in p.elements)
    print("element coverage (properties):", dict(cov.most_common()))
    print(f"-> {out_dir}  and  {data_dir / 'analysis' / 'site_elements.csv'}")


if __name__ == "__main__":
    main()
