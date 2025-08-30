import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'admin' | 'user';
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
  const { isAuthenticated, isLoading, user } = useAuth();

  if (isLoading) {
    // Show loading state
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="wave-bars mb-4">
            <div className="wave-bar h-4"></div>
            <div className="wave-bar h-6"></div>
            <div className="wave-bar h-8"></div>
            <div className="wave-bar h-6"></div>
            <div className="wave-bar h-4"></div>
          </div>
          <p className="text-primary-700 dark:text-primary-300 font-medium">Loading...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirect to login page
    return <Navigate to="/auth" replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    // Redirect to profile page if user doesn't have required role
    return <Navigate to="/profile" replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;