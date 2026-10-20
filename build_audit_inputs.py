"""Audit inputs: one JSON object per identifier with everything an independent judge needs to say whether the atlas
tells the truth about it (Wikidata values, crawl records with page excerpts, profile summary, atlas labels, extraction
notes, review verdicts), split into batches for Opus auditors.

    uv run python build_audit_inputs.py Q7245 [--only P1,P2,...] [--batches 16] [--out analysis/audit/round2]

Reads analysis/map_data.json (step 9), quality_sites.csv, profiles/, llm_extractions*/ and review.json.
Instructions for the auditors live in analysis/audit/INSTRUCTIONS.md; verdicts go to <out>/verdicts_<N>.json.
"""

import argparse
import collections
import csv
import glob
import json
import re
from pathlib import Path

ENTITY_RX = re.compile(r"Twain|Clemens|Твен|טוויין|توين|吐温|トウェイン|트웨인")


def uniq_bucket(s):
    if s["unique_share"] is None or s["descriptive_values"] == 0:
        return "no descriptive data"
    if s["descriptive_values"] < 5:
        return "too few values to judge (< 5)"
    return "mostly unique (> 60%)" if s["unique_share"] > 0.6 else "mixed (30–60%)" if s["unique_share"] >= 0.3 else "mostly repeated (< 30%)"


def excerpt(pages, key):
    t = ""
    for f in [pages / f"{key}.txt"] + sorted(pages.glob(f"{key}__frame*.txt")):
        if f.exists():
            t += "\n" + f.read_text(errors="ignore")
    t = re.sub(r"\s+", " ", t).strip()
    m = ENTITY_RX.search(t)
    head = t[:1200]
    if m and m.start() > 1000:
        head += " […] " + t[max(0, m.start() - 200): m.start() + 800]
    return {"chars": len(t), "excerpt": head}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qid", nargs="?", default="Q7245")
    ap.add_argument("--only", help="comma-separated property ids")
    ap.add_argument("--batches", type=int, default=16)
    ap.add_argument("--out", default="analysis/audit")
    args = ap.parse_args()
    D = Path("data") / args.qid
    an = D / "analysis"
    out = D / args.out
    (out / "batches").mkdir(parents=True, exist_ok=True)
    only = set(args.only.split(",")) if args.only else None
    map_sites = {s["p"]: s for s in json.loads((an / "map_data.json").read_text())["sites"]}
    ids = collections.defaultdict(list)
    for r in json.loads((D / "identifiers.json").read_text()):
        ids[r["property"]].append({"value": r["value"], "url": r["url"]})
    rev = collections.defaultdict(list)
    for x in json.loads((an / "review.json").read_text()):
        rev[x["property"]].append(x)
    sites = []
    for p, s in map_sites.items():
        if only and p not in only:
            continue
        recs = []
        for rf in sorted(glob.glob(str(D / f"records/{p}__*.json"))):
            r = json.loads(Path(rf).read_text())
            pg = r.get("page") or {}
            recs.append({"value": r["value"], "url": r["url"], "wikidata_url": r.get("wikidata_url"), "override_reason": r.get("url_override_reason"),
                         "final_url": pg.get("final_url"), "crawl_status": r["status"], "title": pg.get("title"), "page": excerpt(D / "pages", Path(rf).stem),
                         "screenshot": r.get("screenshot_file")})
        pf = an / f"profiles/{p}.json"
        prof = json.loads(pf.read_text()) if pf.exists() else None
        elements = {}
        for el, vals in (prof["elements"].items() if prof else []):
            if not vals:
                continue
            page = [v for v in vals if (v.get("via") or "").startswith("llm-page")]
            elements[el] = {"n": len(vals), "from_structured": len(vals) - len(page), "from_page_text": len(page),
                            "samples": [{"value": v["value"][:120], "via": (v.get("via") or "")[:60]} for v in vals[:5]]}
        notes = {}
        for d in ("llm_extractions", "llm_extractions_pages"):
            f = an / d / f"{p}.json"
            if f.exists():
                e = json.loads(f.read_text())
                notes[d] = {"about_entity": e.get("about_entity"), "page_kind": e.get("page_kind"), "notes": e.get("notes")}
        sites.append({
            "property": p, "label": s["label"], "host": s["host"], "domain": s["domain"], "wikidata_values": ids[p], "records": recs,
            "atlas_labels": {"status": s["status"], "status_note": s.get("status_note"), "resolved": s["resolved"], "wrong_page_reason": s.get("wrong_page_reason"),
                             "entity_on_page": s["entity_on_page"], "has_data": s["has_data"], "access": s["access"], "access_group": s["access_group"],
                             "format_family": s["format_family"], "formats": s["formats"], "values": s["values"], "page_text_values": s.get("page_values", 0),
                             "descriptive_values": s["descriptive_values"], "unique_share": s["unique_share"], "uniqueness_bucket": uniq_bucket(s),
                             "page_text_only": s["page_text_only"], "wd_match": s["wd_match"], "wd_mismatch": s["wd_mismatch"]},
            "profile_elements": elements, "chrome_elements_parked": {k: len(v) for k, v in (prof or {}).get("chrome_elements", {}).items()},
            "extraction_notes": notes, "review_verdicts": dict(collections.Counter(x["verdict"] for x in rev[p])),
            "review_flags": [{"element": x["element_or_link"], "verdict": x["verdict"], "reason": x["reason"][:200]} for x in rev[p]
                             if x["verdict"] in ("site_disagrees", "wikidata_gap_or_error", "different_entity", "unclear")],
            "previous_audit": s.get("audit"),
        })
    sites.sort(key=lambda s: int(s["property"][1:]))
    n = min(args.batches, len(sites)) or 1
    per = (len(sites) + n - 1) // n
    for i in range(n):
        json.dump(sites[i * per:(i + 1) * per], (out / "batches" / f"batch_{i}.json").open("w"), ensure_ascii=False, indent=1)
    print(f"{len(sites)} sites in {n} batches of {per} -> {out / 'batches'}")


if __name__ == "__main__":
    main()
