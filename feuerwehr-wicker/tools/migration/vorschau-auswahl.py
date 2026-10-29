import os, re, sys, shutil, posixpath, html
DIST, OUT = sys.argv[1], sys.argv[2]
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
def rd(p): return open(os.path.join(DIST, p.strip('/'), 'index.html') if not p.endswith('.html') else os.path.join(DIST, p.strip('/')), encoding='utf-8').read()
home = rd('/')
pages = ['/', '/aktuelles', '/einsaetze', '/einsaetze/2025', '/termine', '/einsatzabteilung', '/einsatzabteilung/fahrzeuge',
         '/einsatzabteilung/fahrzeuge/stlf-20v', '/einsatzabteilung/fahrzeuge/lf-10', '/jugendfeuerwehr', '/miniloescher', '/verein', '/verein/chronik',
         '/neubau', '/neubau/zahlen-daten-fakten', '/mitmachen', '/buergerinfo', '/buergerinfo/verhalten-im-notfall', '/buergerinfo/brandschutz',
         '/buergerinfo/brandschutz/rauchmelder', '/100-jahre', '/kontakt', '/impressum', '/datenschutz', '/barrierefreiheit', '/intern', '/intern/bereich', '/sitemap']
# Berichte und Einsätze, die auf der Startseite verlinkt sind
pages += sorted(set(re.findall(r'href="(/aktuelles/20\d\d/[^"/]+)"', home)))[:7]
pages += sorted(set(re.findall(r'href="(/einsaetze/20\d\d/[^"/]+)"', home)))[:5]
pages = list(dict.fromkeys(p.rstrip('/') or '/' for p in pages))
pageset = set(pages)
def outpath(p): return 'index.html' if p == '/' else p.strip('/') + '/index.html'
def rel(frm, to): return posixpath.relpath(to, posixpath.dirname(frm) or '.')
assets = set()
HINWEIS = 'vorschau-hinweis/index.html'
def fix(frm, s):
    def rep(m):
        attr, url = m.group(1), html.unescape(m.group(2))
        base, _, frag = url.partition('#'); base = base.split('?')[0]
        if url.startswith('//'): return m.group(0)
        if base.startswith(('/_astro/', '/bilder/', '/downloads/')) or re.search(r'\.(svg|png|jpg|webp|ico|css|js|webmanifest)$', base):
            if base.startswith('/downloads/'): return f'{attr}="{rel(frm, HINWEIS)}"'
            assets.add(base); return f'{attr}="{rel(frm, base.lstrip("/"))}"'
        p = base.rstrip('/') or '/'
        if p in pageset: return f'{attr}="{rel(frm, outpath(p))}' + (f'#{frag}' if frag else '') + '"'
        if base == '' and frag: return m.group(0)
        return f'{attr}="{rel(frm, HINWEIS)}"'
    s = re.sub(r'(href|src)="(/[^"]*)"', rep, s)
    s = s.replace('window.location.href = \'/intern/bereich\'', "window.location.href = '" + rel(frm, 'intern/bereich/index.html') + "'")
    return s
TPL = None
for p in pages:
    s = fix(outpath(p), rd(p)); TPL = TPL or s
    os.makedirs(os.path.dirname(os.path.join(OUT, outpath(p))) or OUT, exist_ok=True)
    open(os.path.join(OUT, outpath(p)), 'w', encoding='utf-8').write(s)
# Hinweis-Seite aus Kontakt-Vorlage ableiten
k = fix(HINWEIS, rd('/kontakt'))
main_start = k.index('<main'); main_end = k.index('</main>')
body = ('<main id="inhalt"><section class="container--schmal section"><p class="eyebrow">Vorschau</p><h1>In dieser Vorschau nicht enthalten</h1>'
        '<p>Diese Online-Vorschau zeigt eine Auswahl von rund 40 Seiten. Die vollständige Website umfasst <strong>2.294 Seiten</strong>: 525 Berichte, 1.540 Einsätze seit 2000, alle Termine, PDFs und die Volltextsuche.</p>'
        '<p>Die komplette Fassung lässt sich lokal starten oder in 15 Minuten kostenlos auf Netlify bereitstellen (siehe Livegang-Anleitung, Schritt 3a).</p>'
        f'<p><a class="btn btn--rot" href="{rel(HINWEIS, "index.html")}">Zur Startseite</a></p></section>')
k = k[:main_start] + body + k[main_end:]
k = re.sub(r'<title>.*?</title>', '<title>Nicht in der Vorschau | Feuerwehr Wicker</title>', k)
os.makedirs(os.path.join(OUT, 'vorschau-hinweis'), exist_ok=True)
open(os.path.join(OUT, HINWEIS), 'w', encoding='utf-8').write(k)
# Assets kopieren, CSS-URLs relativ machen
for a in sorted(assets):
    src = os.path.join(DIST, a.lstrip('/'))
    if not os.path.exists(src): print('fehlt', a); continue
    dst = os.path.join(OUT, a.lstrip('/')); os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy(src, dst)
for f in os.listdir(os.path.join(OUT, '_astro')):
    if f.endswith('.css'):
        p = os.path.join(OUT, '_astro', f); c = open(p).read()
        for u in set(re.findall(r'url\((/_astro/[^)]+)\)', c)):
            shutil.copy(os.path.join(DIST, u.lstrip('/')), os.path.join(OUT, u.lstrip('/')))
            c = c.replace(u, './' + u.split('/')[-1])
        open(p, 'w').write(c)
n = sum(len(fs) for _, _, fs in os.walk(OUT)); size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
print('Seiten', len(pages) + 1, 'Dateien', n, 'MB', round(size / 1e6, 1))
