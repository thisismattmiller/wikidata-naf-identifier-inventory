"""Step 8b: can a plain HTTP client actually get each site's data about the entity? Tested with the real curl binary.

    uv run python probe_clients.py Q7245 [--workers 6] [--refetch] [--retry-errors] [--rederive]

For every site: the page the identifier links to, plus (for sites whose values came from data files) up to three of the
data URLs the profile used. Each URL is tried with three client profiles, stopping at the first that serves the record:
    curl     - curl's own User-Agent, no other headers (what "just curl it" means)
    ua       - an identifying User-Agent with contact e-mail (polite-crawler convention)
    browser  - a Chrome User-Agent with a browser's Accept / Accept-Language / Sec-Fetch headers, still no cookies or JS
"Serves the record" means HTTP 200 with the entity's name (any script) in the body decoded with the response's charset;
bot-challenge wording is recorded but a page that names him was served. Results go to analysis/client_probe.json;
build_map_data.py reads it for the access facet. --rederive recomputes tiers from stored results without fetching.
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
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
TIERS = {
    "curl": [],
    "ua": ["-A", UA],
    "browser": ["-A", BROWSER_UA, "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H", "Accept-Language: en-US,en;q=0.9", "-H", "Sec-Fetch-Dest: document", "-H", "Sec-Fetch-Mode: navigate",
                "-H", "Sec-Fetch-Site: none", "-H", "Upgrade-Insecure-Requests: 1"],
}
CHALLENGE = re.compile(r"cf-browser-verification|challenge-platform|__cf_chl|just a moment|checking your browser|enable javascript and cookies to continue|"
                       r"attention required|are you a (robot|human)|verify (that )?you are|access denied|request unsuccessful\. incapsula|captcha", re.I)
ENCODINGS = ["utf-8", "windows-1251", "koi8-r", "gb18030", "shift_jis", "euc-kr", "windows-1250", "iso-8859-1"]
DATA_KINDS = {"xhr", "export", "conneg", "alternate", "api", "extra"}
host_locks, host_last = {}, {}
lock = threading.Lock()


def name_patterns(entity):
    forms = {l["value"] for l in entity["labels"].values()} | {a["value"] for als in entity["aliases"].values() for a in als}
    pats = []
    for f in forms:
        for tok in re.split(r"[\s,.()]+", f):
            if len(tok) >= 4 and not tok.isdigit():
                pats.append(re.escape(tok))
    return re.compile(r"(?<!\w)(" + "|".join(sorted(set(pats), key=len, reverse=True)) + r")(?!\w)", re.I)


def polite(host):
    with lock:
        hl = host_locks.setdefault(host, threading.Lock())
    with hl:
        wait = 1.2 - (time.time() - host_last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        host_last[host] = time.time()


def decode(body, ctype, names):
    m = re.search(r"charset=([\w-]+)", ctype or "", re.I) or re.search(rb'charset=["\']?([\w-]+)', body[:4000], re.I)
    order = ([m.group(1).decode() if isinstance(m.group(1), bytes) else m.group(1)] if m else []) + ENCODINGS
    first = None
    for enc in order:
        try:
            text = body.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
        first = first if first is not None else text
        if names.search(text):
            return text
    return first if first is not None else body.decode("utf-8", "replace")


def fetch(url, tier, names):
    host = urllib.parse.urlsplit(url).hostname or ""
    polite(host)
    cmd = ["curl", "-sS", "-L", "--compressed", "--max-time", "30", "--max-redirs", "10", "-o", "-", "-w", "\n\x1e%{http_code}\t%{content_type}\t%{url_effective}"] + TIERS[tier] + [url]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=45)
    except subprocess.TimeoutExpired:
        return {"status": None, "error": "timeout"}
    out = proc.stdout
    if b"\x1e" not in out:
        return {"status": None, "error": (proc.stderr.decode("utf-8", "replace").strip() or "no response")[:120]}
    body, _, tail = out.rpartition(b"\n\x1e")
    code, ctype, final = (tail.decode("utf-8", "replace").split("\t") + ["", ""])[:3]
    r = {"status": int(code) if code.isdigit() else None, "content_type": ctype.split(";")[0].strip(), "bytes": len(body), "final_url": final[:200]}
    if proc.stderr.strip():
        r["error"] = proc.stderr.decode("utf-8", "replace").strip()[:120]
    text = decode(body, ctype, names)
    if not names.search(text) and "\\u" in text:   # JSON with escaped non-Latin text
        text = re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m.group(1), 16)), text)
    r["name"] = bool(names.search(text))
    r["challenge"] = bool(CHALLENGE.search(text[:20000]))
    r["served"] = r["status"] == 200 and r["name"]   # a challenge page never carries his name; the word "captcha" on a real page is harmless
    return r


def probe_target(t, names):
    t["results"] = {}
    t["tier"] = None
    for tier in TIERS:
        r = fetch(t["url"], tier, names)
        t["results"][tier] = r
        if r.get("served"):
            t["tier"] = tier
            break
    return t


DESCRIPTIVE = {"name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place", "death_place",
               "activity_place", "gender", "occupation", "field_of_activity", "nationality", "language", "description", "work", "subject_of", "related_agent"}


def targets_for(site, profile):
    """The page, plus the data files the profile actually took descriptive values from (not every XHR the page made)."""
    out = [{"url": site["url"], "kind": "page"}]
    if profile:
        used = {v["file"].split("/")[-1] for el, vals in profile.get("elements", {}).items() if el in DESCRIPTIVE
                for v in vals if v.get("file") and not (v.get("via") or "").startswith("llm")}
        seen = {site["url"]}
        for f in profile.get("files", []):
            u = f.get("url")
            if f.get("kind") in DATA_KINDS and f["file"].split("/")[-1] in used and u and u.startswith("http") and u not in seen:
                seen.add(u)
                out.append({"url": u, "kind": f["kind"], "format": f.get("format"), "via": f.get("via")})
            if len(out) >= 4:
                break
    return out


def main():
    args = sys.argv[1:]
    qid = next((a for a in args if a.startswith("Q")), "Q7245")
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 6
    refetch = "--refetch" in args
    an = Path("data") / qid / "analysis"
    out_path = an / "client_probe.json"
    done = json.loads(out_path.read_text()) if out_path.exists() and not refetch else {}
    if "--rederive" in args:
        rank = {"curl": 0, "ua": 1, "browser": 2, None: 3}
        for r in done.values():
            for tg in r["targets"]:
                tg["tier"] = None
                for tier, res in tg["results"].items():
                    res["served"] = res.get("status") == 200 and bool(res.get("name"))
                    if res["served"] and tg["tier"] is None:
                        tg["tier"] = tier
            data = [tg for tg in r["targets"] if tg["kind"] != "page"]
            r["page_tier"] = r["targets"][0]["tier"] if r["targets"] else None
            r["best"] = max((tg["tier"] for tg in (data or r["targets"])), key=lambda k: rank[k]) if r["targets"] else None
        out_path.write_text(json.dumps(done, ensure_ascii=False, indent=1))
        from collections import Counter
        print("re-derived:", Counter(r["best"] or "none" for r in done.values()))
        return
    entity = json.loads((Path("data") / qid / "entity.json").read_text())
    names = name_patterns(entity)
    sites = json.loads((an / "map_data.json").read_text())["sites"]
    profiles = {p.stem: json.loads(p.read_text()) for p in (an / "profiles").glob("P*.json")}
    todo = [s for s in sites if s["url"]]
    cached = {p: {t["url"]: t for t in r["targets"]} for p, r in done.items()}
    print(f"{len(todo)} sites to probe ({len(done)} with cached targets); 3 client profiles, stop at the first that serves the record", flush=True)

    retry_errors = "--retry-errors" in args   # redo targets whose results were timeouts or 429s (often our own concurrency)

    def stale(old):
        return retry_errors and any(r.get("status") in (None, 429, 503) for r in old["results"].values()) and not old.get("tier")

    def run(site):
        ts = []
        for t in targets_for(site, profiles.get(site["p"])):
            old = cached.get(site["p"], {}).get(t["url"])
            ts.append(old if old and not refetch and "tier" in old and not stale(old) else probe_target(t, names))
        data = [t for t in ts if t["kind"] != "page"]
        rank = {"curl": 0, "ua": 1, "browser": 2, None: 3}
        need = data or ts   # a site is as reachable as the hardest of the data files it needs; a page-only site, as its page
        worst = max((t["tier"] for t in need), key=lambda k: rank[k])
        return site["p"], {"label": site["label"], "best": worst, "page_tier": ts[0]["tier"], "targets": ts}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, (p, res) in enumerate(ex.map(run, todo), 1):
            done[p] = res
            codes = " ".join(f"{t['kind']}:{t['tier'] or '-'}" + "".join(f"/{k[0]}{r.get('status') or 'x'}" for k, r in t["results"].items()) for t in res["targets"])
            print(f"  [{i}/{len(todo)}] {p} {res['label'][:28]:28} {res['best'] or 'NONE':8} {codes}", flush=True)
            if i % 10 == 0:
                out_path.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    out_path.write_text(json.dumps(done, ensure_ascii=False, indent=1))
    from collections import Counter
    print(Counter(r["best"] or "none" for r in done.values()))


if __name__ == "__main__":
    main()
