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
  // Guards against reconnect attempts after the hook is torn down (e.g. React StrictMode double-mount)
  const destroyed = useRef(false);

  useEffect(() => { onMessageRef.current = onMessage; }, [onMessage]);
  useEffect(() => { onStatusRef.current = onStatus; }, [onStatus]);

  const connect = useCallback(() => {
    // Don't reconnect if already open, connecting, or destroyed
    if (destroyed.current) return;
    if (
      ws.current?.readyState === WebSocket.OPEN ||
      ws.current?.readyState === WebSocket.CONNECTING
    ) return;

    const socket = new WebSocket(`${WS_BASE_URL}/ws/`);
    ws.current = socket;

    socket.onopen = () => {
      if (destroyed.current) { socket.close(); return; }
      console.log('[WS] Connected');
      clearTimeout(reconnectTimer.current);
      reconnectTimer.current = null;
      onStatusRef.current?.(true);
    };

    socket.onmessage = (evt) => {
      if (destroyed.current) return;
      try {
        const data = JSON.parse(evt.data);
        onMessageRef.current?.(data);
      } catch {
        // ignore parse errors
      }
    };

    socket.onclose = (evt) => {
      if (destroyed.current) return; // don't reconnect after unmount
      onStatusRef.current?.(false);

      // Code 1008 = Policy Violation — the backend sends this when the
      // access_token cookie is expired or missing. We must refresh the
      // HTTP-only cookie before opening a new WebSocket, otherwise every
      // reconnect attempt will also be rejected with 1008.
      if (evt.code === 1008) {
        console.log('[WS] Token expired (1008) — refreshing token before reconnect…');
        import('../api/axios').then(({ default: api }) => {
          api.post('/users/refresh').then(() => {
            console.log('[WS] Token refreshed — reconnecting…');
            if (!destroyed.current) {
              reconnectTimer.current = setTimeout(connect, 500);
            }
          }).catch(() => {
            // Refresh token also invalid/expired — user needs to log in again
            console.warn('[WS] Refresh failed — user must re-login');
          });
        });
        return; // Skip the default 3-second reconnect below
      }

      console.log('[WS] Disconnected — reconnecting in 3s');
      reconnectTimer.current = setTimeout(connect, 3000);
    };

    socket.onerror = () => {
      socket.close();
    };
  }, []);

  useEffect(() => {
    destroyed.current = false;
    connect();

    const handleVisibility = () => {
      if (document.visibilityState === 'visible') connect();
    };
    document.addEventListener('visibilitychange', handleVisibility);

    return () => {
      destroyed.current = true;
      clearTimeout(reconnectTimer.current);
      ws.current?.close();
      ws.current = null;
      document.removeEventListener('visibilitychange', handleVisibility);
    };
  }, [connect]);

  return { reconnect: connect };
}
