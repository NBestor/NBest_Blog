## Implementation Tasks

### Phase 1: 后端 — 北京时间转换工具函数

- [x] Task 1.1: 在 `backend/app/core/` 下创建 `timezone.py`，实现 `toBeijingTime(utcStr)` 函数
  - 输入 UTC `YYYY-MM-DD HH:MM:SS` → 输出北京时间 `YYYY-MM-DD HH:MM:SS`
  - 空值安全处理

### Phase 2: 后端 — 北京时间应用到各 service

- [x] Task 2.1: 在 `article_service.py` 的 `formatArticle()` 和 `formatReadableArticle()` 中，对 `create_time` / `update_time` 调用 `toBeijingTime()`
- [x] Task 2.2: 在 `quick_post_service.py` 的 `formatQuickPost()` 中，对 `create_time` / `update_time` 调用 `toBeijingTime()`
- [x] Task 2.3: 在 `comment_service.py` 的 comment 格式化函数中，对 `create_time` 调用 `toBeijingTime()`

### Phase 3: 后端 — 博客列表排序改为按发布时间

- [x] Task 3.1: 修改 `article_service.py` 中 `listVisibleArticles()` 的 SQL：`ORDER BY articles.update_time DESC` → `ORDER BY articles.create_time DESC, articles.id DESC`

### Phase 4: 前端 — 上传图片按钮显式文字

- [x] Task 4.1: 修改 `BlogEditPage.jsx` 中 `<label className="file-button">`：保留文字"上传图片" + `title` tooltip

### Phase 5: 前端 — 编辑器状态重置

- [x] Task 5.1: 在 `BlogEditPage.jsx` 的 `useEffect` 中添加重置逻辑：当 `draftId` 和 `articleId` 均为 `null` 时，重置 `formData`、`currentDraftId`、`searchParams`、`isLoading`

### Phase 6: 前端 — Markdown 源码切换

- [x] Task 6.1: 在 `BlogDetailPage.jsx` 中添加 `showSource` 状态和切换按钮
- [x] Task 6.2: 在 `global.css` 末尾添加 `.markdown-source` 样式（等宽字体、浅灰背景、保留换行）

### Phase 7: 前端 — 文章详情页显示发布时间

- [x] Task 7.1: 在 `BlogDetailPage.jsx` 的 `.article-body` 下方添加 `.article-time-info` 时间行
- [x] Task 7.2: 在 `global.css` 末尾添加 `.article-time-info` 样式

### Phase 8: 前端 — 导航栏头像

- [x] Task 8.1: 修改 `AppLayout.jsx` 的 `navbar-right` 用户区域：在 `<span className="user-chip">` 前添加头像
  - `user.avatar_url` 存在 → `<img className="navbar-avatar">`
  - 无头像 → `<span className="navbar-avatar-placeholder">` 首字母占位符
- [x] Task 8.2: 在 `global.css` 末尾添加 `.navbar-avatar` / `.navbar-avatar-placeholder` 样式

### 验证清单

- [ ] 后端 `toBeijingTime("2026-06-02 06:00:00")` 返回 `"2026-06-02 14:00:00"`
- [ ] 博客列表 API 返回的 `create_time` 为北京时间
- [ ] 编辑已发布文章后，文章在列表中的排序位置不变
- [ ] 「上传图片」按钮上有可见文字"上传图片"，悬停有 tooltip
- [ ] 从编辑页点击导航栏「写文章」，编辑器重置为空白状态
- [ ] 文章详情页可切换 Markdown 源码视图
- [ ] 文章详情页底部显示发布时间，编辑过的还显示编辑时间
- [ ] 导航栏右上角用户名左侧显示头像或首字母占位符