import sys, re, json
from bs4 import BeautifulSoup
s = BeautifulSoup(open(sys.argv[1], encoding="utf-8", errors="replace").read(), "lxml")
items = []; stack = []
for a in s.find_all("a", href=re.compile(r"page=\d+")):
    d = len(a.find_parents("table"))
    n = int(re.search(r"page=(\d+)", a["href"]).group(1))
    items.append((d, n, a.get_text(strip=True)))
base = min(d for d, _, _ in items)
out = []; st = []
for d, n, t in items:
    lvl = (d - base) // 2
    while len(st) > lvl: st.pop()
    parent = st[-1] if st else None
    out.append({"id": n, "title": t, "level": lvl, "parent": parent})
    st.append(n)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=0)
for o in out: print("  " * o["level"] + f'{o["id"]} {o["title"]}')
