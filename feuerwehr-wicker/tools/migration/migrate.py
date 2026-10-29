"""Migration der alten FF-Wicker-Seite (Roh-HTML) in Astro-Content (Markdown).
Aufruf: python3 -I migrate.py <datadir> <siteroot>
"""
import re, sys, os, json, html, unicodedata, datetime
from bs4 import BeautifulSoup, NavigableString
from markdownify import MarkdownConverter

DATA, SITE = sys.argv[1], sys.argv[2]
RAW = f"{DATA}/raw"
B = "https://www.feuerwehr-wicker.de"
CONTENT = f"{SITE}/src/content"
tree = json.load(open(f"{DATA}/tree.json", encoding="utf-8"))
byid = {t["id"]: t for t in tree}
PARENT_FIX = {**{i: 4 for i in (1089, 557, 890, 33, 1017, 1062, 42, 610)}, 769: 42, 792: 42,
              **{i: 610 for i in (16, 413, 164, 41, 414, 165, 166, 619)},
              **{i: 167 for i in (168, 174, 175, 176, 177, 219, 201, 203)},
              **{i: 70 for i in (338, 334, 125, 124, 148, 149)}, 235: 2, 236: 2, 276: 2, 4: 2, 167: 2, 70: 2,
              **{i: 1039 for i in (1042, 1043, 1046, 1009, 1045, 1082)},
              **{i: 1043 for i in (1049, 1050, 1048, 1051, 1054, 1053)},
              **{i: 3 for i in (455, 913, 585, 587)}, **{i: 20 for i in (313, 76, 79, 200, 77)},
              200: 79, 988: 987}
for k, v in PARENT_FIX.items():
    if k in byid: byid[k]["parent"] = v
order = [t["id"] for t in tree]

# --- Struktur-Entscheidungen -------------------------------------------------
SECTIONS = {  # alte Top-Level-ID -> (bereich-key, url-präfix)
    2: ("einsatzabteilung", "/einsatzabteilung"),
    3: ("jugendfeuerwehr", "/jugendfeuerwehr"),
    416: ("minis", "/miniloescher"),
    20: ("verein", "/verein"),
    1039: ("neubau", "/neubau"),
    834: ("verein", "/verein/tag-der-offenen-tuer"),
    987: ("jubilaeum", "/100-jahre"),
    498: ("mitmachen", "/mitmachen"),
    161: ("buergerinfo", "/buergerinfo"),
    23: ("links", "/links"),
    25: ("downloads", "/downloads"),
}
# Reine Container/Listen der alten Seite (werden durch neue Übersichten ersetzt)
CONTAINERS = {244, 179, 1056, 986, 950, 915, 900, 865, 775, 736, 686, 615, 595, 594, 593,
              592, 591, 590, 298, 180, 1040, 134, 137, 136, 421, 665, 668, 667, 666, 73, 80,
              362, 302, 265, 102, 104, 108, 112, 117, 122, 15, 22, 34, 35, 5, 1, 610, 397, 417}
# Statische Info-Seiten (alles andere in den Bereichen = datierter Bericht)
STATIC = {24, 38, 39, 425, 40, 161, 216, 217, 195, 794, 784, 291, 290, 287, 283, 277, 273, 263,
          252, 251, 248, 247, 246, 234, 229, 471, 507, 498, 704, 522, 500, 502, 1039, 1042, 1043,
          1049, 1050, 1048, 1051, 1054, 1053, 1046, 2, 4, 1089, 557, 890, 33, 1017, 1062, 42, 769,
          792, 16, 413, 164, 41, 414, 165, 166, 619, 235, 236, 167, 168, 174, 175, 176, 177, 219,
          201, 203, 70, 338, 334, 125, 124, 148, 149, 276, 3, 455, 913, 585, 587, 416, 20, 313, 76,
          79, 200, 77, 834, 987, 988, 23, 185, 188, 196, 194, 189, 25, 61, 163}
