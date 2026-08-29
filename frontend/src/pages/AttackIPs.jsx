import { useEffect, useState } from 'react';
import Layout from '../components/layout/Layout';
import AttackIPsTable from '../components/tables/AttackIPsTable';
import { getAttackIPs } from '../api/endpoints';
import toast from 'react-hot-toast';

export default function AttackIPsPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAttackIPs()
      .then((res) => setData(res.data))
      .catch(() => toast.error('Failed to load attack IPs'))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout title="Attack IPs">
      {loading ? (
        <div className="page-loading"><span className="spinner spinner-lg" /></div>
      ) : (
        <AttackIPsTable data={data} />
      )}
    </Layout>
  );
}
