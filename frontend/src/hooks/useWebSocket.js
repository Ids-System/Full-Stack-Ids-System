import { useEffect, useRef, useCallback } from 'react';
import { WS_BASE_URL } from '../api/axios';

/**
 * @param {function} onMessage  - called with parsed JSON data on each message
 * @param {function} onStatus   - called with (true/false) when WS connects/disconnects
 */
export function useWebSocket(onMessage, onStatus) {
  const ws = useRef(null);
  const reconnectTimer = useRef(null);
  const onMessageRef = useRef(onMessage);
  const onStatusRef = useRef(onStatus);

  useEffect(() => { onMessageRef.current = onMessage; }, [onMessage]);
  useEffect(() => { onStatusRef.current = onStatus; }, [onStatus]);

  const connect = useCallback(() => {
    // Don't reconnect if already open or connecting
    if (
      ws.current?.readyState === WebSocket.OPEN ||
      ws.current?.readyState === WebSocket.CONNECTING
    ) return;

    const socket = new WebSocket(`${WS_BASE_URL}/ws/`);
    ws.current = socket;

    socket.onopen = () => {
      console.log('[WS] Connected');
      clearTimeout(reconnectTimer.current);
      reconnectTimer.current = null;
      onStatusRef.current?.(true);
    };

    socket.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data);
        onMessageRef.current?.(data);
      } catch {
        // ignore parse errors
      }
    };

    socket.onclose = () => {
      console.log('[WS] Disconnected — reconnecting in 3s');
      onStatusRef.current?.(false);
      reconnectTimer.current = setTimeout(connect, 3000);
    };

    socket.onerror = () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    connect();

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') connect();
    };
    document.addEventListener('visibilitychange', handleVisibility);

    return () => {
      clearTimeout(reconnectTimer.current);
      ws.current?.close();
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  }, [connect]);

  return { reconnect: connect };
}
