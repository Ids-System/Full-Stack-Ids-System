import { useEffect, useRef } from 'react';
import { Radio } from 'lucide-react';

export default function LiveFeed({ events }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [events]);

  return (
    <div className="table-card live-feed-card">
      <div className="table-header-row">
        <h3 className="table-title">
          <Radio size={14} className="live-icon" />
          Live Attack Feed
        </h3>
        <span className="feed-count">{events.length} events</span>
      </div>
      <div className="live-feed-scroll">
        {events.length === 0 ? (
          <div className="feed-empty">Waiting for live events...</div>
        ) : (
          events.map((evt, i) => (
            <div key={i} className="feed-item">
              <span className="feed-time">
                {new Date(evt.timestamp || Date.now()).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
              <span className={`badge badge-${(evt.severity || '').toLowerCase()}`}>
                {evt.severity || '—'}
              </span>
              <span className="feed-attack">{evt.attack}</span>
              <span className="feed-ip">{evt.source_ip} → {evt.destination_ip}</span>
              <span className="feed-proto badge-proto badge">{evt.protocol}:{evt.port}</span>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
