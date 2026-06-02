function SvgIcon({ children, className = '', title, ...props }) {
  return (
    <svg
      aria-hidden={title ? undefined : true}
      className={`svg-icon ${className}`.trim()}
      fill="none"
      focusable="false"
      role={title ? 'img' : undefined}
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth="2"
      viewBox="0 0 24 24"
      {...props}
    >
      {title ? <title>{title}</title> : null}
      {children}
    </svg>
  );
}

export function SearchIcon(props) {
  return (
    <SvgIcon {...props}>
      <circle cx="11" cy="11" r="7" />
      <path d="m16.5 16.5 4 4" />
    </SvgIcon>
  );
}

export function HeartIcon({ filled = false, ...props }) {
  return (
    <SvgIcon className={filled ? 'heart-icon is-filled' : 'heart-icon'} fill={filled ? 'currentColor' : 'none'} {...props}>
      <path d="M20.8 4.6a5.4 5.4 0 0 0-7.6 0L12 5.8l-1.2-1.2a5.4 5.4 0 1 0-7.6 7.6L12 21l8.8-8.8a5.4 5.4 0 0 0 0-7.6Z" />
    </SvgIcon>
  );
}

export function ChevronIcon({ direction = 'down', ...props }) {
  return (
    <SvgIcon className={`chevron-icon is-${direction}`} {...props}>
      <path d="m6 9 6 6 6-6" />
    </SvgIcon>
  );
}

