## ADDED Requirements

### Requirement: Backend User Profile API
后端 SHALL 新增 `GET /users/{id}/profile` 接口，无需鉴权即可访问，返回指定用户的公开信息。

#### Scenario: 返回用户基本信息
- **WHEN** 通过 `GET /users/{id}/profile` 请求存在的用户
- **THEN** 返回 JSON 包含 `user` 对象，字段为：`id`、`username`、`nickname`、`avatar_url`、`signature`、`role`、`create_time`

#### Scenario: 返回用户统计信息
- **WHEN** 通过 `GET /users/{id}/profile` 请求存在的用户
- **THEN** 返回 JSON 包含 `stats` 对象，字段为：`following_count`（关注数）、`follower_count`（粉丝数）、`article_count`（公开可见的博客数）、`quick_post_count`（公开可见的快写数）

#### Scenario: 返回用户公开博客列表
- **WHEN** 通过 `GET /users/{id}/profile` 请求存在的用户
- **THEN** 返回 JSON 包含 `articles` 数组，每项包含 `id`、`title`、`summary`、`category_name`、`visible_type`、`tags`、`create_time`、`update_time`、`author_nickname`、`user_id`、`like_count`、`comment_count`、`is_liked`、`is_collected`
- **AND** 列表仅包含该用户可见的文章（根据请求者身份：游客仅 public，登录用户包含 public + friend，自己包含全部）

#### Scenario: 返回用户公开快写列表
- **WHEN** 通过 `GET /users/{id}/profile` 请求存在的用户
- **THEN** 返回 JSON 包含 `quick_posts` 数组，每项包含 `id`、`content`、`visible_type`、`create_time`、`update_time`、`author_nickname`、`user_id`、`like_count`、`comment_count`、`is_liked`、`can_manage`
- **AND** 列表仅包含该用户可见的快写（根据请求者身份过滤）

#### Scenario: 用户不存在返回 404
- **WHEN** 通过 `GET /users/{id}/profile` 请求不存在的用户 ID
- **THEN** 返回 HTTP 404 状态码

### Requirement: User Public Profile Page
前端 SHALL 新增 `UserProfilePage.jsx` 页面，路由为 `/user/:id`，展示指定用户的公开信息、统计数据和内容列表。

#### Scenario: 页面显示用户基本信息
- **WHEN** 用户或游客访问 `/user/:id`（存在的用户）
- **THEN** 页面顶部显示用户大头像（圆形，约 80px）、昵称（h1）、@用户名、个性签名
- **AND** 头像 `src` 处理方式与 `ProfilePage.jsx` 一致（相对路径加前缀）
- **AND** 如果用户未设置签名，不显示签名行

#### Scenario: 页面显示统计数据
- **WHEN** 用户或游客访问 `/user/:id`（存在的用户）
- **THEN** 页面显示 4 项统计：关注 N、粉丝 N、博客 N、快写 N
- **AND** 统计数据以横向排列展示

#### Scenario: Tab 切换博客/快写
- **WHEN** 页面加载完成后
- **THEN** 默认显示「博客」Tab，展示该用户的博客列表
- **WHEN** 用户点击「快写」Tab
- **THEN** 切换显示该用户的快写列表

#### Scenario: 博客列表项可点击
- **WHEN** 显示博客列表
- **THEN** 每篇文章标题为可点击链接，点击跳转到 `/blog/detail/{article.id}`
- **AND** 显示文章摘要、分类、可见性标签、点赞数、评论数、发布时间

#### Scenario: 快写列表项可点击
- **WHEN** 显示快写列表
- **THEN** 每条快写为可点击卡片，点击跳转到 `/quick-posts/{post.id}`
- **AND** 显示快写内容、可见性标签、点赞数、评论数、发布时间

#### Scenario: 用户不存在时显示错误
- **WHEN** 用户或游客访问 `/user/:id`（不存在的用户）
- **THEN** 页面显示「用户不存在」提示信息

#### Scenario: 加载中状态
- **WHEN** 页面正在请求后端数据
- **THEN** 显示加载中提示「正在加载用户信息...」

### Requirement: Author Name as Clickable Link
各处显示作者名的位置 SHALL 将 `<span>` 纯文本替换为 `<Link>` 可点击链接，点击跳转到该用户的个人展示页面 `/user/{user_id}`。

#### Scenario: 博客详情页作者名可点击
- **WHEN** 用户查看博客详情页 `/blog/detail/:id`
- **THEN** 文章元信息中的作者名（`author_nickname`）为可点击链接
- **WHEN** 点击作者名
- **THEN** 跳转到 `/user/{article.user_id}`

#### Scenario: 快写详情页作者名可点击
- **WHEN** 用户查看快写详情页 `/quick-posts/:id`
- **THEN** 快写元信息中的作者名（`author_nickname`）为可点击链接
- **WHEN** 点击作者名
- **THEN** 跳转到 `/user/{post.user_id}`

#### Scenario: 首页博客列表作者名可点击
- **WHEN** 用户在首页查看博客列表
- **THEN** 每篇文章卡片中的作者名（`author_nickname`）为可点击链接
- **WHEN** 点击作者名
- **THEN** 跳转到 `/user/{article.user_id}`

#### Scenario: 首页快写列表作者名可点击
- **WHEN** 用户在首页查看快写列表
- **THEN** 每条快写卡片中的作者名（`author_nickname`）为可点击链接
- **WHEN** 点击作者名
- **THEN** 跳转到 `/user/{post.user_id}`

#### Scenario: 博客列表页作者名可点击
- **WHEN** 用户在博客列表页 `/blog` 查看文章列表
- **THEN** 每篇文章卡片中的作者名（`author_nickname`）为可点击链接
- **WHEN** 点击作者名
- **THEN** 跳转到 `/user/{article.user_id}`

### Requirement: Route Configuration for User Profile
路由配置 SHALL 新增用户个人主页路由。

#### Scenario: 路由添加
- **WHEN** 路由配置更新后
- **THEN** `route-config.js` 包含 `{ path: '/user/:id', label: '用户主页', title: '用户主页', visibility: 'public', showInNav: false }`
- **AND** `App.jsx` 包含 `{ path: 'user/:id', element: <UserProfilePage /> }` 子路由
- **AND** 该路由不在导航栏中显示（`showInNav: false`）
- **AND** 游客和登录用户均可访问（`visibility: 'public'`）