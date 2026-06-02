## Context

当前系统已经有 `users.role` 字段，取值为 `user` 或 `admin`，但管理员能力主要停留在角色存在和照片管理的局部权限上。前端导航按登录状态展示入口，尚未支持按角色展示“管理”入口；后端也没有统一的管理员 API、主管身份校验、用户/内容治理接口。

本变更需要把管理员模式做成可登录、可见、可操作、可验证的治理后台。同时新增固定主管账号 `NBest`，用户 ID 为 `0`，初始密码为 `NBest666`，用于任命和管理其他管理员。所有实现应复用当前 FastAPI + SQLite + React + Vite 结构，不引入新的 UI 框架或业务依赖。

## Goals / Non-Goals

**Goals:**

- 提供真实可用的管理员管理前端，管理员和主管登录后顶部导航显示“管理”，普通用户和游客完全看不到管理 UI。
- 后端提供 `/api/admin/*` 管理员 API，统一校验登录身份和角色。
- 初始化并保护固定主管账号 `NBest`，ID 为 `0`，主管可任命/撤销管理员。
- 管理员可以治理普通用户资料和内容，包括删除普通用户、删除博客文章、删除快写、删除评论、删除照片、移除违规头像、强制重命名。
- 普通管理员不能管理其他管理员；主管可以管理管理员，但不能删除或降级主管自身。
- 所有高风险操作前端二次确认，后端再次做权限和目标约束校验。
- 保持普通用户现有写作、快写、照片、Todo、日历、关注流程不变。

**Non-Goals:**

- 不做完整企业后台，不引入复杂审计流、角色组、权限矩阵或多级组织结构。
- 不新增封禁、禁言、内容恢复、软删除回收站，除非后续单独提案。
- 不改变当前普通用户注册和登录流程。
- 不引入新数据库、ORM、UI 组件库或状态管理库。
- 不把普通用户页面改造成后台风格，只新增管理员管理页面和必要样式。

## Decisions

1. 使用固定主管账号而不是新增第三种公开角色。

   设计上继续保留 `users.role` 的 `user/admin` 角色模型，主管通过固定 `id = 0` 且 `username = 'NBest'` 识别。这样可以避免立刻迁移 `CHECK (role IN ('user', 'admin'))` 约束，也不需要大范围改动现有 `UserResponse.role`、导航和权限判断。

   备选方案是新增 `super_admin` 角色。该方案语义更清晰，但 SQLite 现有 `role` CHECK 约束迁移成本更高，且本阶段只需要一个固定主管账号，暂不采用。

2. 在数据库初始化阶段确保主管账号存在。

   `initDatabase()` 在创建 `users` 表和基础索引后，检查 `id = 0` 的用户是否存在：
   - 不存在时插入 `id = 0, username = 'NBest', nickname = 'NBest', role = 'admin'`，密码哈希来自 `NBest666`。
   - 存在时确保该用户 `username`、`nickname`、`role` 保持主管规则，密码不强制覆盖，避免后续用户修改密码后被启动流程重置。

   需要注意 SQLite 自增表可以显式插入 ID 0。后续普通用户仍使用 AUTOINCREMENT 分配正整数 ID。

3. 新增统一管理员权限 helper。

   在后端新增或复用依赖函数：
   - `getCurrentAdmin()`：基于 `getCurrentUser()`，要求 `role == 'admin'`。
   - `getCurrentSupervisor()`：要求 `role == 'admin'` 且 `id == 0` 且 `username == 'NBest'`。
   - `isSupervisor(user)`：供 service 层判断主管约束。

   管理员 API 必须依赖这些 helper，不依赖前端隐藏按钮作为权限控制。

4. 使用独立 `/api/admin` 路由聚合治理接口。

   新增 `backend/app/api/admin.py`，并在 `backend/app/api/router.py` 注册。接口按资源分组：
   - `GET /api/admin/summary`
   - `GET /api/admin/users`
   - `DELETE /api/admin/users/{user_id}`
   - `PATCH /api/admin/users/{user_id}/rename`
   - `DELETE /api/admin/users/{user_id}/avatar`
   - `PATCH /api/admin/users/{user_id}/role`
   - `GET /api/admin/articles`
   - `DELETE /api/admin/articles/{article_id}`
   - `GET /api/admin/quick-posts`
   - `DELETE /api/admin/quick-posts/{quick_post_id}`
   - `GET /api/admin/comments`
   - `DELETE /api/admin/comments/{comment_id}`
   - `GET /api/admin/photos`
   - `DELETE /api/admin/photos/{photo_id}`

   查询接口返回管理页需要的最小字段，例如 ID、作者、标题/摘要、时间、可见性、角色、是否可管理。删除接口保持简单返回 `{ "status": "ok" }`。

