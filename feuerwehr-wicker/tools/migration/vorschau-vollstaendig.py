"""Erzeugt eine möglichst vollständige Online-Vorschau (Claude-Artifact, max. ~500 Dateien):
- alle Seiten außer Einzelberichten/Einzeleinsätzen/Seitennummern
- Berichte: je Jahr eine Seite mit allen Berichten im Volltext (Anker #b-<slug>)
- Einsätze: Jahreslisten mit aufklappbaren Berichten (Anker #e-<jahr>-<nr>)
- Bilder als eingebettete data:-URIs (verkleinert), damit die Dateizahl klein bleibt
Aufruf: python3 -I vorschau2.py <dist> <out>"""
import os, re, sys, shutil, posixpath, html, base64, io, json, collections
from PIL import Image
DIST, OUT = sys.argv[1], sys.argv[2]
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
HINWEIS = 'vorschau-hinweis/index.html'

def rd(rel): return open(os.path.join(DIST, rel), encoding='utf-8').read()
alle = sorted(os.path.relpath(os.path.join(d, f), DIST) for d, _, fs in os.walk(DIST) for f in fs if f == 'index.html')
ber_re = re.compile(r'^aktuelles/(\d{4})/([^/]+)/index\.html$')
ein_re = re.compile(r'^einsaetze/(\d{4})/([^/]+)/index\.html$')
skip_re = re.compile(r'^(aktuelles/seite/|aktuelles/bereich/[^/]+/seite/|suche/|pagefind/)')
berichte = collections.defaultdict(list)
seiten = []
for p in alle:
    m = ber_re.match(p)
    if m: berichte[m.group(1)].append((m.group(2), p)); continue
    if ein_re.match(p) or skip_re.match(p): continue
    seiten.append(p)
# Berichte nach Ereignisjahr (Datum) gruppieren; URL-Ordnerjahr kann abweichen
reihen = collections.defaultdict(list)
for ordner, eintraege in berichte.items():
    for slug, p in eintraege:
        d = re.search(r'<p class="artikel-meta".*?datetime="(\d{4}-\d\d-\d\d)', rd(p), re.S)
        datum = d.group(1) if d else f'{ordner}-01-01'
        reihen[datum[:4]].append((datum, ordner, slug, p))
