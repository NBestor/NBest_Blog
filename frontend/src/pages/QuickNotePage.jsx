import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

function QuickNotePage() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState('');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function getNotes() {
    const response = await httpClient.get('/quick-notes');
    return response.data.items;
  }

  async function refreshNotes() {
    try {
      setNotes(await getNotes());
    } catch {
      setMessage('快记加载失败');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    let isMounted = true;

    async function loadNotes() {
      try {
        const items = await getNotes();
        if (isMounted) {
          setNotes(items);
        }
      } catch {
        if (isMounted) {
          setMessage('快记加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadNotes();

    return () => {
      isMounted = false;
    };
  }, []);

  async function handleCreate(event) {
    event.preventDefault();
    if (!content.trim()) {
      return;
    }

    try {
      await httpClient.post('/quick-notes', { content: content.trim() });
      setContent('');
      await refreshNotes();
    } catch {
      setMessage('快记保存失败');
    }
  }

  async function handleDelete(note) {
    try {
      await httpClient.delete(`/quick-notes/${note.id}`);
      await refreshNotes();
    } catch {
      setMessage('快记删除失败');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>私密快记</h1>
        <p>纯私密记录，仅自己可见。</p>
      </div>

      <form className="content-panel quick-post-form" onSubmit={handleCreate}>
        <textarea value={content} onChange={(event) => setContent(event.target.value)} rows={5} maxLength={2000} />
        <button type="submit">保存快记</button>
      </form>

      {message ? <p className="form-error relation-error">{message}</p> : null}
      {isLoading ? <div className="content-panel">正在加载快记...</div> : null}
      {!isLoading && notes.length === 0 ? (
        <div className="content-panel">
          <p className="empty-text">暂无快记。</p>
        </div>
      ) : null}
      <div className="quick-post-list">
        {notes.map((note) => (
          <article className="content-panel quick-post-card" key={note.id}>
            <p>{note.content}</p>
            <div className="article-meta">
              <span>{note.update_time}</span>
            </div>
            <button className="secondary-button" type="button" onClick={() => handleDelete(note)}>
              删除
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}

export default QuickNotePage;
