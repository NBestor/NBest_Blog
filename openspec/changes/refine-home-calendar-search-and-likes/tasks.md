## 1. 后端搜索能力

- [x] 1.1 新增 `backend/app/schemas/search.py`：定义搜索响应 schema，包含博客结果列表和快记结果列表。
- [x] 1.2 修改 `backend/app/services/article_service.py`：新增 `searchVisibleArticles(query, currentUserId)`，复用现有博客可见性规则，并匹配标题、简介、分类名和标签名。
- [x] 1.3 修改 `backend/app/services/quick_note_service.py`：新增 `searchQuickNotes(userId, query)`，仅搜索当前用户自己的快记正文。
- [x] 1.4 新增 `backend/app/api/search.py`：实现 `GET /api/search?q=...`，游客只返回博客结果，登录用户额外返回自己的快记结果。
- [x] 1.5 修改 `backend/app/api/router.py`：注册搜索 router。
- [x] 1.6 运行 API 验证：博客标题、标签、分类和简介命中时出现在博客结果区。
- [x] 1.7 运行 API 验证：游客搜索不返回快记结果，登录用户只返回自己的快记结果。
- [x] 1.8 运行 API 验证：搜索接口不返回待办和日历数据。

## 2. 前端搜索入口与搜索页

- [x] 2.1 修改 `frontend/src/layouts/AppLayout.jsx`：新增顶部放大镜搜索表单，桌面端 hover/focus 展开，移动端点击/聚焦展开。
- [x] 2.2 修改 `frontend/src/App.jsx`：注册 `/search` 搜索结果页路由。
- [x] 2.3 新增 `frontend/src/pages/SearchPage.jsx`：读取 `q` 参数并调用 `/search` 接口。
- [x] 2.4 修改 `frontend/src/pages/SearchPage.jsx`：分区展示博客结果和快记结果，不混排。
- [x] 2.5 修改 `frontend/src/pages/SearchPage.jsx`：博客结果整卡点击进入博客详情。
- [x] 2.6 修改 `frontend/src/pages/SearchPage.jsx`：快记结果点击进入 `/quick/note`，尽可能携带 query/hash 定位对应快记。
- [x] 2.7 修改 `frontend/src/styles/global.css`：新增导航搜索框、搜索页分区、搜索结果卡片和移动端展开样式。

## 3. 顶部导航精简

- [x] 3.1 修改 `frontend/src/routes/route-config.js`：将博客、待办、日历设置为不在顶部导航显示，但保留路由配置。
- [x] 3.2 修改 `frontend/src/layouts/AppLayout.jsx`：确认导航过滤继续尊重 `showInNav: false`，且搜索入口独立于路由标签显示。
- [x] 3.3 验证游客导航：顶部不显示博客、待办、日历；登录/注册入口仍可见。
- [x] 3.4 验证登录用户导航：顶部不显示博客、待办、日历；用户状态、照片墙、管理入口按权限显示。
- [x] 3.5 验证直接访问：`/todo`、`/calendar` 仍要求登录，`/blog` 仍可直接访问。

## 4. 首页快写与小月历布局

- [x] 4.1 修改 `frontend/src/pages/HomePage.jsx`：移除当前日历 fixed/floating 入口，改为首页上方右侧小月历组件。
- [x] 4.2 修改 `frontend/src/pages/HomePage.jsx`：新增当前月日期格计算，显示当前月小月历。
- [x] 4.3 修改 `frontend/src/pages/HomePage.jsx`：根据当前月日历事件圈选有事件的日期。
- [x] 4.4 修改 `frontend/src/pages/HomePage.jsx`：新增日历箭头状态，默认向上且不显示事件列表。
- [x] 4.5 修改 `frontend/src/pages/HomePage.jsx`：点击箭头后向下并以悬浮层展示本月事件，不挤压其他内容。
- [x] 4.6 修改 `frontend/src/pages/HomePage.jsx`：本月事件中今天及未来事件按日期升序显示，已过去事件置灰并放底部。
- [x] 4.7 修改 `frontend/src/pages/HomePage.jsx`：重排首页上方为快写主区 + 小月历侧区，快写尽量占满左侧可用宽度。
- [x] 4.8 修改 `frontend/src/pages/HomePage.jsx`：保留首页进入博客、待办、日历的入口，待办和日历仍只对登录用户显示私有内容。
- [x] 4.9 修改 `frontend/src/styles/global.css`：新增 `home-top-grid`、小月历、事件日期圈选、箭头、事件悬浮层和移动端单列样式。

## 5. 爱心点赞视觉

- [x] 5.1 新增 `frontend/src/components/LikeButton.jsx`：封装空心爱心、红色实心爱心、点赞数量、禁用态和点击回调。
- [x] 5.2 修改 `frontend/src/pages/BlogDetailPage.jsx`：文章点赞按钮替换为 `LikeButton`。
- [x] 5.3 修改 `frontend/src/pages/QuickPostDetailPage.jsx`：快写点赞按钮替换为 `LikeButton`。
- [x] 5.4 修改 `frontend/src/pages/HomePage.jsx`：首页快写点赞按钮替换为 `LikeButton`，并保持内部按钮不触发卡片跳转。
- [x] 5.5 修改 `frontend/src/components/CommentThread.jsx`：评论点赞按钮替换为 `LikeButton`。
- [x] 5.6 修改 `frontend/src/styles/global.css`：新增爱心点赞按钮样式，未点赞为空心，已点赞为红色实心。
- [x] 5.7 验证文章、快写和评论点赞状态切换后，爱心视觉状态和数量更新正确。

## 6. 前端页面与权限验证

- [x] 6.1 运行 `npm run lint`。
- [x] 6.2 运行 `npm run build`。
- [x] 6.3 使用 in-app browser 验证首页桌面端：快写与小月历并列，小月历在页面内右上角且滚动后不跟随视口。
- [x] 6.4 使用 in-app browser 验证小月历：显示当前月，有事件日期被圈出，箭头展开事件悬浮层且不挤压布局。
- [x] 6.5 使用 in-app browser 验证事件排序：未到达事件按日期排序，已过去事件置灰置底。
- [x] 6.6 使用 in-app browser 验证移动端：快写、小月历、博客内容纵向排列，无横向溢出。
- [x] 6.7 使用 in-app browser 验证搜索：顶部搜索可展开，提交后进入 `/search?q=...`，博客和快记结果分区显示。
- [x] 6.8 使用 in-app browser 验证游客搜索：只显示博客结果，不显示快记、待办、日历结果。
- [x] 6.9 使用 in-app browser 验证导航：博客、待办、日历不再作为顶部标签显示，但对应页面仍可通过首页或直接 URL 访问。

## 7. 后端与 OpenSpec 收尾

- [x] 7.1 运行后端导入验证：`python -m compileall app`。
- [x] 7.2 运行 `openspec validate refine-home-calendar-search-and-likes --strict`。
- [x] 7.3 确认 `openspec/changes/refine-home-calendar-search-and-likes/tasks.md` 所有实现与验证项完成。
- [x] 7.4 汇总本变更实际修改文件、验证结果和已知风险，准备用户验收。
