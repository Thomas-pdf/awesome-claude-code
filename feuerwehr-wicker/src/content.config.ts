import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Bereiche der Wehr – steuern Farben, Filter und Zuordnung.
export const BEREICHE = {
  allgemein: 'Allgemein',
  einsatzabteilung: 'Einsatzabteilung',
  jugendfeuerwehr: 'Jugendfeuerwehr',
  minis: 'Minilöscher',
  verein: 'Verein',
  neubau: 'Neubau',
  jubilaeum: '100 Jahre',
  mitmachen: 'Mitmachen',
  buergerinfo: 'Bürgerinfo',
  links: 'Links',
  downloads: 'Downloads',
} as const;
const bereich = z.enum(Object.keys(BEREICHE) as [keyof typeof BEREICHE, ...(keyof typeof BEREICHE)[]]);

/** Berichte / Neuigkeiten: src/content/berichte/<jahr>/<name>.md */
const berichte = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/berichte' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    bereich: bereich.default('allgemein'),
    teaser: z.string().optional(),
    bild: z.string().optional(),
    entwurf: z.boolean().default(false),
    alteId: z.number().optional(),
    alteUrl: z.string().optional(),
  }),
});

/** Einsätze: src/content/einsaetze/<jahr>/<jahr>-<nr>.md */
const einsaetze = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/einsaetze' }),
  schema: z.object({
    nummer: z.string(),
    datum: z.coerce.date(),
    uhrzeit: z.string().optional(),
    art: z.enum(['Brand', 'Hilfeleistung', 'Sonstiges']).default('Sonstiges'),
    stichwort: z.string(),
    einsatzort: z.string().optional(),
    alarmierung: z.string().optional(),
    dauerMinuten: z.number().optional(),
    fahrzeuge: z.string().optional(),
    kraefte: z.number().optional(),
    weitereKraefte: z.string().optional(),
    bilder: z.array(z.string()).default([]),
    alteId: z.number().optional(),
  }),
});

/** Termine: src/content/termine/<jahr>/<datum>-<name>.md */
const termine = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/termine' }),
  schema: z.object({
    titel: z.string(),
    datum: z.coerce.date(),
    beginn: z.string().optional(),
    ende: z.string().optional(),
    ort: z.string().optional(),
    kategorie: bereich.default('allgemein'),
    oeffentlich: z.boolean().default(true),
  }),
});

/** Feste Seiten (Fahrzeuge, Bürgerinfo, Verein …): src/content/seiten/*.md */
const seiten = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/seiten' }),
  schema: z.object({
    title: z.string(),
    pfad: z.string(),
    bereich: bereich.default('allgemein'),
    stand: z.coerce.date().optional(),
    reihenfolge: z.number().default(999),
    eltern: z.string().optional(),
    beschreibung: z.string().optional(),
    bild: z.string().optional(),
    alteId: z.number().optional(),
    alteUrl: z.string().optional(),
  }),
});

export const collections = { berichte, einsaetze, termine, seiten };
