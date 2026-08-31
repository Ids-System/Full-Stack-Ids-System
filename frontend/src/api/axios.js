import axios from 'axios';

export const BASE_URL = 'http://127.0.0.1:8000';
export const WS_BASE_URL = 'ws://127.0.0.1:8000';

const api = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

// Endpoints that should NEVER trigger a refresh retry
// NOTE: /users/me is intentionally excluded — it's a protected resource, not an auth endpoint.
// A 401 from /users/me should trigger a refresh attempt.
const AUTH_ENDPOINTS = ['/users/refresh', '/users/login', '/users/logout'];

// Auto-refresh on 401 — only for non-auth endpoints
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    const isAuthEndpoint = AUTH_ENDPOINTS.some((path) => original.url?.includes(path));

    if (error.response?.status === 401 && !original._retry && !isAuthEndpoint) {
      original._retry = true;
      try {
        await axios.post(`${BASE_URL}/users/refresh`, {}, { withCredentials: true });
        return api(original);
      } catch {
        // Refresh also failed — just reject, let the caller handle it
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export default api;
