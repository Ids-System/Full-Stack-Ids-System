function fmtDate(str) {
  if (!str) return '—';
  const d = new Date(String(str).replace(/-/g, '/'));
  return isNaN(d.getTime()) ? '—' : d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

export default function BlockedIPsTable({ data }) {
  return (
    <div className="table-card">
      <h3 className="table-title">Blocked IPs</h3>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>IP Address</th>
              <th>Attack</th>
              <th>Date Blocked</th>
            </tr>
          </thead>
          <tbody>
            {(data || []).length === 0 ? (
              <tr><td colSpan={4} className="table-empty">No blocked IPs</td></tr>
            ) : (
              (data || []).map((b) => (
                <tr key={b.ip_id}>
                  <td className="td-mono">{b.ip_id}</td>
                  <td className="td-mono td-highlight">{b.ip}</td>
                  <td>{b.Attack}</td>
                  <td className="td-muted">
                    {fmtDate(b.Date_of_block)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
