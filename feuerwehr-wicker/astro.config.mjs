// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Die spätere Live-Adresse. Für die Vorschau egal, für SEO/Sitemap wichtig.
const SITE = process.env.SITE_URL || 'https://www.feuerwehr-wicker.de';

export default defineConfig({
  site: SITE,
  base: process.env.BASE_PATH || '/',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  integrations: [
    sitemap({ filter: (page) => !page.includes('/intern') }),
  ],
  markdown: {
    smartypants: false,
  },
});
