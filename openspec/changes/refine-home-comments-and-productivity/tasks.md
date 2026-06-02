## 1. 后端评论线程与点赞

- [x] 1.1 修改 `backend/app/db/database.py`：为 `comments` 表增加 `parent_id` 字段，并在初始化/迁移流程中兼容既有评论为顶层评论。
- [x] 1.2 修改 `backend/app/schemas/comment.py`：为评论创建请求增加可选 `parent_id`，为评论响应增加 `parent_id`、`children`、`like_count`、`is_liked` 字段。
- [x] 1.3 修改 `backend/app/services/comment_service.py`：新增父评论合法性校验，确保回复只能指向同一 `target_type/target_id` 下的评论。
- [x] 1.4 修改 `backend/app/services/comment_service.py`：将平铺评论组装为树形线程结构，并兼容 `parent_id` 为空的历史评论。
- [x] 1.5 修改 `backend/app/services/comment_service.py` 与 `backend/app/services/interaction_service.py`：复用 `like_records` 为 `target_type = 'comment'` 的评论点赞提供统计与当前用户点赞状态。
- [x] 1.6 修改 `backend/app/api/articles.py`：博客评论创建接口接收 `parent_id`，评论列表接口返回线程结构与点赞状态。
- [x] 1.7 修改 `backend/app/api/quick_posts.py`：快写评论创建接口接收 `parent_id`，评论列表接口返回线程结构与点赞状态。
- [x] 1.8 修改 `backend/app/api/articles.py` 与 `backend/app/api/quick_posts.py`：新增或复用评论点赞/取消点赞接口，保证未登录用户不能点赞评论。

## 2. 后端快写详情与博客摘要

- [x] 2.1 修改 `backend/app/services/quick_post_service.py`：新增读取单条快写详情能力，并沿用现有可见性规则。
- [x] 2.2 修改 `backend/app/api/quick_posts.py`：新增 `GET /api/quick-posts/{quick_post_id}` 快写详情接口。
- [x] 2.3 修改 `backend/app/services/article_service.py`：统一生成文章列表展示摘要，优先使用手写 `summary`，为空时从正文开头生成短摘要。
- [x] 2.4 修改 `backend/app/schemas/article.py`：确认文章创建/更新/响应 schema 保留简介字段与长度约束，必要时补充字段描述或校验。
- [x] 2.5 修改 `backend/app/api/articles.py`：确认文章创建、更新和列表接口均返回用于词条展示的标题、标签、分类和简介。

## 3. 前端路由与数据接入

- [x] 3.1 修改 `frontend/src/App.jsx`：注册 `/quick-posts/:id` 快写详情页路由。
- [x] 3.2 修改 `frontend/src/routes/route-config.js`：补充快写详情相关路径配置，确保导航栏不把详情页作为独立标签显示。
- [x] 3.3 新增 `frontend/src/pages/QuickPostDetailPage.jsx`：展示快写正文、作者、发布时间、点赞状态与评论线程。
- [x] 3.4 修改 `frontend/src/pages/HomePage.jsx`：并行加载博客列表与快写列表；已登录时额外加载 Todo 与日历摘要；游客不请求私有 Todo/日历接口。
- [x] 3.5 修改 `frontend/src/pages/HomePage.jsx`：博客词条与快写词条主体区域整体可点击进入详情，内部操作按钮阻止冒泡并保留原操作。
- [x] 3.6 修改 `frontend/src/pages/BlogListPage.jsx`：博客词条展示标题、标签、分类和简介，并让词条主体区域可点击进入详情。
- [x] 3.7 修改 `frontend/src/pages/BlogEditPage.jsx`：补齐简介输入、字数限制和当前字数反馈；简介为空时允许提交，由列表展示自动摘要兜底。

## 4. 前端评论组件复用