jahre_b = sorted(reihen)
pageset = set(seiten) | {HINWEIS}
PRO_TEIL = 12
def teil_datei(j, n): return f'aktuelles/{j}/index.html' if n == 0 else f'aktuelles/{j}/teil-{n + 1}/index.html'
slug_datei = {}
for j in jahre_b:
    reihen[j].sort(reverse=True)
    for i, (_, ordner, slug, _) in enumerate(reihen[j]):
        slug_datei[(ordner, slug)] = teil_datei(j, i // PRO_TEIL)
        pageset.add(teil_datei(j, i // PRO_TEIL))

# ---- Bilder einbetten ------------------------------------------------------
cache = {}
def data_uri(path):
    if path in cache: return cache[path]
    src = os.path.join(DIST, path.lstrip('/'))
    if not os.path.exists(src): cache[path] = None; return None
    try:
        if path.endswith('.svg'):
            uri = 'data:image/svg+xml;base64,' + base64.b64encode(open(src, 'rb').read()).decode()
        else:
            im = Image.open(src)
            if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA')
            if im.width > 540: im = im.resize((540, round(im.height * 540 / im.width)), Image.LANCZOS)
            b = io.BytesIO(); im.save(b, "WEBP", quality=48, method=4)
            uri = 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    except Exception:
        uri = None
    cache[path] = uri; return uri

def rel(frm, to): return posixpath.relpath(to, posixpath.dirname(frm) or '.')
assets = set()
def ziel(url):
    """neue Datei (+Anker) für eine absolute Website-URL"""
    base, _, frag = url.partition('#'); base = base.split('?')[0]
    m = re.match(r'^/aktuelles/(\d{4})/teil-(\d+)/?$', base)
    if m: return f'aktuelles/{m.group(1)}/teil-{m.group(2)}/index.html', ''
    m = re.match(r'^/aktuelles/(\d{4})/([^/]+)/?$', base)
    if m: return slug_datei.get((m.group(1), m.group(2)), f'aktuelles/{m.group(1)}/index.html'), f'b-{m.group(2)}'
    m = re.match(r'^/einsaetze/(\d{4})/([^/]+)/?$', base)
    if m: return f'einsaetze/{m.group(1)}/index.html', f'e-{m.group(2)}'
    if re.match(r'^/aktuelles/seite/', base): return 'aktuelles/index.html', ''
    m = re.match(r'^/aktuelles/bereich/([^/]+)/seite/', base)
    if m: return f'aktuelles/bereich/{m.group(1)}/index.html', ''
    p = base.strip('/'); p = (p + '/index.html') if p else 'index.html'
    if p in pageset: return p, frag
    return HINWEIS, ''

def fix(frm, s):
    def bild(m):
        uri = data_uri(html.unescape(m.group(2)))
        return f'{m.group(1)}="{uri}"' if uri else m.group(0)
    s = re.sub(r'(src)="(/(?:bilder|logo-|favicon|og-bild)[^"]*)"', bild, s)
    def rep(m):
        attr, url = m.group(1), html.unescape(m.group(2))
        if url.startswith('//'): return m.group(0)
        b = url.split('#')[0].split('?')[0]
        if b.startswith('/_astro/') or re.search(r'\.(css|js|png|svg|webmanifest|ico)$', b) and not b.startswith('/downloads/'):
            if os.path.exists(os.path.join(DIST, b.lstrip('/'))):
                assets.add(b); return f'{attr}="{rel(frm, b.lstrip("/"))}"'
            return f'{attr}="{rel(frm, HINWEIS)}"'
        if b.startswith(('/bilder/', '/downloads/')) or b.endswith(('.ics', '.xml', '.pdf')):
            return f'{attr}="{rel(frm, HINWEIS)}"'
        datei, anker = ziel(url)
        return f'{attr}="{rel(frm, datei)}' + (f'#{anker}' if anker else '') + '"'
    s = re.sub(r'(href|src)="(/[^"]*)"', rep, s)
    s = s.replace("window.location.href = '/intern/bereich'", "window.location.href = '" + rel(frm, 'intern/bereich/index.html') + "'")
    s = re.sub(r'<script>\s*window\.addEventListener\(\'DOMContentLoaded\'.*?</script>', '', s, flags=re.S)
    return s

def artikel(p):
    s = rd(p)
    titel = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))).strip()
    meta = re.search(r'<p class="artikel-meta"[^>]*>(.*?)</p>', s, re.S)
    body = re.search(r'<article class="prose"[^>]*>(.*?)</article>', s, re.S)
    return titel, (meta.group(1) if meta else ''), (body.group(1) if body else '')

# ---- Jahresseiten mit allen Berichten -------------------------------------------
def jahresseite(j, n):
    frm = teil_datei(j, n)
    basis = f'aktuelles/{j}/index.html'
    vorlage = rd(basis) if os.path.exists(os.path.join(DIST, basis)) else rd('aktuelles/index.html')
    l = reihen[j]; teile_n = (len(l) + PRO_TEIL - 1) // PRO_TEIL
    stueck = l[n * PRO_TEIL:(n + 1) * PRO_TEIL]
    alle_titel = []
    for i, (_, ordner, slug, p) in enumerate(l):
        titel = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', rd(p), re.S).group(1))).strip()
        alle_titel.append((ordner, slug, titel))
    inhalt = ''.join(f'<li><a href="/aktuelles/{o}/{slug}">{html.escape(t)}</a></li>' for o, slug, t in alle_titel)
    teile = []
    for _, _, slug, p in stueck:
        titel, meta, body = artikel(p)
        teile.append(f'<article class="vb-artikel" id="b-{slug}"><p class="vb-meta">{meta}</p><h2>{html.escape(titel)}</h2><div class="prose">{body}</div><p><a class="link-pfeil" href="#vb-inhalt">Zur Übersicht {j}</a></p></article>')
    teilnav = '' if teile_n == 1 else '<nav class="chips" aria-label="Teile">' + ''.join(
        f'<a class="chip" href="/{teil_datei(j, t)[:-len("index.html")]}" {"aria-current=page" if t == n else ""}>Teil {t + 1}</a>' for t in range(teile_n)) + '</nav>'
    main = (f'<main id="inhalt" tabindex="-1"><section class="page-hero"><div class="container"><p class="eyebrow">Aktuelles</p><h1>Berichte {j}' + (f' (Teil {n + 1} von {teile_n})' if teile_n > 1 else '') + '</h1>'
            f'<p>Alle {len(l)} Berichte des Jahres {j} im Volltext. In der fertigen Website hat jeder Bericht eine eigene Seite.</p></div></section>'
            f'<div class="container section"><nav class="chips" aria-label="Jahre">' + ''.join(f'<a class="chip" href="/aktuelles/{x}" {"aria-current=page" if x == j else ""}>{x}</a>' for x in sorted(jahre_b, reverse=True)) + '</nav>'
            + f'<nav class="vb-inhalt" id="vb-inhalt" aria-label="Berichte {j}"><h2>Alle Berichte {j}</h2><ol>{inhalt}</ol></nav>' + teilnav
            + ''.join(teile) + teilnav + '</div></main>')
    s = re.sub(r'<main.*?</main>', lambda _: main, vorlage, flags=re.S)
    s = re.sub(r'<title>.*?</title>', f'<title>Berichte {j} | Feuerwehr Wicker</title>', s)
    s = s.replace('</head>', '<style>.vb-inhalt{background:var(--flaeche);border-radius:var(--radius);padding:1.4rem 1.6rem;margin-bottom:2rem}.vb-inhalt ol{columns:2 280px;margin:0;padding-left:1.2rem}.vb-inhalt li{margin:.2rem 0}.vb-artikel{padding-top:3.5rem;margin-top:3.5rem;border-top:1px solid var(--linie-hell);scroll-margin-top:80px}.vb-artikel h2{font-size:clamp(1.6rem,3vw,2.3rem)}.vb-meta{display:flex;gap:.7rem;color:var(--text-2);font-size:.9rem;margin:0 0 .4rem}</style></head>', 1)
    return fix(frm, s)

