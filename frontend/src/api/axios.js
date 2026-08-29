import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true,
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        await axios.post('http://localhost:8000/users/refresh', {}, { withCredentials: true });
        return api(original);
      } catch {
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