# Feste neue URLs für wichtige Seiten
FIXED = {
    24: "/kontakt", 38: "/kontakt/einsatzabteilung", 39: "/kontakt/jugendfeuerwehr",
    425: "/kontakt/kinderfeuerwehr", 40: "/kontakt/verein",
    161: "/buergerinfo", 216: "/buergerinfo/verhalten-im-notfall", 217: "/buergerinfo/informationen",
    195: "/buergerinfo/brandschutz", 2: "/einsatzabteilung", 4: "/einsatzabteilung/fahrzeuge",
    610: "/einsatzabteilung/fahrzeuge/ehemalige", 167: "/einsatzabteilung/ausbildung",
    70: "/brandschutzerziehung", 3: "/jugendfeuerwehr", 416: "/minilöscher", 20: "/verein",
    79: "/verein/chronik", 313: "/verein/vorstand", 76: "/verein/mitgliedschaft", 77: "/verein/satzung",
    1039: "/neubau", 834: "/verein/tag-der-offenen-tuer", 987: "/100-jahre", 988: "/100-jahre/chronik",
    498: "/mitmachen", 23: "/links", 25: "/downloads", 61: "/downloads/jahresberichte",
    15: "/einsaetze", 22: "/termine", 1: "/", 34: "/sitemap", 35: "/suche", 5: "/intern",
    244: "/aktuelles", 179: "/aktuelles", 73: "/aktuelles?bereich=verein", 421: "/aktuelles?bereich=minis",
}
FIXED[416] = "/minilöscher"
# URL-sichere Variante (Umlaute vermeiden)
for k, v in list(FIXED.items()):
    FIXED[k] = v.replace("ö", "oe")

def slugify(s):
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "seite"

def ancestors(i):
    out = []
    t = byid.get(i)
    while t and t["parent"] is not None:
        out.append(t["parent"]); t = byid.get(t["parent"])
    return out

def section_of(i):
    chain = [i] + ancestors(i)
    for c in chain:
        if c in SECTIONS and c != 1:
            return c
    # Fahrzeuge etc. stehen unter 2
    return None

def read(fn):
    p = f"{RAW}/{fn}"
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else ""

# --- Bilder ------------------------------------------------------------------
IMAGES = {}  # remote url -> lokaler pfad (relativ zu public)
def local_img(src):
    src = html.unescape(src)
    if src.startswith("/"): src = B + src
    if "security_show_epicture.php" in src:
        m = re.search(r"_checkefotoifextern=([^&]+)", src)
        name = "einsatz-" + (m.group(1) if m else str(abs(hash(src))) + ".jpg")
        name = re.sub(r"\.(jpe?g|png|gif|bmp)$", ".webp", name, flags=re.I)
        rel = f"/bilder/einsaetze/{name}"
    elif "/imagebase/" in src:
        name = src.split("/imagebase/")[1].replace("/", "-")
        name = re.sub(r"\.(jpe?g|png|bmp)$", ".webp", name, flags=re.I)
        rel = f"/bilder/archiv/{name}"
    elif "/images/" in src:
        name = src.split("/images/")[1].replace("/", "-")
        rel = f"/bilder/alt/{name}"
    else:
        return src
    IMAGES[src] = rel
    return rel

DOWNLOADS = {}
def local_download(href):
    href = html.unescape(href)
    m = re.search(r"fl=([^&]+)", href)
    name = m.group(1) if m else slugify(href)[:60]
    rel = f"/downloads/dateien/{name}"
    DOWNLOADS[href if href.startswith("http") else B + "/" + href.lstrip("/")] = rel
    return rel

