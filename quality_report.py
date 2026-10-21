"""Step 8: quality report - how each site behaved as a source, and roll-ups across all of them.

    uv run python quality_report.py Q7245 [--probe-embedded]

Reads the crawl records (step 2), representation manifests (steps 4-5), profiles (step 6) and the
Wikidata comparison (step 7) and writes, under data/<qid>/analysis/:

    quality_records.csv   one row per crawled page: resolution, load, page weight, third parties,
                          ads/trackers/consent, challenge/login signals, representations by access route
    quality_sites.csv     one row per identifier property (site): the above rolled up, plus data richness,
                          languages, how much of its data is unique vs repeated on other sites, and overlap
                          with Wikidata
    quality.md            the report: counts and percentages for every quality aspect, then a per-site table

--probe-embedded re-fetches, with plain Python, the pages whose rendered HTML carried embedded data
(JSON-LD / RDFa / microdata / OpenGraph) and checks whether the same markup is in the server's HTML,
so "embedded" data can be split into "there for any HTTP client" vs "only after JavaScript ran".
Results are cached in analysis/embedded_probe.json.
"""

import argparse

from profile_representations import entity_name_tokens, mentions_entity
import csv
import json
import math
import re
import sys
import time
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

STRUCTURED = {"json-ld", "rdf-xml", "turtle", "n-triples", "marcxml", "marc-binary", "mads", "eac-cpf", "json", "xml", "rdfa", "microdata", "opengraph", "csv", "feed"}
EMBEDDED_SYNTAXES = {"json-ld", "rdfa", "microdata", "opengraph"}
RDF_FORMATS = {"json-ld", "rdf-xml", "turtle", "n-triples", "rdfa"}
LIBRARY_FORMATS = {"marcxml", "marc-binary", "mads", "eac-cpf", "marc-json"}

# elements whose values describe the person (used for the unique-vs-shared measure); the rest are
# record plumbing (identifiers, timestamps, licences...) that is by nature site-specific
DESCRIPTIVE = ["name_preferred", "name_variant", "given_name", "family_name", "pseudonym", "birth_date", "death_date", "birth_place", "death_place",
               "activity_place", "gender", "occupation", "field_of_activity", "nationality", "language", "description", "work", "subject_of", "related_agent"]

# third-party host classification (substring match on the host name)
AD_HOSTS = ["doubleclick.net", "googlesyndication", "adtrafficquality.google", "pubmatic", "criteo", "casalemedia", "rubiconproject", "amazon-adsystem",
            "adnxs", "openx", "3lift", "triplelift", "id5-sync", ".ad.gt", "hadronid", "hadron.ad", "adsrvr", "crwdcntrl", "onetag-sys", "liadm.com",
            "a-mo.net", "smartadserver", "33across", "media.net", "360yield", "creativecdn", "indexww", "1rx.io", "sharethrough", "turn.com", "sonobi",
            "intentiq", "gumgum", "seedtag", "pubgw.yahoo", "lijit", "tapad", "kargo", "yieldmo", "adform", "taboola", "outbrain", "mgid", "revcontent",
            "bidswitch", "teads", "appnexus", "advertising.com", "adroll", "zemanta", "imasdk.googleapis", "2mdn.net", "fastclick", "btloader",
            "ad-delivery.net", "adsafeprotected", "moatads", "doubleverify", "bounceexchange", "ingage.tech", "ezoic", "mediavine", "adthrive",
            "raptive", "carbonads", "buysellads", "adsense", "adservice", "quantserve", "rlcdn.com", "bluekai", "demdex", "everesttech", "mathtag",
            "rfihub", "simpli.fi", "stackadapt", "undertone", "unrulymedia", "vidazoo", "primis", "connatix", "adlightning", "amazon-adsystem", "pubnative",
            "nexx360", "sovrn", "mediavine", "adswizz", "springserve", "spotx", "adkernel", "improvedigital", "aniview", "brealtime", "e-planning",
            "exponential.com", "mediafuse", "nativo", "permutive", "rtbhouse", "the-ozone-project", "xandr", "yieldlab", "zeotap", "adition", "adscale",
            "ligatus", "plista", "cdn.adsafeprotected"]
ANALYTICS_HOSTS = ["google-analytics", "googletagmanager", "analytics.google", "stats.g.doubleclick", "cloudflareinsights", "newrelic", "nr-data",
                   "plausible.io", "clarity.ms", "hotjar", "matomo", "piwik", "scorecardresearch", "mixpanel", "segment.io", "segment.com", "heapanalytics",
                   "fullstory", "chartbeat", "parsely", "parse.ly", "mc.yandex", "hm.baidu", "connect.facebook.net", "facebook.com/tr", "sentry.io",
                   "sentry-cdn", "bugsnag", "datadoghq", "amplitude", "mouseflow", "crazyegg", "luckyorange", "statcounter", "quantserve", "comscore",
                   "omtrdc", "adobedtm", "demdex", "tealium", "snowplow", "siteimprove", "monsido", "getsitecontrol", "wikimedia.org/beacon", "umami"]
CONSENT_HOSTS = ["cookielaw", "onetrust", "cookiebot", "privacymanager", "consentmanager", "fundingchoices", "quantcast.mgr", "trustarc", "usercentrics",
                 "didomi", "iubenda", "cookieyes", "cookie-script", "termly", "osano", "cookiefirst", "complianz", "cookiepro", "sourcepoint", "sp-prod",
                 "cmp."]
SOCIAL_HOSTS = ["platform.twitter", "syndication.twitter", "facebook.com", "fbcdn", "instagram.com", "sharethis", "addtoany", "addthis", "linkedin.com",
                "pinterest", "youtube.com", "ytimg", "vimeo", "tiktok", "disqus", "reddit.com"]
CDN_HOSTS = ["jsdelivr", "cdnjs", "unpkg", "googleapis.com", "gstatic", "bootstrapcdn", "jquery.com", "cloudflare.com", "fontawesome", "typekit",
             "fonts.net", "polyfill", "akamai", "fastly", "cloudfront", "azureedge", "jsdelivr", "wp.com", "wikimedia.org", "archive.org", "bunny.net"]
CHALLENGE_HOSTS = ["recaptcha", "hcaptcha", "turnstile", "challenges.cloudflare", "incapsula", "imperva", "perimeterx", "px-cdn", "datadome", "arkoselabs", "funcaptcha"]

# markers in the saved HTML that mean ad slots were set up, even if no ad request fired
AD_MARKUP = re.compile(r"adsbygoogle|google_ads_iframe|div-gpt-ad|data-ad-slot|googletag\.(pubads|defineSlot)|data-ad-client|adsbygoogle\.js|\bid=\"ad-(slot|container|banner)|class=\"[^\"]*\b(adunit|ad-unit|ad-slot|advert)\b", re.I)
CHALLENGE_URL = re.compile(r"recaptcha|hcaptcha|turnstile|challenges\.cloudflare|_Incapsula_Resource|incapsula|perimeterx|datadome|arkoselabs|funcaptcha|cdn-cgi/challenge", re.I)
ADBLOCK_MARKUP = re.compile(r"adblock|ad-blocker|ad blocker", re.I)


