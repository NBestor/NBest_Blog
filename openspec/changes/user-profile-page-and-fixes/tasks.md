## Implementation Tasks

### Phase 1: 后端 — 用户公开个人页 API

- [x] Task 1.1: 在 `user_service.py` 中新增 `getUserProfile(targetUserId, currentUserId)` 函数
  - 调用 `getUserById()` 获取用户基本信息
  - SQL 查询 `following_count`（该用户关注的人数）和 `follower_count`（关注该用户的人数）
  - 调用 `listVisibleArticles()` 筛选该用户公开可见的文章
  - 调用 `listVisibleQuickPosts()` 筛选该用户公开可见的快写
  - `currentUserId` 可为 `None`（游客访问）
  - 用户不存在时返回 `None`

- [x] Task 1.2: 在 `users.py` 中新增 `GET /users/{id}/profile` 接口
  - 路径参数 `id: int`
  - 使用 `getOptionalCurrentUser`（不强制登录）
  - 调用 `getUserProfile()` 获取数据
  - 用户不存在返回 HTTP 404
  - 返回 JSON：`{ "user": {...}, "stats": {...}, "articles": [...], "quick_posts": [...] }`

### Phase 2: 前端 — 修复导航栏头像

- [x] Task 2.1: 修改 `AppLayout.jsx` 中头像 `src` 处理逻辑
  - 添加 `avatarUrl` 变量，与 `ProfilePage.jsx` 一致：相对路径拼接 `http://127.0.0.1:8000` 前缀，完整 URL 直接使用
  - 将 `<img>` 的 `src={user.avatar_url}` 改为 `src={avatarUrl}`

### Phase 3: 前端 — 移除设置页快写可见范围 UI

- [x] Task 3.1: 修改 `UserSettingPage.jsx`
  - 移除 `<form>`、`<select>`、`<button>` 和所有状态/处理函数（`visibleType`、`handleSubmit`、`useEffect` 中的 fetchSettings）
  - 替换为静态提示文字：「快写的可见范围可在首页发布快写时直接设置。」
  - 保留 `page-section`、`page-heading` 结构和「个人设置」标题

### Phase 4: 前端 — 新建用户公开个人展示页面

- [x] Task 4.1: 新建 `frontend/src/pages/UserProfilePage.jsx`
  - 使用 `useParams()` 获取用户 ID
  - 调用 `GET /users/{id}/profile` 获取数据
  - 顶部展示用户头像（80px 圆形）、昵称、@用户名、个性签名
  - 统计行：关注 N | 粉丝 N | 博客 N | 快写 N
  - Tab 切换「博客」「快写」两个标签页
  - 博客列表：复用 `.article-card` 样式，每项可点击跳转 `/blog/detail/{id}`
  - 快写列表：复用 `.quick-post-card` 样式，每项可点击跳转 `/quick-posts/{id}`
  - 加载中显示「正在加载用户信息...」
  - 用户不存在显示「用户不存在」
  - 头像 URL 处理与 `ProfilePage.jsx` 一致

- [x] Task 4.2: 在 `route-config.js` 中添加用户主页路由
  - `{ path: '/user/:id', label: '用户主页', title: '用户主页', visibility: 'public', showInNav: false }`

- [x] Task 4.3: 在 `App.jsx` 中添加用户主页路由
  - import `UserProfilePage`
  - 在 `children` 数组中添加 `{ path: 'user/:id', element: <UserProfilePage /> }`

- [x] Task 4.4: 在 `global.css` 末尾添加用户主页相关样式
  - `.user-profile-header` — 用户信息头部布局（头像 + 信息居中排列）
  - `.user-profile-avatar` — 大头像圆形样式（80px）
  - `.user-profile-stats` — 统计行横向排列
  - `.user-profile-tabs` — Tab 切换按钮样式
  - `.user-profile-content` — 内容列表区域

### Phase 5: 前端 — 各处作者名改为可点击链接

- [x] Task 5.1: 修改 `BlogDetailPage.jsx`
  - 将 `.article-meta` 中的 `<span>{article.author_nickname}</span>` 改为 `<Link to={/user/${article.user_id}}>{article.author_nickname}</Link>`
  - 需要确保 `Link` 已导入（当前已导入）

