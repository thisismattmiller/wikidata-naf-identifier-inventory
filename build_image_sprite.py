"""Step 9b: download every image the sites state for the entity, crop each to a small square and tile them into one sprite sheet.

    uv run python build_image_sprite.py Q7245 [--tile 50] [--cols 12] [--refetch] [--browser]

--browser: URLs that refuse plain clients (403 CDNs, TLS oddities) are fetched once more inside the crawler's Chrome window
(navigate to the image, fetch it from its own origin with the session's cookies), as step 5 does for data files.

Reads analysis/profiles/P*.json (element `image`) and analysis/wikidata_elements.json (Wikidata's own images),
caches the originals under analysis/images/raw/, and writes
    analysis/images/images.json   manifest: one row per distinct URL (sites that state it, fetch status, size, sprite index)
    analysis/twain_images.jpg     the sprite (tile x tile squares, `cols` per row) - copied to docs/ next to the static atlas
build_map_data.py folds the manifest into the atlas's "Images" block.
"""
import base64
import hashlib
import io
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import truststore
from PIL import Image, ImageOps

UA = "wikidata-identifier-inventory/0.1 (research crawl; thisismattmiller@gmail.com)"
BROWSER_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
IMG_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/gif": "gif", "image/webp": "webp", "image/avif": "avif", "image/bmp": "bmp", "image/tiff": "tif", "image/svg+xml": "svg"}


def collect(an):
    """Distinct image URLs with the properties that state them; Wikidata's P18 files become Commons FilePath URLs."""
    urls = {}
    for f in sorted((an / "profiles").glob("P*.json")):
        prof = json.loads(f.read_text())
        for x in prof.get("elements", {}).get("image") or []:
            for v in re.split(r",\s*(?=https?://)", str(x["value"]).strip()):   # some sites pack several URLs in one value
                v = v.strip()
                if not re.match(r"https?://\S+\.\S+", v) or v.rstrip("/").count("/") < 3:
                    continue   # a bare host or a non-URL
                urls.setdefault(v, {"url": v, "p": [], "wd": False})
                if prof["property"] not in urls[v]["p"]:
                    urls[v]["p"].append(prof["property"])
    wd = json.loads((an / "wikidata_elements.json").read_text()).get("image", [])
    for x in wd:
        v = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(x["value"].replace(" ", "_"))
        urls.setdefault(v, {"url": v, "p": [], "wd": False})["wd"] = True
    return list(urls.values())


def fetch(url, raw_dir, refetch=False):
    key = hashlib.sha1(url.encode()).hexdigest()[:16]
    meta_path = raw_dir / f"{key}.json"
    if meta_path.exists() and not refetch:
        meta = json.loads(meta_path.read_text())
        if meta.get("ok") or meta.get("attempts", 1) >= 2:
            return meta
    meta = {"key": key, "url": url, "ok": False}
    fetch_url = re.sub(r"^https?://commons\.wikimedia\.org/wiki/File:", "https://commons.wikimedia.org/wiki/Special:FilePath/", url)
    # first as the project's own client, then once more looking like a browser (several image CDNs 403 anything else) with the OS trust store
    attempts = [(UA, ssl.create_default_context()), (BROWSER_UA, truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT))]
    for n, (ua, ctx) in enumerate(attempts, 1):
        meta["attempts"] = n
        try:
            req = urllib.request.Request(fetch_url, headers={"User-Agent": ua, "Accept": "image/avif,image/webp,image/*,*/*;q=0.8", "Referer": "https://" + urllib.parse.urlsplit(fetch_url).netloc + "/", "Accept-Language": "en-US,en;q=0.8"})
            with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
                _read(r, meta, raw_dir, key)
        except Exception as e:  # noqa: BLE001 - any failure is a row in the manifest
            meta["error"] = re.sub(r"\s+", " ", str(e))[:160]
        if meta["ok"]:
            meta["via"] = "browser-like client" if n == 2 else "plain client"
            break
    meta_path.write_text(json.dumps(meta))
    return meta


