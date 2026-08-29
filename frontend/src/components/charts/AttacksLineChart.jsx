import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Area, AreaChart,
} from 'recharts';
import { format } from 'date-fns';

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
    date: d.date ? format(new Date(d.date), 'MMM d') : '—',
    attacks: d.no_of_attacks,
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