- [x] Task 5.2: 修改 `QuickPostDetailPage.jsx`
  - 将 `.article-meta` 中的 `<span>{post.author_nickname}</span>` 改为 `<Link to={/user/${post.user_id}}>{post.author_nickname}</Link>`
  - 需要确保 `Link` 已导入（当前已导入）

- [x] Task 5.3: 修改 `HomePage.jsx`
  - 博客列表中：将 `<span>{article.author_nickname}</span>` 改为 `<Link to={/user/${article.user_id}}>{article.author_nickname}</Link>`
  - 快写列表中：将 `<span>{post.author_nickname}</span>` 改为 `<Link to={/user/${post.user_id}}>{post.author_nickname}</Link>`
  - 需要确保 `Link` 已导入（当前未导入，需添加）

- [x] Task 5.4: 修改 `BlogListPage.jsx`
  - 将作者名 `<span>{article.author_nickname}</span>` 改为 `<Link to={/user/${article.user_id}}>{article.author_nickname}</Link>`
  - 需要检查 `Link` 是否已导入

### Phase 6: 前端 — 导航栏用户名/头像可点击

- [x] Task 6.1: 修改 `AppLayout.jsx`
  - 将头像和用户名 `<span className="user-chip">` 包裹在 `<Link to={/user/${user.id}}>` 中
  - 退出按钮保持在 Link 之外
  - 游客状态不受影响

### Phase 7: 前端 — 个人中心与用户主页合并

- [x] Task 7.1: 改造 `UserProfilePage.jsx`
  - 使用 `useAuth()` 获取当前登录用户 `user`（已有 import）
  - 判断 `isOwnProfile = isAuthenticated && parseInt(id) === user?.id`
  - 当 `isOwnProfile` 为 true 时，顶部渲染「个人主页」/「个人设置」Tab
  - 「个人设置」Tab 整合 ProfilePage 的功能：
    - 头像预览（80px 圆形）+ 上传/重置按钮
    - 资料修改表单（昵称 input + 签名 textarea + 保存提交）
    - 密码修改表单（旧密码 + 新密码 + 确认新密码 + 修改提交）
  - 各操作调用 `updateUser()` 更新 AuthContext
  - 当 `activeTab === 'settings'` 时隐藏个人主页内容，显示设置区域

- [x] Task 7.2: 从导航栏移除「个人中心」和「设置」
  - 修改 `route-config.js`：移除 `/user/profile` 和 `/user/setting` 路由条目

- [x] Task 7.3: 从 `App.jsx` 移除旧路由
  - 移除 `ProfilePage` import 和 `getRouteElement` 中 `/user/profile` 分支
  - 移除 `UserSettingPage` import 和 `getRouteElement` 中 `/user/setting` 分支

- [x] Task 7.4: 在 `global.css` 添加/调整样式
  - `.user-profile-page-tabs` — 顶层 Tab 切换样式（与现有 `.user-profile-tabs` 区分）
  - `.profile-settings-section` — 设置区域布局样式
  - `.profile-settings-section .avatar-preview` — 头像预览样式
  - `.profile-settings-section .form-panel` — 表单面板样式

### 验证清单

- [ ] 导航栏头像能正常加载显示（有头像用户 + 无头像用户占位符）
- [ ] 导航栏用户名/头像点击跳转到自己主页
- [ ] 自己主页顶部显示「个人主页」和「个人设置」Tab
- [ ] 「个人主页」Tab 显示用户内容（博客/快写列表）
- [ ] 「个人设置」Tab 显示头像上传、资料修改、密码修改
- [ ] 别人主页不显示「个人设置」Tab
- [ ] 「个人中心」和「设置」从导航栏消失
- [ ] `/user/profile` 和 `/user/setting` 路由返回 404
- [ ] `GET /users/{id}/profile` 返回正确的用户信息、统计和内容列表
- [ ] 博客详情页点击作者名跳转到 `/user/{authorId}`
- [ ] 快写详情页点击作者名跳转到 `/user/{authorId}`
- [ ] 首页博客列表点击作者名跳转到 `/user/{authorId}`
- [ ] 首页快写列表点击作者名跳转到 `/user/{authorId}`
- [ ] 博客列表页点击作者名跳转到 `/user/{authorId}`
- [ ] HomePage 发布快写时仍能从 `/users/me/settings` 读取默认 visible_type
