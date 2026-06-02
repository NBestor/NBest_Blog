## ADDED Requirements

### Requirement: 顶部导航隐藏首页化入口
系统 SHALL 从顶部常驻导航中隐藏博客、待办和日历入口，但保留对应页面和路由保护。

#### Scenario: 顶部导航不显示博客待办日历
- **WHEN** 用户查看顶部导航
- **THEN** 导航 SHALL 不显示博客入口
- **AND** 导航 SHALL 不显示待办入口
- **AND** 导航 SHALL 不显示日历入口

#### Scenario: 首页仍提供博客待办日历入口
- **WHEN** 用户打开首页
- **THEN** 首页 SHALL 提供博客内容入口
- **AND** 首页 SHALL 为已登录用户提供待办入口
- **AND** 首页 SHALL 为已登录用户提供日历入口

#### Scenario: 私有路由仍受保护
- **WHEN** 未登录用户直接访问待办或日历路由
- **THEN** 系统 SHALL 继续要求登录
- **AND** 系统 SHALL 不展示私有数据

### Requirement: 顶部导航保留身份状态入口
系统 SHALL 在隐藏首页化入口后继续根据用户状态显示登录、注册、个人和管理相关入口。

#### Scenario: 游客导航
- **WHEN** 未登录用户查看顶部导航
- **THEN** 导航 SHALL 显示登录或注册入口
- **AND** 导航 SHALL 不显示私有用户入口

#### Scenario: 管理员导航
- **WHEN** 管理员用户查看顶部导航
- **THEN** 导航 SHALL 显示管理入口
- **AND** 导航 SHALL 显示当前用户身份状态
