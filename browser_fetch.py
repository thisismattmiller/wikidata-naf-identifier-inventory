"""Step 5: re-fetch, from inside the browser, the representations plain HTTP could not get.

    uv run python browser_fetch.py Q7245 [--only P214,P244] [--force]

For each page whose manifest has representation attempts that failed (4xx/5xx, connection errors,
HTML where data was promised, unreadable bodies), the crawler opens the page in its Chrome window and
runs fetch() *in the page* - with the site's cookies, session and bot clearance - for each failed URL.
Links on another origin that the page is not allowed to read (CORS) are retried by navigating the tab
to that origin first. Results are saved next to the first pass as browser_<kind>_<n>.<ext> and appended
to manifest.json with "via": "browser"; summary.csv is rebuilt.
"""

import argparse
import base64
import json
import re
import subprocess
import sys
import time
import urllib.parse
from collections import Counter
from pathlib import Path

from crawl import ChromeWindow, applescript_string, osascript
from fetch_representations import EXT, sniff, write_summary

HERE = Path(__file__).parent
APPLESCRIPT = HERE / "browser_fetch.applescript"
MAX_LOAD_SECONDS = 45
PER_FETCH_SECONDS = 35
CHALLENGE_TITLE = re.compile(r"just a moment|attention required|checking your browser|verif(y|ying)|security check|human verification|are you a (robot|human)|un momento", re.I)
CHALLENGE_MAX_PAUSE = 20 * 60

KICKOFF_JS = r"""
(function (cands) {
  window.__invFetch = { done: false, results: [] };
  var b64 = function (buf) {
    var bytes = new Uint8Array(buf), bin = '', chunk = 0x8000;
    for (var i = 0; i < bytes.length; i += chunk) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
    return btoa(bin);
  };
  (async function () {
    for (var c of cands) {
      var r = { id: c.id, url: c.url, accept: c.accept || null };
      try {
        var opts = { credentials: 'include', redirect: 'follow' };
        if (c.accept) opts.headers = { 'Accept': c.accept + ', */*;q=0.1' };
        var resp = await fetch(c.url, opts);
        r.status = resp.status; r.final_url = resp.url; r.response_type = resp.type;
        r.content_type = resp.headers.get('content-type');
        var buf = await resp.arrayBuffer();
        r.bytes = buf.byteLength;
        if (buf.byteLength > 20 * 1024 * 1024) r.error = 'too large'; else r.body_b64 = b64(buf);
      } catch (e) { r.error = String(e); }
      window.__invFetch.results.push(r);
      await new Promise(function (res) { setTimeout(res, 700); });
    }
    window.__invFetch.done = true;
  })();
  return 'started';
})(CANDS);
"""


def failed_attempts(manifest):
    """First-pass attempts worth retrying in the browser."""
    out = []
    for i, x in enumerate(manifest["representations"]):
        if x.get("via") == "browser" or x["kind"] == "embedded":
            continue
        status = x.get("status")
        detected = x.get("detected")
        bad = (
            x.get("error")
            or status is None
            or status >= 400
            or (x["kind"] != "conneg" and detected in ("html", "unknown", "empty", "json-invalid", None))
        )
        if bad:
            out.append({"id": i, "url": x["url"], "accept": x.get("accept"), "kind": x["kind"], "source": x["source"]})
    return out


def run_fetch(window, page_url, cands):
    js = KICKOFF_JS.replace("CANDS", json.dumps(cands))
    max_fetch = min(PER_FETCH_SECONDS * len(cands), 900)
    out = osascript(APPLESCRIPT, window.ensure(), page_url, js, str(MAX_LOAD_SECONDS), str(max_fetch), timeout=MAX_LOAD_SECONDS + max_fetch + 60)
    head, _, body = out.partition("\n")
    tab_url, _, tab_title = head.partition("|")
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        data = {"error": f"unparseable: {body[:200]!r}"}
    return tab_url, tab_title, data


def tab_title(window):
    return osascript(f'tell application "Google Chrome" to get title of active tab of window id "{window.ensure()}"')


def wait_out_challenge(window, page_url):
    paused = 0.0
    notified = False
    while CHALLENGE_TITLE.search(tab_title(window)) and paused < CHALLENGE_MAX_PAUSE:
        if paused >= 15 and not notified:
            notified = True
            print(f"    PAUSED: human verification on {page_url} - please click through it in the crawler window", flush=True)
            window.bring_forward()
            try:
                osascript(f'display notification {applescript_string(page_url[:120])} with title "Crawler paused: please verify you are human" sound name "Glass"')
            except RuntimeError:
                pass
        time.sleep(5)
        paused += 5
    if notified:
        print(f"    resumed after {paused:.0f}s", flush=True)


