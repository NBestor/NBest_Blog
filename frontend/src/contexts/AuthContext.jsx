import { useEffect, useMemo, useState } from 'react';

import httpClient from '../api/http-client';
import { AuthContext } from './auth-context';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function fetchCurrentUser() {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await httpClient.get('/auth/me');
        if (isMounted) {
          setUser(response.data);
        }
      } catch {
        localStorage.removeItem('accessToken');
        if (isMounted) {
          setUser(null);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchCurrentUser();

    return () => {
      isMounted = false;
    };
  }, []);

  async function login(credentials) {
    const response = await httpClient.post('/auth/login', credentials);
    localStorage.setItem('accessToken', response.data.access_token);
    setUser(response.data.user);
    return response.data.user;
  }

  async function register(payload) {
    const response = await httpClient.post('/auth/register', payload);
    localStorage.setItem('accessToken', response.data.access_token);
    setUser(response.data.user);
    return response.data.user;
  }

  function logout() {
    localStorage.removeItem('accessToken');
    setUser(null);
  }

  function updateUser(nextUser) {
    setUser(nextUser);
  }

  const value = useMemo(
    () => ({
      user,
      isLoading,
      isAuthenticated: Boolean(user),
      login,
      logout,
      register,
      updateUser,
    }),
    [user, isLoading],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
