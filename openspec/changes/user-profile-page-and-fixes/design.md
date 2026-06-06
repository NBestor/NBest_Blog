## Context

本项目当前有3个待解决问题：

1. **导航栏头像不显示** — `AppLayout.jsx` 中 `<img>` 的 `src` 使用相对路径 `/static/uploads/avatars/...`，缺少后端基础 URL 前缀，浏览器无法加载
2. **设置页快写可见范围冗余** — `UserSettingPage.jsx` 只有快写默认可见范围一个功能，与 `HomePage.jsx` 发布快写时的下拉框功能重叠
3. **缺少用户公开个人页面** — 博客详情/列表、快写详情/列表中的作者名都是 `<span>` 纯文本，无法点击跳转

后端 `formatArticle()` 和 `formatQuickPost()` 已返回 `user_id` 字段，无需修改后端现有接口。

## Goals / Non-Goals

**Goals:**
- 修复导航栏头像 `src` 路径，使其与 `ProfilePage.jsx` 处理方式一致
- 移除 `UserSettingPage.jsx` 中快写默认权限表单，改为提示文字
- 新增后端 `GET /users/{id}/profile` 接口
- 新建前端 `UserProfilePage.jsx` 用户公开个人页面
- 将各处作者名 `<span>` 改为 `<Link to={/user/${id}}>` 可点击链接
- 新增路由 `/user/:id`

**Non-Goals:**
- 不修改 `HomePage.jsx` 读取 `quick_post_default_visible_type` 的逻辑（仍需从后端读取默认值）
- 不修改后端 `/users/me/settings` 接口（保留给 HomePage 使用）
- 不在 UserProfilePage 中添加「关注/取消关注」按钮（关注功能在 FollowPage 已有）
- 不修改数据库 schema

## Decisions

### 1. 导航栏头像修复

**选择**：在 `AppLayout.jsx` 中，头像 `img` 的 `src` 添加 `http://127.0.0.1:8000` 前缀（当 `avatar_url` 为相对路径时）。

```jsx
const avatarUrl = user?.avatar_url
  ? user.avatar_url.startsWith('http')
    ? user.avatar_url
    : `http://127.0.0.1:8000${user.avatar_url}`
  : '';
```

**理由**：
- 与 `ProfilePage.jsx` 中已有的处理逻辑完全一致
- 后端存储的 `avatar_url` 格式为 `/static/uploads/avatars/{userId}/avatar.jpg`
- 如果将来改为完整 URL（如 CDN），`startsWith('http')` 判断可兼容

### 2. 移除设置页快写可见范围 UI

**选择**：将 `UserSettingPage.jsx` 的表单替换为提示文字。

```jsx
<div className="content-panel">
  <h2>快写默认权限</h2>
  <p>快写的可见范围可在首页发布快写时直接设置。</p>
</div>
```

**理由**：
- `HomePage.jsx` 发布快写时已有一个 `<select>` 下拉框选择 visible_type
- 设置页的 `quick_post_default_visible_type` 仅作为初始化默认值，用户每次发布都可以覆盖
- 后端 `/users/me/settings` GET 接口保留不动，`HomePage.jsx` 初始化时仍会调用以获取默认值
- 后端 `/users/me/settings` PUT 接口也保留，万一以后需要恢复此功能

### 3. 用户公开个人页面 — 后端接口

**选择**：新增 `GET /users/{id}/profile`，无需鉴权（公开访问）。

返回格式：
```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "nickname": "Alice",
    "avatar_url": "/static/uploads/avatars/1/avatar.jpg",
    "signature": "Hello World",
    "role": "user",
    "create_time": "2025-01-01 12:00:00"
  },
  "stats": {
    "following_count": 10,
    "follower_count": 5,
    "article_count": 3,
    "quick_post_count": 8
  },
  "articles": [...],
  "quick_posts": [...]
}
```

实现细节：
- `user_service.py` 新增 `getUserProfile(targetUserId, currentUserId)` 函数
  - 获取用户基本信息（`getUserById`）
  - SQL 统计关注数、粉丝数
  - 调用 `article_service.listVisibleArticles()` 过滤出该用户的公开文章
  - 调用 `quick_post_service.listVisibleQuickPosts()` 过滤出该用户的公开快写
- API 层支持 `currentUser` 可选（`getOptionalCurrentUser`），游客也可访问
- 文章和快写列表会根据 `currentUserId` 过滤可见性（游客只能看 public，登录用户可看 public + friend）

**理由**：
- 复用现有的 `listVisibleArticles()` / `listVisibleQuickPosts()` 函数，它们已处理可见性过滤
- 无需新建专门的按用户查询的 SQL
- 游客可以查看任何用户的公开内容

### 4. 用户公开个人页面 — 前端

**选择**：新建 `UserProfilePage.jsx`，路由 `/user/:id`。

页面布局：
```
┌─────────────────────────────────────────┐
│  用户头像 (大)                           │
│  昵称 (h1)                              │
│  @username                              │
│  个性签名                                │
│  关注: N  |  粉丝: N  |  博客: N  |  快写: N │
├─────────────────────────────────────────┤
│  Tab: [博客] [快写]                      │
├─────────────────────────────────────────┤
│  博客/快写列表                           │
└─────────────────────────────────────────┘
```

- 使用 `useParams()` 获取 `id`
- 调用 `GET /users/{id}/profile` 获取数据
- Tab 切换博客/快写列表
- 列表中的每项可点击跳转到详情页
- 头像使用与 ProfilePage 相同的处理逻辑

**理由**：
- 简洁明了的布局，突出用户信息和内容
- Tab 切换避免一次性加载过多内容
- 复用现有 `content-panel` / `article-card` / `quick-post-card` 等样式

### 5. 各处作者名改为可点击链接

**选择**：将各处 `<span>{author_nickname}</span>` 替换为 `<Link to={/user/${user_id}}>{author_nickname}</Link>`。

涉及文件：
- `BlogDetailPage.jsx` — `article.author_nickname` → Link，使用 `article.user_id`
- `QuickPostDetailPage.jsx` — `post.author_nickname` → Link，使用 `post.user_id`
- `HomePage.jsx` — 博客列表和快写列表中的 `author_nickname` → Link，使用 `user_id`
- `BlogListPage.jsx` — 文章卡片中的 `author_nickname` → Link，使用 `user_id`

**理由**：
- 后端返回数据已包含 `user_id`
- 使用 React Router `<Link>` 实现 SPA 内跳转
- 样式上保持与现有文字一致的 `.article-meta span` 外观

### 6. 路由配置

**选择**：在 `route-config.js` 中添加新路由，在 `App.jsx` 中添加路由映射。

```javascript
// route-config.js
{ path: '/user/:id', label: '用户主页', title: '用户主页', visibility: 'public', showInNav: false },

