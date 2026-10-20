"""Redact key-like tokens from the crawl's stored URLs before they go into git.

    uv run python scrub_secrets.py Q7245 [--check]

The page records keep every request URL the rendered page made. Sites embed their own public browser keys in those
(Google Maps / Firebase `AIzaSy…`, Sentry DSNs, New Relic, analytics hit tokens). They are not our secrets, but secret
scanners flag them. This replaces the value of such parameters with <redacted> in data/<QID>/records/ and data/<QID>/analysis/
(the raw pages and representations are not versioned). --check only reports what remains.
"""
import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"AIzaSy[0-9A-Za-z_-]{33}"), "AIzaSy<redacted>"),
    # a key/token value that looks like a credential: 16+ chars of letters and digits, both present, no percent-encoding, no slashes
    # (an identifier such as lookupname?key=Twain%2C%20Mark or partials.json?key=/subjects/x is data, not a secret)
    (re.compile(r"(?i)\b((?:api[_-]?key|apikey|clientkey|client_key|key|token|hittoken|access_token|auth_token|sentry_key|browser_monitoring_key|secret|x-plex-token)=)(?=[A-Za-z0-9_\-]{16,}(?:[&\"'\s]|$))(?=[^&\"'\s]*[A-Za-z])(?=[^&\"'\s]*[0-9])[A-Za-z0-9_\-]+"), r"\1<redacted>"),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9_\-.]{16,}"), r"\1<redacted>"),
]
EXT = {".json", ".csv", ".md", ".txt", ".html", ".jsonl"}


def main():
    args = sys.argv[1:]
    qid = next((a for a in args if a.startswith("Q")), "Q7245")
    check = "--check" in args
    roots = [Path("data") / qid / "records", Path("data") / qid / "analysis", Path("docs"), Path("data") / "landscape"]
    changed = hits = 0
    for root in roots:
        for f in root.rglob("*"):
            if not f.is_file() or f.suffix not in EXT:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            new, n = text, 0
            for rx, repl in PATTERNS:
                new, k = rx.subn(repl, new)
                n += k
            if n:
                hits += n
                print(f"  {f}: {n}")
                if not check:
                    f.write_text(new, encoding="utf-8")
                    changed += 1
    print(f"{hits} matches in {changed if not check else 'unchanged'} files")


if __name__ == "__main__":
    main()
