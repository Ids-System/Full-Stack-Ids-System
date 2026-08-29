import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function Layout({ children, wsConnected, title }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-content">
        <Topbar wsConnected={wsConnected} title={title} />
        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}
