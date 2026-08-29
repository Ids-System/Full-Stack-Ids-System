import { format } from 'date-fns';

const SEVERITY_CLASS = {
  critical: 'badge-critical',
  high: 'badge-high',
  medium: 'badge-medium',
  low: 'badge-low',
};

export default function AlertsTable({ data }) {
  return (
    <div className="table-card">
      <h3 className="table-title">Alerts</h3>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Attack ID</th>
              <th>Severity</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {(data || []).length === 0 ? (
              <tr><td colSpan={4} className="table-empty">No alerts</td></tr>
            ) : (
              (data || []).map((a) => (
                <tr key={a.alert_id}>
                  <td className="td-mono">{a.alert_id}</td>
                  <td className="td-mono">{a.Attackid}</td>
                  <td>
                    <span className={`badge ${SEVERITY_CLASS[a.severity?.toLowerCase()] || 'badge-low'}`}>
                      {a.severity}
                    </span>
                  </td>
                  <td className="td-muted">
                    {a.timestamp ? format(new Date(a.timestamp), 'MMM d, HH:mm:ss') : '—'}
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
