"""Step 7: compare what each site says about the entity with what Wikidata says.

    uv run python compare_wikidata.py Q7245

Reads the site profiles (analysis/profiles/*.json) and the Wikidata entity, derives the same
canonical elements on the Wikidata side, and writes under data/<QID>/analysis/:

    wikidata_elements.json   Wikidata's values per element (with languages / item labels)
    comparison.csv           one row per site x element: status, site values, Wikidata values
    comparison_matrix.csv    site x element grid of status codes
    crosslinks.csv           every same-as link a site asserts, resolved to a Wikidata identifier
                             property where possible, and whether Wikidata agrees
    vocabulary_mapping.csv   site vocabulary/predicate/field -> element -> Wikidata property
    report.md                the findings, readable

Statuses: match (a site value equals a Wikidata value), partial (overlap but not equal, e.g.
year-only date vs full date, or place name contained in the other), mismatch (values on both
sides, none agree), site_only, wikidata_only, present (both have free text, not comparable).
"""

import collections
import csv
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "wikidata-naf-identifier-inventory/0.1 (thisismattmiller@gmail.com)"
ELEMENT_WD = {  # canonical element -> Wikidata property (for the mapping table)
    "name_preferred": "label", "name_variant": "alias / P742 / P1477", "given_name": "P735", "family_name": "P734", "pseudonym": "P742",
    "birth_date": "P569", "death_date": "P570", "birth_place": "P19", "death_place": "P20", "activity_place": "P937 / P551",
    "gender": "P21", "occupation": "P106", "field_of_activity": "P101", "nationality": "P27", "language": "P1412 / P103 / P6886",
    "description": "description", "work": "P800", "subject_of": "- (works about the person; not on the item)", "related_agent": "P26 / P40 / P22 / P25 / P3373", "same_as": "external identifiers",
    "see_also": "P856 / sitelinks", "identifier": "external identifiers", "image": "P18", "source": "references", "record_created": "-",
    "record_modified": "-", "license": "-", "type": "P31",
}
COMPARABLE = ["name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place",
              "death_place", "gender", "occupation", "nationality", "language", "work", "related_agent", "image"]
TEXT_ONLY = ["description", "source", "see_also", "field_of_activity", "activity_place", "subject_of"]
GENDER_WORDS = {"male": {"male", "m", "man", "männlich", "masculino", "masculin", "maschio", "maschile", "homme", "hombre", "mann", "mężczyzna", "мужской",
                         "мужчина", "男", "男性", "남성", "남", "férfi", "b", "1", "q6581097", "masc", "muž", "mies", "mand", "mannlig", "uomo", "mannelijk",
                         "erkek", "mužské", "ανδρας", "άνδρας", "זכר", "ذكر", "male gender", "sexo masculino"},
                "female": {"female", "f", "woman", "weiblich", "femenino", "féminin", "femme", "mujer", "frau", "q6581072", "女", "女性", "여성", "nő", "kobieta",
                           "женский", "женщина", "žena", "vrouw", "kvinna", "kvinne", "kvinde", "nainen", "donna", "kadın"}}
COUNTRY_CODES = {"us": "United States of America", "usa": "United States of America", "xxu": "United States of America", "n-us": "United States of America",
                 "united states": "United States of America", "u.s.": "United States of America", "us-mo": "United States of America",
                 "am": "United States of America", "xd-us": "United States of America", "usa (xd-us)": "United States of America",
                 "أميركية": "American", "אמריקני": "American"}   # spellings Wikidata's demonym list lacks
LANG_CODES = {"en": "English", "eng": "English", "en-us": "English", "en-gb": "English", "de": "German", "fr": "French", "es": "Spanish"}


def api_get(params):
    req = urllib.request.Request("https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json"}),
                                 headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def item_labels(ids):
    """All labels+aliases (every language) for a set of items, cached on disk."""
    cache = Path("data/wikidata_label_cache.json")
    labels = json.loads(cache.read_text()) if cache.exists() else {}
    todo = [i for i in ids if i not in labels]
    for i in range(0, len(todo), 50):
        ents = api_get({"action": "wbgetentities", "ids": "|".join(todo[i:i + 50]), "props": "labels|aliases"})["entities"]
        for qid, e in ents.items():
            labels[qid] = {"labels": {k: v["value"] for k, v in e.get("labels", {}).items()},
                           "aliases": sorted({a["value"] for vs in e.get("aliases", {}).values() for a in vs})}
    cache.write_text(json.dumps(labels, ensure_ascii=False))
    return {i: labels[i] for i in ids if i in labels}


