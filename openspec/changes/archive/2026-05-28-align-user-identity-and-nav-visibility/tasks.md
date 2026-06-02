## 1. 后端注册兼容

- [x] 1.1 修改 `backend/app/schemas/auth.py`：让注册请求支持单一账号名称，并保留旧 `nickname` 字段的兼容输入。
- [x] 1.2 修改 `backend/app/api/auth.py`：注册时将缺省昵称派生为账号名称，保证新用户 `username` 与 `nickname` 一致。
- [x] 1.3 验证注册接口：新单名称 payload 可注册，旧 `username + nickname` payload 仍可注册，重复名称仍返回冲突。

## 2. 前端身份输入与展示

- [x] 2.1 修改 `frontend/src/pages/RegisterPage.jsx`：移除独立昵称输入，只展示一个账号名称输入，并提交兼容后端的注册 payload。
- [x] 2.2 修改 `frontend/src/pages/ProfilePage.jsx`：个人中心避免重复展示完全相同的用户名和昵称，主要展示合并后的用户名称。
- [x] 2.3 修改 `frontend/src/pages/FollowPage.jsx`：关注/粉丝/好友条目以合并后的用户名称为主，只有在用户名和昵称不同时才展示辅助标识。
- [x] 2.4 检查并按需调整 `frontend/src/layouts/AppLayout.jsx`、`frontend/src/pages/HomePage.jsx`、`frontend/src/pages/BlogListPage.jsx`、`frontend/src/pages/BlogDetailPage.jsx`、`frontend/src/pages/PhotoPage.jsx` 的用户名称显示，避免新增重复身份文案。

## 3. 导航按用户状态过滤

- [x] 3.1 修改 `frontend/src/routes/route-config.js`：为路由增加可见性元数据，区分 `public`、`guest`、`auth`，并标记隐藏详情页等非导航入口。
- [x] 3.2 修改 `frontend/src/App.jsx`：尽量从路由元数据维护私有路由集合，减少导航可见性和路由守卫配置漂移。
- [x] 3.3 修改 `frontend/src/layouts/AppLayout.jsx`：根据 `isAuthenticated` 过滤导航；游客不显示快记、草稿、写文章、个人中心、设置、关注管理等私有入口；登录用户不显示登录/注册入口。
- [x] 3.4 确认 `/quick/note` 等私有页面直接输入 URL 时仍由 `ProtectedRoute` 保护。

## 4. 验证

- [x] 4.1 运行后端接口验证：注册新用户后确认返回的 `username` 与 `nickname` 一致，并确认旧 payload 兼容。
- [x] 4.2 运行前端质量检查：执行 `npm run lint` 和 `npm run build`。
- [x] 4.3 使用 in-app browser 验证游客导航：不显示快记等私有入口，直接访问 `/quick/note` 会进入登录流程。
- [x] 4.4 使用 in-app browser 验证登录用户导航：显示快记等个人功能入口，隐藏登录/注册入口，并可正常进入快记页面。
