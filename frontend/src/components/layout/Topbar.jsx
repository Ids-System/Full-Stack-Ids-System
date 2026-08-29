import { useAuth } from '../../context/AuthContext';
import { Wifi, WifiOff } from 'lucide-react';

export default function Topbar({ wsConnected, title }) {
  const { user } = useAuth();

  return (
    <header className="topbar">
      <h1 className="topbar-title">{title}</h1>
      <div className="topbar-right">
        <div className={`ws-badge ${wsConnected ? 'connected' : 'disconnected'}`}>
          {wsConnected ? <Wifi size={14} /> : <WifiOff size={14} />}
          <span>{wsConnected ? 'Live' : 'Offline'}</span>
        </div>
        <div className="topbar-user">
          <span className="topbar-role">{user?.role}</span>
          <span className="topbar-username">{user?.username}</span>
        </div>
      </div>
    </header>
  );
}
