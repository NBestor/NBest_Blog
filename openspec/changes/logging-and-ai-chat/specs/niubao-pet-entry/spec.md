## ADDED Requirements

### Requirement: NiuBao Pet Entry on Homepage
主页（`HomePage.jsx`）左下角 SHALL 添加固定悬浮的牛宝电子宠物入口按钮。

#### Scenario: 按钮位置与样式
- **WHEN** 用户（已登录）访问首页
- **THEN** 页面左下角显示一个固定定位的圆形按钮
- **AND** 按钮位置：`position: fixed; bottom: 20px; left: 20px; z-index: 100`
- **AND** 按钮尺寸：约 60px × 60px
- **AND** 按钮有阴影效果和 hover 缩放动画

#### Scenario: 占位符显示
- **WHEN** 电子宠物形象图片尚未设计好
- **THEN** 按钮显示 🐮 emoji 作为占位符
- **AND** 预留 `<img>` 标签，当图片就绪时直接替换 src 即可

#### Scenario: 点击跳转
- **WHEN** 用户点击电子宠物按钮
- **THEN** 跳转到 `/niubao` 对话页面

#### Scenario: 游客不显示
- **WHEN** 用户未登录
- **THEN** 电子宠物按钮不显示
- **AND** 游客无法访问 `/niubao`（由 ProtectedRoute 保护）