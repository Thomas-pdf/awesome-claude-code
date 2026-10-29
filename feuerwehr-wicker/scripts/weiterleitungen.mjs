// Erzeugt Weiterleitungen alter Adressen (index_main.php?page=…, einsaetze.php?…enr=…)
// für Apache (.htaccess), Netlify (_redirects) und als JSON für die 404-Seite (funktioniert bei jedem Hoster).
// Aufruf: node scripts/weiterleitungen.mjs
import { readFileSync, writeFileSync } from 'node:fs';
const map = JSON.parse(readFileSync(new URL('../tools/migration/redirects.json', import.meta.url)));
const seiten = {}, einsaetze = {};
for (const [k, v] of Object.entries(map)) {
  const ziel = v.startsWith('/aktuelles?') ? '/aktuelles' : v;
  if (k.startsWith('page=')) seiten[k.slice(5)] = ziel;
  if (k.startsWith('enr=')) einsaetze[k.slice(4)] = ziel;
}
writeFileSync(new URL('../public/weiterleitungen.json', import.meta.url), JSON.stringify({ seiten, einsaetze }));

const ht = ['# Weiterleitungen der alten Website (automatisch erzeugt)', 'RewriteEngine On', 'ErrorDocument 404 /404.html', '',
  '# HTTPS erzwingen', 'RewriteCond %{HTTPS} off', 'RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]', ''];
for (const [n, z] of Object.entries(seiten)) {
  ht.push(`RewriteCond %{QUERY_STRING} (^|&)page=${n}(&|$)`, `RewriteRule ^(index_main|main|menu)\\.php$ ${z}? [L,R=301]`);
}
for (const [n, z] of Object.entries(einsaetze)) {
  ht.push(`RewriteCond %{QUERY_STRING} (^|&)enr=${n}(&|$)`, `RewriteRule ^einsaetze\\.php$ ${z}? [L,R=301]`);
}
ht.push('RewriteRule ^einsaetze\\.php$ /einsaetze? [L,R=301]', 'RewriteRule ^termine\\.php$ /termine? [L,R=301]',
  'RewriteRule ^(index|index_main|main|startseite)\\.php$ /? [L,R=301]', 'RewriteRule ^(sitemap|search)\\.php$ /sitemap? [L,R=301]',
  'RewriteRule ^i_login\\.php$ /intern? [L,R=301]', '',
  '# Sicherheits-Header', '<IfModule mod_headers.c>',
  '  Header always set X-Content-Type-Options "nosniff"', '  Header always set Referrer-Policy "strict-origin-when-cross-origin"',
  '  Header always set X-Frame-Options "SAMEORIGIN"', '  Header always set Permissions-Policy "geolocation=(), camera=(), microphone=()"',
  '  Header always set Strict-Transport-Security "max-age=31536000"',
  "  Header always set Content-Security-Policy \"default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'wasm-unsafe-eval'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'\"",
  '</IfModule>');
writeFileSync(new URL('../public/.htaccess', import.meta.url), ht.join('\n') + '\n');

// Netlify: Query-Parameter-Abgleich je Wert
const nl = ['# Weiterleitungen der alten Website (automatisch erzeugt)'];
for (const [n, z] of Object.entries(seiten)) nl.push(`/index_main.php page=${n} ${z} 301!`, `/main.php page=${n} ${z} 301!`);
for (const [n, z] of Object.entries(einsaetze)) nl.push(`/einsaetze.php enr=${n} ${z} 301!`);
nl.push('/einsaetze.php /einsaetze 301!', '/termine.php /termine 301!', '/index_main.php / 301!', '/index.php / 301!', '/i_login.php /intern 301!');
writeFileSync(new URL('../public/_redirects', import.meta.url), nl.join('\n') + '\n');
console.log(`Weiterleitungen: ${Object.keys(seiten).length} Seiten, ${Object.keys(einsaetze).length} Einsätze`);
