# 4. Mitgliederbereich: sichere Architektur für den Echtbetrieb

## Ausgangslage

Die alte Seite hatte einen passwortgeschützten Bereich für ca. 100–150 Aktive mit:
- Anmeldung zu Übungsdiensten und Lehrgängen
- Anzeige eigener Tauglichkeiten (z. B. G26.3-Untersuchung, Atemschutz-Belastungsübung)
- Newsletter/Benachrichtigungen über einen E-Mail-Verteiler

Der Prototyp zeigt unter **`/intern`** eine **Demo mit erfundenen Daten**: Wie könnte das künftig aussehen? Die Demo speichert nichts auf einem Server. Zu- und Absagen werden nur im eigenen Browser simuliert.

## Die wichtigste Erkenntnis vorweg

**Tauglichkeiten sind Gesundheitsdaten** (Art. 9 DSGVO, „besondere Kategorien personenbezogener Daten“). Dafür gelten die strengsten Regeln: Zugriffskonzept, Verschlüsselung, Protokollierung, ggf. eine Datenschutz-Folgenabschätzung, Auftragsverarbeitungsverträge, Löschfristen. **Ein selbst programmierter Mitgliederbereich auf einem privat betreuten PHP-Server – wie bisher – ist dafür nicht mehr vertretbar.** Das zeigt nicht zuletzt die BSI-Meldung.

Deshalb gilt: **Öffentliche Website und Mitgliederbereich strikt trennen.**

```
                    ┌──────────────────────────────┐
  Bürger/Presse ──▶ │  www.feuerwehr-wicker.de      │  statisch, keine Daten,
                    │  (diese neue Website)         │  kein Login, kein PHP
                    └───────────────┬──────────────┘
                                    │ Link „Mitglieder-Login“
                                    ▼
                    ┌──────────────────────────────┐
  Aktive ─────────▶ │  Fachsoftware / Mitglieder-   │  eigener Anbieter, eigene
   (2FA-Login)      │  bereich (getrennt)           │  Domain/Subdomain, AVV,
                    │  Dienste · Lehrgänge ·        │  Rechte & Rollen,
                    │  Tauglichkeiten · Verteiler   │  Backups, Protokoll
                    └──────────────────────────────┘
```

## Optionen im Vergleich

### Option 1: Fertige Feuerwehr-Fachsoftware (⭐ Empfehlung)

In Hessen und bundesweit verbreitete Lösungen decken genau diese Funktionen ab, teilweise bereits über **Stadt oder Kreis lizenziert**:

| Lösung | Typische Funktionen | Hinweise |
|---|---|---|
| **FeuerOn** | Personalverwaltung, Lehrgänge (Anmeldung über Kreis/Land), Qualifikationen, Untersuchungsfristen, Dienstbuch | In Hessen weit verbreitet, häufig von Kreis/Stadt bereitgestellt. **Erste Frage an den Stadtbrandinspektor: Nutzt Flörsheim/MTK das bereits?** |
| **DIVERA 24/7** | Alarmierung/Rückmeldung, Verfügbarkeit, Termine mit Zu-/Absage, Push-Nachrichten, Gruppen/Verteiler, App | Kostenpflichtig je Einheit. Sehr gute Handy-App, oft schon für die Alarmierung im Einsatz |
| **MP-FEUER** | Personal, Atemschutz-/Geräteprüfungen, Untersuchungen, Lehrgänge | Verwaltungsorientiert, oft kommunal lizenziert |

**Vorteile:** professioneller Datenschutz und Sicherheit (AVV, Rechenzentrum, Updates), Apps fürs Handy, Rollen/Rechte, häufig schon vorhanden oder günstig über die Stadt, kein ehrenamtlicher Programmier- und Wartungsaufwand.
**Nachteile:** laufende Lizenzkosten (sofern nicht über Stadt/Kreis), Design nicht frei wählbar, Abhängigkeit vom Anbieter.

### Option 2: Fertige Standardbausteine kombinieren

