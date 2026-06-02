## ADDED Requirements

### Requirement: Consistent visual system
系统 SHALL 在全站使用一致的布局节奏、按钮层级、表单输入、面板、卡片、弹窗和提示样式。

#### Scenario: Common controls share visual rules
- **WHEN** 用户访问首页、文章编辑、草稿、照片墙、Todo、日历、快记、个人中心和设置页面
- **THEN** 页面中的主要按钮、次要按钮、输入框、选择框、文本区域、面板和卡片 MUST 使用一致的高度、边框、圆角、间距和焦点态

#### Scenario: Dialogs share interaction shape
- **WHEN** 页面显示提醒中心、照片预览或其他全局弹窗
- **THEN** 弹窗 MUST 使用一致的遮罩、层级、内容边距、关闭入口和移动端宽度约束

#### Scenario: Navigation remains state driven
- **WHEN** 游客或登录用户访问网站
- **THEN** 导航 MUST 继续只显示当前状态可使用的入口，并保持当前简约博客风格

### Requirement: Responsive layout quality
系统 SHALL 保证关键页面在桌面和移动端视口下可读、可操作且不发生明显重叠或溢出。

#### Scenario: Desktop layout remains stable
- **WHEN** 用户在桌面宽度访问主要页面
- **THEN** 页面内容 MUST 保持合理宽度、面板间距和操作区排列，不出现无意义横向滚动

#### Scenario: Mobile layout stacks safely
- **WHEN** 用户在移动端宽度访问主要页面
- **THEN** 多列布局 MUST 收敛为单列或可用布局，按钮文字、卡片内容和表单字段 MUST NOT 相互遮挡

#### Scenario: Dynamic content does not break containers
- **WHEN** 页面展示较长标题、链接、错误提示或用户输入内容
- **THEN** 文本 MUST 换行、截断或使用安全换行策略，不能撑破父容器

### Requirement: Unified page states
系统 SHALL 为常见页面状态提供一致、可理解的呈现方式。

#### Scenario: Loading state
- **WHEN** 页面正在加载远程数据
- **THEN** 系统 MUST 显示清晰的加载状态，并且加载状态不能遮挡导航或破坏页面布局

#### Scenario: Empty state
- **WHEN** 当前页面没有可展示数据
- **THEN** 系统 MUST 显示空状态提示，而不是展示空白页面或残留操作结果

#### Scenario: Success and error feedback
- **WHEN** 用户完成保存、上传、删除、复制或提交操作
- **THEN** 系统 MUST 给出成功或失败反馈，并且错误提示 MUST 使用一致的视觉语义

#### Scenario: Permission-hidden state
- **WHEN** 当前用户无权使用某项操作
- **THEN** 系统 MUST 隐藏该操作入口或显示明确不可用状态，不能暴露会导致越权操作的入口

### Requirement: Core flow stability
系统 SHALL 在质量收敛后保持已实现核心流程可用。

#### Scenario: Authentication flow
- **WHEN** 用户注册、登录、刷新页面和退出登录
- **THEN** 系统 MUST 保持登录态逻辑正确，游客仍不能访问受保护页面

#### Scenario: Content flows
- **WHEN** 登录用户使用文章草稿、发布、快写、快记、Todo、日历和照片墙核心操作
- **THEN** 对应流程 MUST 可完成，且不会因 UI 调整出现阻断

#### Scenario: Public browsing flow
- **WHEN** 游客访问首页、公开博客、文章详情和照片墙
- **THEN** 系统 MUST 展示公开内容，并且 MUST NOT 展示登录后专属操作

### Requirement: Permission regression coverage
系统 SHALL 对核心权限边界进行回归验证。

#### Scenario: Private resources stay private
- **WHEN** 用户 A 创建私密快记、Todo、日历事件、私密照片或仅自己可见内容
- **THEN** 用户 B 和游客 MUST NOT 看到或操作这些资源

#### Scenario: Owner-only operations remain protected
- **WHEN** 非拥有者尝试修改或删除他人的私有资源
- **THEN** 系统 MUST 拒绝该操作，并保持资源不变

#### Scenario: Guest operations remain limited
- **WHEN** 游客访问需要登录的操作入口或 API
- **THEN** 系统 MUST 拒绝写入类操作，并且前端 MUST NOT 显示登录后专属操作入口

#### Scenario: Admin boundary remains explicit
- **WHEN** 测试管理员执行设计中允许的管理操作
- **THEN** 系统 MUST 允许该操作；普通用户执行同类越权操作时 MUST 被拒绝
