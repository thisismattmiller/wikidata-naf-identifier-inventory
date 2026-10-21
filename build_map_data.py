"""Step 9: one JSON for the web map - every identifier with its quality, access, format, landscape,
comparison and domain facts.

    uv run python build_map_data.py Q7245

Also fills atlas.template.html with that JSON to produce analysis/atlas.html, the web map.

Reads analysis/quality_sites.csv (step 8), analysis/site_elements.csv (step 6), analysis/comparison_matrix.csv
(step 7), analysis/site_domains.json (Opus classification of each site's domain/region), data/landscape/counts.csv
and writes analysis/map_data.json, which atlas.html embeds.
"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

ELEMENTS = ["name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place", "death_place",
            "activity_place", "gender", "occupation", "field_of_activity", "nationality", "language", "description", "work", "subject_of", "related_agent",
            "same_as", "identifier", "image", "source"]
ACCESS_GROUP = {
    "plain HTTP": "plain HTTP",
    "none": "no entity data",
}


TIER_GROUP = {"curl": "plain HTTP", "ua": "HTTP with a User-Agent", "browser": "HTTP with browser headers"}


def client_summary(cp):
    """What each client profile got, per target, for the detail panel."""
    if not cp:
        return None
    rows = []
    for t in cp["targets"]:
        got = {k: ("record" if r.get("served") else "challenge" if r.get("challenge") else r.get("status") or (r.get("error") or "no reply")[:24]) for k, r in t["results"].items()}
        rows.append({"kind": t["kind"], "format": t.get("format"), "url": t["url"], "tier": t["tier"], "got": got})
    return {"best": cp["best"], "page": cp["page_tier"], "targets": rows}


def conneg_summary(cp):
    """Per URL: which Accept headers got a real non-HTML representation naming him, and what format came back."""
    if not cp:
        return None
    rows, serves = [], set()
    for t in cp["targets"]:
        ok = {a.split("/")[-1]: r["format"] for a, r in t["results"].items() if r.get("ok")}
        if t["kind"] != "page":
            # a JSON endpoint that answers JSON to every Accept header is not negotiating; only formats other than its usual one count
            from collections import Counter
            usual = Counter(ok.values()).most_common(1)[0][0] if ok else None
            if len(set(ok.values())) > 1:
                ok = {a: f for a, f in ok.items() if f != usual}
            else:
                ok = {}
        rows.append({"kind": t["kind"], "url": t["url"], "got": ok})
        serves.update(ok.values())
    return {"serves": sorted(serves), "targets": rows}


def access_group(a, has_data=True, cp=None):
    """The access facet: measured with curl (probe_clients.py) when the probe ran; the crawl's own routes otherwise."""
    if cp is not None and has_data:
        best = cp["best"]
        if best is None and cp["page_tier"]:
            # a data URL that is gone (404) or was a template ('$wkpLink') says nothing about reachability; the page does
            failed = [t for t in cp["targets"] if t["kind"] != "page" and not t["tier"]]
            if all("$" in t["url"] or all(r.get("status") == 404 for r in t["results"].values()) for t in failed):
                best = cp["page_tier"]
        if best in TIER_GROUP:
            return TIER_GROUP[best]
        # nothing served his record: a 200 without his name is a shell that needs JavaScript; otherwise every client was refused
        need = [t for t in cp["targets"] if t["kind"] != "page"] or cp["targets"]
        if any(r.get("status") == 200 for t in need for r in t["results"].values()):
            return "JS-rendered page only"
        return "page blocks plain clients"
    a = a.split(" + page text")[0]
    if a in ACCESS_GROUP:
        return ACCESS_GROUP[a]
    if a.startswith("plain HTTP, partly"):
        return "plain HTTP, partly"
    if a.startswith("page text only"):   # his record is page text: the route is whether a plain client gets that page
        return "page blocks plain clients" if "blocked" in a else "untested" if "untested" in a else "plain HTTP"
    if "browser" in a:
        return "browser session only"
    if "blocked" in a:
        return "page blocks plain clients"
    if "js-rendered" in a or "unprobed" in a:
        return "JS-rendered page only"
    return a

# ---------- "everything about him": one block per element, every site's values merged with Wikidata's ----------
UBER = [("name_preferred", "Preferred name"), ("pseudonym", "Pseudonyms"), ("name_variant", "Name variants"), ("given_name", "Given name"), ("family_name", "Family name"),
        ("birth_date", "Birth date"), ("death_date", "Death date"), ("birth_place", "Birth place"), ("death_place", "Death place"), ("activity_place", "Places of activity"),
        ("gender", "Gender"), ("nationality", "Nationality"), ("language", "Languages"), ("occupation", "Occupations"), ("field_of_activity", "Fields of activity"),
        ("description", "Descriptions"), ("work", "Works by him"), ("subject_of", "Works about him"), ("related_agent", "Related people and organisations"),
        ("image", "Images"), ("same_as", "Same-as links"), ("identifier", "Identifiers"), ("see_also", "See also"), ("source", "Sources cited")]
