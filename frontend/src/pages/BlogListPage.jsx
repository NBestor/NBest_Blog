import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import httpClient from '../api/http-client';

const visibleTypeLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function BlogListPage() {
  const navigate = useNavigate();
  const [articles, setArticles] = useState([]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let isMounted = true;

    async function fetchArticles() {
      try {
        const response = await httpClient.get('/articles');
        if (isMounted) {
          setArticles(response.data.items);
        }
      } catch {
        if (isMounted) {
          setMessage('文章列表加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchArticles();

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>博客文章</h1>
        <p>阅读公开文章，以及你有权限访问的好友或私密文章。</p>
      </div>

      {isLoading ? <div className="content-panel">正在加载文章...</div> : null}
      {message ? <p className="form-error relation-error">{message}</p> : null}
      {!isLoading && articles.length === 0 ? (
        <div className="content-panel">
          <p className="empty-text">暂无可见文章。</p>
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
                <span>{visibleTypeLabels[article.visible_type] || '仅自己可见'}</span>
                <span>{article.like_count} 赞</span>
                <span>{article.comment_count} 评论</span>
              </div>
              <div className="draft-meta">
                {article.tags.map((tag) => (
                  <span key={tag}>{tag}</span>
                ))}
              </div>
            </div>
            <span className="article-time">{article.update_time}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

export default BlogListPage;
