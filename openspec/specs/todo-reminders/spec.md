# todo-reminders Specification

## Purpose
TBD - created by archiving change add-todo-reminders. Update Purpose after archive.
## Requirements
### Requirement: 私密待办数据隔离
系统 SHALL 将 Todo 数据强制绑定到当前登录用户，任何用户只能访问自己的待办。

#### Scenario: 游客访问 Todo API
- **WHEN** 未登录访客请求 Todo API
- **THEN** 系统 MUST 拒绝请求并要求登录

#### Scenario: 用户查看待办列表
- **WHEN** 登录用户请求待办列表
- **THEN** 系统 MUST 只返回该用户自己的待办

#### Scenario: 用户修改他人待办
- **WHEN** 登录用户尝试更新或删除不属于自己的待办
- **THEN** 系统 MUST 不返回他人数据，并按不存在处理

### Requirement: 待办 CRUD
系统 SHALL 支持登录用户创建、读取、更新和删除自己的待办。

#### Scenario: 创建待办
- **WHEN** 登录用户提交标题、分类、截止日期和内容
- **THEN** 系统 MUST 创建一条属于该用户的未完成待办

#### Scenario: 更新待办
- **WHEN** 登录用户修改自己待办的标题、分类、截止日期或内容
- **THEN** 系统 MUST 保存修改并更新该待办的更新时间

#### Scenario: 删除待办
- **WHEN** 登录用户删除自己的待办
- **THEN** 系统 MUST 移除该待办，后续列表不再返回

### Requirement: 完成状态管理
系统 SHALL 支持登录用户将自己的待办标记为完成或未完成。

#### Scenario: 标记完成
- **WHEN** 登录用户将未完成待办标记为完成
- **THEN** 系统 MUST 将该待办的完成状态保存为已完成

#### Scenario: 恢复未完成
- **WHEN** 登录用户将已完成待办恢复为未完成
- **THEN** 系统 MUST 将该待办的完成状态保存为未完成

### Requirement: 到期待办提醒查询
系统 SHALL 提供提醒查询能力，返回当前用户未完成且已到期或即将到期的待办。

#### Scenario: 查询提醒
- **WHEN** 登录用户请求 Todo 提醒
- **THEN** 系统 MUST 返回该用户未完成且截止日期不晚于未来 1 天的待办

#### Scenario: 排除已完成待办
- **WHEN** 登录用户请求 Todo 提醒
- **THEN** 系统 MUST NOT 返回已完成待办

#### Scenario: 排除无截止日期待办
- **WHEN** 登录用户请求 Todo 提醒
- **THEN** 系统 MUST NOT 返回没有截止日期的待办

### Requirement: Todo 页面操作
系统 SHALL 在 `/todo` 页面为登录用户提供待办列表和基础操作界面。

#### Scenario: 打开 Todo 页面
- **WHEN** 登录用户打开 `/todo`
- **THEN** 页面 MUST 展示该用户自己的待办列表和新增待办表单

#### Scenario: 页面新增待办
- **WHEN** 登录用户在 `/todo` 页面提交新增表单
- **THEN** 页面 MUST 刷新列表并显示新待办

#### Scenario: 页面编辑待办
- **WHEN** 登录用户在 `/todo` 页面编辑并保存待办
- **THEN** 页面 MUST 展示保存后的待办内容

#### Scenario: 页面切换完成状态
- **WHEN** 登录用户在 `/todo` 页面切换待办完成状态
- **THEN** 页面 MUST 更新该待办的完成状态显示

### Requirement: 全局页面提醒弹窗
系统 SHALL 在登录用户进入网站时展示 Todo 提醒弹窗。

#### Scenario: 登录用户进入网站且存在提醒
- **WHEN** 登录用户进入任意应用页面，且存在已到期或即将到期的未完成待办
- **THEN** 页面 MUST 展示提醒弹窗，并列出需要提醒的待办

#### Scenario: 登录用户进入网站且没有提醒
- **WHEN** 登录用户进入任意应用页面，且不存在需要提醒的待办
- **THEN** 页面 MUST NOT 展示提醒弹窗

#### Scenario: 游客进入网站
- **WHEN** 未登录访客进入任意应用页面
- **THEN** 页面 MUST NOT 请求私密 Todo 提醒，也 MUST NOT 展示 Todo 提醒弹窗

#### Scenario: 关闭提醒弹窗
- **WHEN** 登录用户关闭提醒弹窗
- **THEN** 页面 MUST 关闭弹窗，并在本次页面生命周期内不反复弹出同一提醒

