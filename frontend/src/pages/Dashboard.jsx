import { useState, useEffect, useCallback } from 'react';
import Layout from '../components/layout/Layout';
import StatCard from '../components/cards/StatCard';
import AttacksLineChart from '../components/charts/AttacksLineChart';
import AttackTypeDonut from '../components/charts/AttackTypeDonut';
import AlertsTable from '../components/tables/AlertsTable';
import BlockedIPsTable from '../components/tables/BlockedIPsTable';
import LiveFeed from '../components/ui/LiveFeed';
import { useWebSocket } from '../hooks/useWebSocket';
import {
  getAttackIPs, getAttacks, getAlerts, getBlockedIPs, getStatistics,
} from '../api/endpoints';
import toast from 'react-hot-toast';
import { Swords, Globe, ShieldX, Bell } from 'lucide-react';

export default function Dashboard() {
  const [attackIPs, setAttackIPs] = useState([]);
  const [attacks, setAttacks] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [blockedIPs, setBlockedIPs] = useState([]);
  const [statistics, setStatistics] = useState([]);
  const [liveEvents, setLiveEvents] = useState([]);
  const [wsConnected, setWsConnected] = useState(false);

  const fetchAll = async () => {
    try {
      const [ips, atk, alr, blk, stat] = await Promise.all([
        getAttackIPs(), getAttacks(), getAlerts(), getBlockedIPs(), getStatistics(),
      ]);
      setAttackIPs(ips.data);
      setAttacks(atk.data);
      setAlerts(alr.data);
      setBlockedIPs(blk.data);
      setStatistics(stat.data);
    } catch {
      toast.error('Failed to load dashboard data');
    }
  };

  useEffect(() => { fetchAll(); }, []);

  const handleWsMessage = useCallback((msg) => {
    if (msg.event === 'report_processed') {
      const d = msg.data;
      setAttackIPs(d.attack_ip || []);
      setAttacks(d.attack || []);
      setAlerts(d.alerts || []);
      setBlockedIPs(d.blocked_ip || []);
      setStatistics(d.statistics || []);

      // Build a live event from the latest attack + IP
      const latestIP = d.attack_ip?.at(-1);
      const latestAtk = d.attack?.at(-1);
      const latestAlert = d.alerts?.at(-1);
      if (latestIP && latestAtk) {
        const event = {
          source_ip: latestIP.source_ip,
          destination_ip: latestIP.destination_ip,
          protocol: latestIP.protocol,
          port: latestIP.port,
          attack: latestAtk.attack,
          severity: latestAlert?.severity,
          timestamp: latestIP.timestamp,
        };
        setLiveEvents((prev) => [...prev.slice(-99), event]);
        toast.error(`🚨 ${latestAtk.attack} from ${latestIP.source_ip}`, { duration: 4000 });
      }
      setWsConnected(true);
    }
  }, []);

  useWebSocket(handleWsMessage);

  return (
    <Layout wsConnected={wsConnected} title="Dashboard">
      {/* Stat Cards */}
      <div className="stats-grid">
        <StatCard label="Total Attacks" value={attacks.length} icon={Swords} color="red" />
        <StatCard label="Active Alerts" value={alerts.length} icon={Bell} color="yellow" />
        <StatCard label="Blocked IPs" value={blockedIPs.length} icon={ShieldX} color="purple" />
        <StatCard label="Attack IPs" value={attackIPs.length} icon={Globe} color="cyan" />
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <AttacksLineChart data={statistics} />
        <AttackTypeDonut data={attacks} />
      </div>

      {/* Live Feed */}
      <LiveFeed events={liveEvents} />

      {/* Tables */}
      <div className="tables-grid">
        <AlertsTable data={alerts} />
        <BlockedIPsTable data={blockedIPs} />
      </div>
    </Layout>
  );
}
