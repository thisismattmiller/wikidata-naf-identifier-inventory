"""Step 4: retrieve every data representation the crawl discovered for each identifier page.

    uv run python fetch_representations.py Q7245 [--only P214,P244] [--force] [--workers 6]

For each record in data/<QID>/records/ it collects candidate representations from:
    alternate   <link rel=alternate/describedby/meta type=...> elements and Link: response-header alternates
    export      anchors on the page that look like exports/APIs (MARC, RDF, JSON, SRU ...)
    xhr         JSON/XML endpoints the page itself called while rendering (minus analytics noise)
    embedded    JSON-LD, RDFa, microdata and OpenGraph pulled out of the saved HTML with extruct
    conneg      content negotiation on the final URL (Accept: ld+json / turtle / rdf+xml / json)
fetches each one, sniffs what actually came back, and saves it under
    data/<QID>/representations/<key>/<kind>_<n>.<ext>   with a manifest.json per page
then writes data/<QID>/representations/summary.csv (one row per fetched representation).
"""

import argparse
import concurrent.futures
import csv
import gzip
import hashlib
import json
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import extruct
import truststore

truststore.inject_into_ssl()  # trust what the macOS keychain trusts, like the browser and curl do

USER_AGENT = "Mozilla/5.0 (Macintosh) wikidata-naf-identifier-inventory/0.1 (+mailto:thisismattmiller@gmail.com)"
TIMEOUT = 30
MAX_BYTES = 20 * 1024 * 1024
PER_HOST_DELAY = 1.0
MAX_EXPORT_LINKS = 25
MAX_XHR = 25

CONNEG_ACCEPTS = ["application/ld+json", "text/turtle", "application/rdf+xml", "application/json"]
MACHINE_TYPE_WORDS = ("json", "rdf", "xml", "turtle", "n-triples", "ntriples", "marc", "csv", "yaml", "atom", "rss", "n3", "trig", "nquads")
NOISE_HOSTS = re.compile(
    r"google-analytics|googletagmanager|gtag|doubleclick|googlesyndication|googleadservices|facebook\.|fbcdn|hotjar|"
    r"sentry\.io|segment\.(io|com)|mixpanel|newrelic|nr-data|cloudflareinsights|clarity\.ms|matomo|piwik|plausible\.io|"
    r"adsrvr|adnxs|criteo|taboola|outbrain|pubmatic|rubiconproject|amazon-adsystem|scorecardresearch|quantserve|"
    r"recaptcha|gstatic|googleapis\.com/(js|css)|cookiebot|onetrust|consensu|usercentrics|bing\.com|yandex|wp-json/wp/v2/users|"
    r"fonts\.|/beacon|/collect\b|/pixel|/track|/analytics|/telemetry|/log\b|/metrics|/ping\b|sockjs|/socket\.io",
    re.I,
)

_host_locks = {}
_host_last = {}
_host_guard = threading.Lock()


def throttle(url):
    host = urllib.parse.urlsplit(url).netloc
    with _host_guard:
        lock = _host_locks.setdefault(host, threading.Lock())
    with lock:
        wait = _host_last.get(host, 0) + PER_HOST_DELAY - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _host_last[host] = time.monotonic()


def fetch(url, accept=None):
    """GET a URL; returns dict(status, content_type, final_url, headers, body, error)."""
    headers = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}
    if accept:
        headers["Accept"] = f"{accept}, */*;q=0.1"
    req = urllib.request.Request(url, headers=headers)
    result = {"status": None, "content_type": None, "final_url": None, "headers": {}, "body": b"", "error": None}
    throttle(url)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result.update(status=resp.status, final_url=resp.url, headers=dict(resp.headers))
            body = resp.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as e:
        result.update(status=e.code, final_url=e.url, headers=dict(e.headers), error=f"HTTP {e.code}")
        try:
            body = e.read(MAX_BYTES + 1)
        except Exception:
            body = b""
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)[:200]}"
        return result
    if len(body) > MAX_BYTES:
        result["error"] = "truncated at 20MB"
        body = body[:MAX_BYTES]
    encoding = (result["headers"].get("Content-Encoding") or "").lower()
    try:
        if encoding == "gzip":
            body = gzip.decompress(body)
        elif encoding == "deflate":
            body = zlib.decompress(body, -zlib.MAX_WBITS)
    except Exception:
        pass
    result["body"] = body
    result["content_type"] = (result["headers"].get("Content-Type") or "").split(";")[0].strip().lower() or None
    return result


