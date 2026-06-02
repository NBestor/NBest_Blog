## MODIFIED Requirements

### Requirement: 导航按用户状态展示
系统 SHALL 根据当前用户登录状态和角色展示顶部导航入口，只显示当前用户可直接使用的功能入口。

#### Scenario: 游客查看导航
- **WHEN** 未登录访客打开任意公开页面
- **THEN** 导航 MUST 显示公开浏览入口和登录/注册入口
- **THEN** 导航 MUST NOT 显示快记、草稿、写文章、个人中心、设置、关注管理、管理等登录后或管理员功能入口

#### Scenario: 普通登录用户查看导航
- **WHEN** 已登录普通用户打开应用
- **THEN** 导航 MUST 显示该用户可使用的个人功能入口，包括快记、草稿、写文章、个人中心、设置和关注管理
- **THEN** 导航 MUST NOT 显示登录和注册入口
- **THEN** 导航 MUST NOT 显示管理入口或任何管理员管理 UI

#### Scenario: 管理员查看导航
- **WHEN** 已登录管理员打开应用
- **THEN** 导航 MUST 显示该用户可使用的个人功能入口
- **THEN** 导航 MUST 显示管理入口
- **THEN** 导航 MUST NOT 显示登录和注册入口

#### Scenario: 主管查看导航
- **WHEN** 已登录主管打开应用
- **THEN** 导航 MUST 显示该用户可使用的个人功能入口
- **THEN** 导航 MUST 显示管理入口
- **THEN** 导航 MUST NOT 显示登录和注册入口
