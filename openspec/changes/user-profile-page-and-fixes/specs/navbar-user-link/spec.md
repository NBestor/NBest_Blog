## ADDED Requirements

### Requirement: Navbar User Name and Avatar as Clickable Link
导航栏（`AppLayout.jsx`）右上角已登录用户的头像和用户名 SHALL 包裹在 `<Link>` 中，点击跳转到自己的用户主页 `/user/{user.id}`。

#### Scenario: 有头像用户点击跳转
- **WHEN** 已登录用户设置了头像
- **THEN** 导航栏头像和用户名包裹在同一 `<Link to={/user/${user.id}}>` 中
- **WHEN** 用户点击头像或用户名
- **THEN** 跳转到 `/user/{user.id}` 用户主页

#### Scenario: 无头像用户点击跳转
- **WHEN** 已登录用户未设置头像
- **THEN** 首字母占位符和用户名包裹在同一 `<Link>` 中
- **WHEN** 用户点击占位符或用户名
- **THEN** 跳转到用户主页

#### Scenario: 退出按钮不受影响
- **WHEN** 已登录用户查看导航栏
- **THEN**「退出」按钮仍然在 Link 之外保持独立

#### Scenario: 游客不受影响
- **WHEN** 用户未登录
- **THEN** 导航栏仍显示「登录」NavLink，无变化