import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

const COLORS = ['#00f5ff', '#7c3aed', '#f59e0b', '#10b981', '#ef4444', '#3b82f6'];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div className="chart-tooltip">
        <p className="chart-tooltip-label">{payload[0].name}</p>
        <p className="chart-tooltip-value">{payload[0].value} attacks</p>
      </div>
    );
  }
  return null;
};

export default function AttackTypeDonut({ data }) {
  const counts = {};
  (data || []).forEach((a) => {
    counts[a.attack] = (counts[a.attack] || 0) + 1;
  });
  const chartData = Object.entries(counts).map(([name, value]) => ({ name, value }));

  if (!chartData.length) {
    return (
      <div className="chart-card">
        <h3 className="chart-title">Attack Types</h3>
        <div className="chart-empty">No data yet</div>
      </div>
    );
  }

  return (
    <div className="chart-card">
      <h3 className="chart-title">Attack Types</h3>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={85}
            paddingAngle={3}
            dataKey="value"
          >
            {chartData.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            formatter={(val) => <span style={{ color: '#94a3b8', fontSize: 12 }}>{val}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
