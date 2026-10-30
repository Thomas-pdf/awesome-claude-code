# 1. Inventar der alten Website feuerwehr-wicker.de

Stand der Analyse: 29.10.2026 · Methode: vollständiges automatisches Auslesen aller öffentlich erreichbaren Seiten (Sitemap + Folgen aller internen Links), Einsatzdatenbank (alle Jahrgänge), Terminkalender (alle Monate 2014–2027).

## Überblick

| Bereich | Alte Seite | Neue Seite | Status |
|---|---|---|---|
| Menü- und Inhaltsseiten | 683 Seiten-IDs | 525 Berichte + 106 feste Seiten | ✅ vollständig übernommen |
| Davon reine Übersichts-/Containerseiten | 49 | ersetzt durch neue Übersichten (Aktuelles, Jahresarchive, Bautagebuch) | ✅ |
| Einsätze | 1.540 (2000 – Okt. 2026) | 1.540, je eigene Seite + Jahresstatistik | ✅ vollständig |
| Einsätze mit Bericht-Text | 1.539 | 1.539 | ✅ |
| Einsatzfotos | 1.815 Fotos bei 556 Einsätzen | übernommen | ✅ |
| Fotos in Berichten/Seiten | ca. 4.860 | übernommen (WebP, max. 1.600 px) | ✅ |
| Termine | 3.790 (2014 – 2027) | übernommen, kommende Termine + Archiv je Jahr + iCal-Abo | ✅ |
| Downloads (PDF) | 66 Verweise | 65 Dateien übernommen | ⚠️ 1 Datei auf alter Seite defekt |
| Alte Links (z. B. aus Google/Facebook) | `index_main.php?page=…`, `einsaetze.php?…enr=…` | 2.218 automatische Weiterleitungen | ✅ |

## Berichte nach Bereich

| Bereich | Anzahl |
|---|---|
| Einsatzabteilung (inkl. Übungen, Ausbildung, ältere Berichte ab 2002) | 223 |
| Verein (inkl. Tag der offenen Tür, Archiv bis 2000) | 103 |
| Jugendfeuerwehr (Ausbildung, Jugendarbeit, Zeltlager) | 93 |
| Minilöscher | 85 |
| Neubau Feuerwehrhaus (Förderbescheid, Spatenstich, Richtfest, Bautagebuch Feb.–Sep. 2026) | 11 |
| 100 Jahre Feuerwehr (Festweinprobe, Gottesdienst, TdoT, Oktoberfest, Zapfenstreich) | 10 |

Berichte nach Jahr: 2000–2014 zusammen 87, 2015: 32, 2016: 43, 2017: 55, 2018: 31, 2019: 41, 2020: 29, 2021: 26, 2022: 35, 2023: 31, 2024: 31, 2025: 42, 2026: 41.

## Einsätze nach Jahr

2000: 50 · 2001: 44 · 2002: 50 · 2003: 76 · 2004: 31 · 2005: 37 · 2006: 21 · 2007: 55 · 2008: 47 · 2009: 47 · 2010: 49 · 2011: 44 · 2012: 47 · 2013: 44 · 2014: 43 · 2015: 59 · 2016: 58 · 2017: 52 · 2018: 82 · 2019: 67 · 2020: 56 · 2021: 81 · 2022: 92 · 2023: 86 · 2024: 64 · 2025: 89 · 2026: 68 (Stand 27.10.2026)

## Feste Seiten (Auswahl)

- **Bürgerinformationen:** Verhalten im Notfall, Informationen, 18 Brandschutzthemen (Rauchmelder, Grillen, Silvester, Weihnachtszeit, Hydranten, Rettungswege, Hausnummern, Gartenfeuer …)
- **Wir suchen dich:** Imagefilm, Meine ersten 100 Tage, Jugendfeuerwehr, Feuerwehrverein
- **Neubau:** Zahlen/Daten/Fakten, Wieso? Weshalb? Warum? (6 Unterseiten), Aktuelles Haus
- **Einsatzabteilung:** Fahrzeuge (StLF 20V, LF 10, MTF, MTF Hygiene, 2 Anhänger, Kräder, 8 ehemalige Fahrzeuge), Wir für Sie, Unsere Sicherheit, Ausbildung (8 Unterseiten), Brandschutzerziehung (6 Unterseiten), Sportgruppe
- **Jugendfeuerwehr:** Mitglied werden, Die JF sucht dich, Tannenbaumsammlung, Ostereierverkauf
- **Verein:** Vorstand, Mitgliedschaft/Eintrittserklärung, Chronik (+ Handdruckspritze), Satzung, Tag der offenen Tür
- **100 Jahre:** Übersicht + Chronik
- **Links:** 5 Kategorien · **Downloads:** Jahresberichte, Hits für Kids
- **Kontakt:** Feuerwehrhaus + Ansprechpartner Einsatzabteilung, Jugend, Kinderfeuerwehr, Verein

