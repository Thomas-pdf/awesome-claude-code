// ⚠️ DEMO-DATEN – frei erfunden, keine echten Personen oder Qualifikationen.
const heute = new Date();
const tage = (n: number) => new Date(heute.valueOf() + n * 864e5).toISOString().slice(0, 10);

export const DEMO_MITGLIED = {
  vorname: 'Alex',
  nachname: 'Muster',
  funktion: 'Truppführer/in · Atemschutzgeräteträger/in',
  eintritt: '2014',
  abteilung: 'Einsatzabteilung',
};

export type Status = 'ok' | 'bald' | 'abgelaufen';
export const DEMO_TAUGLICHKEITEN = [
  { name: 'Arbeitsmedizinische Untersuchung (G26.3)', gueltigBis: tage(410), hinweis: 'Atemschutztauglichkeit' },
  { name: 'Belastungsübung Atemschutz-Übungsstrecke', gueltigBis: tage(38), hinweis: 'jährlich, nächster Termin Feuerwehrhaus Hochheim' },
  { name: 'Einsatzübung unter Atemschutz', gueltigBis: tage(-12), hinweis: 'jährlich – bitte nachholen' },
  { name: 'Unterweisung Motorkettensäge', gueltigBis: tage(260), hinweis: 'MKS-Weiterbildung' },
  { name: 'Erste-Hilfe-Ausbildung', gueltigBis: tage(700), hinweis: 'alle 2 Jahre' },
  { name: 'Führerschein Klasse C', gueltigBis: tage(1500), hinweis: 'Maschinist StLF 20V / LF 10' },
];

export const DEMO_QUALIFIKATIONEN = [
  'Truppmann Teil 1 & 2', 'Sprechfunker', 'Atemschutzgeräteträger', 'Truppführer', 'Technische Hilfe VU', 'Maschinist', 'Motorkettensäge Modul A/B',
];

export const DEMO_LEHRGAENGE = [
  { titel: 'Gruppenführer (F III)', ort: 'Hessische Landesfeuerwehrschule Kassel', zeitraum: `${tage(95)} – ${tage(106)}`, plaetze: 1, status: 'offen' },
  { titel: 'Atemschutzgeräteträger', ort: 'Kreisausbildung MTK, Hofheim', zeitraum: `${tage(40)} – ${tage(54)}`, plaetze: 3, status: 'angemeldet' },
  { titel: 'Technische Hilfe – Verkehrsunfall', ort: 'Feuerwehrhaus Flörsheim', zeitraum: tage(22), plaetze: 6, status: 'offen' },
  { titel: 'Sprechfunker Digitalfunk', ort: 'Online + Feuerwehrhaus Hattersheim', zeitraum: `${tage(60)} – ${tage(62)}`, plaetze: 4, status: 'offen' },
  { titel: 'Maschinist für Löschfahrzeuge', ort: 'Kreisausbildung MTK', zeitraum: `${tage(-80)} – ${tage(-70)}`, plaetze: 0, status: 'bestanden' },
];

export const DEMO_VERTEILER = [
  { id: 'ea', name: 'Einsatzabteilung – Dienstbetrieb', beschreibung: 'Übungen, Dienstplan, Änderungen', aktiv: true, pflicht: true },
  { id: 'as', name: 'Atemschutz', beschreibung: 'Übungsstrecke, Untersuchungen, Wartung', aktiv: true },
  { id: 'lg', name: 'Lehrgänge & Seminare', beschreibung: 'Neue Angebote von Kreis und Land', aktiv: true },
  { id: 'ver', name: 'Verein', beschreibung: 'Feste, JHV, Kameradschaftsabend', aktiv: false },
  { id: 'jf', name: 'Jugendwarte & Betreuer', beschreibung: 'Organisation Jugendfeuerwehr', aktiv: false },
];

export const DEMO_NACHRICHTEN = [
  { datum: tage(-1), von: 'Wehrführung', betreff: 'Übung Donnerstag: Treffpunkt Neubau-Baustelle (Objektbegehung)', neu: true },
  { datum: tage(-4), von: 'Atemschutzwart', betreff: 'Neue Termine Atemschutzstrecke Hochheim – bitte eintragen', neu: true },
  { datum: tage(-9), von: 'Gerätewart', betreff: 'StLF 20V: Einweisung für Maschinisten abgeschlossen', neu: false },
  { datum: tage(-16), von: 'Vorstand', betreff: 'Einladung Kameradschaftsabend', neu: false },
];

export const DEMO_DOKUMENTE = [
  { titel: 'Alarm- und Ausrückeordnung (Muster)', typ: 'PDF' },
  { titel: 'Dienstplan 1. Halbjahr (Muster)', typ: 'PDF' },
  { titel: 'Checkliste Fahrzeugübernahme StLF 20V (Muster)', typ: 'PDF' },
  { titel: 'Protokoll Feuerwehrausschuss (Muster)', typ: 'PDF' },
];
