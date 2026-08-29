export default function StatCard({ label, value, icon: Icon, color, sub }) {
  return (
    <div className={`stat-card stat-card--${color}`}>
      <div className="stat-card-icon">
        <Icon size={22} />
      </div>
      <div className="stat-card-body">
        <p className="stat-card-label">{label}</p>
        <h2 className="stat-card-value">{value ?? '—'}</h2>
        {sub && <p className="stat-card-sub">{sub}</p>}
      </div>
    </div>
  );
}