def item_extras(ids):
    """For nationality and place items: demonyms (P1549) and the containing places (P131 chain, P17 country), cached on disk."""
    cache = Path("data/wikidata_item_extras.json")
    extras = json.loads(cache.read_text()) if cache.exists() else {}
    todo = [i for i in ids if i not in extras]
    for i in range(0, len(todo), 50):
        ents = api_get({"action": "wbgetentities", "ids": "|".join(todo[i:i + 50]), "props": "claims"})["entities"]
        for qid, e in ents.items():
            cl = e.get("claims", {})
            demonyms = sorted({c["mainsnak"]["datavalue"]["value"]["text"] for c in cl.get("P1549", []) if c["mainsnak"].get("snaktype") == "value"})
            parents = [c["mainsnak"]["datavalue"]["value"]["id"] for pid in ("P131", "P17") for c in cl.get(pid, []) if c["mainsnak"].get("snaktype") == "value" and c["rank"] != "deprecated"]
            extras[qid] = {"demonyms": demonyms, "parents": sorted(set(parents))}
    cache.write_text(json.dumps(extras, ensure_ascii=False))
    return {i: extras[i] for i in ids if i in extras}


def broader_items(qid, depth=4):
    """The places a place lies in: P131 upwards (county, state, country) plus P17, a few levels."""
    seen, frontier = [], [qid]
    for _ in range(depth):
        ex = item_extras(frontier)
        nxt = [p for f in frontier for p in ex.get(f, {}).get("parents", []) if p not in seen and p != qid]
        if not nxt:
            break
        seen.extend(dict.fromkeys(nxt)); frontier = nxt
    return seen


def claim_values(entity, pid):
    out = []
    for c in entity["claims"].get(pid, []):
        if c["rank"] == "deprecated" or c["mainsnak"].get("snaktype") != "value":
            continue
        out.append((c["mainsnak"]["datavalue"]["value"], c["rank"]))
    return out


def wd_time(v):
    """Wikidata time -> (iso-ish string, precision)."""
    t = v["time"].lstrip("+")
    y, m, d = t[:4], t[5:7], t[8:10]
    p = v["precision"]
    return ({9: y, 10: f"{y}-{m}", 11: f"{y}-{m}-{d}"}.get(p, y), p)


def wikidata_elements(entity):
    el = collections.defaultdict(list)
    for lang, l in entity["labels"].items():
        el["name_preferred"].append({"value": l["value"], "lang": lang, "via": "label"})
    for lang, als in entity["aliases"].items():
        for a in als:
            el["name_variant"].append({"value": a["value"], "lang": lang, "via": "alias"})
    for lang, d in entity["descriptions"].items():
        el["description"].append({"value": d["value"], "lang": lang, "via": "description"})
    for v, _ in claim_values(entity, "P742"):
        el["pseudonym"].append({"value": v, "lang": None, "via": "P742"})
        el["name_variant"].append({"value": v, "lang": None, "via": "P742"})
    for v, _ in claim_values(entity, "P1477"):
        el["name_variant"].append({"value": v["text"], "lang": v["language"], "via": "P1477 birth name"})
    for pid, elname in [("P569", "birth_date"), ("P570", "death_date")]:
        for v, rank in claim_values(entity, pid):
            s, p = wd_time(v)
            el[elname].append({"value": s, "lang": None, "via": pid, "precision": p, "rank": rank})
    item_props = {"P735": "given_name", "P734": "family_name", "P19": "birth_place", "P20": "death_place", "P21": "gender", "P106": "occupation",
                  "P27": "nationality", "P1412": "language", "P103": "language", "P800": "work", "P26": "related_agent", "P40": "related_agent",
                  "P22": "related_agent", "P25": "related_agent", "P3373": "related_agent", "P101": "field_of_activity", "P937": "activity_place",
                  "P551": "activity_place", "P31": "type"}
    items = set()
    for pid, elname in item_props.items():
        for v, rank in claim_values(entity, pid):
            items.add(v["id"])
            el[elname].append({"value": v["id"], "lang": None, "via": pid, "rank": rank})
    labels = item_labels(sorted(items))
    for elname, vals in el.items():
        for v in vals:
            if re.fullmatch(r"Q\d+", v["value"]) and v["value"] in labels:
                v["item"] = v["value"]
                v["labels"] = labels[v["value"]]["labels"]
                v["aliases"] = labels[v["value"]]["aliases"]
                v["value"] = labels[v["value"]]["labels"].get("en", v["value"])
    # nationality items carry demonyms ('American', 'estadounidense'); place items carry the places they lie in (Missouri, Connecticut, United States)
    for v in el.get("nationality", []):
        if v.get("item"):
            v["demonyms"] = item_extras([v["item"]]).get(v["item"], {}).get("demonyms", [])
    for elname in ("birth_place", "death_place", "activity_place"):
        for v in el.get(elname, []):
            if v.get("item"):
                broader = broader_items(v["item"])
                bl = item_labels(broader)
                v["broader"] = sorted({n for q in broader for n in [*bl.get(q, {}).get("labels", {}).values(), *bl.get(q, {}).get("aliases", [])]})
    for v, _ in claim_values(entity, "P18"):
        el["image"].append({"value": v, "lang": None, "via": "P18"})
    for site, s in entity.get("sitelinks", {}).items():
        el["see_also"].append({"value": s["title"], "lang": site.replace("wiki", ""), "via": f"sitelink {site}"})
    return el


