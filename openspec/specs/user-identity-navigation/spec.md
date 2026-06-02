# user-identity-navigation Specification

## Purpose
TBD - created by archiving change align-user-identity-and-nav-visibility. Update Purpose after archive.
## Requirements
### Requirement: 单名称注册
系统 SHALL 在注册界面只要求用户输入一个账号名称，并使用该名称完成账号创建和后续登录识别。

#### Scenario: 使用单一名称注册
- **WHEN** 访客在注册页输入账号名称、密码和确认密码并提交
- **THEN** 系统创建用户，并让该用户的登录标识和展示名称保持一致

#### Scenario: 兼容旧注册请求
- **WHEN** 客户端提交包含 `username` 和 `nickname` 的旧注册请求
- **THEN** 系统 MUST 继续接受该请求，并按兼容逻辑创建用户

### Requirement: 合并身份展示
系统 SHALL 将用户主要身份展示为一个用户名称，避免在同一展示区域重复显示完全相同的用户名和昵称。

#### Scenario: 新用户查看个人信息
- **WHEN** 新注册用户打开个人中心
- **THEN** 页面只突出显示一个用户名称，不重复展示相同的用户名和昵称

#### Scenario: 查看用户关系列表
- **WHEN** 登录用户查看关注、粉丝或好友列表
- **THEN** 每个用户条目 MUST 以合并后的用户名称作为主要标签

### Requirement: 导航按用户状态展示
系统 SHALL 根据当前用户状态展示顶部导航入口，只显示当前用户可直接使用的功能入口。

#### Scenario: 游客查看导航
- **WHEN** 未登录访客打开任意公开页面
- **THEN** 导航 MUST 显示公开浏览入口和登录/注册入口
- **THEN** 导航 MUST NOT 显示快记、草稿、写文章、个人中心、设置、关注管理等登录后功能入口

#### Scenario: 登录用户查看导航
- **WHEN** 已登录用户打开应用
- **THEN** 导航 MUST 显示该用户可使用的个人功能入口，包括快记、草稿、写文章、个人中心、设置和关注管理
- **THEN** 导航 MUST NOT 显示登录和注册入口

### Requirement: 私有路由保持保护
系统 SHALL 保留私有页面的直接访问保护，导航隐藏不能作为权限控制的唯一手段。

#### Scenario: 游客手动访问快记
- **WHEN** 未登录访客直接访问 `/quick/note`
- **THEN** 系统 MUST 阻止进入快记页面，并引导访客登录

#### Scenario: 登录用户访问快记
- **WHEN** 已登录用户访问 `/quick/note`
- **THEN** 系统 MUST 正常展示该用户自己的快记页面

