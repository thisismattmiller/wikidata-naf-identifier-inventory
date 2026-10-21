"""Step 8c: content negotiation survey. Which Accept headers get a non-HTML representation of the entity, and where?

    uv run python probe_conneg.py Q7245 [--workers 6] [--refetch]

Targets: each identifier's page URL, plus the data URLs the profile took values from. Each is requested with
Accept: application/ld+json, application/json, text/turtle, application/rdf+xml, application/n-triples (identifying
User-Agent, no cookies). The body is sniffed for what it really is (a server that says application/json but sends HTML
counts as HTML), and checked for the entity's name. Results: analysis/conneg_probe.json; build_map_data.py shows them
per site.
"""
import json
import re
import subprocess
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

UA = "wikidata-identifier-inventory/0.1 (research crawl; thisismattmiller@gmail.com)"
ACCEPTS = ["application/ld+json", "application/json", "text/turtle", "application/rdf+xml", "application/n-triples"]
DATA_KINDS = {"xhr", "export", "conneg", "alternate", "api", "extra"}
DESCRIPTIVE = {"name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place", "death_place",
               "activity_place", "gender", "occupation", "field_of_activity", "nationality", "language", "description", "work", "subject_of", "related_agent"}
host_locks, host_last, lock = {}, {}, threading.Lock()


def sniff(body, ctype):
    head = body[:4000].lstrip()
    low = head.lower()
    if low.startswith((b"<!doctype html", b"<html")) or b"<html" in low[:2000]:
        return "html"
    if head.startswith((b"{", b"[")):
        return "json-ld" if b"@context" in body[:20000] or b"@id" in body[:5000] else "json"
    if b"<rdf:rdf" in low or b"<rdf:RDF" in head:
        return "rdf-xml"
    if b"<record" in low and (b"marc" in low or b"<controlfield" in low or b"<datafield" in low):
        return "marcxml"
    if head.startswith(b"@prefix") or head.startswith(b"PREFIX") or re.search(rb"^\s*@prefix", head, re.M):
        return "turtle"
    if re.search(rb"^<[^>]+>\s+<[^>]+>\s+(<[^>]+>|\"[^\n]*)\s*\.\s*$", head, re.M):
        return "n-triples"
    if head.startswith(b"<?xml") or head.startswith(b"<"):
        return "xml"
    if b"application/ld+json" in (ctype or "").encode() or b"json" in (ctype or "").encode():
        return "json?"
    return "other"


def polite(host):
    with lock:
        hl = host_locks.setdefault(host, threading.Lock())
    with hl:
        wait = 1.0 - (time.time() - host_last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        host_last[host] = time.time()


def fetch(url, accept, names):
    polite(urllib.parse.urlsplit(url).hostname or "")
    cmd = ["curl", "-sS", "-L", "--compressed", "--max-time", "30", "--max-redirs", "10", "-o", "-", "-w", "\n\x1e%{http_code}\t%{content_type}\t%{url_effective}",
           "-A", UA, "-H", f"Accept: {accept}", url]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=45)
    except subprocess.TimeoutExpired:
        return {"status": None, "error": "timeout"}
    out = proc.stdout
    if b"\x1e" not in out:
        return {"status": None, "error": (proc.stderr.decode("utf-8", "replace").strip() or "no response")[:100]}
    body, _, tail = out.rpartition(b"\n\x1e")
    code, ctype, final = (tail.decode("utf-8", "replace").split("\t") + ["", ""])[:3]
    r = {"status": int(code) if code.isdigit() else None, "content_type": ctype.split(";")[0].strip(), "bytes": len(body), "final_url": final[:200]}
    r["format"] = sniff(body, r["content_type"]) if body else "empty"
    text = body.decode("utf-8", "replace")
    if "\\u" in text:
        text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    r["name"] = bool(names.search(text))
    r["ok"] = r["status"] == 200 and r["format"] not in ("html", "empty", "other", "json?") and r["name"]
    return r


def name_patterns(entity):
    forms = {l["value"] for l in entity["labels"].values()} | {a["value"] for als in entity["aliases"].values() for a in als}
    pats = {re.escape(tok) for f in forms for tok in re.split(r"[\s,.()]+", f) if len(tok) >= 4 and not tok.isdigit()}
    return re.compile(r"(?<!\w)(" + "|".join(sorted(pats, key=len, reverse=True)) + r")(?!\w)", re.I)


def targets_for(site, profile):
    out = [{"url": site["url"], "kind": "page"}]
    if profile:
        used = {v["file"].split("/")[-1] for el, vals in profile.get("elements", {}).items() if el in DESCRIPTIVE
                for v in vals if v.get("file") and not (v.get("via") or "").startswith("llm")}
        seen = {site["url"]}
        for f in profile.get("files", []):
            u = f.get("url")
            if f.get("kind") in DATA_KINDS and f["file"].split("/")[-1] in used and u and u.startswith("http") and u not in seen and "$" not in u:
                seen.add(u)
                out.append({"url": u, "kind": f["kind"], "format": f.get("format")})
            if len(out) >= 3:
                break
    return out


def main():
    args = sys.argv[1:]
    qid = next((a for a in args if a.startswith("Q")), "Q7245")
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 6
    an = Path("data") / qid / "analysis"
    out_path = an / "conneg_probe.json"
    done = json.loads(out_path.read_text()) if out_path.exists() and "--refetch" not in args else {}
    names = name_patterns(json.loads((Path("data") / qid / "entity.json").read_text()))
    sites = json.loads((an / "map_data.json").read_text())["sites"]
    profiles = {p.stem: json.loads(p.read_text()) for p in (an / "profiles").glob("P*.json")}
    todo = [s for s in sites if s["url"] and s["p"] not in done]
    print(f"{len(todo)} sites ({len(done)} cached) x up to 3 URLs x {len(ACCEPTS)} Accept headers", flush=True)

    def run(site):
        ts = []
        for t in targets_for(site, profiles.get(site["p"])):
            t["results"] = {a: fetch(t["url"], a, names) for a in ACCEPTS}
            t["serves"] = sorted({r["format"] for r in t["results"].values() if r.get("ok")})
            ts.append(t)
        return site["p"], {"label": site["label"], "targets": ts, "serves": sorted({f for t in ts for f in t["serves"]})}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (p, res) in enumerate(ex.map(run, todo), 1):
            done[p] = res
            print(f"  [{i}/{len(todo)}] {p} {res['label'][:28]:28} {', '.join(res['serves']) or '-':30} " + " | ".join(f"{t['kind']}: " + " ".join(f"{a.split('/')[-1][:8]}={r.get('format')}{'' if r.get('name') else '!'}" for a, r in t["results"].items()) for t in res["targets"])[:160], flush=True)
            if i % 10 == 0:
                out_path.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    out_path.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    from collections import Counter
    print("sites serving by negotiation:", sum(1 for r in done.values() if r["serves"]), Counter(f for r in done.values() for f in r["serves"]))


if __name__ == "__main__":
    main()
