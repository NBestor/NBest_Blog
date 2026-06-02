## ADDED Requirements

### Requirement: Photo visibility filtering
系统 SHALL 根据当前访问者身份返回其可见的照片列表。

#### Scenario: Guest sees public photos only
- **WHEN** 游客访问照片墙或请求照片列表
- **THEN** 系统 MUST 只返回 `visible_type` 为 `public` 的照片

#### Scenario: Owner sees own private photos
- **WHEN** 登录用户访问照片墙或请求照片列表
- **THEN** 系统 MUST 返回公开照片以及该用户自己的 `self` 照片

#### Scenario: Non-owner cannot see private photo
- **WHEN** 登录用户请求照片列表且列表中存在其他用户的 `self` 照片
- **THEN** 系统 MUST NOT 返回该私密照片

### Requirement: Photo upload and collection
系统 SHALL 允许登录用户上传个人照片，并将头像和文章插图归集为照片墙记录。

#### Scenario: Logged-in user uploads photo
- **WHEN** 登录用户上传合法的 jpg、png 或 webp 图片并选择可见范围
- **THEN** 系统 MUST 保存图片文件，创建照片记录，并在该用户可见的照片列表中返回该照片

#### Scenario: Guest cannot upload photo
- **WHEN** 游客请求上传照片
- **THEN** 系统 MUST 拒绝请求

#### Scenario: Invalid image is rejected
- **WHEN** 登录用户上传非支持类型或无法识别的图片文件
- **THEN** 系统 MUST 拒绝创建照片记录

#### Scenario: Avatar and article images are collected
- **WHEN** 登录用户上传头像或 Markdown 文章插图
- **THEN** 系统 MUST 创建对应来源类型的照片记录用于照片墙展示

### Requirement: Photo preview and link copy
系统 SHALL 支持用户预览单张可见照片并复制图片链接。

#### Scenario: User previews photo
- **WHEN** 用户在照片墙点击一张可见照片
- **THEN** 系统 MUST 展示该照片的大图预览

#### Scenario: User copies photo link
- **WHEN** 用户在照片预览或照片操作区点击复制链接
- **THEN** 系统 MUST 提供该照片的可访问图片链接

#### Scenario: Clipboard copy fails
- **WHEN** 浏览器不允许写入剪贴板
- **THEN** 系统 MUST 显示可手动复制的图片链接或失败提示

### Requirement: Photo visibility management
系统 SHALL 允许照片拥有者或管理员修改照片公开状态。

#### Scenario: Owner changes visibility
- **WHEN** 照片拥有者将照片可见范围改为 `public` 或 `self`
- **THEN** 系统 MUST 保存新的可见范围并在后续列表中按新权限返回

#### Scenario: Non-owner cannot change visibility
- **WHEN** 非拥有者尝试修改其他用户照片的可见范围
- **THEN** 系统 MUST 拒绝修改并保持照片原可见范围

#### Scenario: Admin can manage visibility
- **WHEN** 管理员修改任意照片的可见范围
- **THEN** 系统 MUST 保存新的可见范围

### Requirement: Photo deletion
系统 SHALL 允许照片拥有者或管理员删除照片记录，并清理本地图片文件。

#### Scenario: Owner deletes photo
- **WHEN** 照片拥有者删除自己的照片
- **THEN** 系统 MUST 删除照片记录，后续列表不再返回该照片

#### Scenario: Local uploaded file is removed
- **WHEN** 被删除照片的链接指向本地 `/static/uploads/` 文件
- **THEN** 系统 MUST 删除对应本地文件

#### Scenario: Non-owner cannot delete photo
- **WHEN** 非拥有者尝试删除其他用户照片
- **THEN** 系统 MUST 拒绝删除并保持照片记录存在

#### Scenario: Admin can delete photo
- **WHEN** 管理员删除任意照片
- **THEN** 系统 MUST 删除照片记录，后续列表不再返回该照片

### Requirement: Photo wall UI states
系统 SHALL 根据用户状态展示照片墙操作入口。

#### Scenario: Guest sees browse-only wall
- **WHEN** 游客访问照片墙页面
- **THEN** 页面 MUST 显示公开照片，并且 MUST NOT 显示上传、删除或可见性修改入口

#### Scenario: Logged-in user sees management tools
- **WHEN** 登录用户访问照片墙页面
- **THEN** 页面 MUST 显示上传入口，并对该用户可管理的照片显示删除、复制链接和可见性修改入口

#### Scenario: Empty state
- **WHEN** 当前访问者没有任何可见照片
- **THEN** 页面 MUST 显示空状态提示
