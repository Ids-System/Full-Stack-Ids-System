import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute, PublicRoute } from './components/ui/RouteGuards';
import ErrorBoundary from './components/ui/ErrorBoundary';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import AttackIPsPage from './pages/AttackIPs';
import AttacksHistory from './pages/AttacksHistory';
import AdminPanel from './pages/AdminPanel';
import Profile from './pages/Profile';


export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: '#0f172a',
              color: '#e2e8f0',
              border: '1px solid rgba(0,245,255,0.2)',
              fontFamily: 'Inter, sans-serif',
              fontSize: '13px',
            },
          }}
        />
        <Routes>
          <Route element={<PublicRoute />}>
            <Route path="/" element={<Login />} />
          </Route>
          <Route element={<ProtectedRoute />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/attack-ips" element={<AttackIPsPage />} />
            <Route path="/attacks" element={<AttacksHistory />} />
            <Route path="/profile" element={<Profile />} />
          </Route>
          <Route element={<ProtectedRoute adminOnly />}>
            <Route path="/admin" element={<AdminPanel />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
