import { createContext, useContext, useReducer, ReactNode } from 'react';
import { api, TokenStorage } from '../../shared/api';

type Role = {
  id: number;
  name: string;
};

type Department = {
  id: number;
  name: string;
};

type User = {
  id: number;
  login: string;
  first_name: string;
  last_name: string;
  roles?: Role[];
  departments?: Department[];
};

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

type AuthAction = 
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: User }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CLEAR_ERROR' }
  | { type: 'RESTORE_SESSION'; payload: User };

const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  isLoading: false,
  error: null,
};

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        isLoading: false,
        error: null,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        isLoading: false,
        error: null,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    case 'RESTORE_SESSION':
      return {
        ...state,
        isAuthenticated: true,
        user: action.payload,
        isLoading: false,
        error: null,
      };
    default:
      return state;
  }
};

interface AuthContextValue extends AuthState {
  login: (login: string, password: string) => Promise<void>;
  register: (login: string, firstName: string, lastName: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const login = async (login: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      const formData = new FormData();
      formData.append('login', login);
      formData.append('password', password);

      const response = await api.post('/auth/login', formData);

      if (response.data.status) {
        const { access_token, refresh_token, user } = response.data.data;
        TokenStorage.setTokens({
          accessToken: access_token,
          refreshToken: refresh_token,
        });
        dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      } else {
        dispatch({ type: 'LOGIN_FAILURE', payload: response.data.message || 'Login failed' });
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Login failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: message });
    }
  };

  const register = async (login: string, firstName: string, lastName: string, password: string) => {
    dispatch({ type: 'LOGIN_START' });
    
    try {
      const formData = new FormData();
      formData.append('login', login);
      formData.append('first_name', firstName);
      formData.append('last_name', lastName);
      formData.append('password', password);

      const response = await api.post('/auth/register', formData);

      if (response.data.status) {
        const { access_token, refresh_token, user } = response.data.data;
        TokenStorage.setTokens({
          accessToken: access_token,
          refreshToken: refresh_token,
        });
        dispatch({ type: 'LOGIN_SUCCESS', payload: user });
      } else {
        dispatch({ type: 'LOGIN_FAILURE', payload: response.data.message || 'Registration failed' });
      }
    } catch (error: any) {
      const message = error.response?.data?.message || 'Registration failed';
      dispatch({ type: 'LOGIN_FAILURE', payload: message });
    }
  };

  const logout = () => {
    TokenStorage.removeTokens();
    dispatch({ type: 'LOGOUT' });
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AuthContextValue = {
    ...state,
    login,
    register,
    logout,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};