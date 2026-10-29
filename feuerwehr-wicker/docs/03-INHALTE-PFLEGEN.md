# 3. Inhalte pflegen – Anleitung für Laien

Neue Einsätze, Berichte und Termine einzutragen geht **ohne Programmierkenntnisse**, im Browser oder auf dem Handy. Nach dem Speichern ist die Änderung nach etwa 3–5 Minuten auf der Website sichtbar.

## Einmalig: Zugang einrichten (10 Minuten)

1. Ein kostenloses Konto auf **github.com** anlegen (mit Vereins- oder eigener E-Mail).
2. Den Website-Verantwortlichen bitten, dich zum Repository einzuladen. Er klickt dafür in GitHub auf Settings → Collaborators → Add people.
3. Die Einladung per E-Mail annehmen.
4. **https://app.pagescms.org** öffnen → „Sign in with GitHub“ → das Website-Repository auswählen.
5. Fertig. Links siehst du jetzt die Bereiche **Einsätze, Berichte / Aktuelles, Termine, Feste Seiten**.

> Tipp: Die Adresse app.pagescms.org als Lesezeichen bzw. auf dem Handy als App-Symbol speichern („Zum Home-Bildschirm“).

---

## Einen neuen Einsatz eintragen

1. Links auf **Einsätze** klicken → oben rechts **„Add an entry“**.
2. Ausfüllen:
   - **Einsatznummer:** wie bisher, z. B. `B_2026/69` (B = Brand, H = Hilfeleistung, S = Sonstiges)
   - **Datum** und **Alarmzeit** (z. B. `14:35`)
   - **Einsatzart:** Brand / Hilfeleistung / Sonstiges
   - **Alarmstichwort:** z. B. `F 2 - Brand im Gebäude`
   - **Einsatzstelle:** Ort und Straße, **ohne Hausnummer**
   - **Dauer**, **Fahrzeuge**, **Einsatzkräfte**, **Weitere Kräfte**
   - **Fotos:** optional (siehe Foto-Regeln unten)
   - **Einsatzbericht:** 2–5 Sätze, was passiert ist
3. **Save** klicken. Fertig. Statistik, Startseite und Jahresübersicht aktualisieren sich automatisch.

## Einen Bericht schreiben (Aktuelles)

1. **Berichte / Aktuelles** → „Add an entry“.
2. **Überschrift**, **Datum**, **Bereich** (Einsatzabteilung, Jugendfeuerwehr, Minilöscher, Verein, Neubau …) auswählen.
3. **Kurztext**: 1–2 Sätze. Er erscheint auf der Startseite und in der Übersicht.
4. **Titelbild** hochladen (Querformat, mindestens 1.200 px breit).
5. **Text** schreiben. Die Werkzeugleiste funktioniert wie in Word: Fett, Überschrift, Liste, Bild einfügen, Link.
6. Noch nicht fertig? Haken bei **„Entwurf“** setzen. Dann bleibt der Bericht unsichtbar, bis du den Haken wieder entfernst.
7. **Save**.

## Einen Termin eintragen

1. **Termine** → „Add an entry“.
2. Titel, Datum, Beginn/Ende (z. B. `19:00`), Ort, **Gruppe** (Einsatzabteilung, Jugendfeuerwehr, Minilöscher, Verein, Allgemein).
3. Interne Termine, die nicht öffentlich sein sollen: Haken bei **„Öffentlich anzeigen“** entfernen.
4. **Save**. Der Termin erscheint im Kalender, auf der Startseite und im iCal-Abo.

> Wiederkehrende Übungen (z. B. jeden Donnerstag) müssen einzeln eingetragen werden. Für einen Jahresplan kann ein Helfer mit IT-Erfahrung die Termine auch gesammelt anlegen.

## Eine feste Seite ändern (z. B. Vorstand, Fahrzeuge)