# --- Seiten-URLs vorab bestimmen -----------------------------------------------
def page_title(n):
    s = read(f"page_{n}.html")
    m = re.search(r'class="topic"[^>]*>(.*?)</td>', s, re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else byid.get(n, {}).get("title", f"Seite {n}")

def upd_date(n):
    s = read(f"page_{n}.html")
    m = re.findall(r"upd\. (\d\d)\.(\d\d)\.(\d{4})", s)
    if not m: return None
    d, mo, y = m[-1]
    return f"{y}-{mo}-{d}"

URL = {}; KIND = {}
used = set()
for n in order:
    if n in FIXED:
        URL[n] = FIXED[n]; KIND[n] = "fixed"; continue
for n in order:
    if n in URL: continue
    sec = section_of(n)
    if n in CONTAINERS:
        URL[n] = "/aktuelles"; KIND[n] = "container"; continue
    if n in STATIC or sec in (161, 23, 25):
        base = SECTIONS.get(sec, (None, ""))[1] if sec else ""
        parent = byid[n]["parent"]
        if n in STATIC and parent in URL and KIND.get(parent) != "container" and URL[parent] not in ("/",):
            base = URL[parent]
        base = base.replace("ö", "oe")
        u = f"{base}/{slugify(byid[n]['title'])}"
        while u in used: u += "-2"
        URL[n] = u; used.add(u); KIND[n] = "static"
    else:
        d = upd_date(n) or "2000-01-01"
        u = f"/aktuelles/{d[:4]}/{slugify(byid[n]['title'])}"
        while u in used: u += "-2"
        URL[n] = u; used.add(u); KIND[n] = "bericht"

# Einsatz-URLs
EURL = {}
def einsatz_url(enr):
    return EURL.get(enr, "/einsaetze")

def fix_link(href):
    href = html.unescape(href.strip())
    m = re.search(r"index_main\.php\?page=(\d+)", href) or re.search(r"main\.php\?page=(\d+)", href)
    if m and "feuerwehr-wicker" in href or (m and href.startswith(("index_main", "main", "/"))):
        n = int(m.group(1)); return URL.get(n, "/")
    m = re.search(r"enr=(\d+)", href)
    if m and "einsaetze" in href: return einsatz_url(int(m.group(1)))
    if "termine.php" in href: return "/termine"
    if "secdownload.php" in href or "download.php" in href: return local_download(href)
    if re.search(r"feuerwehr-wicker\.de/?$", href): return "/"
    if "feuerwehr-wicker.de/imagebase" in href: return local_img(href)
    if href.startswith("javascript:popup("):
        m2 = re.search(r"popup\('([^']+)'", href)
        return fix_link(m2.group(1)) if m2 else "#"
    return href

# --- HTML -> Markdown -----------------------------------------------------------
class MD(MarkdownConverter):
    def convert_img(self, el, text, parent_tags=None, **kw):
        src = el.get("src", "")
        if not src or "icon_" in src or "spacer" in src: return ""
        alt = (el.get("alt") or "").replace("[", "").replace("]", "").strip()
        return f"\n\n![{alt}]({local_img(src)})\n\n"
    def convert_a(self, el, text, parent_tags=None, **kw):
        href = el.get("href")
        if not href: return text
        href = fix_link(href)
        t = text.strip()
        if not t: return ""
        if t.startswith("![") or t.startswith("\n"):  # Bild-Link
            return text
        return f"[{t}]({href})"
    def convert_font(self, el, text, parent_tags=None, **kw):
        if (el.get("color") or "").lower() in ("silver", "#c0c0c0", "gray", "grey", "#808080") and text.strip():
            return f"\n\n*{text.strip()}*\n\n"
        return text

def clean_body(soup):
    for t in soup.find_all(["script", "style", "form", "iframe", "noscript"]):
        t.decompose()
    return soup

def convert_html(fragment):
    s = BeautifulSoup(fragment, "lxml")
    clean_body(s)
    for f in s.find_all("font"):
        if f.find_parent("font"): f.unwrap()
    md = MD(heading_style="ATX", bullets="-", newline_style="backslash", strip=["span", "div", "center", "u"]).convert_soup(s)
    md = md.replace("\u00a0", " ")
    md = re.sub(r"^\s*[•·]\s*", "- ", md, flags=re.M)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"(?m)^\s*\\\s*$", "", md)                     # Zeilen nur mit "\\"
    md = re.sub(r"\\\n(?:[ \t]*\\?\n)+", "\n\n", md)            # doppelte Umbrüche = Absatz
    md = re.sub(r"(?m)^(\*\*[^*\n]{3,90}?\*\*)\s*\\$", r"\1", md)
    md = re.sub(r"\\\n(?=\s*(?:- |#|!\[|\n|$))", "\n", md)
    # Fett gesetzte Einzelzeilen -> Zwischenüberschrift
    md = re.sub(r"(?m)^\*\*([^*\n]{3,90}?)\*\*[ \t]*$\n?", r"\n### \1\n\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"(?m)^(#{1,6} .*?)\\$", r"\1", md)
    md = re.sub(r"(?m)\\\n(?=\s*\n)", "\n", md)
    md = re.sub(r"(?m)\\$(?=\Z)", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"\*\*\s*\*\*", "", md)
    md = re.sub(r"(?m)^\*\s*\*$", "", md)
    return md.strip()

def extract_page(n):
    s = read(f"page_{n}.html")
    if not s: return None
    soup = BeautifulSoup(s, "lxml")
    body = soup.body
    if not body: return None
    divs = body.find_all("div", recursive=False)
    # Kopf (Titelbalken) und Fuß (TheTwisters) entfernen
    for d in divs:
        if d.find("td", class_="topic") or "thetwisters" in str(d).lower():
            d.decompose()
    return str(body)

def first_image(md):
    m = re.search(r"!\[[^\]]*\]\(([^)]+)\)", md)
    return m.group(1) if m else None

def subtitle_from(md):
    for line in md.splitlines():
        l = line.strip().strip("*").strip()
        if l and not l.startswith("!") and len(l) > 8:
            return l[:200]
    return ""

def yaml_str(s):
    s = (s or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'

def excerpt(md, n=220):
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[#*_>`|\\-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:n].rsplit(" ", 1)[0] + " …") if len(t) > n else t

BEREICH_DEFAULT = "allgemein"
def bereich_of(n):
    sec = section_of(n)
    if sec is None:
        return BEREICH_DEFAULT
    return SECTIONS[sec][0]

def year_hint(n):
    # Jahres-Container (z.B. "2019") als Fallback für Datum
    for a in ancestors(n):
        t = byid.get(a, {}).get("title", "")
        if re.fullmatch(r"\d{4}", t): return t
    m = re.search(r"(20\d\d|19\d\d)", byid.get(n, {}).get("title", ""))
    return m.group(1) if m else None

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)

def main_pages():
    stats = {"bericht": 0, "static": 0, "fixed": 0, "leer": [], "container": 0}
    nav = []
    for n in order:
        kind = KIND.get(n)
        if kind == "container" or n in (1, 15, 22, 34, 35, 5) or (kind == "fixed" and URL[n].startswith("/aktuelles")):
            stats["container"] += 1; continue
        frag = extract_page(n)
        if frag is None:
            stats["leer"].append(n); continue
        md = convert_html(frag)
        title = page_title(n)
        date = upd_date(n) or "2008-11-18"
        yh = year_hint(n)
        if kind == "bericht" and yh and not date.startswith(yh) and int(yh) < int(date[:4]):
            date = f"{yh}-12-31"
        img = first_image(md)
        common = f'alteId: {n}\nalteUrl: "{B}/index_main.php?page={n}"\n'
        if kind == "bericht":
            stats["bericht"] += 1
            slug = URL[n].split("/aktuelles/")[1]
            ex = excerpt(md, 400)
            for cand in (title, byid[n]["title"]):
                if ex.lower().startswith(cand.lower()):
                    ex = ex[len(cand):].lstrip(" :–-")
            ex = (ex[:220].rsplit(" ", 1)[0] + " …") if len(ex) > 220 else ex
            fm = (f"---\ntitle: {yaml_str(title)}\ndate: {date}\nbereich: {bereich_of(n)}\n"
                  f"teaser: {yaml_str(ex)}\n" + (f"bild: {yaml_str(img)}\n" if img else "") + common + "---\n\n")
            write(f"{CONTENT}/berichte/{slug}.md", fm + md + "\n")
        else:
            stats["static"] += 1
            pfad = URL[n]
            parent = byid[n]["parent"]
            parent_url = URL.get(parent) if parent and KIND.get(parent) in ("static", "fixed") and parent != 1 else None
            fm = (f"---\ntitle: {yaml_str(title)}\npfad: {yaml_str(pfad)}\nbereich: {bereich_of(n)}\n"
                  f"stand: {date}\nreihenfolge: {order.index(n)}\n"
                  + (f"eltern: {yaml_str(parent_url)}\n" if parent_url else "")
                  + f"beschreibung: {yaml_str(excerpt(md, 155))}\n"
                  + (f"bild: {yaml_str(img)}\n" if img else "") + common + "---\n\n")
            fn = pfad.strip("/").replace("/", "__") or "index"
            write(f"{CONTENT}/seiten/{fn}.md", fm + md + "\n")
    return stats

# --- Einsätze ------------------------------------------------------------------
FIELD = {"Datum / Alarmzeit:": "datum", "Alarmierung:": "alarmierung", "Alarmstichwort:": "stichwort",
         "Einsatzstelle:": "einsatzstelle", "Einsatzdauer:": "dauer", "Eingesetzte Fahrzeuge:": "fahrzeuge",
         "Einsatzkräfte FF Wicker:": "kraefte", "Weitere Einsatzkräfte:": "weitere", "Nähere Informationen:": "info"}
def einsaetze():
    out = []
    files = [f for f in os.listdir(RAW) if f.startswith("einsatz_")]
    for f in files:
        enr = int(re.search(r"(\d+)", f).group(1))
        soup = BeautifulSoup(read(f), "lxml")
        th = soup.find("th", class_="thead")
        if not th: continue
        nr = th.get_text(" ", strip=True).replace("Einsatznummer:", "").strip()
        d = {"nummer": nr, "enr": enr}
        for tr in th.find_parent("table").find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                k = tds[0].get_text(" ", strip=True)
                if k in FIELD:
                    if FIELD[k] == "info":
                        d["info"] = convert_html(str(tds[1]))
                    else:
                        d[FIELD[k]] = tds[1].get_text(" ", strip=True)
        imgs = [local_img(i["src"]) for i in soup.find_all("img") if "epicture" in i.get("src", "") or "imagebase" in i.get("src", "")]
        d["bilder"] = imgs
        m = re.match(r"(\d\d)\.(\d\d)\.(\d{4})\s*-\s*(\d\d:\d\d)", d.get("datum", ""))
        if not m: continue
        d["date"] = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"; d["zeit"] = m.group(4)
        out.append(d)
    out.sort(key=lambda x: (x["date"], x["zeit"], x["enr"]))
    for d in out:
        y = d["date"][:4]
        num = d["nummer"].split("/")[-1] if "/" in d["nummer"] else str(d["enr"])
        typ = d["nummer"].split("_")[0] if "_" in d["nummer"] else ""
        slug = f"{y}-{int(num):03d}" if num.isdigit() else f"{y}-{d['enr']}"
        EURL[d["enr"]] = f"/einsaetze/{y}/{slug}"
        d["slug"] = slug; d["typ"] = typ
    return out

def write_einsaetze(out):
    for d in out:
        y = d["date"][:4]
        dauer = re.search(r"(\d+)", d.get("dauer", "") or "")
        kr = re.search(r"(\d+)", d.get("kraefte", "") or "")
        fm = ["---", f"nummer: {yaml_str(d['nummer'])}", f"datum: {d['date']}", f"uhrzeit: \"{d['zeit']}\"",
              f"art: {yaml_str({'B': 'Brand', 'H': 'Hilfeleistung', 'S': 'Sonstiges', 'F': 'Brand', 'T': 'Hilfeleistung'}.get(d['typ'], 'Sonstiges'))}",
              f"stichwort: {yaml_str(d.get('stichwort', ''))}", f"einsatzort: {yaml_str(d.get('einsatzstelle', ''))}",
              f"alarmierung: {yaml_str(d.get('alarmierung', ''))}"]
        if dauer: fm.append(f"dauerMinuten: {dauer.group(1)}")
        fm.append(f"fahrzeuge: {yaml_str(d.get('fahrzeuge', ''))}")
        if kr: fm.append(f"kraefte: {kr.group(1)}")
        fm.append(f"weitereKraefte: {yaml_str(d.get('weitere', ''))}")
        if d["bilder"]:
            fm.append("bilder:"); fm += [f"  - {yaml_str(b)}" for b in d["bilder"]]
        fm.append(f"alteId: {d['enr']}")
        fm.append("---")
        write(f"{CONTENT}/einsaetze/{y}/{d['slug']}.md", "\n".join(fm) + "\n\n" + (d.get("info") or "").strip() + "\n")

# --- Termine ------------------------------------------------------------------------
TYPMAP = {"Übung": "einsatzabteilung", "Jugend": "jugendfeuerwehr", "Minis": "minis", "Aktuelles/Sonstiges": "allgemein"}
def termine():
    seen = set(); out = []
    files = sorted(f for f in os.listdir(RAW) if f.startswith("tag_")) + ["termine_list.html"]
    for f in files:
        soup = BeautifulSoup(read(f), "lxml")
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td", recursive=False)
            if len(tds) != 6: continue
            vals = [td.get_text("\n", strip=True) for td in tds]
            m = re.search(r"(\d\d)\.(\d\d)\.(\d{4})", vals[0])
            if not m: continue
            date = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
            def fixenc(x):
                try: return x.encode("latin1").decode("utf-8")
                except Exception: return x
            titel = fixenc(vals[3]).split("\n")
            ort = fixenc(vals[4]).replace("\n", ", ")
            key = (date, vals[1], titel[0])
            if key in seen: continue
            seen.add(key)
            out.append({"datum": date, "beginn": vals[1].replace(" Uhr", ""), "ende": vals[2].replace(" Uhr", ""),
                        "titel": titel[0], "notiz": " ".join(titel[1:]), "ort": ort,
                        "kategorie": TYPMAP.get(vals[5].strip(), "allgemein")})
    out.sort(key=lambda x: (x["datum"], x["beginn"]))
    cnt = {}
    for t in out:
        base = f"{t['datum']}-{slugify(t['titel'])[:40]}"
        cnt[base] = cnt.get(base, 0) + 1
        fn = base + (f"-{cnt[base]}" if cnt[base] > 1 else "")
        fm = ["---", f"titel: {yaml_str(t['titel'])}", f"datum: {t['datum']}"]
        if re.match(r"\d\d:\d\d", t["beginn"]): fm.append(f"beginn: \"{t['beginn']}\"")
        if re.match(r"\d\d:\d\d", t["ende"]): fm.append(f"ende: \"{t['ende']}\"")
        if t["ort"].strip(): fm.append(f"ort: {yaml_str(t['ort'])}")
        fm.append(f"kategorie: {t['kategorie']}")
        fm.append("---")
        write(f"{CONTENT}/termine/{t['datum'][:4]}/{fn}.md", "\n".join(fm) + "\n\n" + t["notiz"] + "\n")
    return out

if __name__ == "__main__":
    E = einsaetze()            # zuerst, damit Einsatz-Links in Seiten auflösbar sind
    stats = main_pages()
    write_einsaetze(E)
    T = termine()
    json.dump(IMAGES, open(f"{DATA}/images.json", "w"), indent=0)
    json.dump(DOWNLOADS, open(f"{DATA}/downloads.json", "w"), indent=0)
    redirects = {f"page={n}": URL[n] for n in URL}
    redirects.update({f"enr={k}": v for k, v in EURL.items()})
    json.dump(redirects, open(f"{DATA}/redirects.json", "w"), indent=0, ensure_ascii=False)
    stats["einsaetze"] = len(E); stats["termine"] = len(T); stats["bilder"] = len(IMAGES); stats["downloads"] = len(DOWNLOADS)
    json.dump(stats, open(f"{DATA}/stats.json", "w"), indent=1)
    print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in stats.items()}))
