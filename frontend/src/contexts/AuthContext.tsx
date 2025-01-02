import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  loginWithOAuth: (provider: string) => void;
  handleOAuthCallback: (provider: string, code: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // 로컬 스토리지에서 사용자 정보 확인
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = async (email: string, password: string) => {
    try {
      // API 호출 로직 구현 필요
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        throw new Error('로그인 실패');
      }

      const userData = await response.json();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      navigate('/');
    } catch (error) {
      console.error('로그인 에러:', error);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    navigate('/login');
  };

  const loginWithOAuth = (provider: string) => {
    const providers = {
      google: 'https://accounts.google.com/o/oauth2/v2/auth',
      naver: 'https://nid.naver.com/oauth2.0/authorize',
      kakao: 'https://kauth.kakao.com/oauth/authorize',
      meta: 'https://www.facebook.com/v12.0/dialog/oauth'
    };

    const clientIds = {
      google: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      naver: process.env.REACT_APP_NAVER_CLIENT_ID,
      kakao: process.env.REACT_APP_KAKAO_CLIENT_ID,
      meta: process.env.REACT_APP_META_CLIENT_ID
    };

    const redirectUri = `${window.location.origin}/oauth/callback/${provider}`;
    const scope = 'email profile';

    const url = new URL(providers[provider as keyof typeof providers]);
    url.searchParams.append('client_id', clientIds[provider as keyof typeof clientIds] || '');
    url.searchParams.append('redirect_uri', redirectUri);
    url.searchParams.append('response_type', 'code');
    url.searchParams.append('scope', scope);

    window.location.href = url.toString();
  };

  const handleOAuthCallback = async (provider: string, code: string) => {
    try {
      const response = await fetch(`/api/oauth/${provider}/callback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error('OAuth 로그인 실패');
      }

      const userData = await response.json();
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      navigate('/');
    } catch (error) {
      console.error('OAuth 로그인 에러:', error);
      throw error;
    }
  };

  const value = {
    user,
    login,
    loginWithOAuth,
    handleOAuthCallback,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}