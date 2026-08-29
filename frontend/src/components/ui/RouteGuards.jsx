import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export function ProtectedRoute({ adminOnly = false }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="page-loading fullscreen">
        <span className="spinner spinner-lg" />
      </div>
    );
  }

  if (!user) return <Navigate to="/" replace />;
  if (adminOnly && user.role !== 'admin') return <Navigate to="/dashboard" replace />;

  return <Outlet />;
}

export function PublicRoute() {
  const { user, loading } = useAuth();
  if (loading) return <div className="page-loading fullscreen"><span className="spinner spinner-lg" /></div>;
  if (user) return <Navigate to="/dashboard" replace />;
  return <Outlet />;
}
