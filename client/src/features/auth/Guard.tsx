import { useAuth } from './context';
import { ReactNode } from 'react';

interface AuthGuardProps {
  children: ReactNode;
  redirectTo?: string;
}

export const AuthGuard = ({ children, redirectTo = '/login' }: AuthGuardProps) => {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <div>Loading...</div>;
  }
  
  if (!isAuthenticated) {
    window.location.href = redirectTo;
    return null;
  }
  
  return <>{children}</>;
};