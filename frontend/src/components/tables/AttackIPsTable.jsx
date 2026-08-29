import { useState } from 'react';
import { Search } from 'lucide-react';

export default function AttackIPsTable({ data }) {
  const [search, setSearch] = useState('');

  const filtered = (data || []).filter(
    (d) =>
      d.source_ip?.includes(search) ||
      d.destination_ip?.includes(search) ||
      d.protocol?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="table-card full-table-card">
      <div className="table-header-row">
        <h3 className="table-title">Attack IPs</h3>
        <div className="search-box">
          <Search size={14} />
          <input
            type="text"
            placeholder="Filter IPs / protocol..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Source IP</th>
              <th>Destination IP</th>
              <th>Protocol</th>
              <th>Port</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr><td colSpan={6} className="table-empty">No records</td></tr>
            ) : (
              filtered.map((ip) => (
                <tr key={ip.ip_id}>
                  <td className="td-mono">{ip.ip_id}</td>
                  <td className="td-mono td-highlight">{ip.source_ip}</td>
                  <td className="td-mono">{ip.destination_ip}</td>
                  <td><span className="badge badge-proto">{ip.protocol}</span></td>
                  <td className="td-mono">{ip.port}</td>
                  <td className="td-muted">
                    {ip.timestamp ? new Date(ip.timestamp).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '—'}
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
