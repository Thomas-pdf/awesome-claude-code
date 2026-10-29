export type NavItem = { label: string; href: string; kinder?: NavItem[]; beschreibung?: string };

export const NAVIGATION: NavItem[] = [
  { label: 'Aktuelles', href: '/aktuelles' },
  { label: 'Einsätze', href: '/einsaetze' },
  { label: 'Termine', href: '/termine' },
  {
    label: 'Über uns', href: '/einsatzabteilung',
    kinder: [
      { label: 'Einsatzabteilung', href: '/einsatzabteilung', beschreibung: 'Unsere aktive Mannschaft' },
      { label: 'Fahrzeuge & Technik', href: '/einsatzabteilung/fahrzeuge', beschreibung: 'StLF 20V, LF 10, MTF, Kräder …' },
      { label: 'Ausbildung', href: '/einsatzabteilung/ausbildung', beschreibung: 'Übungen & Lehrgänge' },
      { label: 'Jugendfeuerwehr', href: '/jugendfeuerwehr', beschreibung: '10 bis 17 Jahre' },
      { label: 'Minilöscher', href: '/miniloescher', beschreibung: 'Kinderfeuerwehr ab 6 Jahren' },
      { label: 'Verein', href: '/verein', beschreibung: 'Freiwillige Feuerwehr Wicker 1925 e.V.' },
      { label: 'Chronik', href: '/verein/chronik', beschreibung: 'Seit 1925 für Wicker da' },
      { label: '100 Jahre', href: '/100-jahre', beschreibung: 'Unser Jubiläum 2025' },
    ],
  },
  { label: 'Neubau', href: '/neubau' },
  {
    label: 'Bürgerinfo', href: '/buergerinfo',
    kinder: [
      { label: 'Verhalten im Notfall', href: '/buergerinfo/verhalten-im-notfall', beschreibung: 'Richtig den Notruf absetzen' },
      { label: 'Brandschutz-Tipps', href: '/buergerinfo/brandschutz', beschreibung: 'Rauchmelder, Grillen, Silvester …' },
      { label: 'Brandschutzerziehung', href: '/brandschutzerziehung', beschreibung: 'Für Kitas & Schulen' },
      { label: 'Downloads', href: '/downloads', beschreibung: 'Jahresberichte & mehr' },
      { label: 'Links', href: '/links', beschreibung: 'Feuerwehren & Hilfsorganisationen' },
    ],
  },
];

export const FOOTER_LINKS: NavItem[] = [
  { label: 'Kontakt', href: '/kontakt' },
  { label: 'Impressum', href: '/impressum' },
  { label: 'Datenschutz', href: '/datenschutz' },
  { label: 'Barrierefreiheit', href: '/barrierefreiheit' },
  { label: 'Sitemap', href: '/sitemap' },
  { label: 'Mitgliederbereich', href: '/intern' },
];
