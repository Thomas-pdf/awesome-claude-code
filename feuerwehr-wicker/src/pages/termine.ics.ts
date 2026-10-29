import type { APIRoute } from 'astro';
import { termine, bereichName } from '../lib/inhalte';
import { SITE } from '../lib/site';

// iCalendar-Feed aller kommenden und der letzten 60 Tage Termine (zum Abonnieren in Handy/Outlook).
const esc = (s: string) => s.replace(/\\/g, '\\\\').replace(/;/g, '\;').replace(/,/g, '\\,').replace(/\r?\n/g, '\\n');
const ymd = (d: Date) => d.toISOString().slice(0, 10).replace(/-/g, '');
const fold = (l: string) => l.match(/.{1,73}/g)!.join('\r\n ');

export const GET: APIRoute = async () => {
  const grenze = Date.now() - 60 * 864e5;
  const liste = (await termine()).filter((t) => t.data.datum.valueOf() >= grenze);
  const zeilen = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Feuerwehr Wicker//Termine//DE', 'CALSCALE:GREGORIAN', `X-WR-CALNAME:${SITE.kurz}`, 'X-WR-TIMEZONE:Europe/Berlin'];
  for (const t of liste) {
    const tag = ymd(t.data.datum);
    zeilen.push('BEGIN:VEVENT', `UID:${t.id.replace(/\//g, '-')}@feuerwehr-wicker.de`, `DTSTAMP:${new Date().toISOString().replace(/[-:]/g, '').slice(0, 15)}Z`);
    if (t.data.beginn) {
      zeilen.push(`DTSTART;TZID=Europe/Berlin:${tag}T${t.data.beginn.replace(':', '')}00`);
      if (t.data.ende) zeilen.push(`DTEND;TZID=Europe/Berlin:${tag}T${t.data.ende.replace(':', '')}00`);
    } else {
      zeilen.push(`DTSTART;VALUE=DATE:${tag}`);
    }
    zeilen.push(fold(`SUMMARY:${esc(t.data.titel)}`));
    if (t.data.ort) zeilen.push(fold(`LOCATION:${esc(t.data.ort)}`));
    zeilen.push(fold(`CATEGORIES:${esc(bereichName(t.data.kategorie))}`));
    if (t.body?.trim()) zeilen.push(fold(`DESCRIPTION:${esc(t.body.trim())}`));
    zeilen.push('END:VEVENT');
  }
  zeilen.push('END:VCALENDAR');
  return new Response(zeilen.join('\r\n'), { headers: { 'Content-Type': 'text/calendar; charset=utf-8' } });
};
