## ADDED Requirements

### Requirement: 首页展示博客与快写组合内容
系统 SHALL 在首页同时展示博客与快写内容，并在桌面端形成博客为主、快写为辅的布局。

#### Scenario: 桌面端首页布局
- **WHEN** 用户在桌面宽度打开首页
- **THEN** 首页内容区左侧约四分之三 SHALL 展示博客列表
- **AND** 首页内容区右侧约四分之一 SHALL 展示快写列表
- **AND** 两个区域 SHALL 同屏可见且互不遮挡

#### Scenario: 移动端首页布局
- **WHEN** 用户在移动宽度打开首页
- **THEN** 博客列表与快写列表 SHALL 纵向排列
- **AND** 页面内容 SHALL 不出现横向溢出

#### Scenario: 点击博客词条进入详情
- **WHEN** 用户点击博客词条的任意主要内容区域
- **THEN** 系统 SHALL 导航到对应博客详情页
- **AND** 词条内部的明确操作按钮 SHALL 保持各自原有操作

#### Scenario: 点击快写词条进入详情
- **WHEN** 用户点击快写词条的任意主要内容区域
- **THEN** 系统 SHALL 导航到对应快写详情页
- **AND** 词条内部的明确操作按钮 SHALL 保持各自原有操作

### Requirement: 博客词条展示摘要信息
系统 SHALL 在博客列表词条中展示标题、标签、分类和简短简介。

#### Scenario: 使用手写简介
- **WHEN** 博客存在作者填写的简介
- **THEN** 博客词条 SHALL 展示该简介
- **AND** 简介 SHALL 被限制在系统定义的短文本长度内

#### Scenario: 自动生成简介
- **WHEN** 博客没有作者填写的简介
- **THEN** 系统 SHALL 从正文开头生成简介
- **AND** 自动简介 SHALL 去除明显的 Markdown 标记并限制长度

#### Scenario: 编辑博客简介
- **WHEN** 作者创建或编辑博客
- **THEN** 编辑表单 SHALL 提供简介输入项
- **AND** 前端 SHALL 显示简介字数限制与当前字数反馈

### Requirement: 首页展示 Todo 引导
系统 SHALL 在首页左侧提供可折叠的 Todo 引导入口，用于展示当前用户的待办摘要。

#### Scenario: 登录用户默认展开 Todo 引导
- **WHEN** 已登录用户打开首页
- **THEN** Todo 引导 SHALL 默认展开
- **AND** 其中 SHALL 展示该用户可见的待办摘要

#### Scenario: 用户折叠 Todo 引导
- **WHEN** 用户点击 Todo 引导的收起入口
- **THEN** Todo 引导 SHALL 收起为左侧小标识
- **AND** 用户再次点击该标识后 SHALL 重新展开

#### Scenario: 未登录用户不可见私有 Todo
- **WHEN** 未登录用户打开首页
- **THEN** 首页 SHALL 不展示任何私有 Todo 内容
- **AND** 前端 SHALL 不主动请求需要登录的 Todo 数据

### Requirement: 首页展示日历固定入口
系统 SHALL 在首页右上角展示日历摘要入口，并允许用户进入日历详情。

#### Scenario: 桌面端日历入口固定
- **WHEN** 已登录用户在桌面宽度打开首页并滚动页面
- **THEN** 日历摘要入口 SHALL 固定在页面右上角附近
- **AND** 该入口 SHALL 不随主要内容滚动离开视口

#### Scenario: 点击日历入口进入详情
- **WHEN** 用户点击日历摘要入口
- **THEN** 系统 SHALL 导航到日历详情页

#### Scenario: 移动端日历入口不遮挡内容
- **WHEN** 已登录用户在移动宽度打开首页
- **THEN** 日历摘要入口 SHALL 作为普通页面区块展示
- **AND** 该入口 SHALL 不遮挡博客、快写或 Todo 内容

#### Scenario: 未登录用户不可见私有日历
- **WHEN** 未登录用户打开首页
- **THEN** 首页 SHALL 不展示任何私有日历内容
- **AND** 前端 SHALL 不主动请求需要登录的日历数据