LIST_ELEMENTS = {"work", "subject_of", "related_agent", "same_as", "identifier", "see_also", "source"}
LINK_ELEMENTS = {"image", "same_as", "identifier", "see_also", "source"}
NAME_ELEMENTS = {"name_preferred", "pseudonym", "name_variant", "given_name", "family_name"}


def uber_norm(v):
    import re, unicodedata
    v = unicodedata.normalize("NFKC", str(v)).strip()
    v = re.sub(r"T00:00:00(Z|\+00:00)?$", "", v)
    if v.startswith(("http://", "https://")):
        return re.sub(r"^https?://(www\.)?", "", v).rstrip("/").lower()
    return re.sub(r"[\W_]+", " ", v.casefold()).strip()


def build_uber(an, sites):
    import re
    labels = {s["p"]: s["label"] for s in sites}
    wd = json.loads((an / "wikidata_elements.json").read_text())
    wd_forms = {}   # element -> {norm: display}
    for el, vals in wd.items():
        forms = wd_forms.setdefault(el, {})
        for x in vals:
            forms.setdefault(uber_norm(x["value"]), x["value"])
            for lab in (x.get("labels") or {}).values():
                forms.setdefault(uber_norm(lab), x["value"])
    name_pool = {}
    for el in NAME_ELEMENTS:
        name_pool.update(wd_forms.get(el, {}))
    profiles = {f.stem: json.loads(f.read_text()) for f in sorted((an / "profiles").glob("P*.json"))}
    blocks = []
    for el, title in UBER:
        pool = name_pool if el in NAME_ELEMENTS else wd_forms.get(el, {})
        chips = {}            # norm -> {v, n, p, lang}
        holdings = []
        total = 0
        for p, prof in profiles.items():
            vals = prof.get("elements", {}).get(el) or []
            if el not in LINK_ELEMENTS:
                vals = [x for x in vals if not x.get("uri")]
            if not vals:
                continue
            total += len(vals)
            seen_here = set()
            firsts = []
            for x in vals:
                v = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(x["value"]))).strip()
                if not v:
                    continue
                k = uber_norm(v)
                if k not in seen_here and len(firsts) < 10:
                    firsts.append(v[:120])
                seen_here.add(k)
                c = chips.setdefault(k, {"v": v if el == "image" else v[:160], "n": 0, "p": [], "lang": x.get("lang") or None})
                if p not in c["p"]:
                    c["p"].append(p); c["n"] += 1
                if not c["lang"] and x.get("lang"):
                    c["lang"] = x["lang"]
            if el in LIST_ELEMENTS:
                holdings.append({"p": p, "n": len(seen_here), "first": firsts})
        for k, c in chips.items():
            c["wd"] = k in pool
            if c["lang"] in ("en", "und", "mul", "none"):
                c["lang"] = None
        order = sorted(chips.values(), key=lambda c: (-c["n"], c["v"].casefold()))
        cap = 500
        if el in LIST_ELEMENTS:   # long lists: chips only for values several sites share; the holdings carry the rest
            order, cap = [c for c in order if c["n"] >= 2], 120
        wd_only = [{"v": v, "lang": None} for k, v in (wd_forms.get(el, {}) if el not in NAME_ELEMENTS else {}).items() if k not in chips]
        # Wikidata's own list for name elements: labels/aliases the sites never state
        if el in NAME_ELEMENTS:
            wd_only = [{"v": x["value"], "lang": x.get("lang")} for x in wd.get(el, []) if uber_norm(x["value"]) not in chips]
        seen_wd = set(); dedup = []
        for x in wd_only:
            if x["v"] not in seen_wd:
                seen_wd.add(x["v"]); dedup.append(x)
        holdings.sort(key=lambda h: -h["n"])
        blocks.append({
            "el": el, "title": title, "total": total, "sites": sum(1 for p, prof in profiles.items() if (prof.get("elements", {}).get(el))),
            "distinct": len(chips), "wd_n": len(wd.get(el, [])), "wd_sites_agree": sum(1 for c in chips.values() if c["wd"]),
            "chips": order[:cap], "more": max(0, len(order) - cap), "wd_only": dedup[:80], "wd_only_more": max(0, len(dedup) - 80),
            "holdings": holdings, "list": el in LIST_ELEMENTS, "wide": len(chips) > 60 or el in LIST_ELEMENTS,
        })
    sprite_manifest = an / "images" / "images.json"   # from build_image_sprite.py
    if sprite_manifest.exists():
        m = json.loads(sprite_manifest.read_text())
        items = [{"url": r["url"], "p": r["p"], "wd": r.get("wd", False), "i": r.get("sprite"), "w": r.get("w"), "h": r.get("h"),
                  "via": r.get("via"), "error": None if r.get("ok") else (r.get("error") or "failed")} for r in m["images"]]
        ok_urls = {r["url"] for r in m["images"] if r.get("ok")}
        for b in blocks:
            if b["el"] == "image":
                b["sprite"] = {"file": m["sprite"], "tile": m["tile"], "cols": m["cols"], "count": m["count"], "fetched": m.get("fetched"), "items": items}
                # a value whose URL(s) are all in the sprite needs no chip; a value packing several URLs is kept only if one of them failed
                b["chips"] = [c for c in b["chips"] if not all(part.strip() in ok_urls for part in re.split(r",\s*(?=https?://)", c["v"]))]
                b["wd_only"] = []
    return {"blocks": blocks, "labels": labels}


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else "Q7245"
    an = Path("data") / qid / "analysis"
    sites = list(csv.DictReader((an / "quality_sites.csv").open()))
    elements = {r["property"]: r for r in csv.DictReader((an / "site_elements.csv").open())}
    matrix = {r["property"]: r for r in csv.DictReader((an / "comparison_matrix.csv").open())}
    domains = json.loads((an / "site_domains.json").read_text()) if (an / "site_domains.json").exists() else {}
    landscape = {r["property"]: r for r in csv.DictReader((Path("data") / "landscape" / "counts.csv").open())}
    identifiers = json.loads((Path("data") / qid / "identifiers.json").read_text())
    client_probe = json.loads((an / "client_probe.json").read_text()) if (an / "client_probe.json").exists() else {}   # probe_clients.py
    conneg_probe = json.loads((an / "conneg_probe.json").read_text()) if (an / "conneg_probe.json").exists() else {}   # probe_conneg.py
    audit = {}   # end-to-end Opus audit of each site: analysis/audit/verdicts_*.json
    rounds = [(an / "audit", 1), (an / "audit" / "round2", 2)]
    for d, rnd in rounds:
        for vf in sorted(d.glob("verdicts_*.json")) if d.exists() else []:
            for v in json.loads(vf.read_text()):
                audit[v["property"]] = {k: v.get(k) for k in ("verdict", "page_shows_record", "captured_faithfully", "wrong_values", "missing", "label_issues", "notable", "confidence")}
                audit[v["property"]]["round"] = rnd   # a later round's verdict replaces the earlier one
    first_url = {}
    for rec in identifiers:
        first_url.setdefault(rec["property"], rec["url"])

    def b(v):
        return v == "True"

    def num(v, f=float):
        try:
            return f(v)
        except (TypeError, ValueError):
            return None

    out = []
    for s in sites:
        p = s["property"]
        el = elements.get(p, {})
        filled = [e for e in ELEMENTS if num(el.get(e), int)]
        mx = matrix.get(p, {})
        formats = sorted({f for f in s["entity_formats"].split(", ") if f})
        if "marc-json" in s["formats_used"].split(", ") and "json" in formats:
            formats = sorted((set(formats) - {"json"}) | {"marc-json"})   # the profiler parsed that JSON as MARC
        if not formats and s["has_entity_data"] == "True":
            formats = sorted({f for f in s["formats_used"].split(", ") if f and f not in ("html", "text", "unknown", "image", "svg")})
        fam = "no entity data"
        mechs = [m for m in s["entity_mechanisms"].split("; ") if m]
        endpoint = any(not m.startswith("embedded") for m in mechs)   # data from a link/conneg/export/XHR, not lifted from the page
        if s.get("page_text_only") == "True":
            fam = "no structured data"   # his record is page text only; there is no serialisation to name
        elif any(f in ("marcxml", "marc-binary", "mads", "eac-cpf", "marc-json") for f in formats):
            fam = "library format"
        elif endpoint and any(f in ("json-ld", "rdf-xml", "turtle", "n-triples") for f in formats):
            fam = "RDF"
        elif endpoint and any(f in ("json", "xml", "csv", "feed") for f in formats):
            fam = "ad-hoc JSON/XML"
        elif any(f in ("rdfa", "microdata", "json-ld", "opengraph") for f in formats):
            fam = "embedded markup"
        elif s["has_entity_data"] == "True":
            fam = "no structured data"
        d = domains.get(p, {})
        out.append({
            "p": p, "label": s["label"], "host": s["hosts"].split("; ")[0], "url": first_url.get(p),
            "domain": d.get("domain", "unclassified"), "region": d.get("region"),
            "pages": int(s["pages"]), "status": s["status"], "resolved": b(s["resolved"]), "wrong_page_reason": s.get("wrong_page_reason") or None, "status_note": s.get("status_note") or None,
            "entity_on_page": b(s.get("entity_on_page")), "page_text_only": b(s.get("page_text_only")),
            "challenge": b(s["challenge_widget"]), "paused": b(s["challenge_paused"]), "login": b(s["login_box"]), "consent": b(s["consent_manager"]),
            "ads": s["ads"], "ad_hosts": int(s["ad_hosts"]), "analytics": int(s["analytics_hosts"]), "third_party": int(s["third_party_hosts"]),
            "html_kb": int(s["html_kb"]), "load_s": num(s["load_seconds"]),
            "has_data": b(s["has_entity_data"]), "access": s["entity_data_access"], "access_group": access_group(s["entity_data_access"], b(s["has_entity_data"]), client_probe.get(p)),
            "client": client_summary(client_probe.get(p)),
            "conneg": conneg_summary(conneg_probe.get(p)),
            "formats": formats, "format_family": fam, "mechanisms": [m for m in s["entity_mechanisms"].split("; ") if m],
            "llm": b(s["needed_llm_extraction"]), "elements": filled, "n_elements": int(s["elements"]), "values": int(s["values"]),
            "languages": int(s["languages"]), "unique_share": num(s["unique_share"]), "descriptive_values": int(s["descriptive_values"]),
            "page_values": int(s.get("page_text_values") or 0),
            "useful": num(s.get("useful_score"), float) or 0, "beyond_wd": int(s.get("values_beyond_wikidata") or 0),
            "useful_by": dict((k, int(v)) for k, v in (x.split(":") for x in (s.get("useful_by") or "").split("; ") if x)),
            "wd": {k: mx.get(k) for k in ELEMENTS if mx.get(k) and mx.get(k) != "wikidata_only"},
            "wd_match": int(s["wd_match"]), "wd_mismatch": int(s["wd_mismatch"]), "not_in_wd": int(s["values_not_in_wikidata"]),
            "rank": num(s["p244_rank"], int), "share": num(s["p244_share"]),
            "audit": audit.get(p),
        })
    out.sort(key=lambda r: int(r["p"][1:]))

    top = []
    for r in sorted(landscape.values(), key=lambda r: int(r["rank"]))[:60]:
        top.append({"p": r["property"], "label": r["label"], "share": float(r["share"]), "human_share": float(r["human_share"]), "items": int(r["items"]),
                    "crawled": r["property"] in {s["p"] for s in out}})
    meta = {
        "qid": qid, "sites": len(out), "p244_items": int(landscape["P244"]["items"]) if "P244" in landscape else None,
        "ext_id_properties": len(landscape), "used_properties": sum(1 for r in landscape.values() if int(r["items"]) > 0),
        "domain_counts": dict(Counter(s["domain"] for s in out).most_common()),
        "audit_counts": dict(Counter((s["audit"] or {}).get("verdict", "not audited") for s in out).most_common()),
    }
    uber = build_uber(an, out)
    payload = json.dumps({"meta": meta, "sites": out, "top": top, "uber": uber}, ensure_ascii=False)
    (an / "map_data.json").write_text(payload)
    template = Path("atlas.template.html")
    if template.exists():
        html = template.read_text().replace("/*__DATA__*/", payload.replace("</", "<\\/"))
        (an / "atlas.html").write_text(html)
        docs = Path("docs")   # the static site GitHub Pages serves (.github/workflows/pages.yml)
        docs.mkdir(exist_ok=True)
        head, body = html.split("</style>\n", 1)   # the artifact host wraps the page itself; a static file needs the skeleton
        (docs / "index.html").write_text(
            '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<meta name="description" content="What the external identifiers on a Wikidata bibliographic name actually link to: the data behind each of Mark Twain\'s 315 identifiers, how a machine can get it, how it is serialised, and how useful it is beyond Wikidata.">\n'
            + head + "</style>\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")
    print(f"{len(out)} sites -> {an / 'map_data.json'} and atlas.html; domains: {meta['domain_counts']}")


if __name__ == "__main__":
    main()
