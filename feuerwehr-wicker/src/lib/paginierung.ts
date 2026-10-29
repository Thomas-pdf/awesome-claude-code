import { berichte } from './inhalte';
export const PRO_SEITE = 24;
export async function jahreListe() {
  const alle = await berichte();
  return [...new Set(alle.map((b) => String(b.data.date.getUTCFullYear())))].sort().reverse();
}
export const seitenzahl = (n: number) => Math.max(1, Math.ceil(n / PRO_SEITE));
export const ausschnitt = <T,>(l: T[], seite: number) => l.slice((seite - 1) * PRO_SEITE, seite * PRO_SEITE);
