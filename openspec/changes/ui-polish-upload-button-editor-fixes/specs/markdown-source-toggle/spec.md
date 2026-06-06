## ADDED Requirements

### Requirement: Markdown Source Toggle on Article Detail Page
文章详情页（`BlogDetailPage.jsx`）SHALL 在渲染后的 Markdown 内容上方提供一个「📄 显示原始 Markdown」切换按钮。点击按钮 MUST 在渲染视图和原始 Markdown 源码之间切换。按钮文案 SHALL 根据当前状态变化：显示源码时为「📄 显示渲染效果」，显示渲染时为「📄 显示原始 Markdown」。

#### Scenario: 默认显示渲染视图
- **WHEN** 用户打开任意文章详情页
- **THEN** 文章正文通过 `@bytemd/react` 的 `<Viewer>` 组件渲染显示，按钮文案为「📄 显示原始 Markdown」

#### Scenario: 点击切换到源码视图
- **WHEN** 用户点击「📄 显示原始 Markdown」按钮
- **THEN** `<Viewer>` 内容区域替换为 `<pre className="markdown-source">` 显示原始 Markdown 源码，按钮文案变为「📄 显示渲染效果」

#### Scenario: 点击切换回渲染视图
- **WHEN** 当前显示源码视图，用户点击「📄 显示渲染效果」按钮
- **THEN** `<pre>` 内容区域替换回 `<Viewer>` 渲染视图，按钮文案变为「📄 显示原始 Markdown」

#### Scenario: 源码保留格式
- **WHEN** 文章包含多级标题、代码块、表格等 Markdown 语法
- **THEN** 切换到源码视图时，所有原始 Markdown 标记、换行和缩进完整保留显示

#### Scenario: 切换不影响其他交互
- **WHEN** 用户在源码视图和渲染视图之间切换
- **THEN** 评论、点赞、收藏等功能正常工作不受影响