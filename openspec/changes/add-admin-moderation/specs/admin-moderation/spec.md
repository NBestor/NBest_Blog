## ADDED Requirements

### Requirement: 主管账号初始化
系统 SHALL 在数据库初始化后保证存在固定主管账号，账号 ID 为 `0`，账号名为 `NBest`，角色为 `admin`，初始密码为 `NBest666`。

#### Scenario: 首次初始化主管账号
- **WHEN** 系统启动并初始化数据库，且不存在 ID 为 `0` 的用户
- **THEN** 系统 MUST 创建 ID 为 `0`、账号名为 `NBest`、角色为 `admin` 的主管账号
- **THEN** 主管账号 MUST 可以使用密码 `NBest666` 登录

#### Scenario: 已存在主管账号
- **WHEN** 系统启动并初始化数据库，且 ID 为 `0` 的用户已存在
- **THEN** 系统 MUST 确保该用户账号名为 `NBest` 且角色为 `admin`
- **THEN** 系统 MUST NOT 在每次启动时强制覆盖该账号当前密码

### Requirement: 管理员 API 访问控制
系统 SHALL 为所有管理员 API 提供后端权限校验，只有已登录管理员可以访问普通管理员能力，只有主管可以访问管理员任命和管理员管理能力。

#### Scenario: 游客访问管理员 API
- **WHEN** 未登录访客请求任意 `/api/admin/*` 接口
- **THEN** 系统 MUST 拒绝请求

#### Scenario: 普通用户访问管理员 API
- **WHEN** 普通登录用户请求任意 `/api/admin/*` 接口
- **THEN** 系统 MUST 拒绝请求

#### Scenario: 普通管理员访问普通管理员 API
- **WHEN** 普通管理员请求用户列表、内容列表或内容删除类管理员接口
- **THEN** 系统 MUST 允许该请求按管理员规则执行

#### Scenario: 普通管理员访问主管 API
- **WHEN** 普通管理员请求任命管理员、撤销管理员或管理管理员账号的接口
- **THEN** 系统 MUST 拒绝请求

#### Scenario: 主管访问主管 API
- **WHEN** `NBest` 主管请求任命管理员、撤销管理员或管理管理员账号的接口
- **THEN** 系统 MUST 允许该请求按主管规则执行

### Requirement: 管理员概览
系统 SHALL 提供管理员概览能力，用于管理员查看用户、文章、快写、评论和照片等治理对象的汇总状态。

#### Scenario: 管理员查看概览
- **WHEN** 管理员打开管理页面或请求管理员概览接口
- **THEN** 系统 MUST 返回可治理资源的汇总数量和基础状态

#### Scenario: 普通用户无法查看概览
- **WHEN** 普通用户打开管理页面或请求管理员概览接口
- **THEN** 系统 MUST 阻止其查看管理员概览数据

### Requirement: 用户治理
系统 SHALL 允许管理员查看用户列表，并按权限处理普通用户的违规资料。

#### Scenario: 管理员查看用户列表
- **WHEN** 管理员请求用户管理列表
- **THEN** 系统 MUST 返回用户 ID、账号名、展示名、角色、头像状态、注册时间和是否可管理

#### Scenario: 管理员删除普通用户
- **WHEN** 管理员删除普通用户
- **THEN** 系统 MUST 删除该用户及其关联内容
- **THEN** 后续普通列表和详情接口 MUST NOT 返回该用户已删除的内容

#### Scenario: 普通管理员删除管理员
- **WHEN** 普通管理员尝试删除主管、自己或其他管理员
- **THEN** 系统 MUST 拒绝该请求

#### Scenario: 主管删除管理员
- **WHEN** 主管尝试删除普通管理员
- **THEN** 系统 MUST 按主管规则允许该请求

#### Scenario: 主管删除自己
- **WHEN** 主管尝试删除 ID 为 `0` 的主管账号
- **THEN** 系统 MUST 拒绝该请求

#### Scenario: 管理员强制重命名用户
- **WHEN** 管理员对可管理用户执行强制重命名
- **THEN** 系统 MUST 将目标用户的账号名或展示名更新为合规占位名称
- **THEN** 目标用户后续页面展示 MUST 使用更新后的名称

#### Scenario: 管理员移除违规头像
- **WHEN** 管理员对可管理用户执行移除头像操作
- **THEN** 系统 MUST 清空目标用户头像，使其回到默认头像状态

### Requirement: 管理员任命
系统 SHALL 允许主管任命普通用户为管理员，并允许主管撤销普通管理员身份。

#### Scenario: 主管任命管理员
- **WHEN** 主管将普通用户设置为管理员
- **THEN** 系统 MUST 将目标用户角色更新为 `admin`
- **THEN** 目标用户下次获取当前用户信息时 MUST 体现管理员身份

#### Scenario: 主管撤销管理员
- **WHEN** 主管将普通管理员撤销为普通用户
- **THEN** 系统 MUST 将目标用户角色更新为 `user`
- **THEN** 目标用户 MUST 不再拥有管理员 API 权限

#### Scenario: 主管降级自己
- **WHEN** 主管尝试撤销 ID 为 `0` 的主管账号管理员身份
- **THEN** 系统 MUST 拒绝该请求

#### Scenario: 普通管理员任命管理员
- **WHEN** 普通管理员尝试任命或撤销管理员
- **THEN** 系统 MUST 拒绝该请求

### Requirement: 内容治理
系统 SHALL 允许管理员删除违规博客文章、快写、评论和照片。

#### Scenario: 管理员删除博客文章
- **WHEN** 管理员删除一篇博客文章
- **THEN** 系统 MUST 删除该文章
- **THEN** 普通文章列表和文章详情 MUST NOT 再返回该文章

#### Scenario: 管理员删除快写
- **WHEN** 管理员删除一条快写
- **THEN** 系统 MUST 删除该快写
- **THEN** 普通首页动态流 MUST NOT 再返回该快写

#### Scenario: 管理员删除评论
- **WHEN** 管理员删除一条评论
- **THEN** 系统 MUST 删除该评论
- **THEN** 对应文章或快写评论列表 MUST NOT 再返回该评论

#### Scenario: 管理员删除照片
- **WHEN** 管理员删除一张照片
- **THEN** 系统 MUST 删除该照片记录
- **THEN** 照片墙列表 MUST NOT 再返回该照片

### Requirement: 管理前端页面
系统 SHALL 提供管理员专用管理页面，并按身份显示普通管理员能力和主管能力。

#### Scenario: 管理员打开管理页面
- **WHEN** 管理员打开 `/admin`
- **THEN** 系统 MUST 显示管理页面
- **THEN** 页面 MUST 提供用户、文章、快写、评论和照片治理入口

#### Scenario: 主管打开管理页面
- **WHEN** 主管打开 `/admin`
- **THEN** 系统 MUST 显示管理页面
- **THEN** 页面 MUST 额外显示管理员任命和管理员管理入口

#### Scenario: 普通用户打开管理页面
- **WHEN** 普通登录用户直接访问 `/admin`
- **THEN** 系统 MUST 阻止其进入管理页面
- **THEN** 系统 MUST NOT 显示管理员管理按钮或数据

#### Scenario: 游客打开管理页面
- **WHEN** 未登录访客直接访问 `/admin`
- **THEN** 系统 MUST 引导其登录或拒绝访问

#### Scenario: 管理员执行危险操作
- **WHEN** 管理员点击删除用户、删除文章、删除快写、删除评论或删除照片
- **THEN** 前端 MUST 在提交请求前显示明确的二次确认

