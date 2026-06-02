import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';

const emptyForm = {
  title: '',
  category: '',
  due_date: '',
  content: '',
};

function buildPayload(formData, isDone = false) {
  return {
    title: formData.title.trim(),
    category: formData.category.trim() || null,
    due_date: formData.due_date || null,
    content: formData.content.trim() || null,
    is_done: isDone,
  };
}

function TodoPage() {
  const [todos, setTodos] = useState([]);
  const [formData, setFormData] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState(emptyForm);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function getTodos() {
    const response = await httpClient.get('/todos');
    return response.data.items;
  }

  async function refreshTodos() {
    try {
      setTodos(await getTodos());
    } catch {
      setMessage('待办加载失败');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    let isMounted = true;

    async function loadTodos() {
      try {
        const items = await getTodos();
        if (isMounted) {
          setTodos(items);
        }
      } catch {
        if (isMounted) {
          setMessage('待办加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadTodos();

    return () => {
      isMounted = false;
    };
  }, []);

  function handleFormChange(event) {
    const { name, value } = event.target;
    setFormData((currentData) => ({ ...currentData, [name]: value }));
  }

  function handleEditChange(event) {
    const { name, value } = event.target;
    setEditData((currentData) => ({ ...currentData, [name]: value }));
  }

  async function handleCreate(event) {
    event.preventDefault();
    setMessage('');
    if (!formData.title.trim()) {
      return;
    }

    try {
      await httpClient.post('/todos', buildPayload(formData));
      setFormData(emptyForm);
      await refreshTodos();
    } catch {
      setMessage('待办创建失败');
    }
  }

  function startEdit(todo) {
    setEditingId(todo.id);
    setEditData({
      title: todo.title,
      category: todo.category || '',
      due_date: todo.due_date || '',
      content: todo.content || '',
    });
  }

  async function handleUpdate(event, todo) {
    event.preventDefault();
    setMessage('');
    if (!editData.title.trim()) {
      return;
    }

    try {
      await httpClient.put(`/todos/${todo.id}`, buildPayload(editData, todo.is_done));
      setEditingId(null);
      setEditData(emptyForm);
      await refreshTodos();
    } catch {
      setMessage('待办保存失败');
    }
  }

  async function handleToggleDone(todo) {
    setMessage('');
    try {
      await httpClient.patch(`/todos/${todo.id}/status`, { is_done: !todo.is_done });
      await refreshTodos();
    } catch {
      setMessage('状态更新失败');
    }
  }

  async function handleDelete(todo) {
    setMessage('');
    try {
      await httpClient.delete(`/todos/${todo.id}`);
      await refreshTodos();
    } catch {
      setMessage('待办删除失败');
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>待办清单</h1>
        <p>记录自己的任务、截止时间和到期提醒。</p>
      </div>

      <form className="content-panel todo-form" onSubmit={handleCreate}>
        <div className="todo-form-grid">
          <label>
            标题
            <input name="title" value={formData.title} onChange={handleFormChange} maxLength={120} required />
          </label>
          <label>
            分类
            <input name="category" value={formData.category} onChange={handleFormChange} maxLength={40} />
          </label>
          <label>
            截止日期
            <input name="due_date" type="date" value={formData.due_date} onChange={handleFormChange} />
          </label>
        </div>
        <label>
          内容
          <textarea name="content" value={formData.content} onChange={handleFormChange} rows={3} maxLength={1000} />
        </label>
        <button type="submit">新增待办</button>
      </form>

      {message ? <p className="form-error relation-error">{message}</p> : null}
      {isLoading ? <div className="content-panel">正在加载待办...</div> : null}
      {!isLoading && todos.length === 0 ? (
        <div className="content-panel">
          <p className="empty-text">暂无待办。</p>
        </div>
      ) : null}

      <div className="todo-list">
        {todos.map((todo) => (
          <article className={`content-panel todo-card ${todo.is_done ? 'is-done' : ''}`} key={todo.id}>
            {editingId === todo.id ? (
              <form className="todo-edit-form" onSubmit={(event) => handleUpdate(event, todo)}>
                <div className="todo-form-grid">
                  <label>
                    标题
                    <input name="title" value={editData.title} onChange={handleEditChange} maxLength={120} required />
                  </label>
                  <label>
                    分类
                    <input name="category" value={editData.category} onChange={handleEditChange} maxLength={40} />
                  </label>
                  <label>
                    截止日期
                    <input name="due_date" type="date" value={editData.due_date} onChange={handleEditChange} />
                  </label>
                </div>
                <label>
                  内容
                  <textarea
                    name="content"
                    value={editData.content}
                    onChange={handleEditChange}
                    rows={3}
                    maxLength={1000}
                  />
                </label>
                <div className="editor-actions">
                  <button type="submit">保存</button>
                  <button className="secondary-button" type="button" onClick={() => setEditingId(null)}>
                    取消
                  </button>
                </div>
              </form>
            ) : (
              <>
                <div className="todo-card-header">
                  <label className="todo-check">
                    <input type="checkbox" checked={todo.is_done} onChange={() => handleToggleDone(todo)} />
                    <span>{todo.is_done ? '已完成' : '未完成'}</span>
                  </label>
                  <div className="todo-card-meta">
                    {todo.category ? <span>{todo.category}</span> : null}
                    {todo.due_date ? <span>截止 {todo.due_date}</span> : <span>无截止日期</span>}
                  </div>
                </div>
                <h2>{todo.title}</h2>
                {todo.content ? <p>{todo.content}</p> : null}
                <div className="article-meta">
                  <span>更新 {todo.update_time}</span>
                </div>
                <div className="editor-actions">
                  <button type="button" onClick={() => startEdit(todo)}>
                    编辑
                  </button>
                  <button className="secondary-button" type="button" onClick={() => handleDelete(todo)}>
                    删除
                  </button>
                </div>
              </>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}

export default TodoPage;
