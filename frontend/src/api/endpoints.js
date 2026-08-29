import api from './axios';

// Auth
export const login = (data) => api.post('/users/login', data);
export const logout = () => api.post('/users/logout');
export const getMe = () => api.get('/users/me');
export const changePassword = (data) => api.put('/users/password', data);

// Dashboard
export const getAttackIPs = () => api.get('/dashboard/attack-ips');
export const getAttacks = () => api.get('/dashboard/attacks');
export const getAlerts = () => api.get('/dashboard/alerts');
export const getBlockedIPs = () => api.get('/dashboard/block-ips');
export const getStatistics = () => api.get('/dashboard/statistics');

// Admin
export const getAllUsers = () => api.get('/admin/users');
export const addUser = (data) => api.post('/admin/users', data);
export const updateRole = (data) => api.patch('/admin/users', data);
export const deleteUser = (data) => api.delete('/admin/users', { data });
export const clearAttackHistory = () => api.delete('/admin/attack-history');
export const exportReport = () =>
  api.get('/admin/export', { responseType: 'blob' });
