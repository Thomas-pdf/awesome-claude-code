"""Lädt alle Bilder/Downloads der alten Seite und speichert sie optimiert (WebP, max. 1600px).
Aufruf: python3 -I images.py <datadir> <public-dir>"""
import json, os, sys, io, time, requests
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageOps
DATA, PUB = sys.argv[1], sys.argv[2]
S = requests.Session(); S.headers["User-Agent"] = "FF-Wicker-Migration/1.0 (Website-Relaunch)"
imgs = json.load(open(f"{DATA}/images.json")); dls = json.load(open(f"{DATA}/downloads.json"))
fails = []
def fetch(url):
    for i in range(4):
        try:
            r = S.get(url, timeout=60)
            if r.status_code == 200 and r.content: return r.content
            if r.status_code == 404: return None
        except Exception: pass
        time.sleep(2 ** i)
    return None
def img(item):
    url, rel = item
    out = PUB + rel
    if os.path.exists(out): return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    b = fetch(url)
    if not b: fails.append(url); return
    try:
        im = Image.open(io.BytesIO(b))
        if rel.endswith(".gif"):
            open(out, "wb").write(b); return
        im = ImageOps.exif_transpose(im)
        im = im.convert("RGBA") if im.mode in ("P", "LA", "RGBA") else im.convert("RGB")
        if im.width > 1600: im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        im.save(out, "WEBP", quality=74, method=5)
    except Exception as e:
        fails.append(url)
def dl(item):
    url, rel = item
    out = PUB + rel
    if os.path.exists(out): return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    b = fetch(url)
    if b and not b[:15].lower().startswith((b"<html", b"<!doctype")): open(out, "wb").write(b)
    else: fails.append(url)
with ThreadPoolExecutor(6) as ex:
    list(ex.map(img, imgs.items()))
    list(ex.map(dl, dls.items()))
json.dump(fails, open(f"{DATA}/fails.json", "w"), indent=0)
print("fertig, fehlgeschlagen:", len(fails))
