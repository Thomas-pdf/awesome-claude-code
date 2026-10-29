# 2. Schritt für Schritt bis zum Livegang (für Nicht-Techniker)

Diese Anleitung führt vom Prototyp bis zur fertigen Website unter www.feuerwehr-wicker.de. Fachbegriffe sind erklärt. Plane insgesamt **2 bis 6 Wochen** ein. Am längsten dauern meist die Abstimmungen (Wehrführung, Vorstand, Stadt, Bildrechte), nicht die Technik.

> **Kurzfassung:** (1) Prototyp intern zeigen → (2) offene Punkte klären → (3) Hosting wählen → (4) Website dort einrichten → (5) Inhalte rechtlich prüfen → (6) Domain umstellen → (7) alte Seite abschalten.

---

## Schritt 0: Was ist das überhaupt für eine Website?

- Die neue Seite ist eine **statische Website**. Sie besteht nur aus fertigen HTML-Dateien, Bildern und PDFs. Es gibt **keine Datenbank und kein PHP**, über das jemand einbrechen könnte. Die Sicherheitslücke, wegen der die alte Seite vom Netz musste, ist bei dieser Bauweise praktisch ausgeschlossen.
- Die Inhalte liegen als einfache Textdateien (Markdown) im Repository auf GitHub. Bei jeder Änderung baut ein Programm (Astro) die Website neu und lädt sie hoch.
- Laien pflegen die Inhalte später in einer Web-Oberfläche (**Pages CMS**), siehe `03-INHALTE-PFLEGEN.md`.

---

## Schritt 1: Prototyp intern präsentieren

1. Vorschau öffnen (Link aus dem Chat bzw. siehe README).
2. Mit Wehrführung und Vorstand durchgehen. Gute Fragen dafür:
   - Stimmen Struktur und Menü?
   - Gefällt das Design? Soll das echte Wappen/Logo rein?
   - Wer soll künftig Inhalte pflegen (2–4 Personen)?
3. Die Liste `05-OFFENE-PUNKTE.md` ausdrucken und Punkt für Punkt klären.

---

## Schritt 2: Wem gehört was? (sehr wichtig)

Kläre **vorab** schriftlich (eine E-Mail reicht):

| Frage | Warum |
|---|---|
| Wer ist **Betreiber** der Website: der Verein „Freiwillige Feuerwehr Wicker 1925 e.V.“ oder die Stadt Flörsheim? | Davon hängen Impressum, Datenschutz und ggf. Barrierefreiheitspflichten ab. Viele Städte haben Regeln für die Öffentlichkeitsarbeit ihrer Wehren. |
| Wem gehört die **Domain** feuerwehr-wicker.de? | Laut deiner Info einer Privatperson (dem jetzigen Hoster). Empfehlung: Domain langfristig **auf den Verein** übertragen, damit sie nicht an eine Person gebunden ist. |
| Wer bekommt die **Zugänge** (GitHub, Hosting, Domain)? | Mindestens **zwei** Personen aus dem Verein, nie nur eine. Passwörter in einem Passwort-Manager ablegen. |

---

## Schritt 3: Hosting auswählen (wo die Website „wohnt“)

Alle Optionen bieten **kostenloses SSL** (das Schloss im Browser, https) über Let's Encrypt.

