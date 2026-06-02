import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import AdminRoute from './components/AdminRoute';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import AppLayout from './layouts/AppLayout';
import AdminPage from './pages/AdminPage';
import BlogDetailPage from './pages/BlogDetailPage';
import BlogDraftPage from './pages/BlogDraftPage';
import BlogEditPage from './pages/BlogEditPage';
import BlogListPage from './pages/BlogListPage';
import CalendarPage from './pages/CalendarPage';
import FollowPage from './pages/FollowPage';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';
import PlaceholderPage from './pages/PlaceholderPage';
import PhotoPage from './pages/PhotoPage';
import QuickPostDetailPage from './pages/QuickPostDetailPage';
import ProfilePage from './pages/ProfilePage';
import QuickNotePage from './pages/QuickNotePage';
import RegisterPage from './pages/RegisterPage';
import SearchPage from './pages/SearchPage';
import TodoPage from './pages/TodoPage';
import UserSettingPage from './pages/UserSettingPage';
import { privatePaths, routes } from './routes/route-config';

function getRouteElement(route) {
  if (route.path === '/') {
    return <HomePage />;
  }

  if (route.path === '/user/login') {
    return <LoginPage />;
  }

  if (route.path === '/user/register') {
    return <RegisterPage />;
  }

  if (route.path === '/user/profile') {
    return (
      <ProtectedRoute>
        <ProfilePage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/blog/edit') {
    return (
      <ProtectedRoute>
        <BlogEditPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/blog') {
    return <BlogListPage />;
  }

  if (route.path === '/blog/detail/sample') {
    return <BlogDetailPage />;
  }

  if (route.path === '/blog/draft') {
    return (
      <ProtectedRoute>
        <BlogDraftPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/user/follow') {
    return (
      <ProtectedRoute>
        <FollowPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/quick/note') {
    return (
      <ProtectedRoute>
        <QuickNotePage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/user/setting') {
    return (
      <ProtectedRoute>
        <UserSettingPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/todo') {
    return (
      <ProtectedRoute>
        <TodoPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/calendar') {
    return (
      <ProtectedRoute>
        <CalendarPage />
      </ProtectedRoute>
    );
  }

  if (route.path === '/photo') {
    return <PhotoPage />;
  }

  if (route.path === '/admin') {
    return (
      <AdminRoute>
        <AdminPage />
      </AdminRoute>
    );
  }

  const element = <PlaceholderPage title={route.title} description={route.description} />;

  if (privatePaths.has(route.path)) {
    return <ProtectedRoute>{element}</ProtectedRoute>;
  }

  return element;
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    errorElement: <NotFoundPage />,
    children: [
      ...routes.map((route) => ({
        path: route.path === '/' ? undefined : route.path.slice(1),
        index: route.path === '/',
        element: getRouteElement(route),
      })),
      {
        path: 'blog/detail/:id',
        element: <BlogDetailPage />,
      },
      {
        path: 'quick-posts/:id',
        element: <QuickPostDetailPage />,
      },
      {
        path: 'search',
        element: <SearchPage />,
      },
      {
        path: '404',
        element: <NotFoundPage />,
      },
      {
        path: '*',
        element: <NotFoundPage />,
      },
    ],
  },
]);

function App() {
  return (
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  );
}

export default App;
