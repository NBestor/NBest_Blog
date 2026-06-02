import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';

import { useAuth } from '../contexts/use-auth';

function RegisterPage() {
  const { isAuthenticated, register } = useAuth();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirm_password: '',
  });
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

    if (formData.password !== formData.confirm_password) {
      setErrorMessage('两次输入的密码不一致');
      return;
    }

    setIsSubmitting(true);
    try {
      await register(formData);
      navigate('/', { replace: true });
    } catch (error) {
      if (error.response?.status === 409) {
        setErrorMessage('用户名已存在');
      } else if (error.response?.status === 422) {
        setErrorMessage('用户名需为 3-32 位英文、数字、下划线或中横线，密码至少 6 位');
      } else if (!error.response) {
        setErrorMessage('无法连接后端服务，请确认 8000 端口已启动');
      } else {
        setErrorMessage('注册失败，请检查输入');
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <section className="auth-section">
      <div className="auth-panel">
        <h1>注册</h1>
        <form onSubmit={handleSubmit}>
          <label>
            账号名称
            <input
              name="username"
              value={formData.username}
              onChange={handleChange}
              pattern="[a-zA-Z0-9_-]{3,32}"
              title="账号名称需为 3-32 位英文、数字、下划线或中横线"
              required
            />
          </label>
          <label>
            密码
            <input
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              minLength={6}
              required
            />
          </label>
          <label>
            确认密码
            <input
              name="confirm_password"
              type="password"
              value={formData.confirm_password}
              onChange={handleChange}
              minLength={6}
              required
            />
          </label>
          {errorMessage && <p className="form-error">{errorMessage}</p>}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? '注册中...' : '注册'}
          </button>
        </form>
        <p>
          已有账号？<Link to="/user/login">去登录</Link>
        </p>
      </div>
    </section>
  );
}

export default RegisterPage;
