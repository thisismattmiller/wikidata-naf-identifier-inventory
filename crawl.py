"""Step 2: open every identifier URL in Chrome (driven by AppleScript) and record what is there.

    uv run python crawl.py Q7245 [--only P214,P244] [--limit N] [--force] [--retry-status challenge_suspected,load_failed]

For each identifier it saves, under data/<QID>/:
    pages/<key>.html    the rendered DOM (after client-side JS ran)
    pages/<key>.txt     the visible text of the page
    records/<key>.json  everything extract.js found (links, embedded data, signals, headers...)
Already-recorded identifiers are skipped unless --force or --retry-status matches, so the run can be resumed.

Chrome must allow JavaScript from Apple Events (View > Developer menu). The crawler opens its own
Chrome window and leaves your other windows alone. Keep that window unobscured if you can; Chrome
throttles rendering in hidden windows and extract.js records document.visibilityState so you can tell.
"""

import argparse
import hashlib
import signal
import json
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

import Quartz

HERE = Path(__file__).parent
EXTRACT_JS = (HERE / "extract.js").read_text()
PREFETCH_JS = (HERE / "prefetch.js").read_text()
APPLESCRIPT = HERE / "crawl_page.applescript"

MAX_LOAD_SECONDS = 45
MAX_SETTLE_SECONDS = 12
OSASCRIPT_TIMEOUT = MAX_LOAD_SECONDS + MAX_SETTLE_SECONDS + 60
PER_HOST_DELAY = 3.0  # seconds between two hits on the same host
# A real browser usually passes a Cloudflare-style check by itself in a few seconds; one that
# needs a click ("Verify you are human") is left to the user: the crawler pauses, brings its
# window forward, and polls until the page changes.
CHALLENGE_POLL = 5.0
CHALLENGE_NOTIFY_AFTER = 15.0
CHALLENGE_MAX_PAUSE = 20 * 60
EMPTY_PAGE_MAX_WAIT = 30.0


def osascript(script, *args, timeout=60):
    cmd = ["osascript"] + ([str(script)] if isinstance(script, Path) else ["-e", script]) + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"osascript exited {proc.returncode}")
    return proc.stdout.rstrip("\n")