- [x] 4.1 新增 `frontend/src/components/CommentThread.jsx`：统一渲染博客与快写的嵌套评论、回复入口、点赞按钮、加载状态、空状态和错误提示。
- [x] 4.2 修改 `frontend/src/pages/BlogDetailPage.jsx`：用 `CommentThread` 替换原有博客评论区，支持顶层评论、回复、评论点赞和刷新。
- [x] 4.3 修改 `frontend/src/pages/QuickPostDetailPage.jsx`：接入 `CommentThread`，支持快写评论、嵌套回复和评论点赞。
- [x] 4.4 修改 `frontend/src/components/CommentThread.jsx`：评论输入框 placeholder 统一为“请说点什么吧~”，提交按钮嵌在文本框右下角。
- [x] 4.5 修改 `frontend/src/components/CommentThread.jsx`：限制嵌套缩进最大视觉宽度，保证深层回复在移动端不横向溢出。

## 5. 首页 Todo 与日历入口

- [x] 5.1 修改 `frontend/src/pages/HomePage.jsx`：新增左侧可折叠 Todo 引导，已登录用户默认展开，展示最近未完成待办摘要并可进入 `/todo`。
- [x] 5.2 修改 `frontend/src/pages/HomePage.jsx`：新增首页右上角日历摘要入口，桌面端固定在视口右上区域，点击进入 `/calendar`。
- [x] 5.3 修改 `frontend/src/pages/HomePage.jsx`：移动端将日历入口降级为普通页面区块，避免遮挡博客、快写和 Todo 内容。
- [x] 5.4 修改 `frontend/src/pages/HomePage.jsx`：Todo 与日历数据加载失败时只影响对应区块，不阻断博客与快写内容展示。

## 6. 样式与响应式

- [x] 6.1 修改 `frontend/src/styles/global.css`：新增首页博客 3/4 + 快写 1/4 组合布局、移动端单列布局与词条整体点击状态。
- [x] 6.2 修改 `frontend/src/styles/global.css`：新增评论输入框、内嵌提交按钮、嵌套评论缩进、评论点赞和回复状态样式。
- [x] 6.3 修改 `frontend/src/styles/global.css`：新增快写详情页样式，并与博客详情页在内容密度和互动区保持一致。
- [x] 6.4 修改 `frontend/src/styles/global.css`：新增 Todo 引导、折叠标识、日历固定入口和移动端降级样式。
- [x] 6.5 修改 `frontend/src/styles/global.css`：检查长标题、长标签、长评论、长 Markdown 内容在桌面和移动端不重叠、不横向溢出。

## 7. 后端验证

- [x] 7.1 运行后端导入验证：`python -m compileall app`。
- [x] 7.2 运行 API 验证：历史评论无 `parent_id` 时仍作为顶层评论返回。
- [x] 7.3 运行 API 验证：博客和快写都能创建顶层评论与合法回复，跨目标 `parent_id` 被拒绝。
- [x] 7.4 运行 API 验证：评论点赞与取消点赞可用，未登录用户不能点赞评论。
- [x] 7.5 运行 API 验证：快写详情接口遵守公开、私有和不存在内容的可见性规则。
- [x] 7.6 运行 API 验证：文章列表在手写简介为空时返回自动摘要。

## 8. 前端验证

- [x] 8.1 运行 `npm run lint`。
- [x] 8.2 运行 `npm run build`。
- [x] 8.3 使用 in-app browser 验证首页桌面端：博客在左侧主区域、快写在右侧区域，Todo 默认展开，日历固定在右上且不遮挡内容。
- [x] 8.4 使用 in-app browser 验证首页移动端：博客、快写、Todo、日历纵向排列，无横向滚动和内容重叠。
- [x] 8.5 使用 in-app browser 验证博客详情：评论输入框样式正确，placeholder 正确，顶层评论、回复、评论点赞可用。
- [x] 8.6 使用 in-app browser 验证快写详情：从首页快写词条进入详情，快写点赞、评论、回复和评论点赞可用。
- [x] 8.7 使用 in-app browser 验证游客状态：首页不展示私有 Todo/日历内容，不请求私有接口，私有路由仍受保护。

## 9. OpenSpec 收尾

- [x] 9.1 运行 `openspec validate refine-home-comments-and-productivity --strict`。
- [x] 9.2 确认 `openspec/changes/refine-home-comments-and-productivity/tasks.md` 中所有实现与验证项完成。
- [x] 9.3 汇总本变更实际修改文件、验证结果和已知风险，准备用户验收。
