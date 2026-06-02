## ADDED Requirements

### Requirement: 顶部导航提供可展开搜索入口
系统 SHALL 在顶部导航中提供一个放大镜搜索入口，并在用户悬停、聚焦或移动端点击时展开为可输入的搜索框。

#### Scenario: 桌面端展开搜索框
- **WHEN** 用户在桌面端将鼠标悬停到搜索入口或聚焦搜索控件
- **THEN** 搜索入口 SHALL 从放大镜按钮展开为文本输入框
- **AND** 用户 SHALL 能输入搜索关键词

#### Scenario: 移动端展开搜索框
- **WHEN** 用户在移动端点击搜索入口
- **THEN** 搜索入口 SHALL 展开为文本输入框
- **AND** 搜索框 SHALL 不遮挡主要导航操作

#### Scenario: 提交搜索
- **WHEN** 用户输入非空关键词并提交搜索
- **THEN** 系统 SHALL 跳转到搜索结果页
- **AND** 搜索结果页 SHALL 使用该关键词加载结果

### Requirement: 搜索范围限定为博客和快记
系统 SHALL 只搜索博客和当前用户可访问的快记，不搜索待办或日历。

#### Scenario: 游客搜索
- **WHEN** 未登录用户提交搜索
- **THEN** 系统 SHALL 返回可见博客结果
- **AND** 系统 SHALL 不返回快记结果
- **AND** 系统 SHALL 不返回待办或日历结果

#### Scenario: 登录用户搜索
- **WHEN** 已登录用户提交搜索
- **THEN** 系统 SHALL 返回该用户可见的博客结果
- **AND** 系统 SHALL 返回该用户自己的快记结果
- **AND** 系统 SHALL 不返回待办或日历结果

### Requirement: 博客搜索匹配标题标签分类和简介
系统 SHALL 使用博客标题、标签、tag、分类和简介内容匹配搜索关键词。

#### Scenario: 标题命中博客
- **WHEN** 搜索关键词出现在博客标题中
- **THEN** 搜索结果 SHALL 在博客结果区显示该博客

#### Scenario: 标签命中博客
- **WHEN** 搜索关键词出现在博客标签或 tag 中
- **THEN** 搜索结果 SHALL 在博客结果区显示该博客

#### Scenario: 分类命中博客
- **WHEN** 搜索关键词出现在博客分类名称中
- **THEN** 搜索结果 SHALL 在博客结果区显示该博客

#### Scenario: 简介命中博客
- **WHEN** 搜索关键词出现在博客手写简介或自动生成简介中
- **THEN** 搜索结果 SHALL 在博客结果区显示该博客

### Requirement: 快记搜索只匹配当前用户快记正文
系统 SHALL 仅在用户登录后搜索当前用户自己的快记正文内容。

#### Scenario: 当前用户快记命中
- **WHEN** 已登录用户搜索的关键词出现在自己的快记正文中
- **THEN** 搜索结果 SHALL 在快记结果区显示该快记

#### Scenario: 其他用户快记不返回
- **WHEN** 搜索关键词只出现在其他用户的快记正文中
- **THEN** 搜索结果 SHALL 不显示其他用户的快记

### Requirement: 搜索结果分区展示
搜索结果页 SHALL 将博客结果和快记结果分区展示，并保持各自的进入方式。

#### Scenario: 同时存在博客和快记结果
- **WHEN** 搜索关键词同时命中博客和快记
- **THEN** 页面 SHALL 显示博客结果区
- **AND** 页面 SHALL 显示快记结果区
- **AND** 两类结果 SHALL 不混排

#### Scenario: 点击博客结果
- **WHEN** 用户点击博客搜索结果主体区域
- **THEN** 系统 SHALL 导航到对应博客详情页

#### Scenario: 点击快记结果
- **WHEN** 用户点击快记搜索结果主体区域
- **THEN** 系统 SHALL 导航到快记页
- **AND** 系统 SHOULD 尽可能定位到对应快记内容