// App.jsx
{ path: 'user/:id', element: <UserProfilePage /> }
```

**理由**：
- `showInNav: false` — 用户主页不在导航栏中显示（通过点击作者名进入）
- `visibility: 'public'` — 游客也可访问

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 用户不存在时返回 404 | 后端检查 `getUserById` 返回 None 时抛 404 |
| 游客访问 friend-only 内容 | `listVisibleArticles/listVisibleQuickPosts` 已处理可见性过滤 |
| 硬编码 `http://127.0.0.1:8000` 不够灵活 | 与 `ProfilePage.jsx` 保持一致，后续可统一提取为常量 |
| 设置页移除 UI 后用户找不到设置入口 | 改为提示文字，引导用户去首页设置 |
| UserProfilePage 加载数据量大 | Tab 切分 + 后端分页（复用已有分页逻辑） |

### 7. 导航栏用户名/头像可点击

**选择**：将导航栏中头像和用户名包裹在 `<Link to={/user/${user.id}}>` 中。

```jsx
<Link to={`/user/${user.id}`}>
  {avatarUrl ? (
    <img className="navbar-avatar" src={avatarUrl} alt={displayName} />
  ) : (
    <span className="navbar-avatar-placeholder">{displayName?.charAt(0)}</span>
  )}
  <span className="user-chip">{displayName}</span>
</Link>
```

**理由**：
- 与各处作者名改为 Link 的行为保持一致
- `user.id` 来自 AuthContext，始终可用
- 无头像用户同样可点击占位符跳转

### 8. 个人中心与用户主页合并

**选择**：改造 `UserProfilePage.jsx`，当 `id === user.id` 时顶部显示「个人主页」/「个人设置」两个 Tab。

**「个人主页」Tab**：与当前 UserProfilePage 展示逻辑一致。

**「个人设置」Tab**：整合 ProfilePage 功能区域：
- 头像预览 + 上传/重置
- 资料修改表单（昵称 + 签名）
- 密码修改表单

**路由变化**：
- `/user/:id` — 用户主页（合并后的页面）
- 移除 `/user/profile` — 功能合并到 `/user/{myId}` 的「个人设置」Tab
- 移除 `/user/setting` — 只剩快写默认权限提示文字，不再需要独立页面
- 从 `route-config.js` 移除 `/user/profile` 和 `/user/setting` 条目
- 从 `App.jsx` 移除对应路由和 ProfilePage/UserSettingPage import

**导航栏变化**：
- 移除「个人中心」NavLink（`/user/profile`）
- 移除「设置」NavLink（`/user/setting`）
- 用户名/头像变为可点击 Link → `/user/{myId}`

**理由**：
- 减少导航栏入口数量，降低认知负担
- 自己的主页和别人的主页使用同一 URL 模式 `/user/:id`
- 通过 `isOwnProfile` 判断是否显示设置 Tab，代码简洁
- ProfilePage 和 UserSettingPage 的功能被合并后不再需要

## Open Questions

- 无