def schreibe(p, s):
    os.makedirs(os.path.dirname(os.path.join(OUT, p)) or OUT, exist_ok=True)
    open(os.path.join(OUT, p), 'w', encoding='utf-8').write(s)

for p in seiten:
    if re.match(r'^aktuelles/\d{4}/index\.html$', p): continue
    schreibe(p, fix(p, rd(p)))
for j in jahre_b:
    for n in range((len(reihen[j]) + PRO_TEIL - 1) // PRO_TEIL):
        schreibe(teil_datei(j, n), jahresseite(j, n))

# Hinweisseite
k = fix(HINWEIS, rd('kontakt/index.html'))
body = ('<main id="inhalt"><section class="page-hero"><div class="container"><p class="eyebrow">Vorschau</p><h1>Nur in der vollständigen Website</h1>'
        '<p>Diese Online-Vorschau enthält alle Seiten, alle Berichte und alle Einsätze. Nicht enthalten sind hier nur die PDF-Downloads, die Volltextsuche, der Kalender-Export und die Einsatzfotos (je Einsatz eine eigene Seite).</p></div></section>'
        '<div class="container section"><p>Diese Funktionen sind in der fertigen Website vorhanden und lassen sich lokal oder nach der Einrichtung bei einem Hoster nutzen (siehe Livegang-Anleitung, Schritt 3a).</p>'
        f'<p><a class="btn btn--rot" href="{rel(HINWEIS, "index.html")}">Zur Startseite</a></p></div></main>')
k = re.sub(r'<main.*?</main>', lambda _: body, k, flags=re.S)
k = re.sub(r'<title>.*?</title>', '<title>Nur in der Vollversion | Feuerwehr Wicker</title>', k)
schreibe(HINWEIS, k)

for a in sorted(assets):
    d = os.path.join(OUT, a.lstrip('/')); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy(os.path.join(DIST, a.lstrip('/')), d)
# Schriftdateien aus CSS: nur latin/latin-ext behalten
for f in os.listdir(os.path.join(OUT, '_astro')):
    if not f.endswith('.css'): continue
    p = os.path.join(OUT, '_astro', f); c = open(p).read()
    c = re.sub(r'@font-face\{[^}]*\}', lambda m: m.group(0) if re.search(r'-latin-(ext-)?[^.]*\.[^.]+\.woff2', m.group(0)) else '', c)
    c = re.sub(r',url\(/_astro/[^)]+\.woff\) format\("woff"\)', '', c)
    for u in set(re.findall(r'url\((/_astro/[^)]+)\)', c)):
        shutil.copy(os.path.join(DIST, u.lstrip('/')), os.path.join(OUT, u.lstrip('/'))); c = c.replace(u, './' + u.split('/')[-1])
    open(p, 'w').write(c)

dateien = sorted(os.path.relpath(os.path.join(d, f), OUT) for d, _, fs in os.walk(OUT) for f in fs)
groessen = {f: os.path.getsize(os.path.join(OUT, f)) for f in dateien}
print('Dateien', len(dateien), 'MB', round(sum(groessen.values()) / 1e6, 1), 'größte', sorted(groessen.items(), key=lambda x: -x[1])[:4])
json.dump(groessen, open(os.path.join(OUT, '..', 'groessen.json'), 'w'))
