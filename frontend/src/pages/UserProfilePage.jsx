import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

import httpClient from '../api/http-client';
import { useAuth } from '../contexts/use-auth';

const visibleLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function UserProfilePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated, updateUser, user: currentUser } = useAuth();
  const [profile, setProfile] = useState(null);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('articles');
  const [pageTab, setPageTab] = useState('profile');

  // Settings state (from ProfilePage)
  const [profileData, setProfileData] = useState({ nickname: '', signature: '' });
  const [passwordData, setPasswordData] = useState({ old_password: '', new_password: '', confirm_password: '' });
  const [profileMessage, setProfileMessage] = useState('');
  const [avatarMessage, setAvatarMessage] = useState('');
  const [passwordMessage, setPasswordMessage] = useState('');

  const isOwnProfile = isAuthenticated && parseInt(id) === currentUser?.id;

  async function loadProfile() {
    try {
      const response = await httpClient.get(`/users/${id}/profile`);
      setProfile(response.data);
      setMessage('');
    } catch (error) {
      if (error.response?.status === 404) {
        setMessage('用户不存在');
      } else {
        setMessage('用户信息加载失败');
      }
      setProfile(null);
    }
  }

  useEffect(() => {
    let isMounted = true;

    async function init() {
      await loadProfile();
      if (isMounted) {
        setIsLoading(false);
      }
    }

    init();

    return () => {
      isMounted = false;
    };
  }, [id]);

  async function handleDeleteArticle(articleId, e) {
    e.stopPropagation();
    if (!window.confirm('确定要删除这篇博客吗？此操作不可撤销。')) return;
    try {
      await httpClient.delete(`/articles/${articleId}`);
      setMessage('');
      await loadProfile();
    } catch {
      setMessage('博客删除失败');
    }
  }

  async function handleDeleteQuickPost(postId, e) {
    e.stopPropagation();
    if (!window.confirm('确定要删除这条快写吗？此操作不可撤销。')) return;
    try {
      await httpClient.delete(`/quick-posts/${postId}`);
      setMessage('');
      await loadProfile();
    } catch {
      setMessage('快写删除失败');
    }
  }

  // Init settings form data when profile loads
  useEffect(() => {
    if (profile && isOwnProfile) {
      setProfileData({
        nickname: profile.user.nickname || '',
        signature: profile.user.signature || '',
      });
    }
  }, [profile, isOwnProfile]);

  function handleProfileChange(event) {
    const { name, value } = event.target;
    setProfileData((prev) => ({ ...prev, [name]: value }));
  }

  function handlePasswordChange(event) {
    const { name, value } = event.target;
    setPasswordData((prev) => ({ ...prev, [name]: value }));
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
    if (!file) return;

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

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在加载用户信息...</div>
      </section>
    );
  }

  if (!profile) {
    return (
      <section className="page-section">
        <div className="content-panel">
          <p className="empty-text">{message || '用户不存在'}</p>
          <Link className="primary-link" to="/">
            返回首页
          </Link>
        </div>
      </section>
    );
  }

  const { user, stats, articles, quick_posts } = profile;
  const displayName = user.nickname || user.username;
  const showLoginName = user.username && user.nickname && user.username !== user.nickname;
  const avatarUrl = user.avatar_url
    ? user.avatar_url.startsWith('http')
      ? user.avatar_url
      : `${user.avatar_url}`
    : '';

  return (
    <section className="page-section user-profile-page">
      {isOwnProfile && (
        <div className="user-profile-page-tabs">
          <button
            className={pageTab === 'profile' ? 'active' : ''}
            onClick={() => setPageTab('profile')}
            type="button"
          >
            个人主页
          </button>
          <button
            className={pageTab === 'settings' ? 'active' : ''}
            onClick={() => setPageTab('settings')}
            type="button"
          >
            个人设置
          </button>
        </div>
      )}

      {pageTab === 'settings' && isOwnProfile ? (
        <div className="profile-settings-section">
          <div className="profile-grid">
            <div className="content-panel profile-settings-card">
              <div className="avatar-preview">
                {avatarUrl ? <img src={avatarUrl} alt={displayName} /> : <span>{displayName[0]}</span>}
              </div>
              <dl>
                <div>
                  <dt>账号名称</dt>
                  <dd>{displayName}</dd>
                </div>
                {showLoginName && (
                  <div>
                    <dt>登录标识</dt>
                    <dd>{user.username}</dd>
                  </div>
                )}
                <div>
                  <dt>角色</dt>
                  <dd>{user.role === 'admin' ? '管理员' : '用户'}</dd>
                </div>
                <div>
                  <dt>注册时间</dt>
                  <dd>{user.create_time}</dd>
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
        </div>
      ) : (
        <>
          <div className="content-panel user-profile-header">
            <div className="user-profile-avatar">
              {avatarUrl ? (
                <img src={avatarUrl} alt={displayName} />
              ) : (
                <span>{displayName[0]}</span>
              )}
            </div>
            <h1>{displayName}</h1>
            {showLoginName ? <p className="user-profile-username">@{user.username}</p> : null}
            {user.signature ? <p className="user-profile-signature">{user.signature}</p> : null}
            <div className="user-profile-stats">
              <span>关注 {stats.following_count}</span>
              <span>粉丝 {stats.follower_count}</span>
              <span>博客 {stats.article_count}</span>
              <span>快写 {stats.quick_post_count}</span>
            </div>
          </div>

          <div className="user-profile-tabs">
            <button
              className={activeTab === 'articles' ? 'active' : ''}
              onClick={() => setActiveTab('articles')}
              type="button"
            >
              博客
            </button>
            <button
              className={activeTab === 'quick_posts' ? 'active' : ''}
              onClick={() => setActiveTab('quick_posts')}
              type="button"
            >
              快写
            </button>
          </div>

          <div className="user-profile-content">
            {activeTab === 'articles' ? (
              articles.length === 0 ? (
                <div className="content-panel">
                  <p className="empty-text">暂无可见博客。</p>
                </div>
              ) : (
                <div className="article-list">
                  {articles.map((article) => (
                    <article
                      className="content-panel article-card clickable-card"
                      key={article.id}
                      onClick={() => navigate(`/blog/detail/${article.id}`)}
                    >
                      <div className="article-card-main">
                        <h2>{article.title}</h2>
                        <p>{article.summary || '暂无简介'}</p>
                        <div className="article-meta">
                          <span>{article.category_name || '无分类'}</span>
                          <span>{visibleLabels[article.visible_type] || '仅自己可见'}</span>
                          <span>{article.like_count} 赞</span>
                          <span>{article.comment_count} 评论</span>
                        </div>
                        <div className="draft-meta">
                          {(article.tags || []).map((tag) => (
                            <span key={tag}>{tag}</span>
                          ))}
                        </div>
                      </div>
                      {isOwnProfile && (
                        <div className="editor-actions" style={{marginTop:8}}>
                          <button
                            className="secondary-button"
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              navigate(`/blog/edit?articleId=${article.id}`);
                            }}
                          >
                            ✏️ 编辑
                          </button>
                          <button
                            className="secondary-button"
                            type="button"
                            onClick={(e) => handleDeleteArticle(article.id, e)}
                          >
                            🗑 删除
                          </button>
                        </div>
                      )}
                      <span className="article-time">{article.create_time}</span>
                    </article>
                  ))}
                </div>
              )
            ) : quick_posts.length === 0 ? (
              <div className="content-panel">
                <p className="empty-text">暂无可见快写。</p>
              </div>
            ) : (
              <div className="quick-post-list compact">
                {quick_posts.map((post) => (
                  <article
                    className="content-panel quick-post-card clickable-card"
                    key={post.id}
                    onClick={() => navigate(`/quick-posts/${post.id}`)}
                  >
                    <div className="article-meta">
                      <span>{visibleLabels[post.visible_type]}</span>
                    </div>
                    <p>{post.content}</p>
                    <div className="article-meta">
                      <span>{post.like_count} 赞</span>
                      <span>{post.comment_count} 评论</span>
                      <span>{post.create_time}</span>
                    </div>
                    {isOwnProfile && (
                      <div className="editor-actions">
                        <button
                          className="secondary-button"
                          type="button"
                          onClick={(e) => handleDeleteQuickPost(post.id, e)}
                        >
                          🗑 删除
                        </button>
                      </div>
                    )}
                  </article>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </section>
  );
}

export default UserProfilePage;