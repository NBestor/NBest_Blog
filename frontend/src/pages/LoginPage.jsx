import { useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '../contexts/use-auth';

function LoginPage() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [errorMessage, setErrorMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((currentData) => ({ ...currentData, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setErrorMessage('');
    setIsSubmitting(true);

    try {
      await login(formData);
      navigate(location.state?.from || '/', { replace: true });
    } catch {
      setErrorMessage('用户名或密码不正确');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="auth-section">
      <div className="auth-panel">
        <h1>登录</h1>
        <form onSubmit={handleSubmit}>
          <label>
            用户名
            <input name="username" value={formData.username} onChange={handleChange} required />
          </label>
          <label>
            密码
            <input
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </label>
          {errorMessage && <p className="form-error">{errorMessage}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? '登录中...' : '登录'}
          </button>
        </form>
        <p>
          还没有账号？<Link to="/user/register">去注册</Link>
        </p>
      </div>
    </section>
  );
}

export default LoginPage;
