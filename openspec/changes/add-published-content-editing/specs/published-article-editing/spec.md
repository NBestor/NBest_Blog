## ADDED Requirements

### Requirement: Update Published Article API
系统 SHALL 提供 `PUT /api/articles/{article_id}` 接口，允许已发布文章的作者修改标题、简介、内容、分类、标签和可见范围。接口 MUST 要求登录认证，且仅文章作者本人可编辑。编辑后 SHALL 更新 `update_time` 字段。

#### Scenario: 作者成功编辑已发布文章
- **WHEN** 已发布文章的作者发送包含有效字段的 PUT 请求
- **THEN** 系统返回 `200` 及更新后的文章详情，`update_time` 刷新

#### Scenario: 非作者尝试编辑
- **WHEN** 非文章作者的登录用户发送 PUT 请求
- **THEN** 系统返回 `403` 权限不足错误

#### Scenario: 未登录用户请求
- **WHEN** 未登录用户请求该接口
- **THEN** 系统返回 `401` 未授权错误

#### Scenario: 文章不存在
- **WHEN** 请求的 `article_id` 对应文章不存在或为草稿
- **THEN** 系统返回 `404` 文章不存在错误

#### Scenario: 字段校验失败
- **WHEN** 请求中 title 为空或 content 为空
- **THEN** 系统返回 `422` 校验错误

### Requirement: Edit Button on Blog List Page
前端博客列表页（`BlogListPage.jsx`）SHALL 在用户自己的已发布文章卡片上显示「✏️ 编辑」按钮。点击按钮 MUST 跳转到 `/blog/edit?articleId={id}` 编辑器页面。非作者的文章卡片上 SHALL NOT 显示编辑按钮。

#### Scenario: 自己的文章有编辑按钮
- **WHEN** 已登录用户浏览博客列表，且列表中存在自己发布的文章
- **THEN** 该文章卡片上显示「✏️ 编辑」按钮

#### Scenario: 他人的文章无编辑按钮
- **WHEN** 已登录用户浏览博客列表，看到其他用户发布的文章
- **THEN** 文章卡片上不显示编辑按钮

#### Scenario: 游客浏览无编辑按钮
- **WHEN** 游客浏览博客列表
- **THEN** 任何文章卡片上均不显示编辑按钮

#### Scenario: 点击编辑按钮跳转
- **WHEN** 用户点击自己文章卡片上的「✏️ 编辑」按钮
- **THEN** 浏览器跳转到 `/blog/edit?articleId={id}` 编辑器页面

### Requirement: Editor Supports Published Article via articleId Parameter
文章编辑器（`BlogEditPage.jsx`）SHALL 支持 `articleId` URL 参数。当参数存在时，编辑器 MUST 从 `GET /api/articles/{id}` 加载已发布文章数据填入表单，保存按钮 SHALL 调用 `PUT /api/articles/{id}` 而非草稿 API，并隐藏「发布」按钮。编辑期间 AI 生成简介按钮 MUST 保持可用。

#### Scenario: articleId 参数加载已发布文章
- **WHEN** 用户访问 `/blog/edit?articleId=5` 且该文章属于当前用户
- **THEN** 编辑器加载文章标题、简介、内容、分类、标签、可见范围

#### Scenario: 保存已发布文章
- **WHEN** 用户在编辑器中修改已发布文章并点击「保存」
- **THEN** 系统调用 `PUT /api/articles/{id}` 更新文章，页面提示「保存成功」

#### Scenario: 编辑已发布文章时隐藏发布按钮
- **WHEN** 编辑器以 `articleId` 模式加载
- **THEN** 页面不显示「发布」按钮，显示「保存修改」按钮

#### Scenario: AI 生成按钮保持可用
- **WHEN** 编辑器以 `articleId` 模式加载
- **THEN** 「🤖 AI 生成」按钮正常显示且可用

#### Scenario: articleId 参数优先级高于 draftId
- **WHEN** 用户同时传入 `?articleId=5&draftId=3`
- **THEN** 编辑器以 `articleId` 模式加载（优先）