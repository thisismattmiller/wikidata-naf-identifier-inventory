"""Landscape: which external identifiers do bibliographic entities carry?

    uv run python identifier_landscape.py [--anchor P244]

A "bibliographic entity" is any Wikidata item with a Library of Congress authority ID (P244). For
every external-identifier property we count how many of those items carry it, overall and for the
human (P31 = Q5) subset, using the QLever Wikidata endpoint (https://qlever.dev/api/wikidata - fresh,
fast, but every query must finish within 30 s - it answers HTTP 429 with "Operation timed out" - so a
single GROUP BY over all 1.7M items times out; we group over 200k-item slices (ORDER BY ?item LIMIT/OFFSET)
and add the slices up, checkpointing each slice to data/landscape/chunks.jsonl).

Outputs under data/landscape/: counts.csv (one row per property, sorted by item count), landscape.md
(the ranked table with shares, class breakdown of P244 items, and where Q7245's identifiers sit).
"""

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://qlever.dev/api/wikidata"
CHUNK = 200_000  # anchor items per query (~6 s each); the whole set in one GROUP BY exceeds QLever's 30 s limit
PREFIXES = "PREFIX wdt: <http://www.wikidata.org/prop/direct/> PREFIX wd: <http://www.wikidata.org/entity/> PREFIX wikibase: <http://wikiba.se/ontology#> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX schema: <http://schema.org/> "
OUT = Path("data") / "landscape"


class QueryTimeout(RuntimeError):
    pass


def sparql(query, retries=3):
    req = urllib.request.Request(ENDPOINT, data=(PREFIXES + query).encode(), headers={
        "Accept": "application/sparql-results+json", "Content-Type": "application/sparql-query",
        "User-Agent": "wikidata-identifier-inventory/0.1 (thisismattmiller@gmail.com)"})
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.load(resp)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if "timed out" in body:
                raise QueryTimeout(body[:200]) from None
            last = f"{e.code} {body[:200]}"
        except Exception as e:  # noqa: BLE001
            last = e
        else:
            if "exception" in data:
                if "timed out" in data["exception"]:
                    raise QueryTimeout(data["exception"][:200])
                last = data["exception"][:200]
            else:
                return data["results"]["bindings"]
        time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"query failed: {last}")


def val(b, k):
    return b[k]["value"] if k in b else None


def external_id_properties():
    rows = sparql("""SELECT ?p ?label ?formatter ?subject WHERE {
      ?p wikibase:propertyType wikibase:ExternalId .
      OPTIONAL { ?p rdfs:label ?label FILTER(LANG(?label) = "en") }
      OPTIONAL { ?p wdt:P1630 ?formatter }
      OPTIONAL { ?p wdt:P1629 ?subject }
    }""")
    props = {}
    for b in rows:
        pid = val(b, "p").rsplit("/", 1)[-1]
        d = props.setdefault(pid, {"property": pid, "label": None, "formatter": None, "subject": None})
        d["label"] = d["label"] or val(b, "label")
        d["formatter"] = d["formatter"] or val(b, "formatter")
        d["subject"] = d["subject"] or (val(b, "subject") or "").rsplit("/", 1)[-1] or None
    return props


def count_chunk(anchor, offset, humans_only=False):
    """{pid: items in this slice carrying pid}. Slices are disjoint, so per-slice DISTINCT counts add up."""
    extra = " ?item wdt:P31 wd:Q5 ." if humans_only else ""
    q = f"""SELECT ?p (COUNT(DISTINCT ?item) AS ?n) WHERE {{
      {{ SELECT ?item WHERE {{ ?item wdt:{anchor} ?a }} ORDER BY ?item LIMIT {CHUNK} OFFSET {offset} }}
      ?item ?p ?v .{extra} ?prop wikibase:directClaim ?p ; wikibase:propertyType wikibase:ExternalId .
    }} GROUP BY ?p"""
    return {val(b, "p").rsplit("/", 1)[-1]: int(val(b, "n")) for b in sparql(q)}


