import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';

import ApiStatus from '../components/ApiStatus';
import { SearchIcon } from '../components/icons';
import ReminderModal from '../components/ReminderModal';
import { useAuth } from '../contexts/use-auth';
import { routes } from '../routes/route-config';

function canShowRoute(route, isAuthenticated, user) {
  if (route.showInNav === false) {
    return false;
  }

  if (route.visibility === 'admin') {
    return user?.role === 'admin';
  }

  if (route.visibility === 'auth') {
    return isAuthenticated;
  }

  if (route.visibility === 'guest') {
    return !isAuthenticated;
  }

  return true;
}

function AppLayout() {
  const { isAuthenticated, logout, user } = useAuth();
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');
  const navRoutes = routes.filter((route) => canShowRoute(route, isAuthenticated, user));
  const primaryNavRoutes = navRoutes.slice(0, 8);
  const secondaryNavRoutes = navRoutes.slice(8);
  const displayName = user?.nickname || user?.username;

  function handleSearchSubmit(event) {
    event.preventDefault();
    const query = searchQuery.trim();
    if (!query) {
      return;
    }
    navigate(`/search?q=${encodeURIComponent(query)}`);
  }

  return (
    <>
      <header className="navbar">
        <nav>
          <div className="navbar-branding">
            <NavLink to="/">私人博客</NavLink>
          </div>
          <div className="navbar-left">
            {primaryNavRoutes.map((route) => (
              <NavLink key={route.path} to={route.path}>
                {route.label}
              </NavLink>
            ))}
          </div>
          <div className="navbar-right">
            <ApiStatus />
            <form className="nav-search" onSubmit={handleSearchSubmit}>
              <button aria-label="搜索" type="submit">
                <SearchIcon />
              </button>
              <input
                onChange={(event) => setSearchQuery(event.target.value)}
                placeholder="搜索博客或快写"
                value={searchQuery}
              />
            </form>
            {isAuthenticated ? (
              <>
                <span className="user-chip">{displayName}</span>
                <button className="text-button" onClick={logout} type="button">
                  退出
                </button>
              </>
            ) : (
              <NavLink to="/user/login">登录</NavLink>
            )}
          </div>
        </nav>
        {secondaryNavRoutes.length > 0 ? (
          <nav className="navbar-subnav">
            {secondaryNavRoutes.map((route) => (
              <NavLink key={route.path} to={route.path}>
                {route.label}
              </NavLink>
            ))}
          </nav>
        ) : null}
      </header>
      <main className="main-layout">
        <Outlet />
      </main>
      <ReminderModal key={user?.id || 'guest'} isAuthenticated={isAuthenticated} />
    </>
  );
}

export default AppLayout;

