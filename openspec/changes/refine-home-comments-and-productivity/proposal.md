## Why

当前首页、评论和个人效率入口仍是多个功能分散展示：博客与快写分离，评论只能平铺，Todo/日历入口不够贴近首页使用场景。需要把首页调整成真正的个人信息工作台，同时提升博客和快写的评论互动体验。

## What Changes

- 调整评论输入 UI：
  - 博客评论和快写评论的输入框使用更容易和背景区分的颜色。
  - 评论输入框默认文本统一为 `请说点什么吧~`。
  - 评论按钮嵌入文本框右下角，不再作为独立外部按钮。
- 新增嵌套评论能力：
  - 博客评论和快写评论都支持回复评论。
  - 回复在视觉上按层级向右缩进，呈递进关系。
  - 每条评论都可以点赞。
  - 评论区需要同时支持新增顶层评论和回复某条评论。
- 调整首页信息结构：
  - 首页同时显示博客和快写。
  - 首页主内容区域左侧约 3/4 展示博客列表。
  - 首页右侧约 1/4 展示快写列表。
  - 博客和快写词条整体可点击进入详情页，不要求只能点击标题。
- 新增快写详情页：
  - 快写词条可进入独立详情页。
  - 快写详情页展示快写正文、评论、嵌套回复和点赞。
- 调整博客词条信息：
  - 编写博客时保留简介/摘要字段。
  - 简介有明确字数限制。
  - 如果没有手写简介，系统使用正文开头若干行生成短简介用于词条展示。
  - 首页和博客列表中的博客词条显示标题、标签、分类和简介。
- 调整首页 Todo 和日历入口：
  - 日历作为首页最右上角固定框，不随页面滚动。
  - 点击首页日历固定框后进入或放大到日历详细页。
  - Todo 作为首页最左侧可收起/展开的引导标识。
  - Todo 引导默认打开，再次点击收回。
  - Todo 引导内展示当前用户的待办摘要内容。
- 不引入新的 UI 框架。
- 不改变现有文章、快写、Todo、日历的核心数据归属和权限规则。

## Capabilities

### New Capabilities

- `threaded-comments`: 博客和快写的嵌套评论、回复、评论点赞和评论输入 UI。
- `home-dashboard-layout`: 首页博客/快写合并布局、固定日历入口和可收起 Todo 引导。
- `quick-post-detail`: 快写详情页、快写词条整体点击进入详情。

### Modified Capabilities

- `user-identity-navigation`: 首页仍需按用户状态显示个人入口，新增首页 Todo/日历辅助入口不得向游客暴露私有数据。

## Impact

- 后端：
  - 可能修改 `backend/app/db/database.py`，为评论增加 `parent_id`，并为评论点赞复用或扩展点赞记录。
  - 可能修改 `backend/app/services/comment_service.py`、`interaction_service.py`、`quick_post_service.py`、`article_service.py`。
  - 可能修改 `backend/app/api/articles.py` 和 `backend/app/api/quick_posts.py`，支持评论回复、评论点赞和快写详情接口。
  - 可能修改评论相关 schema。
- 前端：
  - 可能修改 `frontend/src/pages/HomePage.jsx`，实现首页博客/快写/Todo/日历组合布局。
  - 可能修改 `frontend/src/pages/BlogListPage.jsx`、`BlogDetailPage.jsx`、`BlogEditPage.jsx`。
  - 可能新增 `frontend/src/pages/QuickPostDetailPage.jsx`。
  - 可能新增或抽取评论组件，例如 `frontend/src/components/CommentThread.jsx`。
  - 可能修改 `frontend/src/App.jsx` 和 `frontend/src/routes/route-config.js`，增加快写详情路由。
  - 修改 `frontend/src/styles/global.css`，补充首页布局、评论输入、嵌套评论、固定日历框和 Todo 引导样式。
- OpenSpec：
  - 新增 `threaded-comments`、`home-dashboard-layout`、`quick-post-detail` 规格。
  - 修改 `user-identity-navigation` 规格，补充首页辅助入口的数据可见性要求。
