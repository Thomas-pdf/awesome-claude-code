import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { berichte, bereichName } from '../lib/inhalte';
import { SITE } from '../lib/site';
export async function GET(context: APIContext) {
  const liste = (await berichte()).slice(0, 30);
  return rss({
    title: `${SITE.kurz} – Aktuelles`,
    description: SITE.beschreibung,
    site: context.site!,
    items: liste.map((b) => ({ title: b.data.title, pubDate: b.data.date, description: b.data.teaser, link: `/aktuelles/${b.id}/`, categories: [bereichName(b.data.bereich)] })),
    customData: '<language>de-de</language>',
  });
}