def applescript_string(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


WINDOW_STATE = Path("data") / "chrome_window.json"


class ChromeWindow:
    """The one Chrome window the crawler drives.

    Its id is remembered in data/chrome_window.json so every run and every script reuses the
    same window instead of opening a new one (opening a window steals focus; navigating one
    does not). It is only created if it does not exist, and is never closed by the scripts.
    """

    def __init__(self):
        self.id = None
        try:
            self.id = json.loads(WINDOW_STATE.read_text()).get("id")
        except (OSError, ValueError):
            pass

    @staticmethod
    def window_ids():
        return osascript('tell application "Google Chrome" to get id of every window').split(", ")

    def ensure(self):
        if self.id is not None:
            # Chrome occasionally fails to answer for a moment; don't open a new window on one miss
            last = None
            for attempt in range(5):
                try:
                    if self.id in self.window_ids():
                        return self.id
                    osascript(f'tell application "Google Chrome" to get title of active tab of window id "{self.id}"')
                    return self.id
                except RuntimeError as e:
                    last = e
                time.sleep(2.0)
            print(f"  Chrome window {self.id} is gone ({str(last)[:80]})", flush=True)
            self.id = None
        # window ids are text in Chrome's dictionary (and too big for AppleScript integers)
        new_id = osascript(
            'tell application "System Events" to set frontApp to name of first application process whose frontmost is true\n'
            'tell application "Google Chrome"\n'
            "set w to make new window\n"
            'set URL of active tab of w to "about:blank"\n'
            "set wid to id of w\nend tell\n"
            # creating a window brings Chrome forward; give focus back to whatever had it
            'tell application "System Events" to set frontmost of process frontApp to true\n'
            "return wid"
        ).strip()
        time.sleep(0.5)
        ids = self.window_ids()
        if new_id not in ids:
            # Chrome sometimes reports a bogus id for a window it just made; the new window is frontmost
            front = osascript('tell application "Google Chrome" to get {id, URL of active tab} of window 1').split(", ")
            if front[0] in ids and front[1].strip() == "about:blank":
                print(f"  Chrome reported window {new_id} but the new window is {front[0]}", flush=True)
                new_id = front[0]
        self.id = new_id
        WINDOW_STATE.write_text(json.dumps({"id": self.id}))
        print(f"  opened Chrome window {self.id} (reused by later runs; close it yourself when done)", flush=True)
        return self.id

    def bring_forward(self):
        try:
            osascript(
                'tell application "Google Chrome"\n'
                f'set index of window id "{self.id}" to 1\nactivate\nend tell'
            )
        except RuntimeError:
            pass

    def cg_window_id(self):
        """The window-server ID of our window, so screencapture can grab it even when covered."""
        bounds, title = osascript(
            'tell application "Google Chrome"\n'
            f'set b to bounds of window id "{self.id}"\n'
            'return ((item 1 of b) as text) & "," & ((item 2 of b) as text) & "," & ((item 3 of b) as text) & "," & ((item 4 of b) as text) & linefeed & '
            f'(title of active tab of window id "{self.id}")\nend tell'
        ).split("\n", 1)
        left, top, right, bottom = (int(float(x)) for x in bounds.split(","))
        candidates = []
        for w in Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID
        ):
            if w.get("kCGWindowOwnerName") != "Google Chrome" or w.get("kCGWindowLayer") != 0:
                continue
            b = w.get("kCGWindowBounds", {})
            if (int(b.get("X", -1)), int(b.get("Y", -1)), int(b.get("Width", -1)), int(b.get("Height", -1))) == (left, top, right - left, bottom - top):
                candidates.append(w)
        if len(candidates) > 1:
            candidates = [w for w in candidates if w.get("kCGWindowName") == title] or candidates
        return candidates[0]["kCGWindowNumber"] if candidates else None

    def screenshot(self, path):
        wid = self.cg_window_id()
        if wid is None:
            return False
        proc = subprocess.run(
            ["screencapture", "-x", "-o", "-t", "jpg", "-l", str(wid), str(path)], capture_output=True, text=True, timeout=30
        )
        return proc.returncode == 0 and path.exists()

    def close(self):
        """Leave the window open (and blank) for the next run; only a hung window is really closed."""
        if self.id is None:
            return
        try:
            osascript(f'tell application "Google Chrome" to set URL of active tab of window id "{self.id}" to "about:blank"')
        except RuntimeError:
            pass

    def discard(self):
        """Close the window for real (used when a page has hung Chrome's scripting channel)."""
        if self.id is None:
            return
        try:
            osascript(f'tell application "Google Chrome" to close window id "{self.id}"')
        except RuntimeError:
            pass
        self.id = None
        WINDOW_STATE.unlink(missing_ok=True)

    def load(self, url):
        """Navigate (url) or re-harvest (url='') and return (timed_out, tab_url, tab_title, page)."""
        for attempt in range(2):
            try:
                out = osascript(
                    APPLESCRIPT,
                    str(self.ensure()),
                    url,
                    PREFETCH_JS,
                    EXTRACT_JS,
                    str(MAX_LOAD_SECONDS),
                    str(MAX_SETTLE_SECONDS),
                    timeout=OSASCRIPT_TIMEOUT,
                )
                break
            except RuntimeError as e:
                if "window id" not in str(e) or attempt:
                    raise
                time.sleep(2.0)  # the window vanished (or Chrome hiccuped): ensure() will replace it
                self.id = None
        head, _, body = out.partition("\n")
        timed_out, tab_url, tab_title = head.split("|", 2)
        try:
            page = json.loads(body)
        except json.JSONDecodeError:
            page = {"extract_error": f"unparseable result: {body[:300]!r}"}
        return timed_out == "true", tab_url, tab_title, page