5. 管理约束放在后端 service 层。

   API 层负责鉴权和参数接收，具体约束由 service 层执行：
   - 普通管理员只能删除或修改普通用户。
   - 普通管理员不能删除自己、主管或任何管理员。
   - 主管可以任命普通用户为管理员，也可以撤销管理员为普通用户。
   - 主管不能删除、降级、强制改名或移除自己头像。
   - 删除用户时遵循现有外键级联，清理该用户文章、照片、快写、快记、Todo、日历等关联数据。

   这样前端无论是否误显示按钮，后端都会给出 403 或 404。

6. 前端新增管理员受保护路由。

   新增 `AdminPage.jsx`，路由为 `/admin`。新增 `AdminRoute` 或扩展 `ProtectedRoute`，要求当前用户为管理员；非登录用户跳转登录，普通用户访问显示无权限或跳转首页。

   `route-config.js` 新增 `visibility: 'admin'` 的“管理”入口。`AppLayout.jsx` 的导航过滤逻辑扩展为：
   - `public`：所有人可见。
   - `guest`：未登录可见。
   - `auth`：已登录可见。
   - `admin`：`user.role === 'admin'` 可见。

   管理页面内部根据 `user.id === 0 && user.username === 'NBest'` 显示任命/撤销管理员按钮；普通管理员看不到这些主管操作。

7. 管理页采用分区列表而不是复杂后台表格。

   为符合当前博客产品风格，管理页使用 tabs 或分区列表：
   - 概览
   - 用户
   - 文章
   - 快写
   - 评论
   - 照片
   - 管理员设置，仅主管可见

   每个分区提供加载、空状态、错误提示、危险操作按钮和二次确认。移动端采用单列卡片布局，桌面端可使用紧凑列表，不新增表格库。

8. 前端不缓存管理员权限判断结果作为安全依据。

   管理页可根据 `AuthContext.user` 控制 UI 可见性，但每次管理操作仍以 API 返回为准。若后端返回 401/403，页面显示错误并刷新当前分区。

## Risks / Trade-offs

- [Risk] 固定 ID 0 与 SQLite AUTOINCREMENT 行为存在实现细节风险。→ Mitigation：在初始化脚本中显式插入并验证 `id = 0`，用 API 回归覆盖主管登录、普通用户注册 ID 分配和主管保护。
- [Risk] 继续使用 `role = admin` 表示普通管理员和主管，语义上不如 `super_admin` 清晰。→ Mitigation：把主管判断集中到 helper，后续若需要多主管或权限矩阵，可单独迁移角色模型。
- [Risk] 删除用户会级联删除大量数据，误操作代价高。→ Mitigation：前端必须二次确认，后端禁止普通管理员删除管理员/主管，并在删除按钮文案中明确影响。
- [Risk] 管理员列表查询可能一次返回较多数据。→ Mitigation：本阶段先按当前小型项目规模实现，必要时后续增加分页和搜索。
- [Risk] 违规头像文件删除可能遇到本地文件不存在或路径异常。→ Mitigation：移除头像以数据库状态为准，文件删除失败不阻塞资料恢复默认状态，并避免删除非上传目录文件。
- [Risk] 普通用户直接访问 `/admin` 可能看到短暂加载状态。→ Mitigation：路由保护在用户状态加载完成后再判定，并且管理页面自身二次检查角色。

## Migration Plan

1. 更新数据库初始化逻辑，确保 `NBest` 主管账号存在且受保护。
2. 新增后端管理员权限 helper 和 `/api/admin/*` 路由。
3. 扩展 service 层的管理员查询、删除、重命名、头像移除和角色变更能力。
4. 新增前端 `/admin` 页面、管理员路由保护和顶部“管理”导航入口。
5. 补充全局样式中的管理员列表、分区、危险操作和移动端布局。
6. 运行后端 API 回归：主管、普通管理员、普通用户、游客四类身份。
7. 使用 in-app browser 验证普通用户看不到管理 UI，管理员/主管登录后可见“管理”入口，主管可任命管理员。

Rollback 策略：
- 若前端管理页出现问题，可移除 `/admin` 路由和导航入口，不影响普通用户功能。
- 若后端管理员 API 出现问题，可先取消路由注册。
- `NBest` 账号初始化属于数据变更；回滚时可保留该账号为普通管理员，也可在明确确认后手动删除，但不能影响已有普通用户数据。

## Open Questions

- 主管 `NBest` 的初始密码 `NBest666` 是否需要在第一次登录后强制修改？本设计暂不强制，但建议后续单独增加安全提醒。
- 删除用户是否应立即物理删除，还是后续改为软删除/禁用？本设计按当前需求采用物理删除。
- 强制改名的占位名称格式是否固定，例如 `违规用户_<id>`？设计默认采用可预测占位名，具体格式在任务实现阶段确认。
- 管理员删除文章、快写、评论是否需要记录操作日志？本阶段不做审计日志，后续可新增 `admin-audit-log` 能力。