| Option | Kosten (ca., Stand 2026 – bitte prüfen) | Vorteile | Nachteile | Für wen |
|---|---|---|---|---|
| **A. Beim jetzigen Webspace bleiben** (die Pfade der alten Seite deuten auf ALL-INKL hin) | unverändert | Kein Anbieterwechsel, Server in Deutschland, Weiterleitungen (`.htaccess`) funktionieren sofort | Hängt weiter an der Privatperson. Upload per FTP oder automatisch per GitHub-Action (Vorlage liegt bei) | wenn der Hoster einverstanden ist und weiter helfen möchte |
| **B. Deutscher Webhoster auf den Verein** (z. B. ALL-INKL „Privat“, Hetzner „Webhosting Level 1“, IONOS, Strato) | ca. 2–6 € / Monat | Vertrag auf den Verein, Server in Deutschland, AV-Vertrag einfach, `.htaccess` funktioniert | Einmalige Einrichtung des automatischen Uploads (Vorlage liegt bei) | **Empfehlung**, langfristig sauber |
| **C. Netlify** (kostenloser Tarif) | 0 € | Verbindet sich direkt mit GitHub, baut bei jeder Änderung automatisch, sehr einfach, Weiterleitungen über `_redirects` | US-Anbieter (EU-US-Datenschutzrahmen), Datenschutzerklärung entsprechend ergänzen | schnellster Weg zu einer **vollständigen Vorschau** |
| **D. Cloudflare Pages** (kostenlos) | 0 € | wie C, sehr schnell | US-Anbieter; Weiterleitungen alter Links laufen über die 404-Seite (funktioniert, aber langsamer) | Alternative zu C |

**Meine Empfehlung:**
- **Für die Vorschau und den Testbetrieb:** Netlify (Option C). Das ist in 15 Minuten eingerichtet und zeigt die komplette Seite unter einer Test-Adresse.
- **Für den Echtbetrieb:** Option B (deutscher Hoster, Vertrag auf den Verein) **mit automatischem Upload** über GitHub. Oder Option C, wenn der Vorstand mit einem US-Anbieter einverstanden ist.

### 3a. Vollständige Vorschau auf Netlify (ca. 15 Minuten)

1. Auf **netlify.com** ein kostenloses Konto anlegen („Sign up with GitHub“).
2. „Add new site“ → „Import an existing project“ → GitHub → Repository `awesome-claude-code` auswählen (bzw. das neue eigene Repository nach dem Umzug).
3. Einstellungen:
   - Branch: `feuerwehr-wicker-website`
   - Base directory: `feuerwehr-wicker`
   - Build command: `npm run build`
   - Publish directory: `feuerwehr-wicker/dist`
4. „Deploy“ klicken. Nach 2–3 Minuten gibt es eine Adresse wie `irgendwas.netlify.app`. Das ist die vollständige Vorschau.
5. Unter „Site configuration → Change site name“ einen sprechenden Namen wählen, z. B. `ff-wicker-vorschau`.

### 3b. Echtbetrieb bei einem deutschen Hoster mit automatischem Upload

1. Hosting-Paket auf den Verein abschließen (mit SSL, mindestens 1 GB Speicher, FTP-Zugang).
2. Beim Hoster einen **FTP-Benutzer** anlegen. Notiere Server, Benutzername und Passwort.
3. In GitHub im Repository unter **Settings → Secrets and variables → Actions** drei Geheimnisse anlegen: `FTP_SERVER`, `FTP_USER`, `FTP_PASSWORD`.
4. Die Datei `deploy/github-actions-deploy.yml` nach `.github/workflows/deploy.yml` (im Hauptverzeichnis des Repositorys) kopieren.
5. Ab jetzt wird die Website bei jeder Änderung (auch aus dem CMS) automatisch gebaut und hochgeladen. Das dauert etwa 3–5 Minuten.

---

## Schritt 4: Eigenes Repository (empfohlen)

Der Prototyp liegt im Ordner `feuerwehr-wicker/` im Repository `awesome-claude-code`, Branch `feuerwehr-wicker-website`. Für den Echtbetrieb:

1. Auf GitHub eine **Organisation** „Feuerwehr Wicker“ anlegen (kostenlos), mit mindestens 2 Verantwortlichen als Besitzer.
2. Dort ein neues, **privates** Repository `website` anlegen.
3. Den Inhalt des Ordners `feuerwehr-wicker/` hineinkopieren (Claude Code kann das in 5 Minuten erledigen).
4. In `.pages.yml` das Präfix `feuerwehr-wicker/` entfernen (steht als Kommentar in der Datei).

---

## Schritt 5: Inhalte rechtlich prüfen (vor dem Livegang!)

