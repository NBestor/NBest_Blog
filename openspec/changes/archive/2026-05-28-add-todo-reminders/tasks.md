## 1. 后端数据与接口

- [x] 1.1 修改 `backend/app/db/database.py`：新增 `todos` 表和 `user_id/is_done/due_date` 相关索引。
- [x] 1.2 新增 `backend/app/schemas/todo.py`：定义 Todo 创建、更新、响应和列表 schema。
- [x] 1.3 新增 `backend/app/services/todo_service.py`：实现当前用户维度的列表、创建、更新、删除、完成状态切换和提醒查询。
- [x] 1.4 新增 `backend/app/api/todos.py`：实现 `GET/POST/PUT/DELETE /api/todos` 相关接口和 `GET /api/todos/reminders`。
- [x] 1.5 修改 `backend/app/api/router.py`：注册 Todo router。

## 2. 前端 Todo 页面

- [x] 2.1 新增 `frontend/src/pages/TodoPage.jsx`：实现待办列表、新增表单、编辑保存、删除和完成状态切换。
- [x] 2.2 修改 `frontend/src/App.jsx`：将 `/todo` 从占位页替换为受保护的 `TodoPage`。
- [x] 2.3 修改 `frontend/src/styles/global.css`：补充 Todo 页面所需布局、表单、列表、状态和操作样式。

## 3. 全局提醒弹窗

- [x] 3.1 新增 `frontend/src/components/TodoReminderModal.jsx`：登录用户查询 `/todos/reminders` 并展示提醒弹窗。
- [x] 3.2 修改 `frontend/src/layouts/AppLayout.jsx`：挂载 Todo 提醒弹窗，游客不查询提醒，关闭后本次页面生命周期不重复弹出。
- [x] 3.3 修改 `frontend/src/styles/global.css`：补充提醒弹窗样式。

## 4. 后端验证

- [x] 4.1 运行后端 API 验证：游客访问 Todo API 被拒绝。
- [x] 4.2 运行后端 API 验证：登录用户可创建、列表、更新、删除自己的 Todo。
- [x] 4.3 运行后端 API 验证：用户无法修改或删除他人的 Todo。
- [x] 4.4 运行后端 API 验证：提醒接口只返回当前用户未完成且已到期/未来 1 天内到期的 Todo。

## 5. 前端验证

- [x] 5.1 运行 `npm run lint`。
- [x] 5.2 运行 `npm run build`。
- [x] 5.3 使用 in-app browser 验证 `/todo` 页面：新增、编辑、删除、完成状态切换可用。
- [x] 5.4 使用 in-app browser 验证全局提醒弹窗：存在提醒时弹出，关闭后不反复弹出；游客不弹出。