# ---------- normalisation & matching ----------

def fold(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    return s


def name_key(s):
    """'Twain, Mark, 1835-1910' / 'Mark Twain' / 'TWAIN Mark' -> frozenset of name tokens."""
    s = fold(s)
    s = re.sub(r"\(.*?\)|\[.*?\]", " ", s)
    s = re.sub(r"\b1[0-9]{3}\b|\b(ca|b|d|fl|approximately)\.?", " ", s)
    toks = [t for t in re.split(r"[^\w']+", s) if t and len(t) > 1 and t not in ("de", "von", "van", "sieur", "mr", "mrs")]
    return frozenset(toks)


def date_key(s):
    s = str(s).strip()
    m = re.match(r"^(\d{4})-?(\d{2})?-?(\d{2})?", s.lstrip("+"))
    if not m:
        m = re.search(r"(\d{4})", s)
        return (m.group(1), None, None) if m else None
    return (m.group(1), m.group(2), m.group(3))


def compare_dates(site_vals, wd_vals):
    best = "mismatch"
    if all(str(sv["value"]).startswith("http") for sv in site_vals):
        return "uri_or_label_only"
    for sv in site_vals:
        if str(sv["value"]).startswith("http"):
            continue
        sk = date_key(sv["value"])
        if not sk:
            md = re.fullmatch(r"(\d{2})-(\d{2})", str(sv["value"]).strip())
            if md and any(date_key(wv["value"])[1:] == md.groups() for wv in wd_vals):
                best = "partial"
            continue
        for wv in wd_vals:
            wk = date_key(wv["value"])
            if sk == wk:
                return "match"
            if sk[0] == wk[0] and (sk[1] is None or wk[1] is None or sk[1] == wk[1]) and (sk[2] is None or wk[2] is None):
                best = "partial"
    return best


def item_names(wv):
    names = set()
    if wv.get("labels"):
        names.update(wv["labels"].values())
        names.update(wv.get("aliases", []))
    names.update(wv.get("demonyms", []))   # 'American', 'estadounidense', 'statunitense' for United States
    names.add(wv["value"])
    return {fold(n) for n in names}


def broader_names(wv):
    return {fold(n) for n in wv.get("broader", [])}


def stem_match(a, b):
    """'typografoi' ~ 'typografos', 'journalistes' ~ 'journaliste': same first 6+ letters, both long enough."""
    return len(a) >= 7 and len(b) >= 7 and a[:6] == b[:6]


# contradiction-capable elements vs additive ones: a site listing an occupation, work, relative or name form Wikidata lacks
# adds information, it does not contradict Wikidata, so a non-match there is 'no_overlap', never 'mismatch'
ADDITIVE = {"occupation", "language", "work", "related_agent", "pseudonym", "name_variant", "field_of_activity", "activity_place"}
WD_NAME_POOL = []        # every name form Wikidata has for him (labels, aliases, pseudonyms, birth name) - set by main()
WD_NAME_TOKENS = set()   # folded tokens of those forms, for given/family names coming from a pseudonym heading


def compare_item_text(site_vals, wd_vals, synonyms=None, stems=False):
    """Site strings vs Wikidata items: equal to any label/alias in any language -> match; containment -> partial."""
    best = "mismatch"
    if all(fold(sv["value"]).startswith("http") for sv in site_vals):
        best = "uri_or_label_only"
    for sv in site_vals:
        s = fold(sv["value"])
        if synonyms and s in synonyms:
            s = fold(synonyms[s])
        if s.startswith("http"):
            if any(wv.get("item") and wv["item"].lower() in s for wv in wd_vals):
                return "match"
            continue
        for wv in wd_vals:
            names = item_names(wv)
            if s in names:
                return "match"
            if any(n and (n in s or s in n) and len(min(n, s, key=len)) >= 4 for n in names):
                best = "partial"
            elif stems and any(stem_match(tok, n) for tok in re.split(r"[^\w]+", s) for n in names):
                best = "partial"
            elif best != "partial":
                wider = broader_names(wv)   # 'Missouri', 'Connecticut, United States': coarser than Wikidata's village, not wrong
                if s in wider or any(n and (n in s) and len(n) >= 4 for n in wider):
                    best = "partial"
    return best


def compare_names(site_vals, wd_vals):
    wd_keys = {name_key(w["value"]) for w in wd_vals}
    best = "mismatch"
    for sv in site_vals:
        k = name_key(sv["value"])
        if not k:
            continue
        if k in wd_keys:
            return "match"
        if any(k <= w or w <= k for w in wd_keys if w and k):
            best = "partial"
    return best


GENDER_FOLDED = {g: {fold(w) for w in ws} for g, ws in GENDER_WORDS.items()}


def gender_of(text):
    s = fold(text).strip()
    tail = re.split(r"[#/:]", s)[-1]  # URIs: schema.org/Male, gnd/gender#male, wikidata Q6581097
    for g, words in GENDER_FOLDED.items():
        if s in words or tail in words:
            return g
    return None


def compare_gender(site_vals, wd_vals):
    wd_g = next((gender_of(n) for w in wd_vals for n in [w["value"]] + list(w.get("labels", {}).values()) if gender_of(n)), None)
    got = {gender_of(sv["value"]) for sv in site_vals} - {None}
    if wd_g in got:
        return "match"
    return "mismatch" if got else "uri_or_label_only"


def unmatched_values(element, site_vals, wd_vals):
    """Site values that do not correspond to any Wikidata value (what the site adds)."""
    out = []
    if element in ("name_preferred", "name_variant", "pseudonym", "given_name", "family_name"):
        wd_keys = {name_key(w["value"]) for w in (WD_NAME_POOL or wd_vals)}
        for sv in site_vals:
            k = name_key(sv["value"])
            if k and k not in wd_keys and not any(k <= w for w in wd_keys if w):
                out.append(sv["value"])
    elif element in ("occupation", "nationality", "birth_place", "death_place", "language"):
        for sv in site_vals:
            if compare_item_text([sv], wd_vals) not in ("match", "partial"):
                out.append(sv["value"])
    elif element == "work":
        wd_keys = {name_key(w["value"]) for w in wd_vals}
        out = [sv["value"] for sv in site_vals if name_key(sv["value"]) not in wd_keys]
    return list(dict.fromkeys(out))


def compare(element, site_vals, wd_vals):
    if not site_vals and not wd_vals:
        return ""
    if not wd_vals:
        return "site_only"
    if not site_vals:
        return "wikidata_only"
    r = _compare(element, site_vals, wd_vals)
    if element in ADDITIVE and r == "mismatch":
        return "no_overlap"
    return r


def _compare(element, site_vals, wd_vals):
    if element in ("birth_date", "death_date"):
        return compare_dates(site_vals, wd_vals)
    if element in ("work", "related_agent"):
        r = compare_names(site_vals, wd_vals)
        return {"match": "overlap", "partial": "overlap", "mismatch": "no_overlap"}[r]
    if element in ("name_preferred", "name_variant", "pseudonym"):
        # any of his name forms: a pseudonym heading ('Conte, Louis de') or a label in another script ('马克·吐温') is still him
        return compare_names(site_vals, WD_NAME_POOL or wd_vals)
    if element in ("given_name", "family_name"):
        r = compare_item_text([{"value": re.sub(r"[,.]", "", v["value"])} for v in site_vals], wd_vals)
        for v in site_vals:
            toks = [x for x in re.split(r"[^\w']+", fold(v["value"])) if len(x) > 1]
            if r == "mismatch" and toks and all(x in WD_NAME_TOKENS or x in ("de", "von", "van") for x in toks):
                return "match"   # 'Louis de' / 'Conte' from the Sieur Louis de Conte pseudonym
        return r
    if element == "gender":
        return compare_gender(site_vals, wd_vals)
    if element == "nationality":
        vals = [{"value": re.sub(r".*#", "", v["value"])} for v in site_vals]   # GND's geographic-area-code#XD-US
        return compare_item_text(vals, wd_vals, COUNTRY_CODES, stems=True)
    if element == "language":
        return compare_item_text(site_vals, wd_vals, LANG_CODES)
    if element == "occupation":
        return compare_item_text(site_vals, wd_vals, stems=True)
    if element in ("birth_place", "death_place"):
        return compare_item_text(site_vals, wd_vals)
    if element == "image":
        return "present"
    return "present"


# ---------- cross-links ----------

def property_regexes(identifiers):
    """P1793 format regex per identifier property, cached."""
    cache = Path("data/wikidata_property_regex_cache.json")
    regs = json.loads(cache.read_text()) if cache.exists() else {}
    todo = sorted({r["property"] for r in identifiers} - set(regs))
    for i in range(0, len(todo), 50):
        ents = api_get({"action": "wbgetentities", "ids": "|".join(todo[i:i + 50]), "props": "claims"})["entities"]
        for pid, e in ents.items():
            vals = [c["mainsnak"]["datavalue"]["value"] for c in e.get("claims", {}).get("P1793", []) if c["mainsnak"].get("snaktype") == "value"]
            regs[pid] = vals[0] if vals else None
    cache.write_text(json.dumps(regs))
    return regs


def normalise_target(value, regex):
    """Trim the junk formatters leave around an id (names/n79021164, 118624822/about, DA00300263.rdf, 500020427-agent)."""
    def full(rx, c):
        try:
            return bool(re.fullmatch(rx, c))
        except re.error:  # Wikidata regexes are PCRE (\p{L} etc.); treat as unknown
            return True
    cands = [value]
    for pat in (r"^(names|subjects|authorities)/", r"/about$", r"\.(rdf|json|xml|ttl|html)$", r"-agent$", r"^sourceID/.*", r"/$"):
        cands.append(re.sub(pat, "", cands[-1]))
    for c in cands:
        if c and regex and full(regex, c):
            return c, True
    return value, bool(regex and full(regex, value))


def identifier_matchers(identifiers):
    """regex -> property, built from every formatter URL Wikidata knows for the identifier properties."""
    pats = []
    for r in identifiers:
        for f in set(r["all_formatter_urls"] + r["formatter_uri_for_rdf"] + r["third_party_formatter_urls"]):
            if "$1" not in f:
                continue
            core = re.escape(re.sub(r"^https?://(www\.)?", "", f)).replace(r"\$1", "(?P<v>[^/?#]+(?:/[^/?#]+)*?)", 1).replace(r"\$1", "(?P=v)")
            try:
                pats.append((re.compile(r"^(?:https?://)?(?:www\.)?" + core + r"/?$", re.I), r["property"], r["property_label"]))
            except re.error:
                continue
    return pats


def resolve_link(uri, matchers):
    u = uri.strip()
    for pat, prop, label in matchers:
        m = pat.match(u)
        if m:
            return prop, label, urllib.parse.unquote(m.group("v"))
    m = re.search(r"wikidata\.org/(?:entity|wiki)/(Q\d+)", u)
    if m:
        return "wikidata", "Wikidata", m.group(1)
    return None, None, None


def normalise_via(via):
    """Collapse a value's provenance to a predicate/field family for the vocabulary mapping."""
    via = via.split(" (")[0]
    m = re.match(r"llm:(?:[\w.-]+:\s*)?(.*)", via)
    if m:
        detail = m.group(1)
        if (t := re.search(r"(?:datafield|MARC|tag)\s*'?(\d{3})", detail)):
            return f"llm:MARC {t.group(1)}"
        if (t := re.search(r"og:\w+", detail)):
            return f"llm:{t.group(0)}"
        if re.search(r"microdata|itemprop", detail, re.I):
            return "llm:microdata"
        if re.search(r"biograph|description|text|summary|wiki", detail, re.I):
            return "llm:free text"
        return "llm:json field"
    if via.startswith("json:"):
        return "json:" + via[5:].split(".")[-1].split("[")[0]
    return via.split("/")[0]


def write_vocabulary_mapping(an, profiles):
    agg = collections.defaultdict(set)
    unmapped = collections.defaultdict(set)
    vocab_sites = collections.Counter()
    for prop, prof in profiles.items():
        for v in prof["vocabularies"]:
            vocab_sites[v] += 1
        for pred in prof["unmapped"]:
            unmapped[pred.split(" (")[0]].add(prof["property_label"])
        for el, vals in prof["elements"].items():
            for v in vals:
                agg[(el, normalise_via(v["via"]))].add(prof["property_label"])
    order = ["name_preferred", "name_variant", "pseudonym", "given_name", "family_name", "birth_date", "death_date", "birth_place", "death_place",
             "activity_place", "gender", "occupation", "field_of_activity", "nationality", "language", "description", "work", "subject_of", "related_agent",
             "same_as", "identifier", "see_also", "image", "source", "record_created", "record_modified", "license", "type"]
    L = ["# Vocabulary mapping: site predicates / fields → canonical element → Wikidata", "",
         f"Aggregated over the {len(profiles)} profiled sites. *sites* = how many sites supply that element through that predicate/field. "
         "Prefixes: `json:` = key in an ad-hoc JSON API; `llm:` = extracted by the LLM pass (`llm:og:*` = OpenGraph page metadata, `llm:MARC nnn` = a MARC field inside a JSON record, `llm:free text` = parsed out of a biography/description); "
         "bare three-digit numbers = MARC authority fields; `mads:` / `eac:` = MADS XML / EAC-CPF; otherwise the RDF predicate's local name.", "",
         "| element | Wikidata | predicate / field | sites | examples |", "|---|---|---|---|---|"]
    for el in order:
        rows_ = sorted(((len(sites), pred, sites) for (e, pred), sites in agg.items() if e == el), reverse=True)
        for n, pred, sites in rows_[:12]:
            L.append(f"| {el} | {ELEMENT_WD.get(el, '')} | `{pred[:50]}` | {n} | {', '.join(sorted(sites)[:3])[:80]} |")
    L += ["", "## Unmapped predicates / fields (seen on the entity, not assigned to an element)", "", "| predicate | sites |", "|---|---|"]
    for pred, sites in sorted(unmapped.items(), key=lambda kv: -len(kv[1]))[:50]:
        L.append(f"| `{pred[:70]}` | {len(sites)} |")
    L += ["", "## Vocabularies and formats (sites using each)", "", "| vocabulary | sites |", "|---|---|"]
    for v, n in vocab_sites.most_common(45):
        L.append(f"| `{v}` | {n} |")
    (an / "vocabulary_mapping.md").write_text("\n".join(L) + "\n")


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else "Q7245"
    data_dir = Path("data") / qid
    an = data_dir / "analysis"
    entity = json.loads((data_dir / "entity.json").read_text())
    identifiers = json.loads((data_dir / "identifiers.json").read_text())
    wd_ids = collections.defaultdict(set)
    for r in identifiers:
        wd_ids[r["property"]].add(r["value"])

    wd = wikidata_elements(entity)
    (an / "wikidata_elements.json").write_text(json.dumps(wd, ensure_ascii=False, indent=1))
    WD_NAME_POOL.extend(v for el in ("name_preferred", "name_variant", "pseudonym") for v in wd.get(el, []))
    WD_NAME_TOKENS.update(tok for v in WD_NAME_POOL for tok in name_key(v["value"]))
    WD_NAME_TOKENS.update(fold(v["value"]) for el in ("given_name", "family_name") for v in wd.get(el, []))

    profiles = {p.stem: json.loads(p.read_text()) for p in sorted((an / "profiles").glob("P*.json"), key=lambda p: int(p.stem[1:]))}
    matchers = identifier_matchers(identifiers)
    regexes = property_regexes(identifiers)
    elements = COMPARABLE + TEXT_ONLY

    comparison, matrix, crosslinks, vocab_rows = [], [], [], []
    for prop, prof in profiles.items():
        row = {"property": prop, "label": prof["property_label"]}
        site_el = prof["elements"]
        for el in elements:
            sv = site_el.get(el, [])
            status = compare(el, sv, wd.get(el, []))
            row[el] = status
            if status:
                comparison.append({
                    "property": prop, "label": prof["property_label"], "element": el, "status": status,
                    "site_values": " ‖ ".join(f"{v['value'][:80]}{'@' + v['lang'] if v.get('lang') else ''}" for v in sv[:12]),
                    "site_value_count": len(sv), "site_languages": ", ".join(sorted({v["lang"] for v in sv if v.get("lang")})),
                    "wikidata_values": " ‖ ".join(f"{v['value'][:60]}{'@' + v['lang'] if v.get('lang') else ''}" for v in wd.get(el, [])[:8]),
                    "wikidata_value_count": len(wd.get(el, [])), "wikidata_property": ELEMENT_WD.get(el, ""),
                    "site_via": ", ".join(sorted({v["via"].split("/")[0] for v in sv})[:6]),
                    "site_unmatched": " ‖ ".join(x[:60] for x in unmatched_values(el, sv, wd.get(el, []))[:15]),
                    "site_unmatched_count": len(unmatched_values(el, sv, wd.get(el, []))),
                })
        matrix.append(row)

        for v in site_el.get("same_as", []) + site_el.get("see_also", []) + site_el.get("identifier", []):
            if not v["value"].startswith("http"):
                continue
            p, plabel, val = resolve_link(v["value"], matchers)
            if p is None:
                if v["via"].split("/")[0] not in ("sameAs", "exactMatch", "closeMatch", "P5024", "wikidata"):
                    continue  # only genuine same-as assertions count when the target is unrecognised
                agree = "unknown system"
            elif p == "wikidata":
                agree = "match" if val == qid else "different item"
            else:
                val, valid = normalise_target(val, regexes.get(p))
                if p == prop and val in wd_ids.get(p, set()):
                    continue  # a record linking to itself
                if val in wd_ids.get(p, set()):
                    agree = "match"
                elif not valid:
                    agree = "not an id of that system"
                elif wd_ids.get(p):
                    agree = "different value"
                else:
                    agree = "wikidata lacks"
            crosslinks.append({"property": prop, "label": prof["property_label"], "link": v["value"], "via": v["via"],
                               "target_property": p or "", "target_label": plabel or "", "target_value": val or "", "wikidata": agree})

        for pred, n in prof["unmapped"].items():
            vocab_rows.append({"property": prop, "label": prof["property_label"], "predicate": pred, "element": "", "wikidata_property": "", "count": n})
        seen = set()
        for el, vals in site_el.items():
            for v in vals:
                key = (el, normalise_via(v["via"]))
                if key in seen:
                    continue
                seen.add(key)
                vocab_rows.append({"property": prop, "label": prof["property_label"], "predicate": key[1], "element": el,
                                   "wikidata_property": ELEMENT_WD.get(el, ""), "count": sum(1 for x in vals if normalise_via(x["via"]) == key[1])})

    def write_csv(name, rows, fields=None):
        with (an / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields or list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write_csv("comparison.csv", comparison)
    write_csv("comparison_matrix.csv", matrix, ["property", "label"] + elements)
    write_csv("crosslinks.csv", crosslinks)
    write_csv("vocabulary_mapping.csv", vocab_rows)
    write_vocabulary_mapping(an, profiles)

    # ---------- report ----------
    L = [f"# {qid} ({entity['labels']['en']['value']}): sites vs Wikidata", ""]
    L += [f"{len(profiles)} sites with data representations compared against Wikidata.", ""]
    L += ["## Element coverage and agreement", "", "| element | sites with it | match | partial | mismatch | URI only | site only | Wikidata has |", "|---|---|---|---|---|---|---|---|"]
    for el in elements:
        c = collections.Counter(r["status"] for r in comparison if r["element"] == el)
        has = sum(c[s] for s in ("match", "partial", "mismatch", "site_only", "present", "uri_or_label_only", "overlap", "no_overlap"))
        L.append(f"| {el} | {has} | {c['match'] + c['overlap']} | {c['partial']} | {c['mismatch'] + c['no_overlap']} | {c['uri_or_label_only']} | {c['site_only']} | {len(wd.get(el, []))} values |")
    L += ["", "## Mismatches worth a look", ""]
    for r in comparison:
        if r["status"] == "mismatch" and r["element"] in ("birth_date", "death_date", "birth_place", "death_place", "gender", "name_preferred", "given_name", "family_name"):
            L.append(f"- **{r['label']}** {r['element']}: site `{r['site_values'][:120]}` vs Wikidata `{r['wikidata_values'][:80]}`")
    L += ["", "## Partial agreement (less precise, or different form)", ""]
    for r in comparison:
        if r["status"] == "partial" and r["element"] in ("birth_date", "death_date", "birth_place", "death_place", "nationality", "occupation"):
            L.append(f"- {r['label']} {r['element']}: `{r['site_values'][:100]}` ~ `{r['wikidata_values'][:60]}`")
    L += ["", "## What sites have that Wikidata does not", ""]
    for el in ("name_variant", "name_preferred", "occupation", "work", "pseudonym", "given_name", "family_name"):
        rows_ = [r for r in comparison if r["element"] == el and r["site_unmatched_count"]]
        total = sum(r["site_unmatched_count"] for r in rows_)
        if rows_:
            top = sorted(rows_, key=lambda r: -r["site_unmatched_count"])[:6]
            L.append(f"- **{el}**: {total} site values with no Wikidata counterpart across {len(rows_)} sites; most from " +
                     "; ".join(f"{r['label']} ({r['site_unmatched_count']}: `{r['site_unmatched'][:70]}`)" for r in top))
    for el in ("source", "activity_place", "field_of_activity", "related_agent"):
        so = [r for r in comparison if r["element"] == el and r["status"] in ("site_only", "present", "no_overlap", "overlap")]
        if so:
            L.append(f"- {el}: {len(so)} sites, e.g. " + "; ".join(f"{r['label']} (`{r['site_values'][:50]}`)" for r in so[:4]))
    # scripts
    def script_of(text):
        for ch in text:
            if ch.isalpha():
                try:
                    name = unicodedata.name(ch).split(" ")[0]
                except ValueError:
                    continue
                return {"LATIN": "Latin", "CYRILLIC": "Cyrillic", "CJK": "Han", "HIRAGANA": "Kana", "KATAKANA": "Kana", "HANGUL": "Hangul", "ARABIC": "Arabic",
                        "HEBREW": "Hebrew", "GREEK": "Greek", "DEVANAGARI": "Devanagari", "BENGALI": "Bengali", "THAI": "Thai", "ARMENIAN": "Armenian",
                        "GEORGIAN": "Georgian", "ETHIOPIC": "Ethiopic", "TAMIL": "Tamil", "TELUGU": "Telugu", "GUJARATI": "Gujarati", "KANNADA": "Kannada",
                        "MALAYALAM": "Malayalam", "GURMUKHI": "Gurmukhi", "SINHALA": "Sinhala", "BURMESE": "Burmese", "MYANMAR": "Burmese", "KHMER": "Khmer"}.get(name, name.title())
        return None
    wd_scripts = collections.Counter(script_of(v["value"]) for el in ("name_preferred", "name_variant") for v in wd[el])
    site_scripts = collections.defaultdict(set)
    for prop, prof in profiles.items():
        for el in ("name_preferred", "name_variant"):
            for v in prof["elements"].get(el, []):
                sc = script_of(v["value"])
                if sc:
                    site_scripts[sc].add(prof["property_label"])
    L += ["", "## Name scripts", "", "| script | Wikidata labels/aliases | sites with names in it |", "|---|---|---|"]
    for sc in sorted(set(wd_scripts) | set(site_scripts), key=lambda x: -len(site_scripts.get(x, ()))):
        if sc:
            L.append(f"| {sc} | {wd_scripts.get(sc, 0)} | {len(site_scripts.get(sc, ()))} ({', '.join(sorted(site_scripts.get(sc, ()))[:6])}) |")
    # languages
    wd_langs = {v["lang"] for v in wd["name_preferred"]} | {v["lang"] for v in wd["name_variant"] if v.get("lang")}
    site_langs = collections.Counter()
    for prof in profiles.values():
        for el in ("name_preferred", "name_variant", "description"):
            for v in prof["elements"].get(el, []):
                if v.get("lang"):
                    site_langs[v["lang"]] += 1
    wd_name_keys = {name_key(v["value"]) for el in ("name_preferred", "name_variant") for v in wd[el]}
    mul = entity["labels"].get("mul", {}).get("value")
    new_forms = collections.defaultdict(list)  # lang -> (site, value) for name forms Wikidata lacks
    for prof in profiles.values():
        for el in ("name_preferred", "name_variant"):
            for v in prof["elements"].get(el, []):
                if v.get("lang") and not v["value"].startswith("http"):
                    k = name_key(v["value"])
                    if k and k not in wd_name_keys and not any(k <= w for w in wd_name_keys if w):
                        new_forms[v["lang"]].append((prof["property_label"], v["value"]))
    desc_langs = collections.defaultdict(set)
    for prof in profiles.values():
        for v in prof["elements"].get("description", []):
            if v.get("lang"):
                desc_langs[v["lang"].split("-")[0]].add(prof["property_label"])
    wd_desc_langs = {v["lang"] for v in wd["description"]}
    L += ["", "## Languages", "",
          f"Wikidata has labels in {len(wd_langs)} languages" + (f" plus a `mul` label (`{mul}`) that covers every language where the name is spelled that way" if mul else "") +
          f", aliases in {len(entity['aliases'])}, descriptions in {len(wd_desc_langs)}.",
          f"Sites tag values with {len(site_langs)} distinct language codes; most used: {', '.join(f'{k} ({n})' for k, n in site_langs.most_common(20))}.", "",
          "Languages in which sites carry name forms that Wikidata has in no label or alias (count of forms; examples):", ""]
    for lang, forms in sorted(new_forms.items(), key=lambda kv: -len(kv[1]))[:25]:
        ex = "; ".join(f"`{v[:40]}` ({site[:25]})" for site, v in forms[:3])
        L.append(f"- {lang}: {len(forms)} — {ex}")
    missing_desc = {l: sites for l, sites in desc_langs.items() if l not in wd_desc_langs}
    L += ["", f"Sites provide descriptions in {len(desc_langs)} languages; Wikidata has no description in: " +
          ", ".join(f"{l} ({', '.join(sorted(sites)[:3])})" for l, sites in sorted(missing_desc.items())[:30]), ""]
    # crosslinks
    cl = collections.Counter(r["wikidata"] for r in crosslinks)
    L += ["## Cross-links asserted by sites", "", f"{len(crosslinks)} links from {len({r['property'] for r in crosslinks})} sites: " + ", ".join(f"{k}: {n}" for k, n in cl.most_common()), ""]
    lacks = [r for r in crosslinks if r["wikidata"] == "wikidata lacks"]
    if lacks:
        L.append("Identifiers sites assert that Wikidata does not have at all for this item:")
        for r in lacks[:40]:
            L.append(f"- {r['label']} → {r['target_label']} = `{r['target_value']}`")
    diff = [r for r in crosslinks if r["wikidata"] == "different value"]
    if diff:
        L += ["", "Identifiers where the site points at a different value than Wikidata holds:"]
        for r in diff[:40]:
            L.append(f"- {r['label']} → {r['target_label']} = `{r['target_value']}` (Wikidata: {', '.join(sorted(wd_ids[r['target_property']]))[:80]})")
    unknown = collections.Counter(urllib.parse.urlsplit(r["link"]).netloc for r in crosslinks if r["wikidata"] == "unknown system")
    L += ["", f"Same-as targets not recognised as any Wikidata identifier property (top hosts): {', '.join(f'{h} ({n})' for h, n in unknown.most_common(25))}", ""]
    L += ["## Data-quality observations in the sources", "",
          "- VIAF's RDF emits `schema:alternateName` as given+family name concatenated without a space (`Jean FrançoisAlden`, `Samuel LanghorneClemens`).",
          "- Several sites encode year-only dates as 1 January (Databazeknih `1835-01-01`) or as a range end (NARA `1910-12-31`).",
          "- Genealogy sites (WikiTree, Find a Grave, FamilySearch) expose relatives' records as same-as/see-also links, which look like conflicting identifiers unless filtered.",
          "- Wikidata's own property formatters route some sites through redirectors (toolforge) and several sites' TLS certificates or hosts are broken (see `inventory.md`).", ""]
    review = an / "review.md"
    if review.exists():
        L += ["## Judged disagreements (Opus review pass)", "", "Every mismatch, partial date/place and cross-link disagreement above was judged individually; "
              "full verdicts in `review.json`, write-up in `review.md`. Summary:", ""]
        L += [line for line in review.read_text().splitlines() if not line.startswith("# ")]
        L.append("")
    L += ["## Files", "", "- `comparison.csv` — site × element with values on both sides", "- `comparison_matrix.csv` — status grid",
          "- `crosslinks.csv` — every same-as link, resolved", "- `vocabulary_mapping.csv` / `vocabulary_mapping.md` — site predicate/field → element → Wikidata property",
          "- `review.json` / `review.md` — judged verdicts on every disagreement (Opus review pass)",
          "- `wikidata_elements.json`, `profiles/*.json` — the two sides in full"]
    (an / "report.md").write_text("\n".join(L) + "\n")
    print(f"{len(profiles)} sites compared; {len(comparison)} site×element rows; {len(crosslinks)} cross-links")
    print(collections.Counter(r["status"] for r in comparison).most_common())
    print(f"-> {an / 'report.md'}")


if __name__ == "__main__":
    main()