def file_key(row):
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", row["value"]).strip("_")[:60]
    if safe != row["value"]:
        safe += "_" + hashlib.sha1(row["value"].encode()).hexdigest()[:8]
    return f"{row['property']}__{safe}"


CHALLENGE_TITLE = re.compile(r"verifying your browser|checking (your )?connection|not to be a robot|just a moment|attention required", re.I)


def classify(record, page):
    """Rough status for triage; the raw signals stay in the record for a human to judge."""
    if record.get("error"):
        return "load_failed"
    if CHALLENGE_TITLE.search(page.get("title") or record.get("tab_title") or ""):
        return "challenge_suspected"  # extract.js missed some wordings ("Verifying your browser", "Checking connection not to be a robot")
    final = page.get("final_url") or record.get("tab_url") or ""
    if final.startswith(("chrome-error://", "about:blank", "chrome://")) or page.get("extract_error"):
        return "load_failed"
    sig = page.get("signals", {})
    # Challenge widgets/scripts (reCAPTCHA, Incapsula, Cloudflare) are also loaded on ordinary pages by
    # protected sites, so they only count on a bare page; a challenge title or wording counts anywhere.
    elements_on_bare_page = sig.get("challenge_elements") and (page.get("text_length") or 0) < 400
    if "you have been blocked" in sig.get("challenge_words", []) or "access denied" in sig.get("access_words", []):
        return "blocked"
    if sig.get("challenge_title") or sig.get("challenge_words") or elements_on_bare_page:
        return "challenge_suspected"
    if not (page.get("text_length") or 0) and not page.get("title"):
        return "empty_page"  # nothing rendered (yet?): a challenge shell, a redirect in progress, or a blank document
    status = page.get("http_status")
    if status and status >= 400:
        return "http_error"
    if record.get("load_timed_out") and not (page.get("title") or page.get("text_length")):
        return "load_timed_out"  # still blank when we gave up; a rendered page that never "finishes" is fine
    if sig.get("password_inputs") and {"sign in", "log in", "login"} & set(sig.get("access_words", [])):
        return "login_wall_suspected"
    return "ok"