| Prüfpunkt | Was zu tun ist | Wer |
|---|---|---|
| **Impressum** | Gerüst unter `/impressum`. Ergänzen: vertretungsberechtigter Vorstand (Namen), Registergericht + Vereinsregisternummer, verantwortliche Person nach § 18 Abs. 2 MStV. Die alte Seite nannte **keine** verantwortliche Person und verwies noch auf das TMG, das seit Mai 2024 durch das **DDG** ersetzt ist. | Vorstand |
| **Datenschutzerklärung** | Entwurf unter `/datenschutz`, zugeschnitten auf die neue Technik (keine Cookies, kein Tracking). Ergänzen: Hosting-Anbieter, Vorstand. Prüfen lassen, z. B. über den Datenschutzbeauftragten der Stadt oder den Landesfeuerwehrverband Hessen. | Vorstand + DSB |
| **Auftragsverarbeitung (AVV)** | Mit dem Hoster einen AV-Vertrag abschließen. Bei deutschen Hostern geht das meist per Klick im Kundenmenü. | Vorstand |
| **Bildrechte** | Gehören die Fotos dem Verein bzw. haben die Fotografen zugestimmt? Bei Fremdfotos (Presse, Stadt, Hersteller-Visualisierungen wie beim Neubau) die Genehmigung prüfen. Logos fremder Feuerwehren auf den Linkseiten im Zweifel entfernen. | Pressewart |
| **Personen auf Fotos** | Erwachsene bei Übungen und Festen: in der Regel über die Mitgliedschaft bzw. Einwilligung abgedeckt. **Kinder und Jugendliche (Minilöscher, Jugendfeuerwehr: ca. 180 Berichte!)**: Liegen schriftliche Einwilligungen der Eltern vor? Wenn nicht, Bilder mit erkennbaren Kindern entfernen oder verpixeln. | Jugendwarte, Vorstand |
| **Einsatzfotos (1.815 Stück)** | Keine erkennbaren Verletzten, Betroffenen oder Kennzeichen, keine Hausnummern. Ältere Fotos stichprobenartig prüfen. | Wehrführung |
| **Namen** | Nachrufe, Hochzeiten, Ernennungen: Diese Berichte nennen Namen. Bei Nachrufen ggf. Rücksprache mit Angehörigen; ältere private Berichte (Hochzeiten) eventuell nicht übernehmen. | Vorstand |
| **Einsatzberichte** | Keine Details, die Betroffene identifizierbar machen (Adresse, Namen). Die übernommenen Texte nennen meist nur Ort/Straße – vertretbar, aber prüfen. | Wehrführung |
| **Barrierefreiheit** | Betreibt die **Stadt** die Seite, gelten ggf. Vorgaben nach dem Hessischen Behinderten-Gleichstellungsgesetz/BITV. Die Seite ist technisch darauf vorbereitet (Prüfung mit axe: keine Fehler). | Stadt |

---

## Schritt 6: Domain umstellen (DNS) – zusammen mit dem jetzigen Hoster

**Was ist DNS?** Das Telefonbuch des Internets. Es sagt dem Browser, auf welchem Server „www.feuerwehr-wicker.de“ liegt. Beim Umzug wird dieser Eintrag auf den neuen Server geändert. Die Domain selbst bleibt dabei, wo sie ist.

### Vorbereitung (1 Woche vorher)
1. Mit dem jetzigen Hoster einen Termin vereinbaren (ca. 30 Minuten, gern abends).
2. Ihn bitten, die **TTL** der DNS-Einträge auf 300 Sekunden zu senken. Dann wirkt die Umstellung später in Minuten statt Stunden.
3. **E-Mail nicht vergessen!** Wenn Adressen wie info@ oder wehrfuehrung@feuerwehr-wicker.de über den jetzigen Hoster laufen, müssen die **MX-Einträge** unverändert bleiben. Beim Umzug ändern wir **nur** die Einträge für die Website (A/AAAA bzw. CNAME), nicht die Mail.
4. Eine **Sicherung** der alten Seite erstellen lassen (Dateien + Datenbank), auch wegen des internen Bereichs.