def sniff(body, content_type):
    """What the bytes actually are, independent of what the server claimed."""
    head = body[:4000].lstrip()
    text = head.decode("utf-8", "replace")
    low = text.lower()
    if not head:
        return "empty"
    if head[:1] in (b"{", b"["):
        try:
            doc = json.loads(body.decode("utf-8", "replace"))
        except Exception:
            return "json-invalid"
        s = body[:20000].decode("utf-8", "replace")
        if "@context" in s or "@graph" in s or '"@id"' in s:
            return "json-ld"
        return "json"
    first_line = text.split("\n", 1)[0].strip()
    if re.match(r"^(<[^>]+>|_:\S+)\s+<[^>]+>\s+(<[^>]+>|_:\S+|\"(?:[^\"\\\\]|\\\\.)*\"\S*)\s*\.$", first_line):
        return "n-triples"
    if head.startswith(b"<"):
        if "<!doctype html" in low or "<html" in low:
            return "html"
        if "marc21/slim" in low or "<marc:" in low or ("<record" in low and "<datafield" in low):
            return "marcxml"
        if "<rdf:rdf" in low or re.search(r"<\w+:?rdf[\s>]", low) or 'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"' in low and "<mads" not in low:
            return "rdf-xml"
        if "<mods" in low or "loc.gov/mods" in low:
            return "mods"
        if "<mads" in low:
            return "mads"
        if "<feed" in low or "<rss" in low:
            return "feed"
        if "<ead" in low:
            return "ead"
        if "<eac-cpf" in low:
            return "eac-cpf"
        if "<searchretrieveresponse" in low or "oai-pmh" in low:
            return "sru-oai-xml"
        if "<tei" in low:
            return "tei"
        if "<svg" in low:
            return "svg"
        return "xml"
    if re.match(r"^(@prefix|@base|prefix |base )", text, re.I) or (re.search(r"^\s*<[^>]+>\s+(a|<[^>]+>)\s+", text, re.M) and " ." in text):
        return "turtle"
    if re.match(r"^(=LDR|LEADER|=\d{3})", text):
        return "marc-mnemonic"
    if body[:5].isdigit() and len(body) > 24 and body[20:22].isdigit():
        return "marc-binary"
    if head.startswith(b"%PDF"):
        return "pdf"
    if "html" in (content_type or ""):
        return "html"
    if content_type and content_type.startswith("text/csv"):
        return "csv"
    if head[:2] == b"\x89P" or head[:3] == b"\xff\xd8\xff" or head[:4] == b"GIF8":
        return "image"
    return "text" if content_type and content_type.startswith("text/") else "unknown"


EXT = {
    "json": "json", "json-ld": "jsonld", "json-invalid": "json.txt", "html": "html", "rdf-xml": "rdf", "marcxml": "xml",
    "mods": "xml", "mads": "xml", "feed": "xml", "ead": "xml", "eac-cpf": "xml", "sru-oai-xml": "xml", "tei": "xml",
    "svg": "svg", "xml": "xml", "turtle": "ttl", "n-triples": "nt", "marc-mnemonic": "mrk", "marc-binary": "mrc",
    "pdf": "pdf", "csv": "csv", "image": "img", "text": "txt", "unknown": "bin", "empty": "txt",
}


def machine_type(value):
    return bool(value) and any(w in value.lower() for w in MACHINE_TYPE_WORDS)


def parse_link_header(value):
    out = []
    for m in re.finditer(r"<([^>]+)>\s*((?:;[^,]*)*)", value or ""):
        params = dict(re.findall(r';\s*([\w-]+)\s*=\s*"?([^";,]*)"?', m.group(2)))
        out.append((m.group(1), params))
    return out


EXTRA = {}


