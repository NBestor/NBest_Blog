import gfm from '@bytemd/plugin-gfm';
import highlight from '@bytemd/plugin-highlight';
import math from '@bytemd/plugin-math';
import { Viewer } from '@bytemd/react';
import { useEffect, useMemo, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import 'bytemd/dist/index.css';
import 'github-markdown-css/github-markdown-light.css';
import 'highlight.js/styles/github.css';
import 'katex/dist/katex.css';

import httpClient from '../api/http-client';
import CommentThread from '../components/CommentThread';
import LikeButton from '../components/LikeButton';
import { useAuth } from '../contexts/use-auth';

const visibleTypeLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function BlogDetailPage() {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const plugins = useMemo(() => [gfm(), math(), highlight()], []);
  const [article, setArticle] = useState(null);
  const [comments, setComments] = useState([]);
  const [message, setMessage] = useState('');
  const [commentMessage, setCommentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function fetchDetail() {
    const [articleResponse, commentsResponse] = await Promise.all([
      httpClient.get(`/articles/${id}`),
      httpClient.get(`/articles/${id}/comments`),
    ]);
    setArticle(articleResponse.data);
    setComments(commentsResponse.data.items);
  }

  useEffect(() => {
    let isMounted = true;

    async function loadDetail() {
      try {
        const [articleResponse, commentsResponse] = await Promise.all([
          httpClient.get(`/articles/${id}`),
          httpClient.get(`/articles/${id}/comments`),
        ]);
        if (isMounted) {
          setArticle(articleResponse.data);
          setComments(commentsResponse.data.items);
        }
      } catch {
        if (isMounted) {
          setMessage('文章不存在或暂无访问权限');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadDetail();

    return () => {
      isMounted = false;
    };
  }, [id]);

  async function handleToggleLike() {
    try {
      if (article.is_liked) {
        await httpClient.delete(`/articles/${id}/likes`);
      } else {
        await httpClient.post(`/articles/${id}/likes`);
      }
      await fetchDetail();
    } catch {
      setMessage('点赞操作失败');
    }
  }

  async function handleToggleCollect() {
    try {
      if (article.is_collected) {
        await httpClient.delete(`/articles/${id}/collects`);
      } else {
        await httpClient.post(`/articles/${id}/collects`);
      }
      await fetchDetail();
    } catch {
      setMessage('收藏操作失败');
    }
  }

  async function handleCreateComment(content, parentId = null) {
    setCommentMessage('');
    try {
      await httpClient.post(`/articles/${id}/comments`, { content, parent_id: parentId });
      await fetchDetail();
    } catch {
      setCommentMessage('评论发布失败');
    }
  }

  async function handleToggleCommentLike(comment) {
    setCommentMessage('');
    try {
      if (comment.is_liked) {
        await httpClient.delete(`/articles/${id}/comments/${comment.id}/likes`);
      } else {
        await httpClient.post(`/articles/${id}/comments/${comment.id}/likes`);
      }
      await fetchDetail();
    } catch {
      setCommentMessage('评论点赞失败');
    }
  }

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在加载文章...</div>
      </section>
    );
  }

  if (!article) {
    return (
      <section className="page-section">
        <div className="content-panel">
          <p className="empty-text">{message}</p>
          <Link className="primary-link" to="/blog">
            返回博客
          </Link>
        </div>
      </section>
    );
  }

  return (
    <section className="page-section">
      <article className="content-panel article-detail">
        <Link className="primary-link" to="/blog">
          返回博客
        </Link>
        <h1>{article.title}</h1>
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
        <div className="markdown-body article-body">
          <Viewer plugins={plugins} value={article.content} />
        </div>
        <div className="editor-actions">
          <LikeButton count={article.like_count} disabled={!isAuthenticated} isLiked={article.is_liked} onClick={handleToggleLike} />
          <button className="secondary-button" type="button" onClick={handleToggleCollect} disabled={!isAuthenticated}>
            {article.is_collected ? '取消收藏' : '收藏'}
          </button>
          {!isAuthenticated && <p className="form-message">登录后可点赞、收藏和评论。</p>}
          {message && <p className="form-error">{message}</p>}
        </div>
      </article>

      <CommentThread
        comments={comments}
        isAuthenticated={isAuthenticated}
        message={commentMessage}
        onCreate={(content) => handleCreateComment(content)}
        onReply={(comment, content) => handleCreateComment(content, comment.id)}
        onToggleLike={handleToggleCommentLike}
      />
    </section>
  );
}

export default BlogDetailPage;
