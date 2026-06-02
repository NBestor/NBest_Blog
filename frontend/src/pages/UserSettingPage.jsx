import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

function UserSettingPage() {
  const [visibleType, setVisibleType] = useState('public');
  const [message, setMessage] = useState('');

  useEffect(() => {
    let isMounted = true;

    async function fetchSettings() {
      try {
        const response = await httpClient.get('/users/me/settings');
        if (isMounted) {
          setVisibleType(response.data.quick_post_default_visible_type);
        }
      } catch {
        if (isMounted) {
          setMessage('设置加载失败');
        }
      }
    }

    fetchSettings();

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    try {
      await httpClient.put('/users/me/settings', {
        quick_post_default_visible_type: visibleType,
      });
      setMessage('设置已保存');
    } catch {
      setMessage('设置保存失败');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>个人设置</h1>
        <p>设置快写默认可见范围。</p>
      </div>

      <form className="content-panel form-panel" onSubmit={handleSubmit}>
        <h2>快写默认权限</h2>
        <label>
          默认可见范围
          <select value={visibleType} onChange={(event) => setVisibleType(event.target.value)}>
            <option value="public">公开</option>
            <option value="friend">好友可见</option>
            <option value="self">仅自己可见</option>
          </select>
        </label>
        <button type="submit">保存设置</button>
        {message && <p className="form-message">{message}</p>}
      </form>
    </section>
  );
}

export default UserSettingPage;
