import { useEffect, useState } from 'react';
import Layout from '../components/layout/Layout';
import Modal from '../components/ui/Modal';
import {
  getAllUsers, addUser, updateRole, deleteUser,
  clearAttackHistory, exportReport,
} from '../api/endpoints';
import toast from 'react-hot-toast';
import { UserPlus, Trash2, ShieldCheck, Download, AlertTriangle, X } from 'lucide-react';

const ROLES = ['observer', 'admin'];

export default function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showClearModal, setShowClearModal] = useState(false);
  const [roleModal, setRoleModal] = useState(null); // { email, role }
  const [newUser, setNewUser] = useState({ name: '', email: '', password: '' });
  const [exporting, setExporting] = useState(false);

  const fetchUsers = () => {
    getAllUsers().then((res) => setUsers(res.data)).catch(() => toast.error('Failed to fetch users'));
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleAddUser = async (e) => {
    e.preventDefault();
    try {
      await addUser(newUser);
      toast.success('User added');
      setShowAddModal(false);
      setNewUser({ name: '', email: '', password: '' });
      fetchUsers();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to add user');
    }
  };

  const handleUpdateRole = async () => {
    try {
      await updateRole({ email: roleModal.email, role: roleModal.role });
      toast.success('Role updated');
      setRoleModal(null);
      fetchUsers();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to update role');
    }
  };

  const handleDeleteUser = async (email) => {
    try {
      await deleteUser({ email });
      toast.success('User removed');
      fetchUsers();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete user');
    }
  };

  const handleClear = async () => {
    try {
      await clearAttackHistory();
      toast.success('Attack history cleared');
      setShowClearModal(false);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to clear history');
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const res = await exportReport();
      const url = URL.createObjectURL(new Blob([res.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = 'ids_security_report.pdf';
      a.click();
      URL.revokeObjectURL(url);
      toast.success('Report downloaded');
    } catch {
      toast.error('Export failed');
    } finally {
      setExporting(false);
    }
  };

  return (
    <Layout title="Admin Panel">
      {/* Actions Row */}
      <div className="admin-actions">
        <button className="btn btn-primary" onClick={() => setShowAddModal(true)}>
          <UserPlus size={16} /> Add User
        </button>
        <button className="btn btn-outline" onClick={handleExport} disabled={exporting}>
          <Download size={16} /> {exporting ? 'Exporting...' : 'Export PDF'}
        </button>
        <button className="btn btn-danger" onClick={() => setShowClearModal(true)}>
          <AlertTriangle size={16} /> Clear Attack History
        </button>
      </div>

      {/* Users Table */}
      <div className="table-card full-table-card">
        <h3 className="table-title">All Users</h3>
        <div className="table-wrapper">
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr><td colSpan={5} className="table-empty">No users</td></tr>
              ) : (
                users.map((u) => (
                  <tr key={u.id}>
                    <td className="td-mono">{u.id}</td>
                    <td>{u.username}</td>
                    <td className="td-muted">{u.email}</td>
                    <td>
                      <span className={`badge ${u.role === 'admin' ? 'badge-critical' : 'badge-low'}`}>
                        {u.role}
                      </span>
                    </td>
                    <td>
                      <div className="action-btns">
                        <button
                          className="btn-icon btn-icon-edit"
                          title="Change Role"
                          onClick={() => setRoleModal({ email: u.email, role: u.role })}
                        >
                          <ShieldCheck size={14} />
                        </button>
                        <button
                          className="btn-icon btn-icon-delete"
                          title="Delete User"
                          onClick={() => handleDeleteUser(u.email)}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add User Modal */}
      {showAddModal && (
        <Modal title="Add New User" onClose={() => setShowAddModal(false)}>
          <form onSubmit={handleAddUser} className="modal-form">
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                placeholder="johndoe"
                value={newUser.name}
                onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                placeholder="user@ids.com"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={newUser.password}
                onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                required
              />
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-outline" onClick={() => setShowAddModal(false)}>Cancel</button>
              <button type="submit" className="btn btn-primary">Create User</button>
            </div>
          </form>
        </Modal>
      )}

      {/* Update Role Modal */}
      {roleModal && (
        <Modal title="Update Role" onClose={() => setRoleModal(null)}>
          <div className="modal-form">
            <p className="modal-desc">Changing role for <strong>{roleModal.email}</strong></p>
            <div className="form-group">
              <label>Role</label>
              <select
                value={roleModal.role}
                onChange={(e) => setRoleModal({ ...roleModal, role: e.target.value })}
              >
                {ROLES.map((r) => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div className="modal-footer">
              <button className="btn btn-outline" onClick={() => setRoleModal(null)}>Cancel</button>
              <button className="btn btn-primary" onClick={handleUpdateRole}>Save</button>
            </div>
          </div>
        </Modal>
      )}

      {/* Clear History Modal */}
      {showClearModal && (
        <Modal title="⚠️ Confirm Clear" onClose={() => setShowClearModal(false)} danger>
          <div className="modal-form">
            <p className="modal-desc danger-text">
              This will permanently delete all attack history, alerts, blocked IPs, and statistics. This action cannot be undone.
            </p>
            <div className="modal-footer">
              <button className="btn btn-outline" onClick={() => setShowClearModal(false)}>Cancel</button>
              <button className="btn btn-danger" onClick={handleClear}>Yes, Clear All</button>
            </div>
          </div>
        </Modal>
      )}
    </Layout>
  );
}
