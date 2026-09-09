export function EntryCard({ e }) {
  return (
    <a className="entry-card" href={'/entry/' + e.id}>
      <div className="meta-row">
        <span className="chip domain">{e.domain}</span>
        {e.subdomain ? <span className="chip">{e.subdomain}</span> : null}
        <span className="chip">{e.type}</span>
        <span className={'chip src-' + e.provenance_source}>{e.provenance_source.replace('_', ' ')}</span>
        <span className={'chip tier-' + e.tier}>{e.tier}</span>
        {e.status !== 'active' ? <span className={'chip st-' + e.status}>{e.status}</span> : null}
      </div>
      <h3>{e.title}</h3>
      {e.content_body ? <p className="preview">{e.content_body}</p> : null}
      <div className="mono receipt">⬡ {e.receipt_id ? e.receipt_id.slice(0, 24) + '…' : ''}</div>
      <div className="mono timestamp" style={{ fontSize: 11, marginTop: 4 }}>
        {new Date(e.created_at).toISOString()}
      </div>
    </a>
  );
}
