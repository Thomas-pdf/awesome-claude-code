import { getCollection, type CollectionEntry } from 'astro:content';
import { BEREICHE } from '../content.config';

export type Bericht = CollectionEntry<'berichte'>;
export type Einsatz = CollectionEntry<'einsaetze'>;
export type Termin = CollectionEntry<'termine'>;
export type Seite = CollectionEntry<'seiten'>;

export const bereichName = (b: string) => (BEREICHE as Record<string, string>)[b] ?? b;

const df = new Intl.DateTimeFormat('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', timeZone: 'Europe/Berlin' });
const dfLang = new Intl.DateTimeFormat('de-DE', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Berlin' });
const dfWt = new Intl.DateTimeFormat('de-DE', { weekday: 'short', timeZone: 'Europe/Berlin' });
const dfMonat = new Intl.DateTimeFormat('de-DE', { month: 'long', year: 'numeric', timeZone: 'Europe/Berlin' });
export const datum = (d: Date) => df.format(d);
export const datumLang = (d: Date) => dfLang.format(d);
export const wochentag = (d: Date) => dfWt.format(d).replace('.', '');
export const monatJahr = (d: Date) => dfMonat.format(d);

/** Alle veröffentlichten Berichte, neueste zuerst. */
export async function berichte() {
  return (await getCollection('berichte', ({ data }) => !data.entwurf)).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}
export const berichtUrl = (b: Bericht) => `/aktuelles/${b.id}`;

/** Alle Einsätze, neueste zuerst. */
export async function einsaetze() {
  return (await getCollection('einsaetze')).sort(
    (a, b) => b.data.datum.valueOf() - a.data.datum.valueOf() || (b.data.uhrzeit ?? '').localeCompare(a.data.uhrzeit ?? ''),
  );
}
export const einsatzUrl = (e: Einsatz) => `/einsaetze/${e.id}`;
export const einsatzJahr = (e: Einsatz) => e.data.datum.getUTCFullYear();

/** Termine, aufsteigend sortiert. */
export async function termine() {
  return (await getCollection('termine', ({ data }) => data.oeffentlich)).sort(
    (a, b) => a.data.datum.valueOf() - b.data.datum.valueOf() || (a.data.beginn ?? '').localeCompare(b.data.beginn ?? ''),
  );
}
/** "Heute" für die Vorschau: Build-Zeitpunkt. Seite wird bei jedem Build/Deploy neu erzeugt. */
export const heute = () => {
  const d = new Date();
  return new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
};
export async function kommendeTermine(n?: number) {
  const h = heute().valueOf();
  const t = (await termine()).filter((x) => x.data.datum.valueOf() >= h);
  return n ? t.slice(0, n) : t;
}

export async function seiten() {
  return (await getCollection('seiten')).sort((a, b) => a.data.reihenfolge - b.data.reihenfolge);
}
export async function seiteNachPfad(pfad: string) {
  return (await getCollection('seiten')).find((s) => s.data.pfad === pfad);
}
export async function unterseiten(pfad: string) {
  return (await seiten()).filter((s) => s.data.eltern === pfad);
}

export const artKlasse = (art: string) => (art === 'Brand' ? 'brand' : art === 'Hilfeleistung' ? 'hilfe' : 'sonst');
