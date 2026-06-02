import { useState } from 'react';

import LikeButton from './LikeButton';

function CommentComposer({ disabled = false, onSubmit, placeholder = '请说点什么吧~', submitLabel = '评论' }) {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    const value = content.trim();
    if (!value || disabled || isSubmitting) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(value);
      setContent('');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form className="comment-composer" onSubmit={handleSubmit}>
      <textarea
        value={content}
        onChange={(event) => setContent(event.target.value)}
        maxLength={500}
        rows={4}
        placeholder={placeholder}
        disabled={disabled || isSubmitting}
      />
      <button type="submit" disabled={disabled || isSubmitting || !content.trim()}>
        {isSubmitting ? '发送中' : submitLabel}
      </button>
    </form>
  );
}

function CommentItem({ comment, depth, isAuthenticated, onReply, onToggleLike }) {
  const [isReplying, setIsReplying] = useState(false);
  const indentDepth = Math.min(depth, 4);

  async function handleReply(content) {
    await onReply(comment, content);
    setIsReplying(false);
  }

  return (
    <article className="comment-thread-item" style={{ '--comment-depth': indentDepth }}>
      <div className="comment-thread-card">
        <div className="comment-thread-head">
          <strong>{comment.author_nickname}</strong>
          <span>{comment.create_time}</span>
        </div>
        <p>{comment.content}</p>
        <div className="comment-thread-actions">
          <LikeButton
            count={comment.like_count || 0}
            disabled={!isAuthenticated}
            isLiked={comment.is_liked}
            onClick={() => onToggleLike(comment)}
          />
          {isAuthenticated ? (
            <button className="secondary-button" type="button" onClick={() => setIsReplying((value) => !value)}>
              回复
            </button>
          ) : null}
        </div>
        {isReplying ? (
          <CommentComposer onSubmit={handleReply} submitLabel="回复" />
        ) : null}
      </div>
      {comment.children?.length ? (
        <div className="comment-thread-children">
          {comment.children.map((child) => (
            <CommentItem
              key={child.id}
              comment={child}
              depth={depth + 1}
              isAuthenticated={isAuthenticated}
              onReply={onReply}
              onToggleLike={onToggleLike}
            />
          ))}
        </div>
      ) : null}
    </article>
  );
}

function CommentThread({ comments, isAuthenticated, message, onCreate, onReply, onToggleLike }) {
  return (
    <section className="content-panel comment-panel">
      <h2>评论</h2>
      {message ? <p className="form-error">{message}</p> : null}
      {comments.length === 0 ? <p className="empty-text">暂无评论。</p> : null}
      <div className="comment-thread-list">
        {comments.map((comment) => (
          <CommentItem
            key={comment.id}
            comment={comment}
            depth={0}
            isAuthenticated={isAuthenticated}
            onReply={onReply}
            onToggleLike={onToggleLike}
          />
        ))}
      </div>
      {isAuthenticated ? (
        <CommentComposer onSubmit={(content) => onCreate(content)} submitLabel="发表评论" />
      ) : (
        <p className="form-message">登录后可以评论、回复和点赞。</p>
      )}
    </section>
  );
}

export default CommentThread;
