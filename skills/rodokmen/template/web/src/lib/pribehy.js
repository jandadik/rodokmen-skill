// Seznam všech příběhů: hlavní (web.json → pribeh, text generated/pribeh.md) + další (web.json → dalsi_pribehy).
// Každý příběh má vlastní stránku /pribehy/<slug>/, stránka /pribehy/ je jejich rozcestník.
import { config } from './data.js';

const hlavni = import.meta.glob('../generated/pribeh.md', { eager: true });
const dalsi = import.meta.glob('../generated/pribehy/*.md', { eager: true });

export const hlavniSlug = config.pribeh?.slug || 'hlavni';

export const pribehy = [
  ...(config.maPribeh && hlavni['../generated/pribeh.md']
    ? [{ ...config.pribeh, slug: hlavniSlug, hlavni: true, mod: hlavni['../generated/pribeh.md'] }]
    : []),
  ...(config.dalsi_pribehy ?? [])
    .filter((d) => dalsi[`../generated/pribehy/${d.slug}.md`])
    .map((d) => ({ ...d, hlavni: false, mod: dalsi[`../generated/pribehy/${d.slug}.md`] })),
].map((p) => ({ ...p, title: p.mod.frontmatter.title, lead: p.mod.frontmatter.lead, url: `/pribehy/${p.slug}/` }));
