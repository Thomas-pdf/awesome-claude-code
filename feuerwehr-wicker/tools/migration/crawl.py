import re, os, sys, time, json, html, hashlib
import requests
from concurrent.futures import ThreadPoolExecutor
OUT = sys.argv[1]
B = "https://www.feuerwehr-wicker.de"
S = requests.Session(); S.headers["User-Agent"] = "FF-Wicker-Migration/1.0 (Website-Relaunch)"
os.makedirs(f"{OUT}/raw", exist_ok=True)
def get(url, fn, data=None):
    p = f"{OUT}/raw/{fn}"
    if os.path.exists(p): return open(p, encoding="utf-8", errors="replace").read()
    for i in range(4):
        try:
            r = S.post(url, data=data, timeout=40) if data else S.get(url, timeout=40)
            r.encoding = "utf-8"
            t = r.text
            open(p, "w", encoding="utf-8").write(t); time.sleep(0.15); return t
        except Exception as e:
            time.sleep(2 ** i)
    return ""
# 1) pages: discover via sitemap + BFS on page= links
sm = open(f"{OUT}/sitemap.html", encoding="utf-8", errors="replace").read()
ids = set(int(x) for x in re.findall(r"page=(\d+)", sm))
done = set(); meta = {}
skip = {5}
def page(n):
    idx = get(f"{B}/index_main.php?page={n}", f"idx_{n}.html")
    fr = [u for u in re.findall(r'frame src="([^"]+)"', idx) if "menu.php" not in u and "line_black" not in u]
    src = fr[0] if fr else f"{B}/main.php?page={n}"
    src = src.replace("fbc=", "&fbc=") if "&fbc" not in src and "fbc=" in src else src
    body = get(src, f"page_{n}.html") if n not in skip else ""
    return n, src, body
while True:
    todo = sorted(ids - done - skip)
    if not todo: break
    with ThreadPoolExecutor(4) as ex:
        for n, src, body in ex.map(page, todo):
            done.add(n); meta[n] = src
            for x in re.findall(r"index_main\.php\?page=(\d+)", body): ids.add(int(x))
            for x in re.findall(r"main\.php\?page=(\d+)", body): ids.add(int(x))
    print("pages", len(done), flush=True)
json.dump(meta, open(f"{OUT}/pages.json", "w"), indent=1)
# 2) Einsätze
for y in range(2000, 2027):
    get(f"{B}/einsaetze.php", f"einsaetze_{y}.html", data={"jahr": str(y), "page": "15"})
enrs = set()
for y in range(2000, 2027):
    t = open(f"{OUT}/raw/einsaetze_{y}.html", encoding="utf-8").read()
    enrs |= set(int(x) for x in re.findall(r"enr=(\d+)", t))
print("einsaetze", len(enrs), max(enrs), flush=True)
with ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda n: get(f"{B}/einsaetze.php?page=15&action=showone&enr={n}", f"einsatz_{n}.html"), sorted(enrs)))
# 3) Termine
get(f"{B}/termine.php?page=22&action=showlist", "termine_list.html")
days = set()
for y in range(2014, 2027):
    for m in range(1, 13):
        t = get(f"{B}/termine.php?page=22&monat={m}&jahr={y}", f"termine_{y}_{m}.html")
        days |= set(re.findall(r"_day=(\d{4}-\d{1,2}-\d{1,2})", t))
print("termin-tage", len(days), flush=True)
with ThreadPoolExecutor(4) as ex:
    list(ex.map(lambda d: get(f"{B}/termine.php?page=22&action=showday&_day={d}", f"tag_{d}.html"), sorted(days)))
print("DONE", flush=True)
