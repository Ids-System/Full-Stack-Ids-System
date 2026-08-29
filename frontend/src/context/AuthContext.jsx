import { createContext, useContext, useState, useEffect } from 'react';
import { getMe, logout as logoutApi } from '../api/endpoints';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMe()
      .then((res) => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const logout = async () => {
    await logoutApi().catch(() => {});
    setUser(null);
  };

  const refreshUser = () => {
    return getMe().then((res) => setUser(res.data)).catch(() => setUser(null));
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
