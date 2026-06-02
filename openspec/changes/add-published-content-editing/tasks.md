## 1. 已发布文章后端

- [x] 1.1 在 `backend/app/services/article_service.py` 中新增 `updatePublishedArticle(userId, articleId, ...)` 函数，SQL 去掉 `is_draft=1` 限制，返回更新后的文章
- [x] 1.2 在 `backend/app/api/articles.py` 中新增 `PUT /api/articles/{article_id}` 路由，鉴权仅作者本人，调用 `updatePublishedArticle`

## 2. 已发布快写后端

- [x] 2.1 在 `backend/app/services/quick_post_service.py` 中新增 `updateQuickPost(userId, postId, content, visibleType)` 函数
- [x] 2.2 在 `backend/app/api/quick_posts.py` 中新增 `PUT /api/quick-posts/{quick_post_id}` 路由，鉴权仅作者本人

## 3. 博客列表编辑入口

- [x] 3.1 在 `BlogListPage.jsx` 中获取当前用户 ID，自己的文章卡片上添加「✏️ 编辑」按钮，点击跳转 `/blog/edit?articleId={id}`

## 4. 编辑器支持 articleId 参数

- [x] 4.1 在 `BlogEditPage.jsx` 中新增 `articleId` URL 参数支持，从 `GET /api/articles/{id}` 加载已发布文章
- [x] 4.2 根据模式切换保存逻辑（articleId 时调 `PUT /api/articles/{id}`），切换按钮文案（显示「保存修改」、隐藏「发布」）
- [x] 4.3 确保 `articleId` 优先级高于 `draftId`，AI 生成简介按钮保持可用

## 5. 快写内联编辑

- [x] 5.1 在 `HomePage.jsx` 的快写卡片中，自己的快写加「✏️ 编辑」按钮，实现内联编辑切换
- [x] 5.2 实现内联编辑的保存和取消交互，空内容校验
