"""Step 1: list every external identifier on a Wikidata entity and the URL it links to.

    uv run python fetch_identifiers.py Q7245

Writes data/<QID>/entity.json (raw Wikidata entity), data/<QID>/wikidata_page.html
(the entity page as served) and data/<QID>/identifiers.json (one row per identifier
value, with the URL the Wikidata page links to).
"""

import html
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://www.wikidata.org/w/api.php"
USER_AGENT = "wikidata-naf-identifier-inventory/0.1 (thisismattmiller@gmail.com)"

P_FORMATTER_URL = "P1630"
P_THIRD_PARTY_FORMATTER_URL = "P3303"
P_FORMATTER_URI_RDF = "P1921"
P_SOURCE_WEBSITE = "P1896"
P_SUBJECT_ITEM = "P1629"
P_ISSUED_BY = "P2378"
P_APPLIES_IF_REGEX = "P8460"


def api_get(params):
    params = {**params, "format": "json"}
    req = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def get_entities(ids, props, languages="en"):
    entities = {}
    ids = list(ids)
    for i in range(0, len(ids), 50):
        params = {"action": "wbgetentities", "ids": "|".join(ids[i : i + 50]), "props": props}
        if languages:
            params["languages"] = languages
        data = api_get(params)
        entities.update(data["entities"])
    return entities


def snak_value(snak):
    if snak.get("snaktype") != "value":
        return None
    value = snak["datavalue"]["value"]
    if isinstance(value, dict):
        return value.get("id") or value.get("text")
    return value


def claim_values(entity, pid):
    """Non-deprecated values of a property, preferred rank first."""
    claims = [c for c in entity.get("claims", {}).get(pid, []) if c["rank"] != "deprecated"]
    claims.sort(key=lambda c: c["rank"] != "preferred")
    return [v for c in claims if (v := snak_value(c["mainsnak"])) is not None]


def wikidata_urlencode(value):
    # Same escaping Wikibase uses (wfUrlencode) when it expands a formatter URL
    return urllib.parse.quote_plus(value, safe=";@$!*(),/~:")


def pick_formatter(prop_entity, value):
    """Pick the formatter URL the Wikidata UI would use for this value.

    Formatter statements can carry an "applies if regular expression matches"
    qualifier (e.g. IMDb nm… vs tt…), so the choice depends on the value.
    """
    candidates = []
    for claim in prop_entity.get("claims", {}).get(P_FORMATTER_URL, []):
        if claim["rank"] == "deprecated":
            continue
        formatter = snak_value(claim["mainsnak"])
        if not formatter:
            continue
        regexes = [
            snak_value(q) for q in claim.get("qualifiers", {}).get(P_APPLIES_IF_REGEX, [])
        ]
        regex_match = False
        if regexes:
            try:
                regex_match = any(re.fullmatch(r, value) for r in regexes if r)
            except re.error:
                regex_match = False
            if not regex_match:
                continue
        # preferred rank wins, then a formatter whose regex matched this value
        candidates.append((claim["rank"] != "preferred", not regex_match, formatter))
    if not candidates:
        return None
    candidates.sort(key=lambda c: c[:2])
    return candidates[0][2]


def page_links(qid, out_dir):
    """The identifier links exactly as rendered on the entity page: {(pid, value): href}.

    The page is the source of truth for "what the identifier links to"; it can differ
    from the formatter URL we compute (cached renders, redirector formatters, escaping).
    """
    req = urllib.request.Request(
        f"https://www.wikidata.org/wiki/{qid}", headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        page = resp.read().decode("utf-8")
    (out_dir / "wikidata_page.html").write_text(page)

    links = {}
    groups = re.split(r'<div class="wikibase-statementgroupview" id="(P\d+)"', page)
    for pid, block in zip(groups[1::2], groups[2::2]):
        for href, text in re.findall(
            r'<a class="wb-external-id external" href="([^"]+)"[^>]*>(.*?)</a>', block
        ):
            links.setdefault((pid, html.unescape(text)), html.unescape(href))
    return links


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else "Q7245"
    out_dir = Path("data") / qid
    out_dir.mkdir(parents=True, exist_ok=True)

    entity = get_entities([qid], "labels|descriptions|aliases|claims|sitelinks", languages=None)[qid]
    (out_dir / "entity.json").write_text(json.dumps(entity, ensure_ascii=False, indent=1))

    id_claims = {
        pid: claims
        for pid, claims in entity["claims"].items()
        if claims[0]["mainsnak"]["datatype"] == "external-id"
    }
    props = get_entities(id_claims.keys(), "labels|descriptions|claims")

    # labels for the "subject item" / "issued by" items of each property (the institution/database)
    related = set()
    for prop in props.values():
        related.update(claim_values(prop, P_SUBJECT_ITEM))
        related.update(claim_values(prop, P_ISSUED_BY))
    related_labels = {
        k: v.get("labels", {}).get("en", {}).get("value")
        for k, v in get_entities(sorted(related), "labels").items()
    }

    def labelled(ids):
        return [{"id": i, "label": related_labels.get(i)} for i in ids]

    links = page_links(qid, out_dir)

    rows = []
    for pid, claims in id_claims.items():
        prop = props[pid]
        for claim in claims:
            value = snak_value(claim["mainsnak"])
            if value is None:
                continue
            formatter = pick_formatter(prop, value)
            computed_url = (
                formatter.replace("$1", wikidata_urlencode(value)) if formatter else None
            )
            rows.append(
                {
                    "property": pid,
                    "property_label": prop.get("labels", {}).get("en", {}).get("value"),
                    "property_description": prop.get("descriptions", {})
                    .get("en", {})
                    .get("value"),
                    "value": value,
                    "rank": claim["rank"],
                    # link as shown on the Wikidata page, else the one we compute
                    "url": links.get((pid, value)) or computed_url,
                    "wikidata_page_url": links.get((pid, value)),
                    "computed_url": computed_url,
                    "formatter_url": formatter,
                    "all_formatter_urls": claim_values(prop, P_FORMATTER_URL),
                    "third_party_formatter_urls": claim_values(prop, P_THIRD_PARTY_FORMATTER_URL),
                    "formatter_uri_for_rdf": claim_values(prop, P_FORMATTER_URI_RDF),
                    "source_website": claim_values(prop, P_SOURCE_WEBSITE),
                    "subject_item": labelled(claim_values(prop, P_SUBJECT_ITEM)),
                    "issued_by": labelled(claim_values(prop, P_ISSUED_BY)),
                }
            )

    rows.sort(key=lambda r: (int(r["property"][1:]), r["value"]))
    (out_dir / "identifiers.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))

    label = entity.get("labels", {}).get("en", {}).get("value")
    no_url = [r for r in rows if not r["url"]]
    print(f"{qid} ({label}): {len(id_claims)} identifier properties, {len(rows)} values")
    on_page = sum(1 for r in rows if r["wikidata_page_url"])
    print(f"  with a URL: {len(rows) - len(no_url)} ({on_page} taken from the page links)")
    print(f"  without a formatter URL: {len(no_url)}")
    for r in no_url:
        print(f"    no URL: {r['property']} {r['property_label']} = {r['value']}")
    print(f"wrote {out_dir / 'identifiers.json'}")


if __name__ == "__main__":
    main()