def classify_host(host):
    h = host.lower()
    if any(p in h for p in CHALLENGE_HOSTS):
        return "challenge"
    if any(p in h for p in CONSENT_HOSTS):
        return "consent"
    if any(p in h for p in ANALYTICS_HOSTS):
        return "analytics"
    if any(p in h for p in AD_HOSTS):
        return "ads"
    if any(p in h for p in SOCIAL_HOSTS):
        return "social"
    if any(p in h for p in CDN_HOSTS):
        return "cdn"
    return "other"


WRONG_PAGE = [  # (url pattern, reason, only when the page never mentions the entity)
    (re.compile(r"^https?://web\.archive\.org/web/\d*\*/"), "Wayback calendar page, not an archived snapshot", False),
    (re.compile(r"^https?://viaf\.org/(\w+/)?processed/"), "VIAF 'processed' redirect page never forwarded to the cluster", True),
    (re.compile(r"^https?://wikidata-externalid-url\.toolforge\.org/"), "toolforge redirector page, never forwarded", True),
]
CHALLENGE_TITLE = re.compile(r"verifying your browser|checking (your )?connection|not to be a robot|just a moment|attention required", re.I)


def strong_name(text):
    low = text.lower()
    return ("twain" in low and "spirit" not in low[: low.find("twain") + 40]) or ("clemens" in low and ("samuel" in low or "langhorne" in low))


def wrong_page_reason(r):
    """A page that loaded fine (status ok) but is not the entity's record."""
    pg = r.get("page") or {}
    final = pg.get("final_url") or r.get("tab_url") or r["url"]
    if CHALLENGE_TITLE.search(pg.get("title") or r.get("tab_title") or ""):
        return "challenge page ('" + (pg.get("title") or r.get("tab_title"))[:40] + "')"
    for rx, reason, needs_absence in WRONG_PAGE:
        if rx.search(final) and not (needs_absence and r["entity_on_page"]):
            return reason
    if not r["entity_on_page"] and pg.get("signals", {}).get("not_found_words") and (pg.get("text_length") or 0) < 1500:
        return "not-found wording on a short page that never mentions the entity"
    if re.search(r"\(\s*Spirit\s*\)", (pg.get("title") or "") + " " + (r.get("text_head") or "")) and not strong_name(r.get("text_head") or ""):
        return "'(Spirit)' heading: a library record for books channelled through a medium, not him"
    if not r["entity_on_page"]:
        # a catalogue record whose heading is somebody else (Koha: "MARC view › Muguet, Christian (Nomi di persona) › ...")
        title = pg.get("title") or r.get("tab_title") or ""
        for seg in re.split(r"\s*[›>»|]\s*", title):
            if re.match(r"^[A-ZÀ-Þ][^,()]{1,40}, [A-ZÀ-Þ][^()›>]{1,40}", seg.strip()):
                return f"record for a different person ('{seg.strip()[:50]}')"
    return None


NAME_TOKENS_Q = set()


def load_records(data_dir, name_tokens):
    NAME_TOKENS_Q.update(name_tokens)
    recs = []
    for path in sorted((data_dir / "records").glob("*.json")):
        r = json.loads(path.read_text())
        r["key"] = path.stem
        text = (data_dir / r["text_file"]).read_text(errors="ignore") if r.get("text_file") and (data_dir / r["text_file"]).exists() else ""
        for frame_txt in sorted((data_dir / "pages").glob(f"{r['key']}__frame*.txt")):
            text += "\n" + frame_txt.read_text(errors="ignore")   # <frameset> sites keep the record in a child frame
        r["entity_on_page"] = mentions_entity(text, name_tokens)
        r["text_head"] = text[:600]
        r["status_note"] = None
        title = (r.get("page") or {}).get("title") or ""
        if r["status"] == "ok" and not r["entity_on_page"] and re.search(r"captcha|rewrite (the )?characters|are you (a )?human|verify (that )?you are", text[:2000], re.I):
            r["status"], r["status_note"] = "challenge_suspected", "CAPTCHA on the page"
        words = re.findall(r"\S+", text[:3000])
        if r["status"] == "ok" and not r["entity_on_page"] and len(words) > 40 and sum(len(w) for w in words) / len(words) > 14:
            r["status"], r["status_note"] = "blocked", "page text is obfuscated (bot block or failed render)"
        if r["status"] == "ok" and not r["entity_on_page"] and len(text) < 4000 and re.search(r"not understood|no results|no matches|not found|nicht gefunden|introuvable|no se encontr|не найден", text[:3000], re.I):
            r["status"], r["status_note"] = "http_error", "not-found wording on the page"
        if r["status"] in ("login_wall_suspected", "http_error") and len(text) > 400 and (r["entity_on_page"] or re.search(r"MARC|Authorit|Autorit|Notice|Record|Fitxa|Registre|Details", title)):
            # a Koha/Primo "log in" link or a HEAD request's error code, with his record fully rendered underneath
            r["status_note"] = f"{r['status'].replace('_', ' ')} but the record rendered in full"
            r["status"] = "ok"
        if re.search(r"Processed record not found|does not appear in this dataset", text[:3000]):
            r["status"], r["status_note"] = "http_error", "record not found (dead identifier, or a dead link pattern on the site)"
        if not r["entity_on_page"] and len(text) < 2000 and r.get("html_file") and (data_dir / r["html_file"]).exists():
            # innerText misses content hidden under a consent modal (Vatican OPAC); fall back to the saved DOM's text
            html_text = re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", (data_dir / r["html_file"]).read_text(errors="ignore")))
            r["entity_on_page"] = mentions_entity(html_text, name_tokens)
        r["wrong_page_reason"] = None
        if r["status"] in ("ok", "login_wall_suspected"):   # a Koha/Primo login box is site chrome, the record is still judged
            reason = wrong_page_reason(r)
            if reason:
                r["status"], r["wrong_page_reason"] = "wrong_page", reason
        recs.append(r)
    return recs


def load_manifests(data_dir):
    out = {}
    for path in (data_dir / "representations").glob("*/manifest.json"):
        m = json.loads(path.read_text())
        out[path.parent.name] = m
    return out


def load_profiles(data_dir):
    out = {}
    for path in (data_dir / "analysis" / "profiles").glob("P*.json"):
        out[path.stem] = json.loads(path.read_text())
    return out


MECHANISM = {"alternate": "link rel=alternate", "conneg": "content negotiation", "export": "export link", "xhr": "page XHR/API", "api": "replayed API call",
             "extra": "data link on the page"}   # extra_representations.json: a data URL the page links to (LUX's /data/person/ Linked Art)


def route_of(rep):
    """How a saved representation was obtained."""
    if rep["kind"] == "embedded":
        return "embedded"
    if rep["kind"] == "api" or rep.get("via") == "browser":
        return "browser"
    return "http"


def file_route(fname):
    base = fname.split("/")[-1]
    if base.startswith("embedded_"):
        return "embedded"
    if base.startswith(("browser_", "api_")):
        return "browser"
    if base.startswith("llm") or base.endswith("P.json"):
        return "http"
    return "http"


def norm_value(v):
    return re.sub(r"[\W_]+", " ", str(v).lower()).strip()


NAME_ELEMENTS = {"name_preferred", "name_variant", "pseudonym"}
UNIQ_CAP = 50   # each element weighs at most this many distinct values in a site's unique share, so a catalogue's holdings list cannot swamp the rest

