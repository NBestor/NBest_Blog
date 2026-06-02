## 1. 后端数据与接口

- [x] 1.1 修改 `backend/app/db/database.py`：新增 `calendar_events` 表和 `user_id/event_date/is_yearly` 相关索引。
- [x] 1.2 新增 `backend/app/schemas/calendar_event.py`：定义日历事件创建、更新、响应、列表和提醒 schema。
- [x] 1.3 新增 `backend/app/services/calendar_event_service.py`：实现当前用户维度的事件列表、月份查询、创建、更新、删除、年度重复显示日期计算和未来 7 天提醒查询。
- [x] 1.4 新增 `backend/app/api/calendar_events.py`：实现 `GET/POST/PUT/DELETE /api/calendar-events` 和 `GET /api/calendar-events/reminders`。
- [x] 1.5 修改 `backend/app/api/router.py`：注册日历事件 router。

## 2. 前端日历页面

- [x] 2.1 新增 `frontend/src/pages/CalendarPage.jsx`：实现月历网格、月份切换、事件标注、事件列表和事件表单。
- [x] 2.2 修改 `frontend/src/App.jsx`：将 `/calendar` 从占位页替换为受保护的 `CalendarPage`。
- [x] 2.3 修改 `frontend/src/styles/global.css`：补充日历页面网格、日期格、事件标签、表单和操作样式。

## 3. 统一提醒中心

- [x] 3.1 新增 `frontend/src/components/ReminderModal.jsx`：并行查询 `/todos/reminders` 和 `/calendar-events/reminders`，按分组展示提醒。
- [x] 3.2 修改 `frontend/src/layouts/AppLayout.jsx`：用统一提醒中心替换 `TodoReminderModal`，游客不查询提醒，关闭后本次页面生命周期不重复弹出。
- [x] 3.3 删除或停用 `frontend/src/components/TodoReminderModal.jsx`：避免保留两个全局提醒弹窗。
- [x] 3.4 修改 `frontend/src/styles/global.css`：调整提醒弹窗样式以支持 Todo 和日历两类分组。

## 4. 后端验证

- [x] 4.1 运行后端 API 验证：游客访问日历 API 被拒绝。
- [x] 4.2 运行后端 API 验证：登录用户可创建、月份查询、更新、删除自己的日历事件。
- [x] 4.3 运行后端 API 验证：用户无法修改或删除他人的日历事件。
- [x] 4.4 运行后端 API 验证：年度重复事件在后续年份对应月份可显示，非重复事件不跨年显示。
- [x] 4.5 运行后端 API 验证：未来 7 天提醒包含年度重复事件，并排除提醒窗口外事件。

## 5. 前端验证

- [x] 5.1 运行 `npm run lint`。
- [x] 5.2 运行 `npm run build`。
- [x] 5.3 使用 in-app browser 验证 `/calendar` 页面：月历可见，月份切换可用，事件标记和事件表单可见。
- [x] 5.4 使用 in-app browser 验证统一提醒中心：存在日历提醒时弹出；同时存在 Todo 和日历提醒时分组展示；游客不弹出。