def candidates(record):
    """The representations worth fetching for one page: list of dicts(kind, source, url, accept)."""
    page = record.get("page", {})
    final_url = page.get("final_url") or record.get("url")
    seen = set()
    out = []

    def add(kind, source, url, accept=None, note=None):
        if not url or url.startswith(("javascript:", "mailto:", "data:")):
            return
        url = urllib.parse.urljoin(final_url, url)
        key = (url, accept)
        if key in seen:
            return
        seen.add(key)
        out.append({"kind": kind, "source": source, "url": url, "accept": accept, "note": note})

    for link in page.get("link_elements", []):
        rel = (link.get("rel") or "").lower()
        if any(r in rel for r in ("alternate", "describedby", "meta")) and (machine_type(link.get("type")) or machine_type(link.get("href"))) and not link.get("hreflang"):
            add("alternate", f"<link rel={rel} type={link.get('type')}>", link.get("href"), note=link.get("title"))
    headers = (page.get("response_headers") or {}).get("headers") or {}
    for url, params in parse_link_header(headers.get("link")):
        rel = params.get("rel", "").lower()
        if any(r in rel for r in ("alternate", "describedby", "meta")) and (machine_type(params.get("type")) or machine_type(url)):
            add("alternate", f"Link: header rel={rel} type={params.get('type')}", url)

    n = 0
    for link in page.get("machine_links", []):
        if n >= MAX_EXPORT_LINKS or not link.get("href"):
            continue
        reasons = set(link.get("reasons", []))
        if (reasons - {"text"}) or machine_type(link.get("text")):
            add("export", f"anchor '{(link.get('text') or '')[:60]}' ({','.join(sorted(reasons))})", link["href"])
            n += 1

    n = 0
    for xhr in page.get("xhr_requests", []):
        url = xhr.get("url") or ""
        if n >= MAX_XHR or NOISE_HOSTS.search(url):
            continue
        add("xhr", f"xhr {xhr.get('initiator')} status={xhr.get('status')} type={xhr.get('content_type')}", url)
        n += 1

    # extra_representations.json: {property: [url, ...]} - data endpoints the page never advertises
    # (e.g. a JS app whose record lives at /data/... while the page shell carries nothing)
    for url in EXTRA.get(record["property"], []):
        add("extra", "extra_representations.json", url)

    # negotiate on the identifier URL itself (the one Wikidata links to), not on whatever it redirected to
    if record.get("status") in ("ok", "login_wall_suspected"):
        for accept in CONNEG_ACCEPTS:
            add("conneg", f"Accept: {accept}", record["url"], accept=accept)
    return out


def embedded(record, out_dir, data_dir):
    """Structured data embedded in the saved HTML, via extruct."""
    html_file = record.get("html_file")
    if not html_file:
        return []
    html = (data_dir / html_file).read_text(errors="replace")
    base = record["page"].get("final_url") or record["url"]
    try:
        found = extruct.extract(html, base_url=base, syntaxes=["json-ld", "microdata", "rdfa", "opengraph"], uniform=True, errors="ignore")
    except Exception as e:
        return [{"kind": "embedded", "source": "extruct", "error": str(e)[:200]}]
    rows = []
    for syntax, items in found.items():
        if not items:
            continue
        # RDFa: ignore pages where it is nothing but OpenGraph/Twitter card properties
        if syntax == "rdfa":
            keys = {k for item in items for k in item if k != "@id"}
            if keys and all(k.startswith(("http://ogp.me", "@type")) or "twitter" in k for k in keys):
                continue
        fname = f"embedded_{syntax}.json"
        (out_dir / fname).write_text(json.dumps(items, ensure_ascii=False, indent=1))
        rows.append({"kind": "embedded", "source": f"extruct {syntax}", "url": base, "status": None, "content_type": None,
                     "detected": syntax, "bytes": (out_dir / fname).stat().st_size, "items": len(items), "file": fname})
    return rows


MAX_PAGES = 60


def next_pages(url, body):
    """For a JSON payload like {"summary": {"page": 0, "totalPages": 8}, ...} loaded from ?page=0, the URLs of the remaining pages."""
    try:
        doc = json.loads(body)
    except Exception:
        return []
    summary = doc.get("summary") if isinstance(doc, dict) else None
    if not isinstance(summary, dict):
        return []
    try:
        page, total = int(summary.get("page", 0)), int(summary.get("totalPages", 1))
    except (TypeError, ValueError):
        return []
    if page != 0 or total <= 1:
        return []
    return [re.sub(r"([?&])page=\d+", rf"\g<1>page={n}", url) for n in range(1, total)]


