import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import httpClient from '../api/http-client';
import { ChevronIcon } from '../components/icons';
import LikeButton from '../components/LikeButton';
import { useAuth } from '../contexts/use-auth';

const visibleLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function formatMonth(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}`;
}

function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function buildMonthDays(date) {
  const year = date.getFullYear();
  const month = date.getMonth();
  const firstDay = new Date(year, month, 1);
  const start = new Date(year, month, 1 - firstDay.getDay());
  return Array.from({ length: 42 }, (_, index) => {
    const day = new Date(start);
    day.setDate(start.getDate() + index);
    return {
      date: formatDate(day),
      dayNumber: day.getDate(),
      isCurrentMonth: day.getMonth() === month,
    };
  });
}

function sortCalendarEvents(events) {
  const today = formatDate(new Date());
  return [...events].sort((a, b) => {
    const aPast = a.display_date < today;
    const bPast = b.display_date < today;
    if (aPast !== bPast) {
      return aPast ? 1 : -1;
    }
    return a.display_date.localeCompare(b.display_date);
  });
}

function HomeCalendar({ events, message, onOpenCalendar }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const monthDate = useMemo(() => new Date(), []);
  const monthKey = formatMonth(monthDate);
  const days = useMemo(() => buildMonthDays(monthDate), [monthDate]);
  const eventDates = useMemo(() => new Set(events.map((event) => event.display_date)), [events]);
  const sortedEvents = useMemo(() => sortCalendarEvents(events), [events]);
  const today = formatDate(new Date());

  return (
    <aside className="content-panel home-month-calendar">
      <button className="home-calendar-compact" onClick={onOpenCalendar} type="button">
        日历
      </button>
      <div className="home-calendar-full">
        <div className="home-widget-head">
          <div>
            <h2>日历</h2>
            <span>{monthKey}</span>
          </div>
          <div className="home-calendar-actions">
            <button className="secondary-button" onClick={onOpenCalendar} type="button">
              详情
            </button>
            <button
              aria-expanded={isExpanded}
              aria-label={isExpanded ? '收起本月事件' : '展开本月事件'}
              className="calendar-expand-button"
              onClick={() => setIsExpanded((value) => !value)}
              type="button"
            >
              <ChevronIcon direction={isExpanded ? 'up' : 'down'} />
            </button>
          </div>
        </div>
        {message ? <p className="form-error">{message}</p> : null}
        <div className="mini-calendar-weekdays">
          {['日', '一', '二', '三', '四', '五', '六'].map((day) => (
            <span key={day}>{day}</span>
          ))}
        </div>
        <div className="mini-calendar-grid">
          {days.map((day) => (
            <span
              className={[
                'mini-calendar-day',
                day.isCurrentMonth ? '' : 'is-muted',
                eventDates.has(day.date) ? 'has-event' : '',
                day.date === today ? 'is-today' : '',
              ]
                .filter(Boolean)
                .join(' ')}
              key={day.date}
            >
              {day.dayNumber}
            </span>
          ))}
        </div>
        {isExpanded ? (
          <div className="calendar-event-popover">
            <div className="home-widget-head">
              <h3>本月事件</h3>
              <button className="secondary-button" onClick={onOpenCalendar} type="button">
                打开日历
              </button>
            </div>
            {sortedEvents.length === 0 ? <p className="empty-text">本月暂无事件。</p> : null}
            {sortedEvents.map((event) => {
              const isPast = event.display_date < today;
              return (
                <article className={`calendar-popover-event ${isPast ? 'is-past' : ''}`} key={`${event.id}-${event.display_date}`}>
                  <strong>{event.title}</strong>
                  <span>{event.display_date}</span>
                </article>
              );
            })}
          </div>
        ) : null}
      </div>
    </aside>
  );
}

function HomePage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [articles, setArticles] = useState([]);
  const [quickPosts, setQuickPosts] = useState([]);
  const [todos, setTodos] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [content, setContent] = useState('');
  const [visibleType, setVisibleType] = useState('public');
  const [message, setMessage] = useState('');
  const [todoMessage, setTodoMessage] = useState('');
  const [calendarMessage, setCalendarMessage] = useState('');
  const [isTodoOpen, setIsTodoOpen] = useState(true);
  const [isLoading, setIsLoading] = useState(true);

  const upcomingTodos = useMemo(() => todos.filter((todo) => !todo.is_done).slice(0, 5), [todos]);

  const loadHome = useCallback(async () => {
    setMessage('');
    const publicRequests = [httpClient.get('/articles'), httpClient.get('/quick-posts')];
    const privateRequests = isAuthenticated
      ? [
          httpClient.get('/todos').catch(() => ({ data: { items: [] }, privateError: 'todo' })),
          httpClient
            .get('/calendar-events', { params: { month: formatMonth(new Date()) } })
            .catch(() => ({ data: { items: [] }, privateError: 'calendar' })),
          httpClient.get('/users/me/settings').catch(() => null),
        ]
      : [];

    try {
      const [articlesResponse, quickPostsResponse, todosResponse, calendarResponse, settingsResponse] = await Promise.all([
        ...publicRequests,
        ...privateRequests,
      ]);
      setArticles(articlesResponse.data.items);
      setQuickPosts(quickPostsResponse.data.items);

      if (isAuthenticated) {
        setTodos(todosResponse?.data?.items || []);
        setCalendarEvents(calendarResponse?.data?.items || []);
        setTodoMessage(todosResponse?.privateError ? '待办加载失败' : '');
        setCalendarMessage(calendarResponse?.privateError ? '日历加载失败' : '');
        if (settingsResponse?.data?.quick_post_default_visible_type) {
          setVisibleType(settingsResponse.data.quick_post_default_visible_type);
        }
      } else {
        setTodos([]);
        setCalendarEvents([]);
        setTodoMessage('');
        setCalendarMessage('');
      }
    } catch {
      setMessage('首页内容加载失败');
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    let isMounted = true;

    async function run() {
      if (isMounted) {
        setIsLoading(true);
      }
      await loadHome();
    }

    run();

    return () => {
      isMounted = false;
    };
  }, [isAuthenticated, loadHome]);

  async function handleCreateQuickPost(event) {
    event.preventDefault();
    if (!content.trim()) {
      return;
    }

    try {
      await httpClient.post('/quick-posts', { content: content.trim(), visible_type: visibleType });
      setContent('');
      await loadHome();
    } catch {
      setMessage('快写发布失败');
    }
  }

  async function handleToggleQuickPostLike(event, post) {
    event.stopPropagation();
    try {
      if (post.is_liked) {
        await httpClient.delete(`/quick-posts/${post.id}/likes`);
      } else {
        await httpClient.post(`/quick-posts/${post.id}/likes`);
      }
      await loadHome();
    } catch {
      setMessage('点赞操作失败');
    }
  }

  async function handleDeleteQuickPost(event, post) {
    event.stopPropagation();
    try {
      await httpClient.delete(`/quick-posts/${post.id}`);
      await loadHome();
    } catch {
      setMessage('删除失败');
    }
  }

  return (
    <section className="page-section home-dashboard-page">
      <div className="page-heading">
        <h1>首页</h1>
        <p>博客、快写、待办和日历在这里汇合。</p>
      </div>

      {isAuthenticated ? (
        <aside className={`home-todo-guide ${isTodoOpen ? 'is-open' : 'is-closed'}`}>
          <button className="home-todo-toggle" onClick={() => setIsTodoOpen((value) => !value)} type="button">
            待办
          </button>
          {isTodoOpen ? (
            <div className="home-todo-panel">
              <div className="home-widget-head">
                <h2>待办</h2>
                <button onClick={() => navigate('/todo')} type="button">
                  查看
                </button>
              </div>
              {todoMessage ? <p className="form-error">{todoMessage}</p> : null}
              {upcomingTodos.length === 0 ? <p className="empty-text">暂无未完成待办。</p> : null}
              {upcomingTodos.map((todo) => (
                <button className="home-mini-item" key={todo.id} onClick={() => navigate('/todo')} type="button">
                  <strong>{todo.title}</strong>
                  <span>{todo.due_date || '无截止日期'}</span>
                </button>
              ))}
            </div>
          ) : null}
        </aside>
      ) : null}

      {message ? <p className="form-error relation-error">{message}</p> : null}
      {isLoading ? <div className="content-panel">正在加载首页...</div> : null}

      <div className="home-main-grid">
        <section className="home-article-column">
          <div className="section-heading-row">
            <h2>博客</h2>
            <button className="secondary-button" onClick={() => navigate('/blog')} type="button">
              全部
            </button>
          </div>
          {articles.length === 0 ? (
            <div className="content-panel">
              <p className="empty-text">暂无可见博客。</p>
            </div>
          ) : null}
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
                    <span>{article.author_nickname}</span>
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
                <span className="article-time">{article.update_time}</span>
              </article>
            ))}
          </div>
        </section>

        <aside className="home-right-rail">
          {isAuthenticated ? <HomeCalendar events={calendarEvents} message={calendarMessage} onOpenCalendar={() => navigate('/calendar')} /> : null}

          <section className="home-quick-column">
            {isAuthenticated ? (
              <form className="content-panel quick-post-form" onSubmit={handleCreateQuickPost}>
                <textarea
                  maxLength={1000}
                  onChange={(event) => setContent(event.target.value)}
                  placeholder="写一条快写..."
                  rows={4}
                  value={content}
                />
                <div>
                  <select onChange={(event) => setVisibleType(event.target.value)} value={visibleType}>
                    <option value="public">公开</option>
                    <option value="friend">好友可见</option>
                    <option value="self">仅自己可见</option>
                  </select>
                  <button type="submit">发布快写</button>
                </div>
              </form>
            ) : (
              <div className="content-panel">
                <p className="empty-text">登录后可以发布快写、查看待办和日历。</p>
              </div>
            )}

            <div className="section-heading-row">
              <h2>快写</h2>
            </div>
            {quickPosts.length === 0 ? (
              <div className="content-panel">
                <p className="empty-text">暂无可见快写。</p>
              </div>
            ) : null}
            <div className="quick-post-list compact">
              {quickPosts.map((post) => (
                <article
                  className="content-panel quick-post-card clickable-card"
                  key={post.id}
                  onClick={() => navigate(`/quick-posts/${post.id}`)}
                >
                  <div className="article-meta">
                    <span>{post.author_nickname}</span>
                    <span>{visibleLabels[post.visible_type]}</span>
                  </div>
                  <p>{post.content}</p>
                  <div className="article-meta">
                    <span>{post.like_count} 赞</span>
                    <span>{post.comment_count} 评论</span>
                    <span>{post.create_time}</span>
                  </div>
                  <div className="editor-actions">
                    <LikeButton
                      count={post.like_count}
                      disabled={!isAuthenticated}
                      isLiked={post.is_liked}
                      onClick={(event) => handleToggleQuickPostLike(event, post)}
                    />
                    {post.can_manage ? (
                      <button className="secondary-button" onClick={(event) => handleDeleteQuickPost(event, post)} type="button">
                        删除
                      </button>
                    ) : null}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </aside>
      </div>
    </section>
  );
}

export default HomePage;

