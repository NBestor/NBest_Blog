import { HeartIcon } from './icons';

function LikeButton({ count = 0, disabled = false, isLiked = false, onClick, title = '点赞' }) {
  return (
    <button
      aria-pressed={isLiked}
      className={`like-button ${isLiked ? 'is-liked' : ''}`}
      disabled={disabled}
      onClick={onClick}
      title={title}
      type="button"
    >
      <HeartIcon filled={isLiked} />
      <span>{count}</span>
    </button>
  );
}

export default LikeButton;

