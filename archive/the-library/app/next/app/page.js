import { supabase, DOMAINS, CONSENT_GATED } from '../lib/supabase';
import { EntryCard } from './entry-card';

export const dynamic = 'force-dynamic';

export default async function Home() {
  const { count } = await supabase
    .from('mc_entries')
    .select('*', { count: 'exact', head: true });

  const { data: entries } = await supabase
    .from('mc_entries')
    .select('id, title, content_body, domain, subdomain, type, provenance_source, tier, status, receipt_id, created_at')
    .order('created_at', { ascending: false })
    .limit(20);

  return (
    <main>
      <section className="hero">
        <h1>
          The living archive of{' '}
          <span style={{ color: 'var(--teal)' }}>TerAustralis</span>
        </h1>
        <p className="sub">
          Canonical memory for the project&apos;s works, decisions, and canon — plus a curated
          index outward. Reads open to every human and AI. Writes pass through consent. Every
          entry carries its provenance: source, tier, status.
        </p>
        <p className="mono" style={{ marginTop: 14, fontSize: 14 }}>
          <span className="count">{count ?? 0}</span>{' '}
          <span style={{ color: 'var(--dim)' }}>entries in the permanent record</span>
        </p>
        <form className="searchbar" action="/search">
          <input name="q" placeholder="Search the archive…" aria-label="Search" />
          <button type="submit">Search</button>
        </form>
      </section>

      <h2 className="section-title">Domains</h2>
      <div className="domain-grid">
        {DOMAINS.map((d) => (
          <a key={d} className="domain-card" href={'/browse?d=' + encodeURIComponent(d)}>
            {d}
            {CONSENT_GATED.includes(d) && <span className="gated">consent-gated</span>}
          </a>
        ))}
      </div>

      <h2 className="section-title">Latest entries</h2>
      {(entries || []).map((e) => (
        <EntryCard key={e.id} e={e} />
      ))}
    </main>
  );
}
