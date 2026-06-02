import { Navigate, useLocation } from 'react-router-dom';

import { useAuth } from '../contexts/use-auth';

function AdminRoute({ children }) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在确认管理员权限...</div>
      </section>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/user/login" state={{ from: location.pathname }} replace />;
  }

  if (user?.role !== 'admin') {
    return (
      <section className="page-section">
        <div className="content-panel">
          <p className="empty-text">暂无管理权限。</p>
        </div>
      </section>
    );
  }

  return children;
}

export default AdminRoute;
