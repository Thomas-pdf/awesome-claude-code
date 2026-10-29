// Zentrale Stammdaten – hier ändern, wirkt überall (Kopf, Fuß, Impressum, SEO).
export const SITE = {
  name: 'Freiwillige Feuerwehr Flörsheim-Wicker',
  kurz: 'Feuerwehr Wicker',
  verein: 'Freiwillige Feuerwehr Wicker 1925 e.V.',
  gegruendet: 1925,
  strasse: 'Flörsheimer Str. 2',
  plz: '65439',
  ort: 'Flörsheim am Main',
  ortsteil: 'Wicker',
  telefon: '06145 7873',
  telefonLink: '+4961457873',
  fax: '06145 941099',
  email: 'info@feuerwehr-wicker.de',
  emailWehrfuehrung: 'wehrfuehrung@feuerwehr-wicker.de',
  facebook: 'https://www.facebook.com/FeuerwehrWicker',
  instagram: '',
  beschreibung:
    'Die Freiwillige Feuerwehr Flörsheim-Wicker: 365 Tage im Jahr, rund um die Uhr ehrenamtlich für Sie im Einsatz. Aktuelles, Einsätze, Termine, Jugendfeuerwehr, Minilöscher und Verein.',
  geo: { lat: 50.0057, lon: 8.4113 },
};

export const UEBUNGSZEITEN = [
  { gruppe: 'Einsatzabteilung', zeit: 'Donnerstag ab 19:00 Uhr (Übung) · Samstag ab 13:30 Uhr (Technischer Dienst)', link: '/einsatzabteilung' },
  { gruppe: 'Jugendfeuerwehr', zeit: 'Montag 18:30 – 20:30 Uhr', link: '/jugendfeuerwehr', alter: '10 – 17 Jahre' },
  { gruppe: 'Minilöscher', zeit: 'Montag 16:30 – 18:00 Uhr (Termine im Kalender)', link: '/miniloescher', alter: '6 – 10 Jahre' },
  { gruppe: 'Alters- & Ehrenabteilung', zeit: 'Regelmäßige Treffen – Termine siehe Kalender', link: '/verein' },
];
