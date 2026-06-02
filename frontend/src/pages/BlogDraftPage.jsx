import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import httpClient from '../api/http-client';

const visibleTypeLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function BlogDraftPage() {
  const [drafts, setDrafts] = useState([]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function fetchDrafts() {
    setMessage('');
    setIsLoading(true);

    try {
      const response = await httpClient.get('/articles/drafts');
      setDrafts(response.data.items);
    } catch {
      setMessage('草稿列表加载失败');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    let isMounted = true;

    async function loadDrafts() {
      try {
        const response = await httpClient.get('/articles/drafts');
        if (isMounted) {
          setDrafts(response.data.items);
        }
      } catch {
        if (isMounted) {
          setMessage('草稿列表加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadDrafts();

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleDelete(draftId) {
    try {
      await httpClient.delete(`/articles/drafts/${draftId}`);
      await fetchDrafts();
    } catch {
      setMessage('删除失败');
    }
  }

  async function handlePublish(draftId) {
    try {
      await httpClient.post(`/articles/drafts/${draftId}/publish`);
      await fetchDrafts();
    } catch {
      setMessage('发布失败');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>草稿箱</h1>
        <p>继续编辑、删除或发布你的 Markdown 草稿。</p>
      </div>

      <div className="draft-toolbar">
        <Link className="primary-link" to="/blog/edit">
          新建草稿
        </Link>
      </div>

      {isLoading ? <div className="content-panel">正在加载草稿...</div> : null}
      {message ? <p className="form-error relation-error">{message}</p> : null}

      {!isLoading && drafts.length === 0 ? (
        <div className="content-panel">
          <p className="empty-text">还没有草稿。</p>
        </div>
      ) : null}

      {!isLoading && drafts.length > 0 ? (
        <div className="draft-list">
          {drafts.map((draft) => (
            <article className="content-panel draft-item" key={draft.id}>
              <div>
                <h2>{draft.title}</h2>
                <p>{draft.summary || '无摘要'}</p>
                <div className="draft-meta">
                  <span>{draft.category_name || '无分类'}</span>
                  <span>{visibleTypeLabels[draft.visible_type] || '仅自己可见'}</span>
                  {draft.tags.map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
                <span>更新于 {draft.update_time}</span>
              </div>
              <div className="draft-actions">
                <Link to={`/blog/edit?draftId=${draft.id}`}>继续编辑</Link>
                <button type="button" onClick={() => handlePublish(draft.id)}>
                  发布
                </button>
                <button className="secondary-button" type="button" onClick={() => handleDelete(draft.id)}>
                  删除
                </button>
              </div>
            </article>
          ))}
        </div>
      ) : null}
    </section>
  );
}

export default BlogDraftPage;
