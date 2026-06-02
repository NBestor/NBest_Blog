import { useState } from 'react';

import httpClient from '../api/http-client';
import { useAuth } from '../contexts/use-auth';

function ProfilePage() {
  const { updateUser, user } = useAuth();
  const displayName = user?.nickname || user?.username || '';
  const shouldShowLoginName = Boolean(user?.username && user?.nickname && user.username !== user.nickname);
  const [profileData, setProfileData] = useState({
    nickname: user?.nickname || '',
    signature: user?.signature || '',
  });
  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [profileMessage, setProfileMessage] = useState('');
  const [avatarMessage, setAvatarMessage] = useState('');
  const [passwordMessage, setPasswordMessage] = useState('');
  const avatarUrl = user?.avatar_url
    ? user.avatar_url.startsWith('http')
      ? user.avatar_url
      : `http://127.0.0.1:8000${user.avatar_url}`
    : '';

  function handleProfileChange(event) {
    const { name, value } = event.target;
    setProfileData((currentData) => ({ ...currentData, [name]: value }));
  }

  function handlePasswordChange(event) {
    const { name, value } = event.target;
    setPasswordData((currentData) => ({ ...currentData, [name]: value }));
  }

  async function handleProfileSubmit(event) {
    event.preventDefault();
    setProfileMessage('');

    try {
      const response = await httpClient.put('/users/me', profileData);
      updateUser(response.data);
      setProfileMessage('资料已保存');
    } catch {
      setProfileMessage('资料保存失败');
    }
  }

  async function handleAvatarChange(event) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    setAvatarMessage('');
    const formData = new FormData();
    formData.append('avatar', file);

    try {
      const response = await httpClient.post('/users/me/avatar', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      updateUser(response.data);
      setAvatarMessage('头像已更新');
    } catch {
      setAvatarMessage('头像上传失败，请选择 jpg、png 或 webp 图片');
    } finally {
      event.target.value = '';
    }
  }

  async function handleAvatarReset() {
    setAvatarMessage('');

    try {
      const response = await httpClient.delete('/users/me/avatar');
      updateUser(response.data);
      setAvatarMessage('头像已重置');
    } catch {
      setAvatarMessage('头像重置失败');
    }
  }

  async function handlePasswordSubmit(event) {
    event.preventDefault();
    setPasswordMessage('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setPasswordMessage('两次输入的新密码不一致');
      return;
    }

    try {
      await httpClient.put('/users/me/password', passwordData);
      setPasswordData({ old_password: '', new_password: '', confirm_password: '' });
      setPasswordMessage('密码已修改');
    } catch {
      setPasswordMessage('密码修改失败，请检查旧密码');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>个人中心</h1>
        <p>管理头像、账号名称、签名与登录密码。</p>
      </div>

      <div className="profile-grid">
        <div className="content-panel profile-card">
          <div className="avatar-preview">
            {avatarUrl ? <img src={avatarUrl} alt={displayName} /> : <span>{displayName[0]}</span>}
          </div>
          <dl>
            <div>
              <dt>账号名称</dt>
              <dd>{displayName}</dd>
            </div>
            {shouldShowLoginName ? (
              <div>
                <dt>登录标识</dt>
                <dd>{user.username}</dd>
              </div>
            ) : null}
            <div>
              <dt>角色</dt>
              <dd>{user?.role === 'admin' ? '管理员' : '用户'}</dd>
            </div>
            <div>
              <dt>注册时间</dt>
              <dd>{user?.create_time}</dd>
            </div>
          </dl>
          <label className="file-button">
            上传头像
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleAvatarChange} />
          </label>
          <button className="secondary-button" type="button" onClick={handleAvatarReset}>
            重置头像
          </button>
          {avatarMessage && <p className="form-message">{avatarMessage}</p>}
        </div>

        <form className="content-panel form-panel" onSubmit={handleProfileSubmit}>
          <h2>资料修改</h2>
          <label>
            账号名称
            <input name="nickname" value={profileData.nickname} onChange={handleProfileChange} required />
          </label>
          <label>
            个性签名
            <textarea
              name="signature"
              value={profileData.signature}
              onChange={handleProfileChange}
              maxLength={120}
              rows={4}
            />
          </label>
          <button type="submit">保存资料</button>
          {profileMessage && <p className="form-message">{profileMessage}</p>}
        </form>

        <form className="content-panel form-panel" onSubmit={handlePasswordSubmit}>
          <h2>密码修改</h2>
          <label>
            旧密码
            <input
              name="old_password"
              type="password"
              value={passwordData.old_password}
              onChange={handlePasswordChange}
              minLength={6}
              required
            />
          </label>
          <label>
            新密码
            <input
              name="new_password"
              type="password"
              value={passwordData.new_password}
              onChange={handlePasswordChange}
              minLength={6}
              required
            />
          </label>
          <label>
            确认新密码
            <input
              name="confirm_password"
              type="password"
              value={passwordData.confirm_password}
              onChange={handlePasswordChange}
              minLength={6}
              required
            />
          </label>
          <button type="submit">修改密码</button>
          {passwordMessage && <p className="form-message">{passwordMessage}</p>}
        </form>
      </div>
    </section>
  );
}

export default ProfilePage;
