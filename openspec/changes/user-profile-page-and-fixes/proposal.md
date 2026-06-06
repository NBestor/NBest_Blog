## Why

当前存在3个问题，以及2项交互优化：

### 原有问题

1. **导航栏头像无法显示**：`AppLayout.jsx` 中头像的 `src` 直接使用后端返回的 `user.avatar_url`（相对路径如 `/static/uploads/avatars/1/avatar.jpg`），缺少 `http://127.0.0.1:8000` 前缀，导致 img 标签无法加载图片。`ProfilePage.jsx` 已正确处理此问题，但导航栏没有。

2. **设置页快写可见范围冗余**：`UserSettingPage.jsx` 唯一功能是设置快写默认可见范围。但 `HomePage.jsx` 发布快写时已有下拉选择框控制可见范围，功能完全重叠。需要移除设置页的快写默认权限 UI。

3. **缺少用户公开个人展示页面**：博客详情页、快写详情页、博客列表页、首页快写列表中的作者名都是纯文本 `<span>`，不可点击。需要新增用户公开个人页面（`/user/:id`），展示该用户的关注/粉丝数、博客列表、快写列表、个人简介等信息，并将各处作者名改为可点击链接。

### 新增交互优化

4. **导航栏用户名/头像可点击**：右上角自己的用户名和头像应可点击，跳转到自己的用户主页 `/user/{myId}`，与各处作者名 Link 行为一致。

5. **个人中心与用户主页合并**：当前存在 `/user/profile`（个人中心，修改昵称/签名/头像/密码）和 `/user/:id`（用户主页，展示内容）两个独立页面。在自己访问自己主页时，应将两者合并为一个页面，顶部用 Tab 切换「个人主页」和「个人设置」。访问别人主页时仅显示「个人主页」内容。合并后移除导航栏中「个人中心」和「设置」两个入口。

## What Changes

### 修复导航栏头像显示
- `AppLayout.jsx` 中头像 `img` 的 `src` 添加后端基础路径前缀（与 `ProfilePage.jsx` 一致的处理方式）

### 移除设置页快写可见范围
- `UserSettingPage.jsx` 移除快写默认权限表单 UI，改为提示「快写可见范围可在首页发布时直接设置」
- 后端 `/users/me/settings` 接口保留不动（HomePage 初始化时还需读取默认值）

### 新增用户公开个人页面 + 作者名可点击
- 后端新增 `GET /users/{id}/profile` 接口，返回用户信息 + 统计（关注数、粉丝数、博客数、快写数）+ 该用户的公开博客列表 + 该用户的公开快写列表
- 前端新增 `UserProfilePage.jsx`，展示头像、昵称、签名、关注/粉丝/博客/快写统计，以及博客和快写列表
- 前端路由添加 `/user/:id` → `UserProfilePage`
- `BlogDetailPage.jsx`、`QuickPostDetailPage.jsx`、`HomePage.jsx`、`BlogListPage.jsx` 中将作者名从 `<span>` 改为 `<Link to={/user/${authorId}}>`

### 导航栏用户名/头像可点击
- `AppLayout.jsx` 中用户名和头像包裹 `<Link>`，点击跳转 `/user/{myId}`

### 个人中心与用户主页合并
- `UserProfilePage.jsx` 改造：访问自己主页时顶部显示「个人主页」和「个人设置」两个 Tab
  - 「个人主页」Tab = 当前的用户展示内容（头像、统计、博客/快写列表）
  - 「个人设置」Tab = 整合 `ProfilePage.jsx` 的功能（修改昵称/签名、上传/删除头像、修改密码）
- 访问别人主页时仅显示「个人主页」
- 从 `AppLayout.jsx` 导航栏移除「个人中心」（`/user/profile`）和「设置」（`/user/setting`）入口
- 从 `route-config.js` 移除 `/user/profile` 和 `/user/setting` 路由条目
- 从 `App.jsx` 移除对应路由和 import
- `ProfilePage.jsx` 和 `UserSettingPage.jsx` 功能合并后原文件可保留或清理

## Capabilities

### New Capabilities

- `navbar-avatar-fix`: 修复导航栏头像无法显示的问题
- `remove-settings-quick-post`: 从设置页移除快写默认可见范围 UI
- `user-public-profile`: 新增用户公开个人展示页面 + 各处作者名改为可点击链接
- `navbar-user-link`: 导航栏用户名/头像可点击跳转自己主页
- `profile-merge`: 个人中心与用户主页合并，Tab 切换「个人主页」/「个人设置」

## Impact

| 层级 | 文件 | 改动 |
|------|------|------|
| 后端 API | `users.py` | 新增 `GET /users/{id}/profile` 接口 |
| 后端 service | `user_service.py` | 新增 `getUserProfile()` 函数 |
| 后端 service | `article_service.py` | `formatArticle()` / `formatReadableArticle()` 确保返回 `user_id` |
| 后端 service | `quick_post_service.py` | `formatQuickPost()` 确保返回 `user_id` |
| 前端 | `AppLayout.jsx` | 修复头像 src 路径；用户名/头像变为可点击 Link |
| 前端 | `UserProfilePage.jsx` | **改造**：合并个人设置功能，Tab 切换 |
| 前端 | `App.jsx` | 移除 `/user/profile` 和 `/user/setting` 路由；添加 `/user/:id` |
| 前端 | `route-config.js` | 移除 `/user/profile` 和 `/user/setting` 条目 |
| 前端 | `BlogDetailPage.jsx` | 作者名改为 Link |
| 前端 | `QuickPostDetailPage.jsx` | 作者名改为 Link |
| 前端 | `HomePage.jsx` | 作者名改为 Link |
| 前端 | `BlogListPage.jsx` | 作者名改为 Link |
| 前端 | `global.css` | 新增用户主页相关样式 + 个人设置 Tab 样式 |
| 前端 | `ProfilePage.jsx` | 功能合并后不再需要（可删除） |
| 前端 | `UserSettingPage.jsx` | 功能合并后不再需要（可删除） |