def process(record, data_dir, force, redo=None):
    key = Path(record["html_file"]).stem if record.get("html_file") else None
    key = key or f"{record['property']}__{hashlib.sha1(record['value'].encode()).hexdigest()[:10]}"
    out_dir = data_dir / "representations" / key
    manifest_path = out_dir / "manifest.json"
    if manifest_path.exists() and not force:
        text = manifest_path.read_text()
        # redo pages written by an older version of this script, or whose manifest matches --redo
        if '"key"' in text and not (redo and re.search(redo, text)):
            return json.loads(text)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = embedded(record, out_dir, data_dir)
    counters = Counter()
    queue = list(candidates(record))
    paginated = 0
    while queue:
        cand = queue.pop(0)
        res = fetch(cand["url"], cand["accept"])
        row = {**cand, "status": res["status"], "content_type": res["content_type"], "final_url": res["final_url"],
               "error": res["error"], "bytes": len(res["body"])}
        if res["body"]:
            detected = sniff(res["body"], res["content_type"])
            row["detected"] = detected
            # content negotiation that just returns the HTML page again is a non-result: note it, don't keep the body
            if cand["kind"] == "conneg" and detected == "html":
                row["file"] = None
            else:
                counters[cand["kind"]] += 1
                fname = f"{cand['kind']}_{counters[cand['kind']]}.{EXT.get(detected, 'bin')}"
                (out_dir / fname).write_bytes(res["body"])
                row["file"] = fname
                # paginated JSON (id.loc.gov's "Subject Of Works" / "Contributor To Works" panels): the page only ever
                # loads page 0, so follow ?page=N up to MAX_PAGES while the payload says there are more
                if detected == "json" and cand["kind"] == "xhr" and "page=" in cand["url"]:
                    for url in next_pages(cand["url"], res["body"]):
                        if paginated < MAX_PAGES:
                            paginated += 1
                            queue.append({**cand, "url": url, "source": f"pagination of {cand['url'][:80]}"})
        rows.append(row)

    manifest = {"key": key, "property": record["property"], "property_label": record["property_label"], "value": record["value"],
                "url": record["url"], "final_url": record["page"].get("final_url"), "page_status": record.get("status"),
                "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "representations": rows}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qid", nargs="?", default="Q7245")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--redo", help="regex: re-fetch pages whose existing manifest.json matches it (e.g. CERTIFICATE_VERIFY)")
    args = ap.parse_args()
    data_dir = Path("data") / args.qid
    only = set(args.only.split(",")) if args.only else None
    extra_path = data_dir / "extra_representations.json"
    EXTRA.update(json.loads(extra_path.read_text()) if extra_path.exists() else {})
    records = [json.loads(p.read_text()) for p in sorted((data_dir / "records").glob("*.json"))]
    records = [r for r in records if not only or r["property"] in only]
    print(f"{len(records)} pages")

    manifests = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process, r, data_dir, args.force, args.redo): r for r in records}
        for i, fut in enumerate(concurrent.futures.as_completed(futures), 1):
            r = futures[fut]
            try:
                m = fut.result()
            except Exception as e:
                print(f"[{i}/{len(records)}] {r['property']} {r['value']}: FAILED {e}", flush=True)
                continue
            manifests.append(m)
            got = Counter(x.get("detected") for x in m["representations"] if x.get("file"))
            print(f"[{i}/{len(records)}] {r['property']} {r['property_label']}: {dict(got) or '-'}", flush=True)

    write_summary(data_dir)


def write_summary(data_dir):
    """summary.csv: one row per representation attempt, from every manifest on disk."""
    manifests = []
    for path in (data_dir / "representations").glob("*/manifest.json"):
        manifests.append({"key": path.parent.name, **json.loads(path.read_text())})
    manifests.sort(key=lambda m: (int(m["property"][1:]), m["value"]))
    fields = ["property", "property_label", "value", "page_url", "kind", "via", "source", "request_url", "accept", "status", "content_type", "detected", "bytes", "items", "file", "error"]
    with (data_dir / "representations" / "summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for m in manifests:
            for x in m["representations"]:
                w.writerow({**x, "property": m["property"], "property_label": m["property_label"], "value": m["value"], "via": x.get("via", "http"),
                            "page_url": m["url"], "request_url": x.get("url"), "file": f"{m['key']}/{x['file']}" if x.get("file") else ""})
    kept = [(m, x) for m in manifests for x in m["representations"] if x.get("file")]
    print(f"\n{len(kept)} representations saved for {len({m['url'] for m, _ in kept})} of {len(manifests)} pages")
    print("by format:", dict(Counter(x.get("detected") for _, x in kept).most_common()))
    print("by source:", dict(Counter(x["kind"] for _, x in kept).most_common()))
    print(f"-> {data_dir / 'representations' / 'summary.csv'}")


if __name__ == "__main__":
    main()
