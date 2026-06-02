import { Navigate, useLocation } from 'react-router-dom';

import { useAuth } from '../contexts/use-auth';

function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在确认登录状态...</div>
      </section>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/user/login" state={{ from: location.pathname }} replace />;
  }

  return children;
}

export default ProtectedRoute;
