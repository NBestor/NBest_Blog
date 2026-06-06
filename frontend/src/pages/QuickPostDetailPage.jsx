import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

import httpClient from '../api/http-client';
import CommentThread from '../components/CommentThread';
import LikeButton from '../components/LikeButton';
import { useAuth } from '../contexts/use-auth';

const visibleLabels = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};

function QuickPostDetailPage() {
  const { id } = useParams();
  const { isAuthenticated, user } = useAuth();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [message, setMessage] = useState('');
  const [commentMessage, setCommentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [editingPostId, setEditingPostId] = useState(null);
  const [editContent, setEditContent] = useState('');
  const [editVisibleType, setEditVisibleType] = useState('public');

  async function fetchDetail() {
    const [postResponse, commentsResponse] = await Promise.all([
      httpClient.get(`/quick-posts/${id}`),
      httpClient.get(`/quick-posts/${id}/comments`),
    ]);
    setPost(postResponse.data);
    setComments(commentsResponse.data.items);
  }

  useEffect(() => {
    let isMounted = true;

    async function loadDetail() {
      try {
        const [postResponse, commentsResponse] = await Promise.all([
          httpClient.get(`/quick-posts/${id}`),
          httpClient.get(`/quick-posts/${id}/comments`),
        ]);
        if (isMounted) {
          setPost(postResponse.data);
          setComments(commentsResponse.data.items);
        }
      } catch {
        if (isMounted) {
          setMessage('快写不存在或暂无访问权限');
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
      if (post.is_liked) {
        await httpClient.delete(`/quick-posts/${id}/likes`);
      } else {
        await httpClient.post(`/quick-posts/${id}/likes`);
      }
      await fetchDetail();
    } catch {
      setMessage('点赞操作失败');
    }
  }

  async function handleCreateComment(content, parentId = null) {
    setCommentMessage('');
    try {
      await httpClient.post(`/quick-posts/${id}/comments`, { content, parent_id: parentId });
      await fetchDetail();
    } catch {
      setCommentMessage('评论发布失败');
    }
  }

  async function handleToggleCommentLike(comment) {
    setCommentMessage('');
    try {
      if (comment.is_liked) {
        await httpClient.delete(`/quick-posts/${id}/comments/${comment.id}/likes`);
      } else {
        await httpClient.post(`/quick-posts/${id}/comments/${comment.id}/likes`);
      }
      await fetchDetail();
    } catch {
      setCommentMessage('评论点赞失败');
    }
  }

  function handleStartEdit() {
    setEditingPostId(post.id);
    setEditContent(post.content);
    setEditVisibleType(post.visible_type);
  }

  function handleCancelEdit() {
    setEditingPostId(null);
    setEditContent('');
  }

  async function handleSaveEdit() {
    if (!editContent.trim()) {
      setMessage('内容不能为空');
      return;
    }

    try {
      await httpClient.put(`/quick-posts/${post.id}`, {
        content: editContent.trim(),
        visible_type: editVisibleType,
      });
      setEditingPostId(null);
      setEditContent('');
      await fetchDetail();
    } catch {
      setMessage('快写编辑失败');
    }
  }

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在加载快写...</div>
      </section>
    );
  }

  if (!post) {
    return (
      <section className="page-section">
        <div className="content-panel">
          <p className="empty-text">{message}</p>
          <Link className="primary-link" to="/">
            返回首页
          </Link>
        </div>
      </section>
    );
  }

  return (
    <section className="page-section quick-post-detail-page">
      <article className="content-panel quick-post-detail">
        <Link className="primary-link" to="/">
          返回首页
        </Link>
        <div className="article-meta">
          <Link to={`/user/${post.user_id}`}>{post.author_nickname}</Link>
          <span>{visibleLabels[post.visible_type]}</span>
          <span>{post.like_count} 赞</span>
          <span>{post.comment_count} 评论</span>
          <span>{post.create_time}</span>
        </div>
        {editingPostId === post.id ? (
          <>
            <textarea
              maxLength={1000}
              onChange={(event) => setEditContent(event.target.value)}
              rows={4}
              value={editContent}
            />
            <div className="editor-actions">
              <select onChange={(event) => setEditVisibleType(event.target.value)} value={editVisibleType}>
                <option value="public">公开</option>
                <option value="friend">好友可见</option>
                <option value="self">仅自己可见</option>
              </select>
              <button onClick={handleSaveEdit} type="button">
                保存
              </button>
              <button className="secondary-button" onClick={handleCancelEdit} type="button">
                取消
              </button>
            </div>
          </>
        ) : (
          <p>{post.content}</p>
        )}
        <div className="editor-actions">
          <LikeButton count={post.like_count} disabled={!isAuthenticated} isLiked={post.is_liked} onClick={handleToggleLike} />
          {user && post.user_id === user.id && editingPostId !== post.id && (
            <button className="secondary-button" type="button" onClick={handleStartEdit}>
              ✏️ 编辑
            </button>
          )}
          {!isAuthenticated && <p className="form-message">登录后可点赞和评论。</p>}
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

export default QuickPostDetailPage;
