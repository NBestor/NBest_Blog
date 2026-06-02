## 1. 后端基础与主管初始化

- [x] 1.1 修改 `backend/app/db/database.py`：在数据库初始化流程中确保 ID 为 `0`、账号名为 `NBest`、角色为 `admin` 的主管账号存在，首次创建密码为 `NBest666`。
- [x] 1.2 修改 `backend/app/db/database.py`：确保已有主管账号启动时保持 `username = NBest`、`nickname = NBest`、`role = admin`，但不覆盖已有密码。
- [x] 1.3 修改 `backend/app/api/auth.py` 或新增等价 helper：实现 `isSupervisor`、`getCurrentAdmin`、`getCurrentSupervisor` 权限判断。
- [x] 1.4 运行登录验证：确认 `NBest / NBest666` 可以登录，且 `/api/auth/me` 返回 `id = 0`、`username = NBest`、`role = admin`。

## 2. 后端管理员服务能力

- [x] 2.1 修改 `backend/app/services/user_service.py`：新增管理员用户列表查询，返回用户基础资料、角色、头像状态和是否可管理。
- [x] 2.2 修改 `backend/app/services/user_service.py`：新增管理员删除用户能力，普通管理员只能删除普通用户，主管可删除普通管理员，主管不能删除自己。
- [x] 2.3 修改 `backend/app/services/user_service.py`：新增强制重命名能力，对可管理用户设置合规占位名称。
- [x] 2.4 修改 `backend/app/services/user_service.py`：新增管理员移除用户头像能力，清空目标用户头像并避免删除非上传目录文件。
- [x] 2.5 修改 `backend/app/services/user_service.py`：新增主管任命/撤销管理员能力，普通管理员不可调用，主管不可降级自己。
- [x] 2.6 修改 `backend/app/services/article_service.py`：新增管理员文章列表和删除文章能力。
- [x] 2.7 修改 `backend/app/services/quick_post_service.py`：新增管理员快写列表和删除快写能力。
- [x] 2.8 修改 `backend/app/services/comment_service.py`：新增管理员评论列表和删除评论能力。
- [x] 2.9 修改 `backend/app/services/photo_service.py`：确认或补齐管理员照片列表与删除照片能力，保持主管/管理员权限一致。
- [x] 2.10 如服务层需要共享类型或格式化逻辑，最小化修改对应 schema 文件，例如 `backend/app/schemas/user.py` 或新增 `backend/app/schemas/admin.py`。

## 3. 后端管理员 API

- [x] 3.1 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/summary`。
- [x] 3.2 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/users`、`DELETE /api/admin/users/{user_id}`、`PATCH /api/admin/users/{user_id}/rename`、`DELETE /api/admin/users/{user_id}/avatar`。
- [x] 3.3 新增 `backend/app/api/admin.py`：实现 `PATCH /api/admin/users/{user_id}/role`，仅主管可用。
- [x] 3.4 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/articles`、`DELETE /api/admin/articles/{article_id}`。
- [x] 3.5 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/quick-posts`、`DELETE /api/admin/quick-posts/{quick_post_id}`。
- [x] 3.6 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/comments`、`DELETE /api/admin/comments/{comment_id}`。
- [x] 3.7 新增 `backend/app/api/admin.py`：实现 `GET /api/admin/photos`、`DELETE /api/admin/photos/{photo_id}`。
- [x] 3.8 修改 `backend/app/api/router.py`：注册管理员路由。
- [x] 3.9 运行 API 权限验证：游客和普通用户访问 `/api/admin/*` 被拒绝。
- [x] 3.10 运行 API 权限验证：普通管理员可以执行普通治理操作，但不能任命/撤销管理员，也不能删除管理员或主管。
- [x] 3.11 运行 API 权限验证：主管可以任命/撤销管理员，可以管理普通管理员，但不能删除或降级自己。
- [x] 3.12 运行 API 内容验证：删除文章、快写、评论、照片后，普通列表和详情接口不再返回对应内容。

## 4. 前端路由与导航权限

- [x] 4.1 修改 `frontend/src/routes/route-config.js`：新增 `/admin` 路由配置，label 为“管理”，visibility 为 `admin`。
- [x] 4.2 修改 `frontend/src/layouts/AppLayout.jsx`：扩展导航可见性逻辑，让“管理”只对 `role = admin` 的用户显示。
- [x] 4.3 新增 `frontend/src/components/AdminRoute.jsx` 或扩展 `ProtectedRoute.jsx`：保护 `/admin`，游客引导登录，普通用户拒绝访问或跳转。
- [x] 4.4 修改 `frontend/src/App.jsx`：注册 `/admin` 页面并接入管理员路由保护。
- [x] 4.5 使用 in-app browser 验证：游客和普通用户顶部导航不显示“管理”，直接访问 `/admin` 不显示管理数据。
- [x] 4.6 使用 in-app browser 验证：普通管理员和主管登录后顶部导航显示“管理”。

## 5. 前端管理员页面

- [x] 5.1 新增 `frontend/src/pages/AdminPage.jsx`：实现管理页布局、概览区、分区切换、加载状态、空状态和错误提示。
- [x] 5.2 修改 `frontend/src/pages/AdminPage.jsx`：实现用户治理列表，包括删除用户、强制重命名、移除头像操作。
- [x] 5.3 修改 `frontend/src/pages/AdminPage.jsx`：实现主管专属任命/撤销管理员操作，普通管理员不可见。
- [x] 5.4 修改 `frontend/src/pages/AdminPage.jsx`：实现文章治理列表和删除文章操作。
- [x] 5.5 修改 `frontend/src/pages/AdminPage.jsx`：实现快写治理列表和删除快写操作。
- [x] 5.6 修改 `frontend/src/pages/AdminPage.jsx`：实现评论治理列表和删除评论操作。
- [x] 5.7 修改 `frontend/src/pages/AdminPage.jsx`：实现照片治理列表和删除照片操作。
- [x] 5.8 修改 `frontend/src/pages/AdminPage.jsx`：所有删除、降级、任命等高风险操作提交前显示二次确认。
- [x] 5.9 修改 `frontend/src/pages/AdminPage.jsx`：操作成功后刷新当前分区，401/403 显示错误并保留页面稳定。

## 6. 前端样式与移动端

- [x] 6.1 修改 `frontend/src/styles/global.css`：新增管理员页面分区、工具栏、统计块、列表卡片和危险按钮样式。
- [x] 6.2 修改 `frontend/src/styles/global.css`：补充管理员页面 900px 和 768px 以下的单列布局。
- [x] 6.3 修改 `frontend/src/styles/global.css`：确保长用户名、长标题、长评论、长图片链接在管理页不横向溢出。
- [x] 6.4 使用 in-app browser 验证桌面端 `/admin`：普通管理员页面无溢出，主管页面显示任命/撤销管理员入口。
- [x] 6.5 使用 in-app browser 验证移动端 `/admin`：导航、分区、列表、二次确认和危险操作按钮不重叠、不横向滚动。

## 7. 自动化与构建验证

- [x] 7.1 运行后端导入/接口脚本验证管理员 API 主要路径。
- [x] 7.2 运行 `npm run lint`。
- [x] 7.3 运行 `npm run build`。
- [x] 7.4 运行 `openspec validate add-admin-moderation --strict`。

## 8. 收尾确认

- [x] 8.1 确认 `openspec/changes/add-admin-moderation/tasks.md` 所有实现与验证项完成。
- [x] 8.2 汇总本变更实际修改文件、管理员/主管测试账号、API 验证结果和浏览器验证结果，准备用户验收。
