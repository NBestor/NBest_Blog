## MODIFIED Requirements

### Requirement: Remove Quick Post Visibility Setting from Settings Page
`UserSettingPage.jsx` 页面 SHALL 不再显示快写默认可见范围设置表单。原来的 `<form>` + `<select>` 交互 SHALL 替换为静态提示文字，告知用户快写可见范围可在首页发布时设置。

后端 `GET /users/me/settings` 和 `PUT /users/me/settings` 接口 SHALL 保持不变，`HomePage.jsx` 初始化时仍通过 `GET /users/me/settings` 读取 `quick_post_default_visible_type` 作为默认值。

#### Scenario: 设置页不再显示快写可见范围下拉框
- **WHEN** 用户访问 `/user/setting` 设置页
- **THEN** 页面不再显示 `<select>` 下拉框选择快写默认可见范围
- **AND** 页面不再显示「保存设置」提交按钮

#### Scenario: 设置页显示提示文字
- **WHEN** 用户访问 `/user/setting` 设置页
- **THEN** 页面显示提示文字：「快写的可见范围可在首页发布快写时直接设置。」
- **AND** 页面标题仍为「个人设置」

#### Scenario: HomePage 仍正常读取默认可见范围
- **WHEN** 已登录用户访问首页 `/`
- **THEN** `HomePage.jsx` 仍调用 `GET /users/me/settings` 获取 `quick_post_default_visible_type`
- **AND** 快写发布表单的可见范围下拉框初始值为该默认值

#### Scenario: 后端设置接口不受影响
- **WHEN** 通过 API 调用 `GET /users/me/settings` 或 `PUT /users/me/settings`
- **THEN** 接口正常返回/更新 `quick_post_default_visible_type`