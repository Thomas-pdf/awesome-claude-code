# Neue Website der Freiwilligen Feuerwehr Flörsheim-Wicker (Prototyp)

Moderner, schneller und sicherer Nachfolger von www.feuerwehr-wicker.de, mit **allen Inhalten der alten Seite**: 525 Berichte, 106 Info-Seiten, 1.540 Einsätze (2000–2026), 3.790 Termine, ca. 6.700 Fotos, 65 PDFs.

| | |
|---|---|
| **Technik** | [Astro](https://astro.build) – statische Website, keine Datenbank, kein PHP |
| **Inhalte** | Markdown-Dateien in `src/content/`, pflegbar im Browser mit [Pages CMS](https://pagescms.org) |
| **Suche** | [Pagefind](https://pagefind.app) – Volltextsuche ohne Server |
| **Design** | hell, im Stil von apple.com; Schrift Inter (lokal); offizielles Logo der Feuerwehren Flörsheim |
| **Datenschutz** | keine Cookies, keine Tracker, Schriften lokal, keine externen Einbindungen |
| **Barrierefreiheit** | WCAG-2-AA-Prüfung mit axe ohne Befund, Tastaturbedienung, „Zum Inhalt springen“ |
| **SEO** | Sitemap, strukturierte Daten (FireStation), Open-Graph-Bilder, saubere URLs, 2.218 Weiterleitungen alter Links |

## Dokumentation

1. [Inventar der alten Seite](docs/01-INVENTAR.md) – was gefunden, übernommen, nicht übernommen
2. [Schritt-für-Schritt bis zum Livegang](docs/02-LIVEGANG-ANLEITUNG.md) – Hosting & Kosten, DNS, SSL, Weiterleitungen, Rechtliches
3. [Inhalte pflegen (für Laien)](docs/03-INHALTE-PFLEGEN.md) – Einsatz/Bericht/Termin eintragen, Foto-Regeln
4. [Mitgliederbereich: Architektur](docs/04-MITGLIEDERBEREICH-ARCHITEKTUR.md) – Fertiglösung vs. Eigenbau
5. [Offene Punkte](docs/05-OFFENE-PUNKTE.md) – Fragen an Wehrführung, Vorstand, Hoster

## Lokal starten

Voraussetzung: [Node.js](https://nodejs.org) 20 oder neuer.

```bash
cd feuerwehr-wicker
npm install
npm run dev        # http://localhost:4321 – Vorschau mit Live-Neuladen
npm run build      # fertige Website in dist/ (inkl. Suchindex & Weiterleitungen)
npm run preview    # gebaute Website ansehen (Suche funktioniert nur hier, nicht in dev)
```

## Aufbau

```
src/
  content/            ← ALLE Inhalte (Markdown)
    berichte/  einsaetze/  termine/  seiten/
  content.config.ts   ← Felder/Regeln der Inhaltstypen
  lib/site.ts         ← Stammdaten: Adresse, Telefon, Übungszeiten
  lib/navigation.ts   ← Hauptmenü
  pages/              ← Seitenvorlagen (Startseite, Aktuelles, Einsätze, Termine, Intern-Demo …)
  components/         ← Bausteine (Kopf, Fuß, Karten, Listen)
  styles/global.css   ← Farben, Schriften, Grundlayout
public/
  bilder/             ← Fotos (WebP), downloads/ ← PDFs
  .htaccess  _redirects  _headers  weiterleitungen.json  ← Weiterleitungen & Sicherheits-Header
tools/migration/      ← Skripte, mit denen die alte Seite übernommen wurde
deploy/               ← Vorlage für automatisches Hochladen zum Hoster
.pages.yml            ← Konfiguration der Pflege-Oberfläche (Pages CMS)
```

## Seitenübersicht

- `/` Startseite: Notruf, Kennzahlen, Aktuelles, letzte Einsätze, nächste Termine, Neubau, Mitmachen
- `/aktuelles` Berichte mit Filter nach Bereich und Jahresarchiv
- `/einsaetze` Einsätze je Jahr mit Statistik (Monate, Einsatzarten, Stunden) und Verlauf seit 2000
- `/termine` kommende Termine mit Gruppenfilter, iCal-Abo (`/termine.ics`), Archiv
- `/einsatzabteilung`, `/jugendfeuerwehr`, `/miniloescher`, `/verein`, `/neubau`, `/100-jahre`, `/buergerinfo`, `/mitmachen` …
- `/intern` **Demo** des Mitgliederbereichs (erfundene Daten, nicht indexiert)
- `/suche`, `/sitemap`, `/kontakt`, `/impressum`, `/datenschutz`, `/barrierefreiheit`, `/rss.xml`
