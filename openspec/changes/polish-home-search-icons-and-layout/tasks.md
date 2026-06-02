## 1. 后端搜索目标修正

- [x] 1.1 修改 `backend/app/schemas/search.py`：将搜索响应中的 `quick_notes` 字段改为 `quick_posts`，类型改用 `QuickPostResponse`
- [x] 1.2 修改 `backend/app/services/quick_post_service.py`：新增 `searchVisibleQuickPosts(query, currentUserId)`，复用现有快写可见性列表后按正文内容过滤
- [x] 1.3 修改 `backend/app/api/search.py`：搜索接口改为返回博客结果和快写结果，不再调用快记搜索
- [x] 1.4 验证搜索 API：确认响应包含 `articles` 与 `quick_posts`，且不包含快记、待办、日历结果

## 2. 矢量图标按钮

- [x] 2.1 新增 `frontend/src/components/icons.jsx`：提供本地内联 SVG 图标组件，包括 `SearchIcon`、`HeartIcon`、`ChevronIcon`
- [x] 2.2 修改 `frontend/src/layouts/AppLayout.jsx`：顶部搜索入口改用 `SearchIcon`，保留可访问标签和展开搜索输入行为
- [x] 2.3 修改 `frontend/src/components/LikeButton.jsx`：点赞按钮改用 `HeartIcon`，未点赞为空心，已点赞为红色实心
- [x] 2.4 修改 `frontend/src/pages/HomePage.jsx`：日历事件展开按钮改用 `ChevronIcon`
- [x] 2.5 修改 `frontend/src/styles/global.css`：补充图标按钮、爱心状态、箭头旋转或方向状态的样式

## 3. 首页布局重排

- [x] 3.1 修改 `frontend/src/pages/HomePage.jsx`：重排首页结构为左侧博客主区、右侧日历加快写区，快写发布框归入右侧快写区
- [x] 3.2 修改 `frontend/src/pages/HomePage.jsx`：保留待办为页面最左侧的小引导或抽屉，不让它变成覆盖主功能的大块内容
- [x] 3.3 修改 `frontend/src/pages/HomePage.jsx`：日历位于右侧区域顶部，快写发布框和快写列表位于日历下方
- [x] 3.4 修改 `frontend/src/styles/global.css`：更新首页网格、右侧栏、博客区、快写区、待办引导的布局样式，减少左右空白
- [x] 3.5 修改 `frontend/src/styles/global.css`：窄屏时只压缩边距、栏宽和日历显示密度，不把博客与快写改成上下堆叠
- [x] 3.6 修改 `frontend/src/styles/global.css`：当右侧区域过窄时，将日历压缩为“日历”入口，不强行显示月历网格

## 4. 搜索结果页调整

- [x] 4.1 修改 `frontend/src/pages/SearchPage.jsx`：读取 `response.data.quick_posts`，显示“快写结果”，移除快记搜索结果逻辑
- [x] 4.2 修改 `frontend/src/pages/SearchPage.jsx`：快写搜索结果点击后进入对应快写详情页
- [x] 4.3 修改 `frontend/src/pages/SearchPage.jsx`：搜索结果布局改为左侧博客、右侧快写，不使用上下堆叠
- [x] 4.4 修改 `frontend/src/styles/global.css`：补充搜索结果双栏样式，窄屏保留左右关系并允许必要的横向压缩或滚动

## 5. 验证与收尾

- [x] 5.1 运行后端可用性检查：至少验证搜索接口能返回博客与快写结果结构
- [x] 5.2 运行前端构建或 lint：确认修改后的 React 代码可以通过项目现有检查
- [x] 5.3 使用浏览器检查首页：确认博客在左、日历和快写在右、待办在最左，窄屏不改变相对位置
- [x] 5.4 使用浏览器检查搜索页：确认博客结果左侧、快写结果右侧，并且能搜到快写正文内容
- [x] 5.5 运行 `openspec validate polish-home-search-icons-and-layout --strict`，确认规格变更仍然有效
