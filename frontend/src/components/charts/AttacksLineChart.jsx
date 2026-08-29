import {
  Tooltip,
  ResponsiveContainer, Area, AreaChart, XAxis, YAxis, CartesianGrid,
} from 'recharts';

// Safely parse YYYY-MM-DD or ISO strings without timezone-shift issues
function parseDate(dateStr) {
  if (!dateStr) return null;
  // "2026-08-29" → treat as local date by replacing - with /
  const d = new Date(String(dateStr).replace(/-/g, '/'));
  return isNaN(d.getTime()) ? null : d;
}

function fmtDate(dateStr) {
  const d = parseDate(dateStr);
  if (!d) return '—';
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="chart-tooltip">
        <p className="chart-tooltip-label">{label}</p>
        <p className="chart-tooltip-value">{payload[0].value} attacks</p>
      </div>
    );
  }
  return null;
};

export default function AttacksLineChart({ data }) {
  const chartData = (data || []).map((d) => ({
    date: fmtDate(d.date),
    attacks: d.no_of_attacks ?? 0,
  }));

  return (
    <div className="chart-card">
      <h3 className="chart-title">Attacks Per Day</h3>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="attackGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#00f5ff" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#00f5ff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="date" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
          <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
          <Tooltip content={<CustomTooltip />} />
          <Area type="monotone" dataKey="attacks" stroke="#00f5ff" strokeWidth={2} fill="url(#attackGrad)" dot={{ r: 3, fill: '#00f5ff' }} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