## Bewusst nicht übernommen

| Was | Grund / Ersatz |
|---|---|
| Interner Bereich (`i_login.php`) | Zugangsdaten nicht vorhanden (bewusst). Ersetzt durch **Demo-Mitgliederbereich** `/intern`. |
| Suchfunktion (PHP) | ersetzt durch Pagefind (statische Volltextsuche, ohne Server) |
| Sitemap (PHP) | neu generiert: `/sitemap` (für Menschen) und `/sitemap-index.xml` (für Google) |
| Link-Formular (`linkformular.php`) | Formular entfällt (Spam-/Sicherheitsrisiko). Linkseiten selbst sind übernommen. |
| DWD-Wetterwarnkarte (eingebundenes Bild vom DWD-Server) | entfällt (Datenübertragung an Dritte). Optional: Link auf warnwetter.de |
| Besucherzähler, „Letzte Updates“-Popup | entfällt (nicht mehr zeitgemäß) |
| Startseiten-Kacheln („Home-Board“) | ersetzt durch automatisch aktuelle Berichte auf der Startseite |
| Frames, Popups, Menübild-Buttons | ersetzt durch modernes, responsives Layout |

## Was nicht ging / Auffälligkeiten

0. **Doppelte Einsatznummer 2020/7:** Auf der alten Seite gibt es sowohl B_2020/7 (Brand) als auch H_2020/7 (Hilfeleistung). Beide sind übernommen (`2020-007` und `2020-007-b`).

1. **2 Dateien sind schon auf der alten Seite defekt:** ein Foto im Bericht „MTK-West Übung 2024“ und die PDF „2024 – Eintrittserklärung Minilöscher“. Bitte neu beschaffen.
2. **Datum der Berichte:** Die alte Seite speichert kein Veröffentlichungsdatum, nur „zuletzt aktualisiert“. Dieses Datum wurde übernommen. Bei älteren Berichten, die später nochmal bearbeitet wurden, kann das Datum daher etwas zu spät liegen. Wo der Bericht in einem Jahresarchiv stand, wurde das Jahr daraus abgeleitet.
3. **Bildbeschreibungen (Alt-Texte):** Die meisten Archivfotos hatten nur Platzhalter-Beschreibungen (z. B. „6“). Für Barrierefreiheit sollten wichtige Bilder nach und nach beschrieben werden.
4. **Widersprüchliche Übungszeiten:** Die alte Seite nennt für die Einsatzabteilung „Übung donnerstags ab 19:00 Uhr, Technischer Dienst samstags ab 13:30 Uhr“. Der Entwurf nannte „samstags 13:30–15:30“. Übernommen wurde die Angabe der alten Seite. → siehe Offene Punkte.
5. **⚠️ Sicherheitsrelevante Beobachtung (nicht getestet!):** Die alte Seite liefert Einsatzfotos über `security_show_epicture.php?_filename=/www/htdocs/…` aus. Der Parameter enthält einen vollständigen Serverpfad. Solche Muster sind häufig anfällig für das Auslesen beliebiger Dateien vom Server (Path Traversal). Das wurde **bewusst nicht ausprobiert**. Der Hoster sollte das prüfen bzw. die alte Seite nach dem Umzug vollständig abschalten. Außerdem verrät die URL den internen Serverpfad.

## Technische Ablage der Rohdaten

- Migrationsskripte: `tools/migration/` (Crawler, Umwandlung nach Markdown, Bild-Optimierung)
- Zuordnung alte → neue Adresse: `tools/migration/redirects.json`
- Statistik des Laufs: `tools/migration/stats.json`