# "useful beyond Wikidata": sum over elements of weight x log2(1 + distinct values Wikidata does not hold). A count, not a share, so
# 700 works outweigh one relative; log-scaled so the 700th title is worth less than the first; weighted by what a reader comes for.
USEFUL_WEIGHTS = {"work": 1.5, "subject_of": 1.5, "related_agent": 1.5, "name_preferred": 1.0, "name_variant": 1.0, "pseudonym": 1.0,
                  "given_name": 0.5, "family_name": 0.5, "occupation": 1.0, "field_of_activity": 1.0, "description": 0.5, "language": 0.5,
                  "activity_place": 1.0, "birth_date": 1.0, "death_date": 1.0, "birth_place": 1.0, "death_place": 1.0, "gender": 0.5, "nationality": 0.5}
WD_KEYS = set()       # uniq_key()s of everything Wikidata holds (labels, aliases, demonyms, containing places) - filled by main()
WD_DATE_KEYS = set()  # digit strings of Wikidata's dates, so a year or year-month on a site counts as already known


def on_wikidata(key):
    el, k = key
    if key in WD_KEYS:
        return True
    if el in ("birth_date", "death_date"):
        return any(d.startswith(k) for d in WD_DATE_KEYS) if k else True
    return False


def uniq_key(el, v):
    """Key for 'does another source state this value': name elements pooled; annotations the page-text pass adds
    ('(translator of ...)', ', 1835-1910') and date punctuation stripped, so 'Orban, Jean-Pierre (translator)' = 'Jean-Pierre Orban'."""
    s = str(v)
    s = re.sub(r"\s*[\(\[][^\)\]]*[\)\]]", " ", s)            # parenthetical annotations
    s = re.sub(r",?\s*\b(ca\.?\s*)?1[0-9]{3}\s*-\s*(1[0-9]{3})?\b\.?$", "", s)   # trailing life dates on headings
    s = re.sub(r"T00:00:00(Z|[+-]\d\d:\d\d)?$", "", s)
    if el in ("birth_date", "death_date"):
        s = re.sub(r"\D", "", s)                                  # 1835-11-30 / 18351130 / 1835.11.30 -> 18351130
    key = norm_value(s)
    if el in NAME_ELEMENTS or el in ("given_name", "family_name"):
        key = " ".join(sorted(t for t in key.split() if len(t) > 1))   # 'twain mark' = 'mark twain'
        el = "name"
    return (el, key)


# ---------- --probe-embedded ----------

