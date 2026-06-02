## 1. UI 与流程盘点

- [x] 1.1 检查 `frontend/src/styles/global.css`：梳理按钮、表单、面板、卡片、弹窗、提示和移动端规则的重复与不一致。
- [x] 1.2 检查 `frontend/src/layouts/AppLayout.jsx` 和 `frontend/src/routes/route-config.js`：确认导航仍按用户状态展示，记录需要复测的游客/登录态入口。
- [x] 1.3 检查核心页面 JSX：`HomePage.jsx`、`BlogListPage.jsx`、`BlogDetailPage.jsx`、`BlogEditPage.jsx`、`BlogDraftPage.jsx`、`ProfilePage.jsx`、`FollowPage.jsx`、`PhotoPage.jsx`、`TodoPage.jsx`、`CalendarPage.jsx`、`QuickNotePage.jsx`、`UserSettingPage.jsx`，记录明显 UI 不一致或状态缺口。
- [x] 1.4 检查全局弹窗组件 `frontend/src/components/ReminderModal.jsx`：确认提醒中心与照片预览等弹窗的遮罩、层级和移动端宽度可统一。

## 2. 全局样式收敛

- [x] 2.1 修改 `frontend/src/styles/global.css`：统一基础按钮、次要按钮、文本按钮、表单输入、选择框和文本区域的高度、边框、圆角、焦点态。
- [x] 2.2 修改 `frontend/src/styles/global.css`：统一 `content-panel`、列表卡片、空状态、加载状态、成功提示和错误提示样式。
- [x] 2.3 修改 `frontend/src/styles/global.css`：统一弹窗遮罩、弹窗内容宽度、关闭/操作区样式，覆盖提醒中心和照片预览。
- [x] 2.4 修改 `frontend/src/styles/global.css`：补充长文本、长链接、按钮文本和窄屏 grid 的安全换行/收敛规则。
- [x] 2.5 修改 `frontend/src/styles/global.css`：完善 900px 和 768px 断点下的主要页面布局，避免横向溢出和内容重叠。

## 3. 页面状态与结构细节

- [x] 3.1 如盘点发现缺口，修改 `frontend/src/pages/HomePage.jsx`：统一首页快写、动态流、评论区的表单、空状态和操作区。
- [x] 3.2 如盘点发现缺口，修改 `frontend/src/pages/BlogEditPage.jsx` 和 `frontend/src/pages/BlogDraftPage.jsx`：统一编辑器、草稿列表和保存/错误状态。
- [x] 3.3 如盘点发现缺口，修改 `frontend/src/pages/PhotoPage.jsx`、`TodoPage.jsx`、`CalendarPage.jsx`、`QuickNotePage.jsx`：统一个人工具页面的表单、列表、空状态和操作区。
- [x] 3.4 如盘点发现缺口，修改 `frontend/src/pages/ProfilePage.jsx`、`FollowPage.jsx`、`UserSettingPage.jsx`：统一个人资料、关注列表和设置页的表单/列表状态。
- [x] 3.5 如盘点发现缺口，修改 `frontend/src/components/ReminderModal.jsx`：使用全局弹窗样式并保证移动端不溢出。

## 4. 缺陷修复边界

- [x] 4.1 如 API 复测发现真实权限或流程缺陷，最小化修改对应后端文件，并在此任务下记录具体文件。复测未发现需修改的后端文件。
- [x] 4.2 如浏览器复测发现真实前端流程阻断，最小化修改对应页面或组件，并在此任务下记录具体文件。移动端文章详情长链接溢出已在 `frontend/src/styles/global.css` 中修复。
- [x] 4.3 确认本变更未新增业务模块、未改变已确认业务规则、未引入新依赖。

## 5. 自动化与构建验证

- [x] 5.1 运行 `npm run lint`。
- [x] 5.2 运行 `npm run build`。
- [x] 5.3 运行 `openspec validate polish-global-ui-and-flows --strict`。

## 6. API 权限回归验证

- [x] 6.1 运行 API 验证：游客写入类接口被拒绝，受保护资源接口需要登录。
- [x] 6.2 运行 API 验证：用户 A 的私密快记、Todo、日历事件和私密照片不返回给用户 B 或游客。
- [x] 6.3 运行 API 验证：非拥有者无法修改或删除他人的私有资源。
- [x] 6.4 如测试管理员可用，运行 API 验证：管理员允许的管理操作可执行，普通用户同类越权操作被拒绝。

## 7. in-app browser 视觉与流程验证

- [x] 7.1 使用 in-app browser 验证游客页面：首页、博客列表、文章详情、照片墙可浏览，登录后专属入口和操作不显示。
- [x] 7.2 使用 in-app browser 验证登录流程：注册/登录/刷新/退出后导航和受保护页面行为正确。
- [x] 7.3 使用 in-app browser 验证登录用户核心页面：文章编辑/草稿、快写/快记、Todo、日历、照片墙、个人中心、关注、设置页面可见且主要操作区不溢出。
- [x] 7.4 使用 in-app browser 验证移动端宽度：导航、表单、列表、弹窗和长文本不重叠、不产生明显横向滚动。
- [x] 7.5 使用 in-app browser 验证弹窗：提醒中心和照片预览遮罩、内容宽度、关闭入口在桌面和移动端可用。

## 8. 收尾确认

- [x] 8.1 确认 `openspec/changes/polish-global-ui-and-flows/tasks.md` 所有实现与验证项完成。
- [x] 8.2 汇总本变更实际修改文件和验证结果，准备用户验收。
