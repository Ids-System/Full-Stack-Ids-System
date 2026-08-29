import { useState } from 'react';
import Layout from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { changePassword } from '../api/endpoints';
import toast from 'react-hot-toast';
import { User, Lock, ShieldCheck } from 'lucide-react';

export default function Profile() {
  const { user } = useAuth();
  const [form, setForm] = useState({ old_password: '', new_password: '', confirm: '' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.new_password !== form.confirm) {
      toast.error('Passwords do not match');
      return;
    }
    setLoading(true);
    try {
      await changePassword({ old_password: form.old_password, new_password: form.new_password });
      toast.success('Password updated!');
      setForm({ old_password: '', new_password: '', confirm: '' });
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout title="Profile">
      <div className="profile-grid">
        {/* User Info Card */}
        <div className="glass-card profile-card">
          <div className="profile-avatar">
            <User size={40} />
          </div>
          <h2 className="profile-name">{user?.username}</h2>
          <p className="profile-email">{user?.email}</p>
          <div className="profile-role-badge">
            <ShieldCheck size={14} />
            {user?.role}
          </div>
        </div>

        {/* Change Password Card */}
        <div className="glass-card">
          <h3 className="card-title">
            <Lock size={16} /> Change Password
          </h3>
          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>Current Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={form.old_password}
                onChange={(e) => setForm({ ...form, old_password: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>New Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={form.new_password}
                onChange={(e) => setForm({ ...form, new_password: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Confirm New Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={form.confirm}
                onChange={(e) => setForm({ ...form, confirm: e.target.value })}
                required
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? <span className="spinner" /> : 'Update Password'}
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}