def save_results(manifest, out_dir, results, cands_by_id, counters):
    rows = []
    for r in results:
        cand = cands_by_id[r["id"]]
        row = {"kind": cand["kind"], "source": cand["source"], "url": cand["url"], "accept": cand.get("accept"), "via": "browser", "retry_of": r["id"],
               "status": r.get("status"), "content_type": (r.get("content_type") or "").split(";")[0].strip().lower() or None,
               "final_url": r.get("final_url"), "response_type": r.get("response_type"), "error": r.get("error"), "bytes": r.get("bytes")}
        if r.get("body_b64"):
            body = base64.b64decode(r["body_b64"])
            detected = sniff(body, row["content_type"])
            row["detected"] = detected
            if cand["kind"] == "conneg" and detected == "html":
                row["file"] = None
            else:
                counters[cand["kind"]] += 1
                fname = f"browser_{cand['kind']}_{counters[cand['kind']]}.{EXT.get(detected, 'bin')}"
                (out_dir / fname).write_bytes(body)
                row["file"] = fname
        rows.append(row)
    manifest["representations"].extend(rows)
    return rows


def process(window, manifest, out_dir):
    cands = failed_attempts(manifest)
    if not cands:
        return None
    page_url = manifest["url"]
    cands_by_id = {c["id"]: c for c in cands}
    counters = Counter()

    tab_url, title, data = run_fetch(window, page_url, cands)
    if CHALLENGE_TITLE.search(title or ""):
        wait_out_challenge(window, page_url)
        tab_url, title, data = run_fetch(window, "", cands)
    results = data.get("results", [])
    rows = save_results(manifest, out_dir, results, cands_by_id, counters)
    if data.get("error"):
        manifest["browser_pass_error"] = data["error"]

    # CORS fallback: the page could not read these; fetch them from their own origin
    succeeded = {r["id"] for r in results if r.get("body_b64")}
    blocked = [c for c in cands if c["id"] not in succeeded]
    by_origin = {}
    for c in blocked:
        origin = urllib.parse.urlsplit(c["url"])._replace(path="", query="", fragment="").geturl()
        by_origin.setdefault(origin, []).append(c)
    page_origin = urllib.parse.urlsplit(tab_url or page_url)._replace(path="", query="", fragment="").geturl()
    for origin, group in by_origin.items():
        if origin == page_origin or not origin.startswith("http"):
            continue
        _, title, data = run_fetch(window, group[0]["url"], group)
        if CHALLENGE_TITLE.search(title or ""):
            wait_out_challenge(window, group[0]["url"])
            _, title, data = run_fetch(window, "", group)
        rows += save_results(manifest, out_dir, data.get("results", []), cands_by_id, counters)

    manifest["browser_pass_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qid", nargs="?", default="Q7245")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true", help="redo pages that already had a browser pass")
    args = ap.parse_args()
    data_dir = Path("data") / args.qid
    only = set(args.only.split(",")) if args.only else None

    todo = []
    for path in sorted((data_dir / "representations").glob("*/manifest.json")):
        m = json.loads(path.read_text())
        if only and m["property"] not in only:
            continue
        if m.get("browser_pass_at") and not args.force:
            continue
        if failed_attempts(m):
            todo.append((m, path.parent))
    print(f"{len(todo)} pages with representations to retry in the browser")

    window = ChromeWindow()
    try:
        for i, (m, out_dir) in enumerate(todo, 1):
            n = len(failed_attempts(m))
            print(f"[{i}/{len(todo)}] {m['property']} {m['property_label']}: {n} to fetch from {m['url'][:70]}", flush=True)
            try:
                rows = process(window, m, out_dir) or []
            except subprocess.TimeoutExpired:
                print("    osascript timed out; reopening the window", flush=True)
                window.discard()
                continue
            except RuntimeError as e:
                print(f"    error: {str(e)[:150]}", flush=True)
                continue
            got = Counter(r.get("detected") for r in rows if r.get("file"))
            print(f"    saved {dict(got) or '-'}", flush=True)
    finally:
        window.close()
    write_summary(data_dir)


if __name__ == "__main__":
    main()
