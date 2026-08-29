import { useEffect, useState } from 'react';
import Layout from '../components/layout/Layout';
import { getAttacks } from '../api/endpoints';
import toast from 'react-hot-toast';
import { Search } from 'lucide-react';

export default function AttacksHistory() {
  const [data, setData] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAttacks()
      .then((res) => setData(res.data.data || []))
      .catch(() => toast.error('Failed to load attacks'))
      .finally(() => setLoading(false));
  }, []);

  const filtered = data.filter(
    (d) =>
      d.attack?.toLowerCase().includes(search.toLowerCase()) ||
      d.description?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Layout title="Attacks History">
      {loading ? (
        <div className="page-loading"><span className="spinner spinner-lg" /></div>
      ) : (
        <div className="table-card full-table-card">
          <div className="table-header-row">
            <h3 className="table-title">All Attacks</h3>
            <div className="search-box">
              <Search size={14} />
              <input
                type="text"
                placeholder="Search attack type..."
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
                  <th>Attack Type</th>
                  <th>Description</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {filtered.length === 0 ? (
                  <tr><td colSpan={4} className="table-empty">No attacks found</td></tr>
                ) : (
                  filtered.map((atk) => (
                    <tr key={atk.attack_id}>
                      <td className="td-mono">{atk.attack_id}</td>
                      <td><span className="badge badge-attack">{atk.attack}</span></td>
                      <td className="td-desc">{atk.description}</td>
                      <td className="td-muted">
                        {atk.date ? new Date(String(atk.date).replace(/-/g, '/')).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : '—'}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </Layout>
  );
}