def class_breakdown(anchor):
    rows = sparql(f"""SELECT ?class ?label (COUNT(DISTINCT ?item) AS ?n) WHERE {{
      ?item wdt:{anchor} ?a . ?item wdt:P31 ?class .
      OPTIONAL {{ ?class rdfs:label ?label FILTER(LANG(?label) = "en") }}
    }} GROUP BY ?class ?label ORDER BY DESC(?n) LIMIT 40""")
    return [{"class": val(b, "class").rsplit("/", 1)[-1], "label": val(b, "label"), "items": int(val(b, "n"))} for b in rows]


def totals(anchor):
    t = int(val(sparql(f"SELECT (COUNT(DISTINCT ?item) AS ?n) WHERE {{ ?item wdt:{anchor} ?a }}")[0], "n"))
    h = int(val(sparql(f"SELECT (COUNT(DISTINCT ?item) AS ?n) WHERE {{ ?item wdt:{anchor} ?a . ?item wdt:P31 wd:Q5 }}")[0], "n"))
    return t, h


def ids_per_item_distribution(anchor, total):
    """How many external identifiers does a P244 item typically have? (sliced like the counts)"""
    buckets = {}
    for offset in range(0, total, CHUNK):
        rows = sparql(f"""SELECT ?bucket (COUNT(?item) AS ?n) WHERE {{
          {{ SELECT ?item (COUNT(DISTINCT ?p) AS ?k) WHERE {{
               {{ SELECT ?item WHERE {{ ?item wdt:{anchor} ?a }} ORDER BY ?item LIMIT {CHUNK} OFFSET {offset} }}
               ?item ?p ?v . ?prop wikibase:directClaim ?p ; wikibase:propertyType wikibase:ExternalId . }} GROUP BY ?item }}
          BIND(IF(?k < 2, "1", IF(?k < 4, "2-3", IF(?k < 6, "4-5", IF(?k < 11, "6-10", IF(?k < 21, "11-20", IF(?k < 51, "21-50", "51+")))))) AS ?bucket)
        }} GROUP BY ?bucket""")
        for b in rows:
            buckets[val(b, "bucket")] = buckets.get(val(b, "bucket"), 0) + int(val(b, "n"))
    order = ["1", "2-3", "4-5", "6-10", "11-20", "21-50", "51+"]
    return [{"identifiers": k, "items": buckets[k]} for k in order if k in buckets]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--anchor", default="P244")
    ap.add_argument("--qid", default="Q7245", help="entity whose identifiers are marked in the table")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    ckpt = OUT / "chunks.jsonl"

    props = external_id_properties()
    print(f"{len(props)} external-identifier properties", flush=True)
    total, humans = totals(args.anchor)
    print(f"{total} items with {args.anchor}, {humans} of them humans", flush=True)

    chunks = {}
    if ckpt.exists():
        for line in ckpt.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                chunks[(d["offset"], d["humans_only"])] = d["counts"]
    jobs = [(off, h) for h in (False, True) for off in range(0, total, CHUNK)]
    todo = [j for j in jobs if j not in chunks]
    print(f"{len(chunks)} slices cached, {len(todo)} to query", flush=True)
    with ckpt.open("a") as f:
        for off, h in todo:
            t0 = time.time()
            counts = count_chunk(args.anchor, off, h)
            chunks[(off, h)] = counts
            f.write(json.dumps({"offset": off, "humans_only": h, "counts": counts}) + "\n")
            f.flush()
            print(f"  slice {off:>9,} {'humans' if h else 'all   '}: {len(counts)} properties, {time.time() - t0:.1f}s", flush=True)
    done = {}
    for (off, h), counts in chunks.items():
        for pid, n in counts.items():
            d = done.setdefault(pid, {"property": pid, "items": 0, "humans": 0})
            d["humans" if h else "items"] += n
    for pid in props:
        done.setdefault(pid, {"property": pid, "items": 0, "humans": 0})

    rows = []
    for pid, d in done.items():
        p = props.get(pid, {})
        rows.append({"property": pid, "label": p.get("label"), "items": d["items"], "share": round(100 * d["items"] / total, 2),
                     "humans": d["humans"], "human_share": round(100 * d["humans"] / humans, 2) if humans else 0,
                     "subject_item": p.get("subject"), "formatter_url": p.get("formatter")})
    rows.sort(key=lambda r: (-r["items"], r["property"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    with (OUT / "counts.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "property", "label", "items", "share", "humans", "human_share", "subject_item", "formatter_url"])
        w.writeheader()
        w.writerows(rows)

    classes = class_breakdown(args.anchor)
    try:
        dist = ids_per_item_distribution(args.anchor, total)
    except RuntimeError as e:
        dist = []
        print(f"distribution query failed: {e}", flush=True)

    entity_ids = Path("data") / args.qid / "identifiers.json"
    entity_props = {}
    if entity_ids.exists():
        for rec in json.loads(entity_ids.read_text()):
            entity_props.setdefault(rec["property"], 0)
            entity_props[rec["property"]] += 1
    by_pid = {r["property"]: r for r in rows}

    used = [r for r in rows if r["items"]]
    L = [f"# External identifiers on bibliographic entities (items with {args.anchor})", "",
         f"Source: QLever Wikidata endpoint, {time.strftime('%Y-%m-%d')}. {total:,} items carry {args.anchor} (Library of Congress authority ID); "
         f"{humans:,} ({100 * humans / total:.0f}%) are humans. {len(props):,} external-identifier properties exist in Wikidata; "
         f"{len(used):,} of them appear on at least one {args.anchor} item, {sum(1 for r in used if r['items'] >= 1000):,} on 1,000+ and "
         f"{sum(1 for r in used if r['share'] >= 10):,} on 10% or more.", ""]
    L += ["## What kinds of items are these?", "", "| class | label | items | share |", "|---|---|---|---|"]
    L += [f"| {c['class']} | {c['label'] or ''} | {c['items']:,} | {100 * c['items'] / total:.1f}% |" for c in classes[:25]]
    L.append("")
    if dist:
        L += ["## Identifiers per item", "", "| external identifiers (incl. P244) | items | share |", "|---|---|---|"]
        L += [f"| {d['identifiers']} | {d['items']:,} | {100 * d['items'] / total:.1f}% |" for d in dist]
        L.append("")
    L += ["## Top 150 identifiers", "", f"`share` = percentage of all {args.anchor} items; `human share` = percentage of the human ones. "
          f"`{args.qid}` marks identifiers the test entity carries (count of values).", "",
          "| rank | property | label | items | share | humans | human share | " + args.qid + " |", "|---|---|---|---|---|---|---|---|"]
    for r in rows[:150]:
        mark = f"✓ ×{entity_props[r['property']]}" if entity_props.get(r["property"], 0) > 1 else ("✓" if r["property"] in entity_props else "")
        L.append(f"| {r['rank']} | {r['property']} | {r['label'] or ''} | {r['items']:,} | {r['share']}% | {r['humans']:,} | {r['human_share']}% | {mark} |")
    L.append("")
    if entity_props:
        covered = [p for p in entity_props if p in by_pid]
        ranks = sorted(by_pid[p]["rank"] for p in covered)
        rare = sorted((by_pid[p] for p in covered), key=lambda r: r["items"])[:25]
        L += [f"## Where {args.qid}'s identifiers sit", "",
              f"{args.qid} has {len(entity_props)} identifier properties; {sum(1 for p in covered if by_pid[p]['rank'] <= 50)} are in the top 50, "
              f"{sum(1 for p in covered if by_pid[p]['rank'] <= 150)} in the top 150, median rank {ranks[len(ranks) // 2]}. "
              f"Its rarest identifiers (fewest other {args.anchor} items carry them):", "",
              "| property | label | items with it | share |", "|---|---|---|---|"]
        L += [f"| {r['property']} | {r['label'] or ''} | {r['items']:,} | {r['share']}% |" for r in rare]
        L.append("")
        top_missing = [r for r in rows[:60] if r["property"] not in entity_props]
        L += [f"Top-60 identifiers {args.qid} does **not** have: " + ", ".join(f"{r['property']} {r['label']} ({r['share']}%)" for r in top_missing), ""]
    L += ["Full table: `counts.csv` (all properties, including zero counts).", ""]
    (OUT / "landscape.md").write_text("\n".join(L))
    print(f"-> {OUT / 'landscape.md'}, counts.csv ({len(rows)} properties, {len(used)} used)")


if __name__ == "__main__":
    main()
