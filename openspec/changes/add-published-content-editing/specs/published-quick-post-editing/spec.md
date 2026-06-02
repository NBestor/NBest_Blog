## ADDED Requirements

### Requirement: Update Published Quick Post API
系统 SHALL 提供 `PUT /api/quick-posts/{quick_post_id}` 接口，允许已发布快写的作者修改内容和可见范围。接口 MUST 要求登录认证，且仅快写作者本人可编辑。

#### Scenario: 作者成功编辑快写
- **WHEN** 快写作者发送包含有效 content 和 visible_type 的 PUT 请求
- **THEN** 系统返回 `200` 及更新后的快写数据

#### Scenario: 非作者尝试编辑
- **WHEN** 非快写作者的登录用户发送 PUT 请求
- **THEN** 系统返回 `403` 权限不足错误

#### Scenario: 未登录用户请求
- **WHEN** 未登录用户请求该接口
- **THEN** 系统返回 `401` 未授权错误

#### Scenario: 快写不存在
- **WHEN** 请求的 `quick_post_id` 不存在
- **THEN** 系统返回 `404` 快写不存在错误

### Requirement: Inline Edit on Quick Post Cards
前端首页快写列表中，SHALL 在用户自己的快写卡片上显示「✏️ 编辑」按钮。点击按钮 MUST 将卡片切换为内联编辑模式：内容变为 textarea（预填原内容），可见范围变为下拉选择框，底部显示「保存」和「取消」按钮。非作者的快写卡片上 SHALL NOT 显示编辑按钮。

#### Scenario: 自己的快写有编辑按钮
- **WHEN** 已登录用户在首页看到自己发布的快写
- **THEN** 该快写卡片上显示「✏️ 编辑」按钮

#### Scenario: 他人的快写无编辑按钮
- **WHEN** 已登录用户看到其他用户发布的快写
- **THEN** 快写卡片上不显示编辑按钮

#### Scenario: 点击编辑切换为内联编辑模式
- **WHEN** 用户点击自己快写上的「✏️ 编辑」按钮
- **THEN** 快写内容变为 textarea（预填原内容），可见范围变为下拉框，显示「保存」和「取消」按钮

#### Scenario: 保存内联编辑
- **WHEN** 用户修改内容或可见范围后点击「保存」
- **THEN** 系统调用 `PUT /api/quick-posts/{id}` 更新快写，卡片回到正常显示模式

#### Scenario: 取消内联编辑
- **WHEN** 用户在内联编辑模式下点击「取消」
- **THEN** 卡片恢复到编辑前的显示模式，不发送 API 请求

#### Scenario: 内容为空时保存
- **WHEN** 用户清空 content 后点击「保存」
- **THEN** 前端提示「内容不能为空」，不发送 API 请求