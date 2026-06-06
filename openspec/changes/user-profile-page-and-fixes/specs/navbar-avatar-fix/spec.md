## MODIFIED Requirements

### Requirement: Navbar Avatar Display with Correct URL
导航栏（`AppLayout.jsx`）右上角用户区域 SHALL 正确显示用户头像图片。当 `user.avatar_url` 为相对路径（如 `/static/uploads/avatars/1/avatar.jpg`）时，MUST 拼接后端基础 URL `http://127.0.0.1:8000` 前缀；当 `avatar_url` 已为完整 URL（以 `http` 开头）时，SHALL 直接使用。当用户未设置头像时，SHALL 显示首字母占位符。

处理逻辑 SHALL 与 `ProfilePage.jsx` 保持一致：
```javascript
const avatarUrl = user?.avatar_url
  ? user.avatar_url.startsWith('http')
    ? user.avatar_url
    : `http://127.0.0.1:8000${user.avatar_url}`
  : '';
```

#### Scenario: 有头像用户正确显示头像
- **WHEN** 已登录用户设置了头像（`user.avatar_url = '/static/uploads/avatars/1/avatar.jpg'`）
- **THEN** 导航栏显示圆形头像图片，`<img>` 的 `src` 属性值为 `http://127.0.0.1:8000/static/uploads/avatars/1/avatar.jpg`
- **AND** 头像可以正常加载显示

#### Scenario: 无头像用户显示首字母占位符
- **WHEN** 已登录用户未设置头像（`user.avatar_url` 为空或 null）
- **THEN** 导航栏显示首字母占位符 `<span className="navbar-avatar-placeholder">`

#### Scenario: 游客不显示头像
- **WHEN** 用户未登录
- **THEN** 导航栏不显示头像或占位符，仅显示「登录」链接

#### Scenario: 头像 URL 已是完整路径
- **WHEN** `user.avatar_url` 已以 `http` 开头
- **THEN** 直接使用 `user.avatar_url` 作为 `<img>` 的 `src`，不拼接前缀