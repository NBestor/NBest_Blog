## Why

当前系统设计仅允许编辑草稿（is_draft=1），文章发布后无法修改。但实际使用中，已发布博客和快写经常需要修正错别字、补充内容或重新生成简介。此外，已有的博客和快写均无编辑入口，用户在详情页和列表页找不到编辑按钮。

## What Changes

### 已发布博客编辑
- 新增后端 API `PUT /api/articles/{article_id}`，允许作者编辑已发布文章（标题、简介、内容、分类、标签、可见范围）
- 前端博客列表页每篇自己的文章卡片上添加「✏️ 编辑」按钮，跳转到编辑器
- 前端编辑器支持 `articleId` URL 参数，加载已发布文章到编辑器（复用现有草稿编辑器）
- 编辑器中保留 AI 生成简介按钮

### 已发布快写编辑
- 新增后端 API `PUT /api/quick-posts/{quick_post_id}`，允许作者编辑已发布快写（内容、可见范围）
- 前端首页快写列表中，每篇自己的快写卡片添加「✏️ 编辑」按钮，改为内联编辑（点击按钮后卡片变成 textarea）

## Capabilities

### New Capabilities

- `published-article-editing`: 已发布文章的后端编辑 API 和前端编辑入口
- `published-quick-post-editing`: 已发布快写的后端编辑 API 和前端内联编辑

### Modified Capabilities

<!-- 不修改已有 spec -->

## Impact

| 层级 | 文件 | 改动 |
|------|------|------|
| 后端 service | `article_service.py` | 新增 `updatePublishedArticle()` 函数 |
| 后端 API | `articles.py` | 新增 `PUT /api/articles/{id}` 路由 |
| 后端 service | `quick_post_service.py` | 新增 `updateQuickPost()` 函数 |
| 后端 API | `quick_posts.py` | 新增 `PUT /api/quick-posts/{id}` 路由 |
| 前端 | `BlogListPage.jsx` | 自己的文章卡片加「✏️ 编辑」按钮 |
| 前端 | `BlogEditPage.jsx` | 支持 `articleId` 参数，加载已发布文章到编辑器 |
| 前端 | `HomePage.jsx` | 自己的快写卡片加「✏️ 编辑」内联编辑模式 |