1. **Feste Seiten** → Seite suchen (z. B. „Vorstand“) → Text ändern → **Save**.
2. Das Feld **„Adresse“** bitte nicht ändern. Sonst funktionieren Links auf diese Seite nicht mehr.

## Adresse, Telefon, Übungszeiten ändern

Diese Angaben stehen zentral in der Datei `src/lib/site.ts`. Sie gelten dann überall: Kopf, Fuß, Kontakt, Impressum. Am einfachsten auf github.com die Datei öffnen → Stift-Symbol → Text ändern → „Commit changes“. Oder den Website-Verantwortlichen fragen.

---

## Foto-Regeln (bitte unbedingt beachten)

✅ **Erlaubt / gut:**
- Fahrzeuge, Technik, Übungen, Mannschaftsfotos von Mitgliedern, die einverstanden sind
- Einsatzstellen aus der Distanz, ohne erkennbare Betroffene
- Querformat, scharf, gern mit Feuerwehr-Action

❌ **Nicht veröffentlichen:**
- erkennbare **Verletzte, Betroffene, Schaulustige**
- **Kfz-Kennzeichen**, **Hausnummern**, Namensschilder an Häusern
- **Kinder und Jugendliche** ohne schriftliche Einwilligung der Eltern
- Fotos, die jemand anderes gemacht hat (Presse, Privatleute), ohne Erlaubnis
- Bilder, die Kameraden in unvorteilhaften Situationen zeigen

📏 **Technik:** Fotos direkt vom Handy sind okay. Ideal sind 1.200–2.000 px Breite. Sehr große Bilder (über 5 MB) vorher verkleinern.

🦮 **Bildbeschreibung:** Beim Hochladen kurz beschreiben, was zu sehen ist (z. B. „StLF 20V bei der Übergabe vor dem Feuerwehrhaus“). Das hilft blinden Menschen und Google.

---

## Was passiert im Hintergrund? (zum Verständnis)

1. Pages CMS speichert deine Eingabe als kleine Textdatei (Markdown) im GitHub-Repository.
2. GitHub merkt die Änderung und startet automatisch den „Bau“ der Website (ca. 1–3 Minuten).
3. Die fertige Website wird zum Hoster hochgeladen.

Jede Änderung wird **protokolliert** (wer, wann, was). Fehler lassen sich jederzeit rückgängig machen: in GitHub „History“ öffnen → alte Version wiederherstellen.

## Hilfe, etwas ist kaputt!

- **Website zeigt Änderung nicht an:** 5 Minuten warten, dann Seite neu laden (Strg+F5 bzw. am Handy nach unten ziehen).
- **Fehlermeldung beim Speichern:** Meist fehlt ein Pflichtfeld (rot markiert).
- **Website ist ganz weg oder sieht falsch aus:** Den Website-Verantwortlichen informieren. In GitHub unter „Actions“ sieht man, ob der letzte Bau fehlgeschlagen ist. Die alte Version bleibt in diesem Fall online.

## Für Fortgeschrittene: direkt in Markdown

Alle Inhalte liegen in `src/content/`:

```
src/content/
  berichte/<jahr>/<name>.md      ← Berichte
  einsaetze/<jahr>/<jahr>-<nr>.md ← Einsätze
  termine/<jahr>/<datum>-<name>.md ← Termine
  seiten/<pfad>.md               ← feste Seiten
```

Beispiel Einsatz (`src/content/einsaetze/2026/2026-069.md`):

```markdown
---
nummer: "B_2026/69"
datum: 2026-11-02
uhrzeit: "14:35"
art: "Brand"
stichwort: "F 1 - Brand im Freien"
einsatzort: "Wicker, Feldgemarkung"
alarmierung: "FAE"
dauerMinuten: 45
fahrzeuge: "StLF 20V, MTF"
kraefte: 14
weitereKraefte: "FF Flörsheim, Polizei"
---

Ein brennender Heuballen wurde mit einem C-Rohr abgelöscht.
```