def probe_embedded(data_dir, records, manifests):
    """Which embedded syntaxes are present in the server-sent HTML (no JavaScript)?"""
    import extruct
    import truststore
    import urllib.request

    truststore.inject_into_ssl()
    cache_path = data_dir / "analysis" / "embedded_probe.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    ua = "wikidata-identifier-inventory/0.1 (research crawl; thisismattmiller@gmail.com)"
    last_hit = {}
    # every page that rendered his record: does the server send it to a plain client at all, and with which embedded syntaxes?
    todo = [r for r in records if r["status"] in ("ok", "login_wall_suspected") and r["key"] not in cache
            and (r.get("entity_on_page") or (r["key"] in manifests and any(x["kind"] == "embedded" and x.get("file") for x in manifests[r["key"]]["representations"])))]
    print(f"probing {len(todo)} rendered pages with a plain client (cached: {len(cache)})", flush=True)
    for i, r in enumerate(todo, 1):
        url = (r.get("page") or {}).get("final_url") or r["url"]
        if not url.startswith("http"):
            url = r["url"]
        host = urllib.parse.urlsplit(url).hostname or ""
        wait = 1.0 - (time.time() - last_hit.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        last_hit[host] = time.time()
        entry = {"url": url, "status": None, "syntaxes": [], "error": None}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html,application/xhtml+xml"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                entry["status"] = resp.status
                html = resp.read(5_000_000).decode("utf-8", errors="replace")
            found = extruct.extract(html, base_url=url, syntaxes=["json-ld", "microdata", "rdfa", "opengraph"], uniform=True, errors="ignore")
            entry["syntaxes"] = sorted(k for k, v in found.items() if v)
        except Exception as e:  # noqa: BLE001 - any failure is a finding here
            entry["error"] = str(e)[:200]
            m = re.search(r"HTTP Error (\d+)", entry["error"])
            if m:
                entry["status"] = int(m.group(1))
        cache[r["key"]] = entry
        print(f"  [{i}/{len(todo)}] {r['property']} {host}: {entry['status']} {entry['syntaxes'] or entry['error'] or '-'}", flush=True)
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    return cache


# ---------- per-record metrics ----------

def record_metrics(r, manifest, probe, entity_files):
    pg = r.get("page") or {}
    url = r["url"]
    final = pg.get("final_url") or r.get("tab_url") or url
    hosts = pg.get("third_party_hosts") or {}
    host_classes = defaultdict(list)
    for h in hosts:
        host_classes[classify_host(h)].append(h)
    if not final.startswith("http") or "chromewebdata" in final or final.startswith("chrome-error"):
        final = url
    iframes = [s for s in (pg.get("iframes") or []) if isinstance(s, str) and s.startswith("http")]
    iframe_classes = Counter(classify_host(urllib.parse.urlsplit(s).hostname or "") for s in iframes)
    scripts = [s for s in (pg.get("scripts") or []) if isinstance(s, str)]
    script_classes = Counter(classify_host(urllib.parse.urlsplit(s).hostname or "") for s in scripts)
    html = ""
    if r.get("html_file"):
        try:
            html = (DATA_DIR / r["html_file"]).read_text(errors="replace")
        except OSError:
            html = ""
    ad_markup = bool(AD_MARKUP.search(html))
    ad_requests = bool(host_classes["ads"]) or iframe_classes["ads"] > 0 or script_classes["ads"] > 0
    if ad_requests:
        ads = "ads served"
    elif ad_markup:
        ads = "ad slots in markup, nothing loaded"
    else:
        ads = "none"
    sig = pg.get("signals") or {}
    challenge_widget = bool(host_classes["challenge"]) or any(CHALLENGE_URL.search(u) for u in iframes + scripts) or bool(sig.get("challenge_elements"))

    reps = manifest["representations"] if manifest else []
    attempts = [x for x in reps if x["kind"] != "embedded"]
    saved = [x for x in reps if x.get("file") and x.get("detected") in STRUCTURED and x.get("detected") not in ("json-invalid",)]
    formats_by_route = defaultdict(set)
    for x in saved:
        formats_by_route[route_of(x)].add(x["detected"])
    # browser-only: a format obtained in the browser whose first-pass attempt failed and that http never produced
    http_formats = formats_by_route["http"]
    browser_only = formats_by_route["browser"] - http_formats
    embedded_formats = formats_by_route["embedded"]
    probe_entry = probe.get(r["key"])
    probe_blocked = bool(probe_entry) and (probe_entry.get("error") or probe_entry.get("status") != 200)
    if probe_entry and embedded_formats and not probe_blocked:
        embedded_in_server_html = sorted(embedded_formats & set(probe_entry["syntaxes"]))
        embedded_js_only = sorted(embedded_formats - set(probe_entry["syntaxes"]))
    else:
        embedded_in_server_html, embedded_js_only = [], []
    probe_status = (probe_entry.get("status") or probe_entry.get("error", "")[:40]) if probe_entry else None
    mechanisms, entity_mechanisms, entity_formats, entity_routes = set(), set(), set(), set()
    for x in saved:
        mech = MECHANISM.get(x["kind"]) or f"embedded {x['detected']}"
        mechanisms.add(mech)
        if f"{r['key']}/{x['file']}" in entity_files:
            entity_mechanisms.add(mech)
            entity_formats.add(x["detected"])
            route = route_of(x)
            if route == "embedded":
                if probe_blocked:
                    route = "page blocked for plain HTTP"
                elif probe_entry:
                    route = "http" if x["detected"] in probe_entry["syntaxes"] else "js-rendered page"
                else:
                    route = "rendered page (unprobed)"
            entity_routes.add(route)
    link_header = (pg.get("response_headers") or {}).get("headers", {}).get("link", "") if isinstance(pg.get("response_headers"), dict) else ""
    return {
        "key": r["key"], "property": r["property"], "property_label": r["property_label"], "value": r["value"], "url": url, "final_url": final,
        "host": urllib.parse.urlsplit(final).hostname or "", "status": r["status"], "status_note": r.get("status_note"), "http_status": pg.get("http_status"),
        "title": pg.get("title"), "text_head": r.get("text_head"),
        "entity_on_page": r["entity_on_page"], "wrong_page_reason": r["wrong_page_reason"], "url_override_reason": r.get("url_override_reason"),
        "https": final.startswith("https://"), "redirected": urllib.parse.urlsplit(final).hostname != urllib.parse.urlsplit(url).hostname,
        "load_seconds": r.get("elapsed_seconds"), "load_timed_out": bool(r.get("load_timed_out")), "challenge_paused_seconds": r.get("challenge_paused_seconds") or 0,
        "challenge_widget": challenge_widget, "challenge_title": bool(sig.get("challenge_title")), "password_inputs": sig.get("password_inputs") or 0,
        "access_words": "; ".join(sig.get("access_words") or []), "not_found_words": "; ".join(sig.get("not_found_words") or []),
        "page_lang": pg.get("lang"), "html_bytes": pg.get("html_length") or len(html), "text_chars": pg.get("text_length") or 0,
        "resources": len(pg.get("resources") or []), "scripts": len(scripts), "iframes": len(iframes), "third_party_hosts": len(hosts),
        "ads": ads, "ad_hosts": len(host_classes["ads"]), "ad_host_list": "; ".join(sorted(host_classes["ads"])[:12]), "ad_markup": ad_markup,
        "adblock_notice": bool(ADBLOCK_MARKUP.search(html)),
        "analytics_hosts": len(host_classes["analytics"]), "analytics_host_list": "; ".join(sorted(host_classes["analytics"])[:8]),
        "consent_manager": bool(host_classes["consent"]) or bool(re.search(r"cookie(consent|banner|notice|law|bot)|onetrust|didomi|usercentrics", html, re.I)),
        "social_hosts": len(host_classes["social"]), "cdn_hosts": len(host_classes["cdn"]), "other_third_party_hosts": len(host_classes["other"]),
        "link_header_alternate": "rel=\"alternate\"" in link_header or "rel=alternate" in link_header,
        "rep_attempts": len(attempts), "rep_saved": len(saved),
        "formats_http": ", ".join(sorted(http_formats)), "formats_browser_only": ", ".join(sorted(browser_only)), "formats_embedded": ", ".join(sorted(embedded_formats)),
        "embedded_in_server_html": ", ".join(embedded_in_server_html), "embedded_js_only": ", ".join(embedded_js_only), "probe_status": probe_status, "probe_blocked": bool(probe_blocked),
        "mechanisms": "; ".join(sorted(mechanisms)), "entity_mechanisms": "; ".join(sorted(entity_mechanisms)),
        "entity_formats": ", ".join(sorted(entity_formats)), "entity_routes": "; ".join(sorted(entity_routes)),
        "rdf": bool((http_formats | browser_only | embedded_formats) & RDF_FORMATS), "library_format": bool((http_formats | browser_only) & LIBRARY_FORMATS),
    }


# ---------- per-site metrics ----------

def site_metrics(prop, recs, profiles, comparison, value_sites):
    p = profiles.get(prop)
    label = recs[0]["property_label"]
    # a page that rendered (ok) but never mentions the entity, with nothing about the entity extracted either, is the
    # wrong page: a JS app shell, a redirect that never happened, a home page, a 403 in another language...
    # pages (keys) that yielded descriptive values from structured data, not from the rendered text
    # element rows carry bare file names; the profile's file list maps them to "<key>/<name>"
    bare_to_keys = defaultdict(set)
    for f in (p["files"] if p else []):
        if "/" in f["file"]:
            bare_to_keys[f["file"].split("/")[-1]].add(f["file"].split("/")[0])
    structured_keys = {k for el, vals in (p["elements"].items() if p else []) if el in DESCRIPTIVE
                       for v in vals if v.get("file") and not (v.get("via") or "").startswith("llm") for k in bare_to_keys.get(v["file"].split("/")[-1], ())}
    for r in recs:
        if r["status"] == "wrong_page" and r["key"] in structured_keys and r["wrong_page_reason"] and re.search(r"never (mentions|forwarded)", r["wrong_page_reason"]):
            # VIAF-served libraries: the HTML shell is blank but the record came back through the site's data endpoint
            r["status"], r["wrong_page_reason"], r["status_note"] = "ok", None, "page shell was blank; the record came through the site's data endpoint"
        elif r["status"] == "ok" and (r.get("text_chars") or 0) >= 300 and r["key"] not in structured_keys and len(recs) > 1 and (
                not r["entity_on_page"] or not mentions_entity((r.get("title") or "") + " " + (r.get("text_head") or "")[:400], NAME_TOKENS_Q)):
            r["status"], r["wrong_page_reason"] = "wrong_page", "page heading is not him (another of this property's values is his record)"
    entity_seen = any(r["entity_on_page"] for r in recs) or bool(structured_keys)
    wrong_reason = next((r["wrong_page_reason"] for r in recs if r["wrong_page_reason"]), None)
    if not entity_seen and any(r["status"] == "ok" for r in recs):
        for r in recs:
            if r["status"] == "ok":
                r["status"], r["wrong_page_reason"] = "wrong_page", "page rendered but never mentions the entity"
        wrong_reason = wrong_reason or "page rendered but never mentions the entity"
    statuses = Counter(r["status"] for r in recs)
    any_ok = any(r["status"] == "ok" for r in recs)
    out = {
        "property": prop, "label": label, "pages": len(recs), "hosts": "; ".join(sorted({r["host"] for r in recs})),
        "status": ", ".join(f"{k}×{n}" if n > 1 else k for k, n in statuses.most_common()), "resolved": any_ok,
        "entity_on_page": entity_seen, "wrong_page_reason": wrong_reason or "", "status_note": next((r.get("status_note") for r in recs if r.get("status_note")), "") or "",
        "https": all(r["https"] for r in recs), "load_seconds": round(max((r["load_seconds"] or 0) for r in recs), 1),
        "challenge_widget": any(r["challenge_widget"] for r in recs), "challenge_paused": any(r["challenge_paused_seconds"] > 0 for r in recs),
        "login_box": any(r["password_inputs"] > 0 for r in recs),
        "html_kb": round(max(r["html_bytes"] for r in recs) / 1024), "text_chars": max(r["text_chars"] for r in recs), "resources": max(r["resources"] for r in recs),
        "third_party_hosts": max(r["third_party_hosts"] for r in recs),
        "ads": "ads served" if any(r["ads"] == "ads served" for r in recs) else ("ad slots in markup, nothing loaded" if any(r["ad_markup"] for r in recs) else "none"),
        "ad_hosts": max(r["ad_hosts"] for r in recs), "analytics_hosts": max(r["analytics_hosts"] for r in recs),
        "consent_manager": any(r["consent_manager"] for r in recs), "social_hosts": max(r["social_hosts"] for r in recs),
        "rep_attempts": sum(r["rep_attempts"] for r in recs), "rep_saved": sum(r["rep_saved"] for r in recs),
        "formats_http": ", ".join(sorted({f for r in recs for f in r["formats_http"].split(", ") if f})),
        "formats_browser_only": ", ".join(sorted({f for r in recs for f in r["formats_browser_only"].split(", ") if f})),
        "formats_embedded": ", ".join(sorted({f for r in recs for f in r["formats_embedded"].split(", ") if f})),
        "embedded_js_only": ", ".join(sorted({f for r in recs for f in r["embedded_js_only"].split(", ") if f})),
        "mechanisms": "; ".join(sorted({m for r in recs for m in r["mechanisms"].split("; ") if m})),
        "rdf": any(f in RDF_FORMATS for r in recs for f in r["entity_formats"].split(", ")), "library_format": any(r["library_format"] for r in recs),
    }
    # entity data: what the profile actually extracted about the person
    if p:
        elements = p["elements"]
        vals = [(el, v) for el, vals in elements.items() for v in vals]
        files_used = {v["file"] for el, v in vals if v.get("file") and el in DESCRIPTIVE and not (v.get("via") or "").startswith("llm")}
        routes = Counter(rt for r in recs for rt in r["entity_routes"].split("; ") if rt)
        # "page text only" = nothing *descriptive* about him came from structured data (a site tagline or logo does not count)
        page_text_only = bool(vals) and not any(el in DESCRIPTIVE and not (v.get("via") or "").startswith("llm-page") for el, v in vals)
        if page_text_only:
            # the only data about the entity is the rendered page's text: reachable by a plain client only if the
            # server sends the page to one (the --probe-embedded fetch tells)
            routes = Counter(("page blocked for plain HTTP" if r["probe_blocked"] else "html page text") if r["probe_status"] else "plain HTTP untested"
                             for r in recs if r["entity_on_page"])
        elif any((v.get("via") or "").startswith("llm") for _, v in vals) and not routes:
            routes["http"] += 1  # LLM extractions were made from files already on disk
        descriptive = [(el, v) for el, v in vals if el in DESCRIPTIVE and not v.get("uri") and not str(v["value"]).startswith("http")]
        # distinct values per element (a label repeated in five files is one value); shared = some other site or Wikidata states it
        distinct = {}
        for el, v in descriptive:
            distinct.setdefault(el, {}).setdefault(uniq_key(el, v["value"]), v)
        n_distinct = sum(len(d) for d in distinct.values())
        n_unique = sum(1 for d in distinct.values() for k in d if value_sites[k] <= 1)
        shared = n_distinct - n_unique
        # element-balanced share: each element weighs at most UNIQ_CAP values
        w_tot = sum(min(len(d), UNIQ_CAP) for d in distinct.values())
        w_uni = sum(min(len(d), UNIQ_CAP) * sum(1 for k in d if value_sites[k] <= 1) / len(d) for d in distinct.values() if d)
        # useful beyond Wikidata: per element, distinct values Wikidata does not hold
        beyond = {el: sum(1 for k in d if not on_wikidata(k)) for el, d in distinct.items()}
        useful = sum(USEFUL_WEIGHTS.get(el, 0.5) * math.log2(1 + n) for el, n in beyond.items() if n)
        langs = {v["lang"].split("-")[0] for _, v in vals if v.get("lang")}
        others = {k for k in routes if k != "http"}
        if page_text_only:
            access = "page text only" + (" (page blocked for plain HTTP)" if routes.get("page blocked for plain HTTP") else
                                         " (page served to plain HTTP)" if routes.get("html page text") else " (plain HTTP untested)")
        elif routes.get("http") and not others:
            access = "plain HTTP"
        elif routes.get("http"):
            access = "plain HTTP, partly (" + ", ".join(sorted(others)) + ")"
        elif others:
            access = " / ".join(sorted(others)) + " only"
        else:
            access = "none"
        llm = any((v.get("via") or "").startswith("llm") for _, v in vals)
        n_page = sum(1 for _, v in vals if (v.get("via") or "").startswith("llm-page"))
        if not page_text_only and n_page:
            access += f" + page text for {n_page}/{len(vals)} values"
        out.update({
            "has_entity_data": bool(vals), "entity_data_access": access,
            "entity_formats": "html" if page_text_only else ", ".join(sorted({f for r in recs for f in r["entity_formats"].split(", ") if f})),
            "page_text_only": page_text_only,
            "entity_mechanisms": "; ".join(sorted({m for r in recs for m in r["entity_mechanisms"].split("; ") if m})),
            "data_files_used": len(files_used), "formats_used": ", ".join(sorted(p["formats"])),
            "elements": sum(1 for el, vs in elements.items() if vs), "values": len(vals), "descriptive_values": n_distinct,
            "page_text_values": sum(1 for _, v in vals if (v.get("via") or "").startswith("llm-page")),
            "unique_values": n_unique, "shared_values": shared,
            "useful_score": round(useful, 1), "values_beyond_wikidata": sum(beyond.values()),
            "useful_by": "; ".join(f"{el}:{n}" for el, n in sorted(beyond.items(), key=lambda kv: -USEFUL_WEIGHTS.get(kv[0], 0.5) * math.log2(1 + kv[1])) if n),
            "unique_share": round(w_uni / w_tot, 2) if w_tot else None,
            "languages": len(langs), "language_list": ", ".join(sorted(langs)), "vocabularies": len([v for v in p["vocabularies"] if v != "LLM extraction"]),
            "needed_llm_extraction": llm, "unmapped_predicates": sum(p["unmapped"].values()),
        })
    else:
        out.update({"has_entity_data": False, "entity_data_access": "none", "entity_formats": "", "entity_mechanisms": "", "data_files_used": 0, "formats_used": "", "elements": 0, "values": 0, "descriptive_values": 0, "page_text_values": 0, "useful_score": 0, "values_beyond_wikidata": 0, "useful_by": "",
                    "unique_values": 0, "shared_values": 0, "unique_share": None, "languages": 0, "language_list": "", "vocabularies": 0, "needed_llm_extraction": False, "unmapped_predicates": 0, "page_text_only": False})
    cmp = comparison.get(prop, [])
    st = Counter(c["status"] for c in cmp)
    out.update({
        "wd_match": st["match"], "wd_partial": st["partial"], "wd_mismatch": st["mismatch"], "wd_site_only": st["site_only"] + st["no_overlap"],
        "wd_present_only": st["present"], "values_not_in_wikidata": sum(int(c["site_unmatched_count"] or 0) for c in cmp),
    })
    return out


# ---------- report ----------

def pct(n, d):
    return f"{n} ({100 * n / d:.0f}%)" if d else "0"


def md_table(rows, cols, headers=None):
    headers = headers or cols
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "") if r.get(c) is not None else "") for c in cols) + " |")
    return "\n".join(lines)


