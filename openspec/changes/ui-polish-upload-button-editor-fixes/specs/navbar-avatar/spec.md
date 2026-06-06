## ADDED Requirements

### Requirement: User Avatar Display in Navbar
导航栏（`AppLayout.jsx`）右上角用户区域 SHALL 在用户名左侧显示用户头像。当用户已登录且 `user.avatar_url` 存在时，MUST 显示圆形头像图片；当用户未设置头像时，SHALL 显示首字母圆形占位符。头像 SHALL 与用户名保持垂直居中对齐。

#### Scenario: 有头像用户显示头像图片
- **WHEN** 已登录用户设置了头像（`user.avatar_url` 不为空）
- **THEN** 导航栏右上角用户名左侧显示圆形头像图片，尺寸约 28px

#### Scenario: 无头像用户显示首字母占位符
- **WHEN** 已登录用户未设置头像（`user.avatar_url` 为空或 null）
- **THEN** 导航栏右上角用户名左侧显示圆形首字母占位符，背景为灰色，首字母为昵称或用户名的第一个字符

#### Scenario: 游客不显示头像
- **WHEN** 用户未登录，导航栏显示「登录」链接
- **THEN** 不显示头像或占位符

#### Scenario: 头像与用户名对齐
- **WHEN** 导航栏显示头像和用户名
- **THEN** 头像和用户名在同一水平线上垂直居中对齐

#### Scenario: 点击头像或用户名跳转
- **WHEN** 用户点击头像或用户名区域
- **THEN** 不跳转（保持当前状态，头像仅为视觉标识，用户名保持现有行为不变）