- **Termine & Zu-/Absagen:** z. B. Nextcloud (Kalender + Umfragen) bei einem deutschen Anbieter, oder ein Gruppen-Kalender-Tool
- **Verteiler/Newsletter:** Mailingliste beim E-Mail-Anbieter des Vereins oder ein DSGVO-konformes Newsletter-Tool mit Servern in der EU
- **Tauglichkeiten:** **nicht** in solchen Allzweck-Tools speichern. Besser in der Fachsoftware (Option 1) oder weiter offline durch den Atemschutzbeauftragten

**Vorteile:** günstig, flexibel. **Nachteile:** mehrere Logins, Gesundheitsdaten-Problem bleibt ungelöst, Pflegeaufwand.

### Option 3: Eigenbau (wie in der Demo dargestellt)

Technisch sauber umgesetzt hieße das:
- eigene Anwendung unter `intern.feuerwehr-wicker.de`, **getrennt** von der öffentlichen Seite
- modernes Framework + Datenbank bei einem EU-Anbieter, Login mit **Zwei-Faktor-Authentifizierung**, Rollen (Mitglied, Gruppenführer, Wehrführung, Atemschutzwart, Admin)
- Verschlüsselung, Protokollierung aller Zugriffe auf Gesundheitsdaten, automatische Backups, regelmäßige Updates
- vor dem Start: Datenschutz-Folgenabschätzung, Sicherheitsprüfung (Pentest)

**Vorteile:** genau passend, eigenes Design (wie die Demo).
**Nachteile:** hoher Aufwand (realistisch mehrere Wochen Entwicklung plus dauerhafte Wartung), Haftungsrisiko für den Verein, Abhängigkeit von einzelnen Ehrenamtlichen. **Genau dieses Risiko hat zur BSI-Meldung geführt.**

## Empfehlung

1. **Beim Stadtbrandinspektor bzw. der Stadt nachfragen**, welche Fachsoftware (FeuerOn, DIVERA, MP-FEUER …) bereits genutzt oder angeboten wird. Das ist meist die schnellste, sicherste und günstigste Lösung.
2. Dienst-/Lehrgangsanmeldung, Tauglichkeiten und Verteiler **dort** abbilden.
3. Auf der neuen Website nur einen gut sichtbaren Link **„Mitglieder-Login“** anbieten, der zur Fachsoftware führt (ist im Prototyp schon vorgesehen: oben rechts „Mitglieder“).
4. Die Demo `/intern` dient als **Anforderungsliste und Gesprächsgrundlage**: „So soll es sich für unsere Aktiven anfühlen.“
5. Die **alte Mitglieder-Datenbank** nach dem Umzug sicher exportieren (für die Übernahme) und anschließend löschen. Kein Weiterbetrieb des alten PHP-Logins.

## Was die Demo zeigt (Funktionsumfang als Anforderungsliste)

| Funktion | In der Demo | Anforderung an die echte Lösung |
|---|---|---|
| Login | Formular (jede Eingabe führt in die Demo) | persönliches Konto, 2FA, Passwort-Reset per E-Mail |
| Übersicht | Kennzahlen, Fristen-Warnungen, nächster Dienst | Dashboard mit persönlichen Hinweisen |
| Dienste & Übungen | echte öffentliche Übungstermine, Zu-/Absage | Rückmeldung, Teilnehmerübersicht für Führungskräfte, Erinnerung |
| Lehrgänge | Angebote, Status (offen/angemeldet/bestanden), Interesse melden | Bewerbung → Freigabe Wehrführung → Meldung an Kreis |
| Tauglichkeiten | Ampel (gültig / läuft ab / abgelaufen) mit Restlaufzeit | Pflege nur durch Berechtigte, Erinnerung 60 Tage vorher, Sichtbarkeit nur für die Person selbst + Wehrführung/Atemschutzwart |
| Nachrichten & Verteiler | Rundmails, Verteiler an-/abwählen (Pflichtverteiler gesperrt) | Verteiler je Gruppe, Abmeldung möglich (außer Dienstverteiler), Push optional |
| Dokumente | Musterliste | Ablage mit Rechten (z. B. AAO, Protokolle) |