def write_report(path, qid, recs, sites, probe):
    n_rec, n_site = len(recs), len(sites)
    L = [f"# Source quality report - {qid}", "",
         f"{n_rec} pages crawled for {n_site} identifier properties (sites). Counts below are per **site** unless they say pages; "
         "a site counts as having a property if any of its pages did.", ""]

    # 1 resolution
    L += ["## 1. Did the page resolve?", ""]
    st = Counter(r["status"] for r in recs)
    L.append(md_table([{"status": k, "pages": n, "share": f"{100 * n / n_rec:.0f}%"} for k, n in st.most_common()], ["status", "pages", "share"]))
    L += ["", "Status meanings: `ok` rendered normally; `login_wall_suspected` the page has a password box (the record itself may still be public); "
          "`http_error` 4xx/5xx; `load_failed` the browser never got a usable page (DNS, connection reset, site down); `blocked` an explicit refusal page; "
          "`wrong_page` the browser rendered a page, but not the entity's record (a Wayback calendar, a redirector that never forwarded, "
          "a challenge page the crawler did not recognise, or a page that never mentions the entity and yielded no data about them).", ""]
    wrong = [s for s in sites if s["wrong_page_reason"]]
    if wrong:
        L += [f"Wrong-page sites ({len(wrong)}):", ""]
        L.append(md_table(sorted(wrong, key=lambda s: s["wrong_page_reason"]), ["property", "label", "wrong_page_reason"], ["prop", "site", "why"]))
        L.append("")
    overridden = [r for r in recs if r.get("url_override_reason")]
    if overridden:
        L += [f"- pages crawled at an overridden URL (`url_overrides.json`): {len(overridden)} ({', '.join(sorted({r['property'] for r in overridden}))})"]
    resolved = [s for s in sites if s["resolved"]]
    timed = [r for r in recs if r["load_timed_out"]]
    L += [f"- sites with at least one page rendering normally: **{pct(len(resolved), n_site)}**",
          f"- pages that hit the 45 s load timeout: {pct(len(timed), n_rec)}" + (f" ({', '.join(sorted({r['host'] for r in timed}))})" if timed else ""),
          f"- pages redirected to another host: {pct(sum(1 for r in recs if r['redirected']), n_rec)}",
          f"- pages served over https: {pct(sum(1 for r in recs if r['https']), n_rec)}",
          f"- median load time: {sorted((r['load_seconds'] or 0) for r in recs)[n_rec // 2]:.1f} s; "
          f"slowest 5: " + ", ".join(f"{r['host']} {r['load_seconds']:.0f}s" for r in sorted(recs, key=lambda r: -(r['load_seconds'] or 0))[:5]),
          ""]
    by_host_fail = Counter(r["host"] for r in recs if r["status"] in ("load_failed", "http_error", "blocked"))
    if by_host_fail:
        L += ["Failures by host: " + ", ".join(f"{h} ×{n}" for h, n in by_host_fail.most_common(10)), ""]

    # 2 walls
    L += ["## 2. Walls: challenges, logins, consent", ""]
    L += [f"- sites that loaded a human-verification widget (reCAPTCHA, hCaptcha, Turnstile, Incapsula...): {pct(sum(1 for s in sites if s['challenge_widget']), n_site)}",
          f"- sites where the crawl actually paused for a human: {pct(sum(1 for s in sites if s['challenge_paused']), n_site)}",
          f"- sites with a password box on the page: {pct(sum(1 for s in sites if s['login_box']), n_site)}",
          f"- sites with a cookie-consent manager: {pct(sum(1 for s in sites if s['consent_manager']), n_site)}",
          f"- pages with access wording (subscribe, members, log in...): {pct(sum(1 for r in recs if r['access_words']), n_rec)}",
          f"- pages with not-found wording: {pct(sum(1 for r in recs if r['not_found_words']), n_rec)}", ""]

    # 3 ads
    L += ["## 3. Advertising and tracking", ""]
    ads = Counter(s["ads"] for s in sites)
    L.append(md_table([{"ads": k, "sites": n, "share": f"{100 * n / n_site:.0f}%"} for k, n in ads.most_common()], ["ads", "sites", "share"]))
    L += ["", "\"ads served\" = the rendered page requested at least one ad-network host (DoubleClick, Google Ad Manager, PubMatic, Criteo, Rubicon, Amazon ads, prebid partners...). "
          "Analytics (Google Analytics, Tag Manager, Clarity, New Relic...) are counted separately.", ""]
    L += [f"- sites with analytics/tracking scripts: {pct(sum(1 for s in sites if s['analytics_hosts']), n_site)}",
          f"- sites with social widgets/pixels: {pct(sum(1 for s in sites if s['social_hosts']), n_site)}",
          f"- sites with **no** third-party hosts at all: {pct(sum(1 for s in sites if s['third_party_hosts'] == 0), n_site)}",
          f"- sites with 20+ third-party hosts: {pct(sum(1 for s in sites if s['third_party_hosts'] >= 20), n_site)}", ""]
    ad_sites = sorted((s for s in sites if s["ads"] == "ads served"), key=lambda s: -s["ad_hosts"])
    if ad_sites:
        L += ["Sites serving ads (ad hosts contacted):", ""]
        L.append(md_table(ad_sites, ["property", "label", "ad_hosts", "third_party_hosts", "analytics_hosts"]))
        L.append("")
    adtop = Counter()
    for r in recs:
        for h in r["ad_host_list"].split("; "):
            if h:
                adtop[h] += 1
    if adtop:
        L += ["Most common ad hosts: " + ", ".join(f"{h} ({n})" for h, n in adtop.most_common(12)), ""]

    # 4 page weight
    L += ["## 4. Page weight", ""]
    def dist(key, unit=1, fmt="{:.0f}"):
        vals = sorted(r[key] / unit for r in recs if r["status"] == "ok")
        return f"median {fmt.format(vals[len(vals) // 2])}, 90th pct {fmt.format(vals[int(len(vals) * 0.9)])}, max {fmt.format(vals[-1])}"
    L += [f"- rendered HTML: {dist('html_bytes', 1024)} KB", f"- visible text: {dist('text_chars')} characters", f"- resources loaded: {dist('resources')}",
          f"- scripts: {dist('scripts')}", f"- third-party hosts: {dist('third_party_hosts')}",
          f"- pages with under 500 characters of visible text (thin or empty): {pct(sum(1 for r in recs if r['status'] == 'ok' and r['text_chars'] < 500), n_rec)}", ""]

    # 5 machine-readable data
    L += ["## 5. Machine-readable data", ""]
    with_data = [s for s in sites if s["has_entity_data"]]
    with_any_rep = [s for s in sites if s["rep_saved"] > 0]
    L += [f"- sites where at least one structured file was retrieved (any content, including page plumbing like consent configs): {pct(len(with_any_rep), n_site)}",
          f"- sites whose files contained **data about the entity** (profiled in step 6): **{pct(len(with_data), n_site)}**",
          f"- sites whose entity data came as RDF (JSON-LD, RDF/XML, Turtle, N-Triples, RDFa): {pct(sum(1 for s in sites if s['rdf']), n_site)}",
          f"- sites with a library format (MARC, MADS, EAC-CPF): {pct(sum(1 for s in sites if s['library_format']), n_site)}", ""]
    L += ["### Serialisations (sites offering each, any route)", ""]
    fmt_sites, fmt_entity = Counter(), Counter()
    for s in sites:
        for col in ("formats_http", "formats_browser_only", "formats_embedded"):
            for f in s[col].split(", "):
                if f:
                    fmt_sites[f] += 1
        for f in s["entity_formats"].split(", "):
            if f:
                fmt_entity[f] += 1
    L.append(md_table([{"format": f, "sites": n, "share": f"{100 * n / n_site:.0f}%", "entity": fmt_entity[f], "entity_share": f"{100 * fmt_entity[f] / n_site:.0f}%"} for f, n in fmt_sites.most_common()],
                      ["format", "sites", "share", "entity", "entity_share"], ["format", "sites retrieved", "share", "carried entity data", "share"]))
    L += ["", "\"retrieved\" counts any file of that format, including page plumbing (cookie-consent configs, xhtml-vocab RDFa, OpenGraph cards); "
          "\"carried entity data\" counts only files the step-6 profile actually took values about the person from. "
          "`json` and `xml` are ad-hoc API payloads; `opengraph` is page metadata only (title/description/image).", ""]
    L += ["### How the data was reachable", ""]
    mech, mech_entity = Counter(), Counter()
    for s in sites:
        for m in s["mechanisms"].split("; "):
            if m:
                mech[m] += 1
        for m in s["entity_mechanisms"].split("; "):
            if m:
                mech_entity[m] += 1
    L.append(md_table([{"mechanism": m, "sites": n, "share": f"{100 * n / n_site:.0f}%", "entity": mech_entity[m], "entity_share": f"{100 * mech_entity[m] / n_site:.0f}%"} for m, n in mech.most_common()],
                      ["mechanism", "sites", "share", "entity", "entity_share"], ["mechanism", "sites retrieved", "share", "carried entity data", "share"]))
    L += [""]
    acc = Counter(s["entity_data_access"] for s in sites)
    L += ["### Programmatic access to the entity data", "",
          "Based on which files the step-6 profile actually took values from. `plain HTTP` = a Python client gets everything (including markup that the probe found in the "
          "server-sent HTML); `browser` = the data only came back from fetches run inside the logged-in, bot-cleared browser session or replayed in-page API calls; "
          "`js-rendered page` = the only data is markup that appears after JavaScript runs; `rendered page (unprobed)` = embedded markup not re-checked with Python.", ""]
    L.append(md_table([{"access": k, "sites": n, "share": f"{100 * n / n_site:.0f}%", "data_share": f"{100 * n / len(with_data):.0f}%" if k != "none" else ""} for k, n in acc.most_common()],
                      ["access", "sites", "share", "data_share"], ["access", "sites", "share of all sites", "share of data sites"]))
    L.append("")
    if probe:
        probed = [r for r in recs if r["key"] in probe]
        in_server = [r for r in probed if r["embedded_in_server_html"]]
        js_only = [r for r in probed if r["embedded_js_only"] and not r["embedded_in_server_html"]]
        blocked = [r for r in probed if r["probe_blocked"]]
        L += ["### Embedded markup: present for a plain HTTP client?", "",
              f"{len(probed)} pages with embedded data were re-fetched with Python (no JavaScript, a plain research User-Agent): "
              f"{len(in_server)} had the same markup in the server HTML, {len(js_only)} only had it after JavaScript ran, "
              f"{len(blocked)} refused the plain request.", ""]
        if js_only:
            L += ["JavaScript-only embedded data: " + ", ".join(f"{r['property']} {r['host']} ({r['embedded_js_only']})" for r in js_only), ""]
        if blocked:
            L += ["Refused the Python request (status): " + ", ".join(f"{r['property']} {r['host']} ({r['probe_status']})" for r in blocked), ""]
    browser_only_sites = [s for s in sites if s["formats_browser_only"]]
    if browser_only_sites:
        L += [f"Sites where some format was only retrievable in the browser ({len(browser_only_sites)}): " +
              ", ".join(f"{s['property']} {s['label']} ({s['formats_browser_only']})" for s in browser_only_sites), ""]
    llm_sites = [s for s in sites if s["needed_llm_extraction"]]
    L += [f"- sites whose data was ad-hoc JSON/XML that needed an LLM (Opus) to map onto the schema: {pct(len(llm_sites), n_site)}", ""]

    # 6 richness
    L += ["## 6. Richness, languages and vocabularies", ""]
    def q(key, subset):
        vals = sorted(s[key] for s in subset if s[key] is not None)
        return f"median {vals[len(vals) // 2]}, max {vals[-1]}" if vals else "-"
    L += [f"- schema elements filled per data site: {q('elements', with_data)}", f"- values per data site: {q('values', with_data)}",
          f"- languages tagged per data site: {q('languages', with_data)}; sites with values in 5+ languages: {sum(1 for s in with_data if s['languages'] >= 5)}",
          f"- sites publishing with a standard vocabulary (schema.org, SKOS, FOAF, RDA, MADS, BIBFRAME...): {pct(sum(1 for s in with_data if s['vocabularies']), len(with_data))} of data sites", ""]
    L += ["Richest sites (by distinct values about the entity):", ""]
    L.append(md_table(sorted(with_data, key=lambda s: -s["values"])[:15], ["property", "label", "elements", "values", "languages", "formats_used", "entity_data_access"]))
    L.append("")

    # 7 unique vs repeated
    L += ["## 7. Unique versus repeated information", "",
          "For every descriptive value (names, dates, places, gender, occupations, nationality, language, descriptions, works, related people) we count on how many sites "
          "the same normalised value appears. A value found on only one site is *unique* to that site; record plumbing (identifiers, timestamps, licences) is excluded.", ""]
    tot_desc = sum(s["descriptive_values"] for s in with_data)
    tot_unique = sum(s["unique_values"] for s in with_data)
    L += [f"- descriptive values across all data sites: {tot_desc}; unique to one site: {pct(tot_unique, tot_desc)}; repeated elsewhere: {pct(tot_desc - tot_unique, tot_desc)}",
          f"- sites contributing nothing that another site does not also have: {pct(sum(1 for s in with_data if s['descriptive_values'] and s['unique_values'] == 0), len(with_data))} of data sites",
          f"- sites where more than half of their descriptive values are unique: {sum(1 for s in with_data if (s['unique_share'] or 0) > 0.5)}", ""]
    L += ["Most unique sites (≥10 descriptive values):", ""]
    L.append(md_table(sorted((s for s in with_data if s["descriptive_values"] >= 10), key=lambda s: -(s["unique_share"] or 0))[:15],
                      ["property", "label", "descriptive_values", "unique_values", "unique_share", "values_not_in_wikidata"]))
    L += ["", "Most redundant sites (≥10 descriptive values, lowest unique share):", ""]
    L.append(md_table(sorted((s for s in with_data if s["descriptive_values"] >= 10), key=lambda s: (s["unique_share"] or 0))[:10],
                      ["property", "label", "descriptive_values", "unique_values", "unique_share", "wd_match"]))
    L.append("")

    # 8 vs wikidata
    L += ["## 8. Against Wikidata", ""]
    L += [f"- data sites with at least one element matching Wikidata exactly: {pct(sum(1 for s in with_data if s['wd_match']), len(with_data))}",
          f"- data sites with a mismatch on some element: {pct(sum(1 for s in with_data if s['wd_mismatch']), len(with_data))}",
          f"- data sites offering values Wikidata does not have (after normalisation, before curation): {pct(sum(1 for s in with_data if s['values_not_in_wikidata']), len(with_data))}",
          "- see `beyond_wikidata.md` for the curated list of what those values are, and `review.md` for the judged disagreements", ""]

    if any(s.get("p244_rank") for s in sites):
        L += ["## 8b. Quality by popularity", "", "Sites bucketed by how many bibliographic entities (items with P244) carry their identifier.", ""]
        buckets = [("top 50", lambda s: s["p244_rank"] <= 50), ("51-150", lambda s: 50 < s["p244_rank"] <= 150), ("151-300", lambda s: 150 < s["p244_rank"] <= 300), ("301+", lambda s: s["p244_rank"] > 300)]
        brows = []
        for name, test in buckets:
            grp = [s for s in sites if s.get("p244_rank") and test(s)]
            if not grp:
                continue
            n = len(grp)
            brows.append({"bucket": name, "sites": n, "resolved": pct(sum(1 for s in grp if s["resolved"]), n), "entity_data": pct(sum(1 for s in grp if s["has_entity_data"]), n),
                          "plain_http": pct(sum(1 for s in grp if s["entity_data_access"] == "plain HTTP"), n), "rdf": pct(sum(1 for s in grp if s["rdf"]), n),
                          "ads": pct(sum(1 for s in grp if s["ads"] == "ads served"), n), "consent": pct(sum(1 for s in grp if s["consent_manager"]), n),
                          "median_values": sorted(s["values"] for s in grp)[n // 2]})
        L.append(md_table(brows, ["bucket", "sites", "resolved", "entity_data", "plain_http", "rdf", "ads", "consent", "median_values"],
                          ["popularity", "sites", "resolved", "entity data", "all via plain HTTP", "RDF", "ads", "consent banner", "median values"]))
        L.append("")

    # 9 per-site table
    L += ["## 9. Per-site table", "", "`rank` / `% of P244 items` = how common this identifier is on bibliographic entities (items with a Library of Congress ID), "
          "from `data/landscape/landscape.md`. Sorted by property number. Full detail (one row per page, all ad/analytics hosts) is in `quality_records.csv`; this table is `quality_sites.csv`.", ""]
    cols = ["property", "label", "p244_rank", "p244_share", "pages", "status", "load_seconds", "challenge_widget", "login_box", "consent_manager", "ads", "analytics_hosts", "third_party_hosts",
            "html_kb", "rep_saved", "formats_http", "formats_browser_only", "formats_embedded", "entity_data_access", "elements", "values", "languages", "unique_share", "wd_match", "wd_mismatch", "values_not_in_wikidata"]
    hdr = ["prop", "site", "rank", "% of P244 items", "pages", "status", "load s", "challenge", "login box", "consent", "ads", "analytics", "3rd-party", "HTML KB", "files", "formats (python)",
           "browser only", "embedded", "entity data access", "elements", "values", "langs", "unique", "=WD", "≠WD", "not in WD"]
    L.append(md_table(sorted(sites, key=lambda s: int(s["property"][1:])), cols, hdr))
    L.append("")
    path.write_text("\n".join(L))


def main():
    global DATA_DIR
    ap = argparse.ArgumentParser()
    ap.add_argument("qid", nargs="?", default="Q7245")
    ap.add_argument("--probe-embedded", action="store_true", help="re-fetch pages with embedded data in plain Python to see if the markup is server-side")
    args = ap.parse_args()
    DATA_DIR = Path("data") / args.qid
    an = DATA_DIR / "analysis"

    records = load_records(DATA_DIR, entity_name_tokens(json.loads((DATA_DIR / "entity.json").read_text())))
    manifests = load_manifests(DATA_DIR)
    profiles = load_profiles(DATA_DIR)
    probe_path = an / "embedded_probe.json"
    probe = probe_embedded(DATA_DIR, records, manifests) if args.probe_embedded else (json.loads(probe_path.read_text()) if probe_path.exists() else {})
    comparison = defaultdict(list)
    cmp_path = an / "comparison.csv"
    if cmp_path.exists():
        for row in csv.DictReader(cmp_path.open()):
            comparison[row["property"]].append(row)

    # how many sources carry each descriptive value: every site's distinct keys, plus Wikidata as one more source
    # (a value only one site states but Wikidata already holds is not unique information)
    value_sites = Counter()
    for prop, p in profiles.items():
        seen = {uniq_key(el, v["value"]) for el, vals in p["elements"].items() if el in DESCRIPTIVE for v in vals}
        for k in seen:
            value_sites[k] += 1
    wd_path = an / "wikidata_elements.json"
    if wd_path.exists():
        seen = set()
        for el, vals in json.loads(wd_path.read_text()).items():
            if el in DESCRIPTIVE:
                for v in vals:
                    seen.add(uniq_key(el, v["value"]))
                    seen.update(uniq_key(el, x) for x in (v.get("labels") or {}).values())
                    seen.update(uniq_key(el, x) for x in v.get("aliases") or [])
                    seen.update(uniq_key(el, x) for x in v.get("demonyms") or [])
                    seen.update(uniq_key(el, x) for x in v.get("broader") or [])   # Missouri, Connecticut, United States for his village and town
                    if el in ("birth_date", "death_date"):
                        WD_DATE_KEYS.add(uniq_key(el, v["value"])[1])
        for k in seen:
            value_sites[k] += 1
        WD_KEYS.update(seen)

    # files the profiles took entity values from, as "<key>/<name>" (element rows carry bare file names,
    # the profile's file list carries them keyed by page)
    entity_files = set()
    for p in profiles.values():
        bare = {v["file"].split("/")[-1] for el, vals in p["elements"].items() if el in DESCRIPTIVE for v in vals if v.get("file") and not (v.get("via") or "").startswith("llm")}
        entity_files.update(f["file"] for f in p["files"] if f["file"].split("/")[-1] in bare)
    rec_rows = [record_metrics(r, manifests.get(r["key"]), probe, entity_files) for r in records]
    # popularity of each identifier on bibliographic entities, if identifier_landscape.py has run
    landscape = {}
    lpath = Path("data") / "landscape" / "counts.csv"
    if lpath.exists():
        landscape = {row["property"]: row for row in csv.DictReader(lpath.open())}
    by_prop = defaultdict(list)
    for r in rec_rows:
        by_prop[r["property"]].append(r)
    site_rows = [site_metrics(prop, recs, profiles, comparison, value_sites) for prop, recs in by_prop.items()]
    for s in site_rows:
        lrow = landscape.get(s["property"])
        s["p244_rank"] = int(lrow["rank"]) if lrow else None
        s["p244_share"] = float(lrow["share"]) if lrow else None

    for name, rows in (("quality_records.csv", rec_rows), ("quality_sites.csv", site_rows)):
        with (an / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    write_report(an / "quality.md", args.qid, rec_rows, site_rows, probe)
    print(f"{len(rec_rows)} pages, {len(site_rows)} sites -> {an / 'quality.md'}, quality_sites.csv, quality_records.csv")
    print(f"resolved sites: {sum(1 for s in site_rows if s['resolved'])}; with entity data: {sum(1 for s in site_rows if s['has_entity_data'])}; "
          f"ads served: {sum(1 for s in site_rows if s['ads'] == 'ads served')}; access: {dict(Counter(s['entity_data_access'] for s in site_rows))}")


if __name__ == "__main__":
    main()
