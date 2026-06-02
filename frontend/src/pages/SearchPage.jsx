import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import httpClient from '../api/http-client';

const visibleTypeLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function SearchPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const query = searchParams.get('q')?.trim() || '';
  const [articles, setArticles] = useState([]);
  const [quickPosts, setQuickPosts] = useState([]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    let isMounted = true;

    async function loadResults() {
      if (!query) {
        setArticles([]);
        setQuickPosts([]);
        return;
      }

      setIsLoading(true);
      setMessage('');
      try {
        const response = await httpClient.get('/search', { params: { q: query } });
        if (isMounted) {
          setArticles(response.data.articles || []);
          setQuickPosts(response.data.quick_posts || []);
        }
      } catch {
        if (isMounted) {
          setMessage('搜索失败，请稍后重试');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadResults();

    return () => {
      isMounted = false;
    };
  }, [query]);

  return (
    <section className="page-section search-page">
      <div className="page-heading">
        <h1>搜索</h1>
        <p>{query ? `关键词：${query}` : '请输入关键词搜索博客或快写。'}</p>
      </div>

      {isLoading ? <div className="content-panel">正在搜索...</div> : null}
      {message ? <p className="form-error relation-error">{message}</p> : null}

      <div className="search-results-grid">
        <section className="content-panel search-section">
          <div className="section-heading-row">
            <h2>博客结果</h2>
            <span>{articles.length} 条</span>
          </div>
          {articles.length === 0 ? <p className="empty-text">暂无匹配博客。</p> : null}
          <div className="search-result-list">
            {articles.map((article) => (
              <article
                className="search-result-card clickable-card"
                key={article.id}
                onClick={() => navigate(`/blog/detail/${article.id}`)}
              >
                <h3>{article.title}</h3>
                <p>{article.summary || '暂无简介'}</p>
                <div className="article-meta">
                  <span>{article.author_nickname}</span>
                  <span>{article.category_name || '无分类'}</span>
                  <span>{visibleTypeLabels[article.visible_type] || '仅自己可见'}</span>
                  <span>{article.like_count} 赞</span>
                  <span>{article.comment_count} 评论</span>
                </div>
                <div className="draft-meta">
                  {(article.tags || []).map((tag) => (
                    <span key={tag}>{tag}</span>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="content-panel search-section">
          <div className="section-heading-row">
            <h2>快写结果</h2>
            <span>{quickPosts.length} 条</span>
          </div>
          {quickPosts.length === 0 ? <p className="empty-text">暂无匹配快写。</p> : null}
          <div className="search-result-list">
            {quickPosts.map((post) => (
              <article
                className="search-result-card clickable-card"
                key={post.id}
                onClick={() => navigate(`/quick-posts/${post.id}`)}
              >
                <p>{post.content}</p>
                <div className="article-meta">
                  <span>{post.author_nickname}</span>
                  <span>{visibleTypeLabels[post.visible_type] || '仅自己可见'}</span>
                  <span>{post.like_count} 赞</span>
                  <span>{post.comment_count} 评论</span>
                  <span>{post.update_time}</span>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </section>
  );
}

export default SearchPage;

