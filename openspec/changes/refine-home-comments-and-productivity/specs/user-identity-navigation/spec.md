## ADDED Requirements

### Requirement: 首页私有辅助入口按用户状态展示
系统 SHALL 根据用户登录状态展示首页中的 Todo 与日历辅助入口，并继续保护私有路由。

#### Scenario: 未登录用户访问首页
- **WHEN** 未登录用户打开首页
- **THEN** 首页 SHALL 不展示 Todo 引导与日历摘要中的私有内容
- **AND** 导航栏 SHALL 不显示仅登录用户可用的私有入口

#### Scenario: 已登录用户访问首页
- **WHEN** 已登录用户打开首页
- **THEN** 首页 SHALL 展示该用户可用的 Todo 引导与日历摘要
- **AND** 导航栏 SHALL 只显示该用户当前状态可用的入口

#### Scenario: 直接访问私有路由
- **WHEN** 未登录用户直接打开 Todo、日历或其他私有路由
- **THEN** 系统 SHALL 保持路由保护
- **AND** 前端 SHALL 引导用户登录