def crawl_one(window, row, out_dir, host_last_hit):
    url = row["url"]
    host = urllib.parse.urlsplit(url).netloc
    wait = host_last_hit.get(host, 0) + PER_HOST_DELAY - time.monotonic()
    if wait > 0:
        time.sleep(wait)

    record = {
        "property": row["property"],
        "property_label": row["property_label"],
        "value": row["value"],
        "url": url,
        "crawled_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if row.get("wikidata_url"):
        record["wikidata_url"] = row["wikidata_url"]
        record["url_override_reason"] = row.get("override_reason")
    started = time.monotonic()
    page = {}
    try:
        timed_out, tab_url, tab_title, page = window.load(url)
        record.update(load_timed_out=timed_out, tab_url=tab_url, tab_title=tab_title)
        paused = 0.0
        notified = False
        while paused < CHALLENGE_MAX_PAUSE:
            status = classify(record, page)
            if status == "empty_page" and paused < EMPTY_PAGE_MAX_WAIT:
                pass  # give a slow redirect / challenge shell a little longer to turn into something
            elif status != "challenge_suspected":
                break
            if paused >= CHALLENGE_NOTIFY_AFTER and not notified:
                notified = True
                print(f"    PAUSED: human verification on {tab_url} - please click through it in the crawler window", flush=True)
                window.bring_forward()
                try:
                    osascript(
                        f'display notification {applescript_string(tab_url[:120])} '
                        'with title "Crawler paused: please verify you are human" sound name "Glass"'
                    )
                except RuntimeError:
                    pass  # the notification is a courtesy; keep waiting regardless
            time.sleep(CHALLENGE_POLL)
            paused += CHALLENGE_POLL
            _, tab_url, tab_title, page = window.load("")
            record.update(tab_url=tab_url, tab_title=tab_title)
        record["challenge_paused_seconds"] = paused
        if notified:
            print(f"    resumed after {paused:.0f}s", flush=True)
        try:
            shot = out_dir / "pages" / f"{file_key(row)}.jpg"
            if window.screenshot(shot):
                record["screenshot_file"] = f"pages/{shot.name}"
        except Exception as e:  # a missing screenshot is not worth losing the record
            record["screenshot_error"] = str(e)
    except subprocess.TimeoutExpired:
        record["error"] = "osascript timed out (page hung, or a dialog is blocking the tab)"
        window.discard()  # a hung tab would poison every later page
    except RuntimeError as e:
        record["error"] = str(e)
    host_last_hit[host] = time.monotonic()
    record["elapsed_seconds"] = round(time.monotonic() - started, 1)

    key = file_key(row)
    pages = out_dir / "pages"
    if page.get("html"):
        (pages / f"{key}.html").write_text(page.pop("html"))
        record["html_file"] = f"pages/{key}.html"
    if page.get("text") is not None:
        (pages / f"{key}.txt").write_text(page.pop("text"))
        record["text_file"] = f"pages/{key}.txt"
    for i, frame in enumerate(page.get("frames") or []):
        if frame.get("html"):
            (pages / f"{key}__frame{i}.html").write_text(frame.pop("html"))
            (pages / f"{key}__frame{i}.txt").write_text(frame.pop("text", ""))
            frame["html_file"] = f"pages/{key}__frame{i}.html"
    record["status"] = classify(record, page)
    record["page"] = page
    (out_dir / "records" / f"{key}.json").write_text(json.dumps(record, ensure_ascii=False, indent=1))
    return record


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("qid", nargs="?", default="Q7245")
    ap.add_argument("--only", help="comma-separated property IDs to crawl")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--force", action="store_true", help="re-crawl identifiers that already have a record")
    ap.add_argument("--retry-status", help="re-crawl records whose status is one of these (comma-separated)")
    args = ap.parse_args()

    out_dir = Path("data") / args.qid
    rows = json.loads((out_dir / "identifiers.json").read_text())
    # url_overrides.json: {property: {"url": ..., "reason": ...}} - a resolved redirect, a Wayback snapshot
    # instead of a calendar page, etc. The Wikidata-derived URL is kept in the record as wikidata_url.
    overrides_path = out_dir / "url_overrides.json"
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    for row in rows:
        ov = overrides.get(row["property"])
        if ov and row["url"]:
            row["wikidata_url"], row["url"], row["override_reason"] = row["url"], ov["url"], ov.get("reason")
    (out_dir / "pages").mkdir(exist_ok=True)
    (out_dir / "records").mkdir(exist_ok=True)
    retry = set(args.retry_status.split(",")) if args.retry_status else set()
    only = set(args.only.split(",")) if args.only else None

    todo = []
    for row in rows:
        if not row["url"] or (only and row["property"] not in only):
            continue
        existing = out_dir / "records" / f"{file_key(row)}.json"
        if existing.exists() and not args.force:
            if not retry or json.loads(existing.read_text()).get("status") not in retry:
                continue
        todo.append(row)
    todo = todo[: args.limit] if args.limit else todo
    print(f"{len(todo)} identifiers to crawl ({len(rows)} total)")

    window = ChromeWindow()
    host_last_hit = {}
    # make Ctrl-C / kill run the finally: below so the crawler window gets closed
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    try:
        for i, row in enumerate(todo, 1):
            print(f"[{i}/{len(todo)}] {row['property']} {row['property_label']}: {row['url']}", flush=True)
            record = crawl_one(window, row, out_dir, host_last_hit)
            page = record["page"]
            print(
                f"    {record['status']}  http={page.get('http_status')}  {record['elapsed_seconds']}s  "
                f"alt-links={len(page.get('link_elements', []))} jsonld={len(page.get('jsonld', []))} "
                f"machine-links={len(page.get('machine_links', []))} xhr={len(page.get('xhr_requests', []))}  "
                f"{record.get('error') or page.get('title', '')[:80]!s}",
                flush=True,
            )
    finally:
        window.close()


if __name__ == "__main__":
    main()
