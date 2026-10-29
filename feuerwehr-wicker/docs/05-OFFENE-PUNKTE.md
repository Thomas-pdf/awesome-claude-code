# 5. Offene Punkte und Fragen

Zum Ausdrucken und Abhaken. Sortiert nach Ansprechpartner. **Fett** = vor dem Livegang zwingend.

## A. Mit der Wehrführung klären

- [ ] **Übungszeiten Einsatzabteilung:** Die alte Seite nennt „Übung donnerstags ab 19:00 Uhr + Technischer Dienst samstags ab 13:30 Uhr“, der Entwurf „samstags 13:30–15:30“. Was ist aktuell richtig? (Steht zentral in `src/lib/site.ts`.)
- [ ] Übungszeiten **Minilöscher**: wöchentlich oder 14-täglich montags 16:30–18:00? Altersangabe „6–10 Jahre“ korrekt?
- [ ] **Jugendfeuerwehr**: montags 18:30–20:30, Alter 10–17 Jahre korrekt?
- [ ] **Alters- & Ehrenabteilung:** Gibt es feste Treffen? Eigene Seite gewünscht? (Auf der alten Seite gab es dazu keine eigene Seite.)
- [ ] **Einsatzfotos (1.815 Stück) prüfen lassen:** keine erkennbaren Betroffenen, keine Kennzeichen. Ältere Jahrgänge stichprobenartig.
- [ ] **Einsatzberichte:** Sollen Einsatzstellen weiter mit Straßennamen genannt werden?
- [ ] Mitgliederzahlen aktualisieren (Seite Einsatzabteilung: „48 Frauen und Männer“ vs. Fotounterschrift „58 Mitglieder“).
- [ ] **Mitgliederbereich:** Welche Fachsoftware nutzt Flörsheim/MTK bereits (FeuerOn, DIVERA 24/7, MP-FEUER …)? → siehe `04-MITGLIEDERBEREICH-ARCHITEKTUR.md`
- [ ] Wer pflegt künftig Einsätze, Berichte, Termine? (2–4 Personen benennen)
- [ ] Gibt es interne Termine im Kalender, die **nicht** öffentlich sein sollen? (Derzeit sind alle übernommenen Termine öffentlich, wie auf der alten Seite.)

## B. Mit dem Vereinsvorstand klären

- [ ] **Impressum:** Namen des vertretungsberechtigten Vorstands, Registergericht, Vereinsregisternummer, verantwortliche Person nach § 18 Abs. 2 MStV.
- [ ] **Betreiber der Website:** Verein oder Stadt? Ggf. Abstimmung mit der Stadt Flörsheim (Öffentlichkeitsarbeit der Feuerwehren).
- [ ] **Datenschutzerklärung** prüfen lassen (DSB der Stadt oder Landesfeuerwehrverband Hessen), Hosting-Anbieter eintragen.
- [ ] **Einwilligungen für Fotos von Kindern und Jugendlichen** (ca. 180 Berichte Jugendfeuerwehr/Minilöscher): Liegen sie vor? Wenn nicht: betroffene Bilder entfernen oder verpixeln.
- [ ] **Bildrechte** bei Fremdfotos: Presse, Visualisierung Neubau (Architekt/Stadt?), Logos anderer Feuerwehren auf den Linkseiten.
- [ ] Private Berichte (Hochzeiten 2023/2024, Nachrufe) weiter veröffentlichen? Bei Nachrufen ggf. Angehörige fragen.
- [ ] **Hosting-Entscheidung** (siehe Anleitung, Schritt 3) und Budget (ca. 25–85 €/Jahr).
- [ ] Zugänge: mindestens 2 Verantwortliche für GitHub, Hosting und Domain.
- [ ] **Logo/Wappen:** Das Logo im Prototyp ist ein **Platzhalter** (rotes Schild mit „W“). Bitte das offizielle Wappen bzw. Vereinslogo als Vektordatei (SVG/PDF/EPS) besorgen und die Nutzungsrechte klären.
- [ ] Gutes **Titelfoto** für die Startseite auswählen (derzeit: Gruppenfoto Einsatzabteilung 2024).
- [ ] Instagram-Kanal vorhanden? Dann in `src/lib/site.ts` ergänzen.
- [ ] Eintrittserklärung Minilöscher (PDF) neu hinterlegen. Die Datei ist auf der alten Seite defekt.
- [ ] Spendenkonto/IBAN des Fördervereins auf der Vereinsseite angeben?

## C. Mit dem jetzigen Hoster (Privatperson) klären

- [ ] **Sicherheitshinweis weitergeben:** `security_show_epicture.php` nimmt einen vollständigen Serverpfad als Parameter (`_filename=/www/htdocs/…`). Das ist ein mögliches Einfallstor zum Auslesen von Dateien. Bitte prüfen bzw. bis zur Abschaltung absichern. (Wurde von uns **nicht** getestet.)
- [ ] Ist er bereit, beim Umzug zu helfen (DNS-Termin ca. 30 Minuten)?
- [ ] Wo läuft die **Domain** (Registrar)? Wo laufen die **E-Mail-Postfächer** (info@, wehrfuehrung@, 1.vorsitzender@ …)? Die Mail darf beim Umzug nicht unterbrochen werden!
- [ ] **TTL** der DNS-Einträge eine Woche vorher auf 300 Sekunden senken.
- [ ] Vollständige **Sicherung** der alten Seite (Dateien + Datenbank) vor der Abschaltung.
- [ ] Langfristige **Übertragung der Domain auf den Verein** (Inhaberwechsel/AuthInfo-Code) – im Guten besprechen und Dank aussprechen für die jahrelange Betreuung.
- [ ] Export der Mitgliederdaten aus dem internen Bereich (für eine Fachsoftware), danach sichere Löschung.
- [ ] Hat die alte Seite Unterseiten oder Dateien, die **nicht verlinkt** sind, aber genutzt werden (z. B. direkte PDF-Links in Flyern, QR-Codes)?

## D. Technische Restpunkte (kann Claude Code erledigen)

- [ ] Umzug in ein eigenes, privates Repository des Vereins (siehe Anleitung, Schritt 4).
- [ ] Offizielles Logo einbauen, sobald vorhanden.
- [ ] Bildbeschreibungen (Alt-Texte) für wichtige Archivbilder nachtragen.
- [ ] Optional: Daten älterer Berichte korrigieren, wo „zuletzt geändert“ deutlich nach dem Ereignis liegt.
- [ ] Optional: Hochwertiges Vorschaubild für Social Media (`public/og-bild.jpg`, 1200×630).
- [ ] Nach Livegang: Google Search Console einrichten, Sitemap einreichen.
- [ ] Tägliches automatisches Neubauen einrichten (ist in der Deploy-Vorlage enthalten), damit „Demnächst“-Termine immer aktuell sind.
