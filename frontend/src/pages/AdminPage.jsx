import { useEffect, useMemo, useState } from 'react';

import httpClient from '../api/http-client';
import { useAuth } from '../contexts/use-auth';

const sections = [
  { key: 'users', label: '用户' },
  { key: 'articles', label: '文章' },
  { key: 'quickPosts', label: '快写' },
  { key: 'comments', label: '评论' },
  { key: 'photos', label: '照片' },
];

function getSectionRequest(section) {
  if (section === 'users') {
    return httpClient.get('/admin/users');
  }

  if (section === 'articles') {
    return httpClient.get('/admin/articles');
  }

  if (section === 'quickPosts') {
    return httpClient.get('/admin/quick-posts');
  }

  if (section === 'comments') {
    return httpClient.get('/admin/comments');
  }

  return httpClient.get('/admin/photos');
}

function AdminPage() {
  const { user } = useAuth();
  const isSupervisor = user?.id === 0 && user?.username === 'NBest';
  const [activeSection, setActiveSection] = useState('users');
  const [summary, setSummary] = useState(null);
  const [data, setData] = useState({
    users: [],
    articles: [],
    quickPosts: [],
    comments: [],
    photos: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const summaryItems = useMemo(
    () => [
      ['用户', summary?.users ?? 0],
      ['管理员', summary?.admins ?? 0],
      ['文章', summary?.articles ?? 0],
      ['快写', summary?.quick_posts ?? 0],
      ['评论', summary?.comments ?? 0],
      ['照片', summary?.photos ?? 0],
    ],
    [summary],
  );

  async function fetchSummary() {
    const response = await httpClient.get('/admin/summary');
    setSummary(response.data);
  }

  async function fetchSection(section = activeSection) {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await getSectionRequest(section);
      setData((currentData) => ({ ...currentData, [section]: response.data.items }));
    } catch (error) {
      setErrorMessage(error.response?.status === 403 ? '没有权限执行该操作。' : '管理数据加载失败。');
    } finally {
      setIsLoading(false);
    }
  }

  async function refreshCurrent(section = activeSection) {
    await Promise.all([fetchSummary(), fetchSection(section)]);
  }

  useEffect(() => {
    let isMounted = true;

    async function loadAdminData() {
      setIsLoading(true);
      setErrorMessage('');

      try {
        const [summaryResponse, sectionResponse] = await Promise.all([
          httpClient.get('/admin/summary'),
          getSectionRequest(activeSection),
        ]);
        if (isMounted) {
          setSummary(summaryResponse.data);
          setData((currentData) => ({ ...currentData, [activeSection]: sectionResponse.data.items }));
        }
      } catch (error) {
        if (isMounted) {
          setErrorMessage(error.response?.status === 403 ? '没有权限执行该操作。' : '管理数据加载失败。');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadAdminData();

    return () => {
      isMounted = false;
    };
  }, [activeSection]);

  async function runDangerAction(confirmText, action, successText) {
    if (!window.confirm(confirmText)) {
      return;
    }

    setMessage('');
    setErrorMessage('');
    try {
      await action();
      setMessage(successText);
      await refreshCurrent(activeSection);
    } catch (error) {
      setErrorMessage(error.response?.status === 403 ? '没有权限执行该操作。' : '操作失败，请稍后重试。');
    }
  }

  function renderUserActions(item) {
    return (
      <div className="admin-actions">
        <button
          className="secondary-button"
          type="button"
          disabled={!item.can_manage}
          onClick={() =>
            runDangerAction(
              `确认将 ${item.username} 强制重命名为 user_${item.id}？`,
              () => httpClient.patch(`/admin/users/${item.id}/rename`, {}),
              '用户已重命名。',
            )
          }
        >
          强制改名
        </button>
        <button
          className="secondary-button"
          type="button"
          disabled={!item.can_manage || !item.has_avatar}
          onClick={() =>
            runDangerAction(
              `确认移除 ${item.username} 的头像？`,
              () => httpClient.delete(`/admin/users/${item.id}/avatar`),
              '头像已移除。',
            )
          }
        >
          移除头像
        </button>
        {isSupervisor && item.id !== 0 ? (
          <button
            className="secondary-button"
            type="button"
            disabled={!item.can_change_role}
            onClick={() =>
              runDangerAction(
                item.role === 'admin' ? `确认撤销 ${item.username} 的管理员身份？` : `确认任命 ${item.username} 为管理员？`,
                () => httpClient.patch(`/admin/users/${item.id}/role`, { role: item.role === 'admin' ? 'user' : 'admin' }),
                item.role === 'admin' ? '管理员身份已撤销。' : '管理员已任命。',
              )
            }
          >
            {item.role === 'admin' ? '撤销管理员' : '任命管理员'}
          </button>
        ) : null}
        <button
          className="danger-button"
          type="button"
          disabled={!item.can_manage}
          onClick={() =>
            runDangerAction(
              `确认删除用户 ${item.username}？该用户的关联内容也会被删除。`,
              () => httpClient.delete(`/admin/users/${item.id}`),
              '用户已删除。',
            )
          }
        >
          删除用户
        </button>
      </div>
    );
  }

  function renderUsers() {
    return data.users.map((item) => (
      <article className="admin-card" key={item.id}>
        <div>
          <strong>{item.username}</strong>
          <p>{item.nickname}</p>
          <span>
            ID {item.id} · {item.role === 'admin' ? '管理员' : '普通用户'} · {item.has_avatar ? '有头像' : '默认头像'} ·{' '}
            {item.create_time}
          </span>
        </div>
        {renderUserActions(item)}
      </article>
    ));
  }

  function renderArticles() {
    return data.articles.map((item) => (
      <article className="admin-card" key={item.id}>
        <div>
          <strong>{item.title}</strong>
          <p>{item.summary || item.content}</p>
          <span>
            {item.author_nickname} · {item.is_draft ? '草稿' : '已发布'} · {item.visible_type} · {item.update_time}
          </span>
        </div>
        <div className="admin-actions">
          <button
            className="danger-button"
            type="button"
            onClick={() =>
              runDangerAction(
                `确认删除文章 ${item.title}？`,
                () => httpClient.delete(`/admin/articles/${item.id}`),
                '文章已删除。',
              )
            }
          >
            删除文章
          </button>
        </div>
      </article>
    ));
  }

  function renderQuickPosts() {
    return data.quickPosts.map((item) => (
      <article className="admin-card" key={item.id}>
        <div>
          <strong>{item.author_nickname}</strong>
          <p>{item.content}</p>
          <span>
            {item.visible_type} · {item.like_count} 赞 · {item.comment_count} 评论 · {item.update_time}
          </span>
        </div>
        <div className="admin-actions">
          <button
            className="danger-button"
            type="button"
            onClick={() =>
              runDangerAction(
                '确认删除这条快写？',
                () => httpClient.delete(`/admin/quick-posts/${item.id}`),
                '快写已删除。',
              )
            }
          >
            删除快写
          </button>
        </div>
      </article>
    ));
  }

  function renderComments() {
    return data.comments.map((item) => (
      <article className="admin-card" key={item.id}>
        <div>
          <strong>{item.author_nickname}</strong>
          <p>{item.content}</p>
          <span>
            {item.target_type} #{item.target_id} · {item.create_time}
          </span>
        </div>
        <div className="admin-actions">
          <button
            className="danger-button"
            type="button"
            onClick={() =>
              runDangerAction(
                '确认删除这条评论？',
                () => httpClient.delete(`/admin/comments/${item.id}`),
                '评论已删除。',
              )
            }
          >
            删除评论
          </button>
        </div>
      </article>
    ));
  }

  function renderPhotos() {
    return data.photos.map((item) => (
      <article className="admin-card" key={item.id}>
        <div>
          <strong>{item.author_nickname}</strong>
          <p>{item.url}</p>
          <span>
            {item.source_type} · {item.visible_type} · {item.upload_time}
          </span>
        </div>
        <div className="admin-actions">
          <button
            className="danger-button"
            type="button"
            onClick={() =>
              runDangerAction(
                '确认删除这张照片？',
                () => httpClient.delete(`/admin/photos/${item.id}`),
                '照片已删除。',
              )
            }
          >
            删除照片
          </button>
        </div>
      </article>
    ));
  }

  function renderCurrentSection() {
    if (isLoading) {
      return <p className="empty-text">正在加载管理数据...</p>;
    }

    if (activeSection === 'users') {
      return data.users.length > 0 ? renderUsers() : <p className="empty-text">暂无用户。</p>;
    }

    if (activeSection === 'articles') {
      return data.articles.length > 0 ? renderArticles() : <p className="empty-text">暂无文章。</p>;
    }

    if (activeSection === 'quickPosts') {
      return data.quickPosts.length > 0 ? renderQuickPosts() : <p className="empty-text">暂无快写。</p>;
    }

    if (activeSection === 'comments') {
      return data.comments.length > 0 ? renderComments() : <p className="empty-text">暂无评论。</p>;
    }

    return data.photos.length > 0 ? renderPhotos() : <p className="empty-text">暂无照片。</p>;
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>管理</h1>
        <p>集中处理用户资料和公开内容治理。</p>
      </div>

      <div className="admin-summary">
        {summaryItems.map(([label, value]) => (
          <article key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </article>
        ))}
      </div>

      <div className="content-panel admin-panel">
        <div className="admin-tabs">
          {sections.map((section) => (
            <button
              className={activeSection === section.key ? 'active' : ''}
              key={section.key}
              type="button"
              onClick={() => setActiveSection(section.key)}
            >
              {section.label}
            </button>
          ))}
        </div>
        {isSupervisor ? <p className="form-message">主管模式：可以任命和撤销管理员。</p> : null}
        {message ? <p className="form-message">{message}</p> : null}
        {errorMessage ? <p className="form-error">{errorMessage}</p> : null}
        <div className="admin-list">{renderCurrentSection()}</div>
      </div>
    </section>
  );
}

export default AdminPage;
