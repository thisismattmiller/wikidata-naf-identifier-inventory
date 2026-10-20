"""Step 3: roll the per-page records up into one inventory table.

    uv run python build_inventory.py Q7245

Writes data/<QID>/inventory.csv and data/<QID>/inventory.md (one row per identifier value),
summarising what each site exposes: machine-readable <link rel=alternate>s, Link headers,
embedded JSON-LD / RDFa / microdata, export links, and the background API calls the page made.
"""

import csv
import json
import sys
import urllib.parse
from collections import Counter
from pathlib import Path

MACHINE_TYPES = ("json", "rdf", "xml", "turtle", "n-triples", "ld+json", "marc", "csv", "yaml", "atom", "rss")


def machine_type(value):
    return bool(value) and any(t in value.lower() for t in MACHINE_TYPES)


def summarise(record, row):
    page = record.get("page", {})
    final_url = page.get("final_url") or record.get("tab_url") or ""
    headers = (page.get("response_headers") or {}).get("headers") or {}

    alternates = [
        f"{l.get('rel')} {l.get('type') or ''} {l.get('href')}".strip()
        for l in page.get("link_elements", [])
        if "alternate" in (l.get("rel") or "").lower() and (machine_type(l.get("type")) or machine_type(l.get("href")))
    ]
    other_links = [
        f"{l.get('rel')} {l.get('type') or ''} {l.get('href')}".strip()
        for l in page.get("link_elements", [])
        if "alternate" not in (l.get("rel") or "").lower()
        and (l.get("rel") or "").lower() not in ("canonical", "search", "author", "publisher", "help", "shortlink", "next", "prev", "alternate", "me", "home", "pingback", "edituri", "wlwmanifest", "amphtml", "image_src", "apple-touch-icon", "copyright", "license", "sitemap")
        and not (l.get("rel") or "").lower().startswith("http://www.w3.org/1999/xhtml/vocab#")
    ]
    machine_links = [
        f"{m.get('text') or ''} -> {m.get('href') or '(button)'}"
        for m in page.get("machine_links", [])
        if set(m.get("reasons", [])) - {"text"} or machine_type(m.get("text"))
    ]
    xhr = [x["url"] for x in page.get("xhr_requests", [])]
    sig = page.get("signals", {})
    jsonld_types = sorted({t for j in page.get("jsonld", []) for t in j.get("types", [])})

    return {
        "property": record["property"],
        "property_label": record["property_label"],
        "value": record["value"],
        "institution": "; ".join(filter(None, [i.get("label") for i in row.get("subject_item", []) + row.get("issued_by", [])])),
        "url": record["url"],
        "final_url": final_url,
        "host": urllib.parse.urlsplit(final_url).netloc,
        "status": record.get("status"),
        "http_status": page.get("http_status"),
        "content_type": page.get("content_type"),
        "title": (page.get("title") or record.get("tab_title") or "")[:200],
        "link_header": headers.get("link", ""),
        "alternate_links": " ‖ ".join(alternates),
        "other_link_rels": " ‖ ".join(other_links)[:1500],
        "jsonld_types": ", ".join(jsonld_types),
        "rdfa_typeofs": ", ".join(page.get("rdfa", {}).get("typeofs", []))[:300],
        "microdata_itemtypes": ", ".join(page.get("microdata", {}).get("itemtypes", []))[:300],
        "data_scripts": ", ".join(f"{d.get('type')}#{d.get('id') or ''}" for d in page.get("data_scripts", []))[:300],
        "machine_links": " ‖ ".join(machine_links)[:3000],
        "machine_link_count": len(page.get("machine_links", [])),
        "xhr_requests": " ‖ ".join(xhr)[:3000],
        "challenge_signals": "; ".join(sig.get("challenge_elements", []) + sig.get("challenge_words", [])) + (" [title]" if sig.get("challenge_title") else ""),
        "password_inputs": sig.get("password_inputs"),
        "access_words": ", ".join(sig.get("access_words", [])),
        "not_found_words": ", ".join(sig.get("not_found_words", [])),
        "visibility": page.get("visibility"),
        "text_length": page.get("text_length"),
        "html_file": record.get("html_file", ""),
        "error": record.get("error") or page.get("extract_error") or "",
        "third_party_formatter_urls": " ‖ ".join(row.get("third_party_formatter_urls", [])),
        "formatter_uri_for_rdf": " ‖ ".join(row.get("formatter_uri_for_rdf", [])),
    }


def main():
    qid = sys.argv[1] if len(sys.argv) > 1 else "Q7245"
    out_dir = Path("data") / qid
    identifiers = json.loads((out_dir / "identifiers.json").read_text())
    rows = {(r["property"], r["value"]): r for r in identifiers}

    summary = []
    for path in sorted((out_dir / "records").glob("*.json")):
        record = json.loads(path.read_text())
        summary.append(summarise(record, rows.get((record["property"], record["value"]), {})))
    summary.sort(key=lambda s: (int(s["property"][1:]), s["value"]))

    with (out_dir / "inventory.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    def has_machine(s):
        return bool(s["alternate_links"] or s["link_header"] or s["jsonld_types"] or s["machine_links"] or s["xhr_requests"])

    lines = [
        f"# Identifier inventory for {qid}",
        "",
        f"{len(summary)} identifier pages crawled, {len(identifiers)} identifiers total.",
        "",
        "## Status",
        "",
    ]
    for status, n in Counter(s["status"] for s in summary).most_common():
        lines.append(f"- {status}: {n}")
    lines += [
        "",
        f"Pages with some machine-readable signal (alternate link, Link header, JSON-LD, export link, or background API call): {sum(1 for s in summary if has_machine(s))}",
        "",
        "## Pages",
        "",
        "| property | value | status | http | alternate links | JSON-LD | export/API links | XHR | signals |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for s in summary:
        lines.append(
            f"| {s['property']} {s['property_label']} | [{s['value'][:40]}]({s['url']}) | {s['status']} | {s['http_status'] or ''} "
            f"| {s['alternate_links'].count('‖') + 1 if s['alternate_links'] else 0} | {s['jsonld_types'][:40]} "
            f"| {s['machine_links'].count('‖') + 1 if s['machine_links'] else 0} | {s['xhr_requests'].count('‖') + 1 if s['xhr_requests'] else 0} "
            f"| {s['challenge_signals'] or ('pw' if s['password_inputs'] else '')} |"
        )
    (out_dir / "inventory.md").write_text("\n".join(lines) + "\n")
    print(f"{len(summary)} rows -> {out_dir / 'inventory.csv'} and {out_dir / 'inventory.md'}")
    for status, n in Counter(s["status"] for s in summary).most_common():
        print(f"  {status}: {n}")


if __name__ == "__main__":
    main()