### Umstellung (am Termin)
Je nach Hosting:

- **Deutscher Hoster (Option B):** Domain beim neuen Hoster als „externe Domain“ hinzufügen. Der Hoster nennt eine IP-Adresse. Beim jetzigen Domain-Verwalter den **A-Eintrag** (und ggf. AAAA) für `feuerwehr-wicker.de` und `www` auf diese IP ändern.
- **Netlify (Option C):** In Netlify „Domain management → Add domain“ → `www.feuerwehr-wicker.de`. Netlify zeigt an, welcher Eintrag gesetzt werden muss, typischerweise `www` als **CNAME** auf `<name>.netlify.app` und für `feuerwehr-wicker.de` einen A-Eintrag auf die Netlify-IP.

Danach:
1. 10–60 Minuten warten. Prüfen kann man das unter https://dnschecker.org.
2. SSL-Zertifikat beim neuen Hoster aktivieren bzw. bei Netlify automatisch abwarten.
3. Testen: https://www.feuerwehr-wicker.de, eine alte Adresse wie `…/index_main.php?page=1096` (muss auf den neuen Bericht weiterleiten) und eine E-Mail an info@ (muss weiter ankommen).

### Langfristig: Domain auf den Verein übertragen
Bei .de-Domains geht das über einen **Inhaberwechsel** (beim bisherigen Anbieter beantragen) oder einen **Providerwechsel mit AuthInfo-Code**: Der bisherige Inhaber fordert den Code an, der Verein gibt ihn beim neuen Anbieter ein. Kosten: ca. 0–15 € pro Jahr für die Domain.

---

## Schritt 7: Weiterleitungen alter Links

Ist schon vorbereitet. Alle 678 alten Seitenadressen und 1.540 Einsatzadressen leiten automatisch auf die neue Seite um. So bleiben Google-Treffer, Facebook-Posts und Lesezeichen gültig.

- Apache-Hoster (ALL-INKL, Hetzner, IONOS, Strato …): über `public/.htaccess` (wird automatisch mit hochgeladen).
- Netlify: über `public/_redirects`.
- Jeder andere Hoster: Fallback über die 404-Seite (`public/weiterleitungen.json`).

Neu erzeugen nach Änderungen: `node scripts/weiterleitungen.mjs` (läuft beim Build automatisch).

Nach dem Livegang: In der **Google Search Console** (kostenlos) die Website anmelden und die Sitemap `https://www.feuerwehr-wicker.de/sitemap-index.xml` einreichen. Dann findet Google die neuen Seiten schneller.

---

## Schritt 8: Alte Seite abschalten

1. Nach 1–2 Wochen erfolgreichem Betrieb die alte PHP-Seite **vollständig** vom Server entfernen lassen, nicht nur verstecken. Die Datenbank mit den Mitgliederdaten (interner Bereich) sicher archivieren oder löschen. Sie enthält vermutlich Gesundheitsdaten (Tauglichkeiten).
2. Den Hoster auf die Beobachtung zu `security_show_epicture.php` hinweisen (siehe Inventar, Punkt 5).

---

## Laufende Kosten (Beispielrechnung)

| Posten | pro Jahr |
|---|---|
| Domain .de | 0 – 15 € |
| Hosting (Option B) | 25 – 70 € |
| GitHub (kostenlos für private Repositories) | 0 € |
| Pages CMS (kostenlos, Open Source) | 0 € |
| **Summe** | **ca. 25 – 85 €** |

---

## Technik-Spickzettel (für Helfer mit etwas IT-Erfahrung)

```bash
cd feuerwehr-wicker
npm install          # einmalig
npm run dev          # lokale Vorschau auf http://localhost:4321 (Live-Neuladen)
npm run build        # fertige Website nach dist/ (inkl. Suchindex)
npm run preview      # gebaute Website lokal ansehen
```
Voraussetzung: Node.js 20 oder neuer.