def browser_fetch(window, meta, raw_dir):
    """One in-page fetch of the image from its own origin in the crawler's Chrome window."""
    from browser_fetch import run_fetch
    url, key = meta["url"], meta["key"]
    try:
        tab_url, tab_title, data = run_fetch(window, url, [{"id": key, "url": url, "accept": "image/avif,image/webp,image/*"}])
    except Exception as e:  # noqa: BLE001
        meta["error"] = f"browser: {e}"[:160]
        return meta
    res = (data.get("results") or [{}])[0]
    ctype = (res.get("content_type") or "").split(";")[0].strip().lower()
    meta.update({"status": res.get("status"), "content_type": ctype, "bytes": res.get("bytes"), "final_url": res.get("final_url"), "attempts": 3})
    if res.get("body_b64") and ctype.startswith("image/"):
        ext = IMG_EXT.get(ctype, "bin")
        (raw_dir / f"{key}.{ext}").write_bytes(base64.b64decode(res["body_b64"]))
        meta.update({"file": f"{key}.{ext}", "ok": True, "via": "browser"})
        meta.pop("error", None)
    else:
        meta["error"] = ("browser: " + (res.get("error") or data.get("error") or f"{res.get('status')} {ctype or 'no image body'}"))[:160]
    (raw_dir / f"{key}.json").write_text(json.dumps(meta))
    return meta


def _read(r, meta, raw_dir, key):
    """Store the response body if it is an image; otherwise note why not."""
    ctype = (r.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    data = r.read(12_000_000)
    meta.update({"status": r.status, "content_type": ctype, "bytes": len(data), "final_url": r.geturl()})
    if not ctype.startswith("image/"):
        meta["error"] = f"not an image ({ctype or 'no content type'})"
        return
    ext = IMG_EXT.get(ctype, "bin")
    (raw_dir / f"{key}.{ext}").write_bytes(data)
    meta["file"] = f"{key}.{ext}"
    meta["ok"] = True
    meta.pop("error", None)


def main():
    args = sys.argv[1:]
    qid = next((a for a in args if a.startswith("Q")), "Q7245")
    tile = int(args[args.index("--tile") + 1]) if "--tile" in args else 50
    cols = int(args[args.index("--cols") + 1]) if "--cols" in args else 12
    refetch = "--refetch" in args
    window = None
    if "--browser" in args:
        from crawl import ChromeWindow
        window = ChromeWindow()
    an = Path("data") / qid / "analysis"
    img_dir = an / "images"
    raw_dir = img_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = collect(an)
    print(f"{len(rows)} distinct image URLs from the profiles and Wikidata", flush=True)
    tiles = []
    for i, row in enumerate(rows):
        meta = fetch(row["url"], raw_dir, refetch)
        if window and not meta.get("ok") and "not an image" not in (meta.get("error") or "") and meta.get("via") != "browser" and not (meta.get("error") or "").startswith("browser:"):
            meta = browser_fetch(window, meta, raw_dir)
        row.update({k: meta.get(k) for k in ("ok", "status", "content_type", "bytes", "error", "file", "final_url", "via")})
        if row["ok"]:
            try:
                with Image.open(raw_dir / row["file"]) as im:
                    row["w"], row["h"] = im.size
                    im = ImageOps.exif_transpose(im)
                    if im.mode in ("RGBA", "LA", "P"):
                        bg = Image.new("RGB", im.size, (255, 255, 255))
                        bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
                        im = bg
                    im = ImageOps.fit(im.convert("RGB"), (tile, tile), method=Image.LANCZOS, centering=(0.5, 0.35))
                    row["sprite"] = len(tiles)
                    tiles.append(im)
            except Exception as e:  # noqa: BLE001
                row["ok"] = False
                row["error"] = f"decode failed: {e}"[:160]
        print(f"  [{i + 1}/{len(rows)}] {'ok ' if row['ok'] else 'ERR'} {row['url'][:90]}  {row.get('error') or f'{row.get('w')}x{row.get('h')} {row.get('content_type')}'}", flush=True)
        time.sleep(0.2)
    rows_n = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile, max(1, rows_n) * tile), (255, 255, 255))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * tile, (i // cols) * tile))
    sprite_name = "twain_images.jpg"
    sheet.save(an / sprite_name, "JPEG", quality=86, optimize=True)
    docs = Path("docs")
    if docs.exists():
        sheet.save(docs / sprite_name, "JPEG", quality=86, optimize=True)
    manifest = {"sprite": sprite_name, "tile": tile, "cols": cols, "count": len(tiles), "fetched": time.strftime("%Y-%m-%d"), "images": rows}
    (img_dir / "images.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    print(f"{len(tiles)} tiles in {sprite_name} ({(an / sprite_name).stat().st_size // 1024} KB); {sum(1 for r in rows if not r['ok'])} URLs failed; manifest at {img_dir / 'images.json'}")


if __name__ == "__main__":
    main()
