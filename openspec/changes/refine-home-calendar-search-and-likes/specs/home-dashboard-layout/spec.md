## ADDED Requirements

### Requirement: 首页日历为页面内小月历
系统 SHALL 在首页内容区右上角展示页面内小月历，并且该小月历不得随页面滚动继续贴在视口上。

#### Scenario: 首页显示当前月小月历
- **WHEN** 已登录用户打开首页
- **THEN** 首页 SHALL 在上方右侧显示当前月小月历
- **AND** 小月历 SHALL 显示当前月日期格

#### Scenario: 日历不随滚动固定
- **WHEN** 用户滚动首页
- **THEN** 小月历 SHALL 作为首页内容自然滚动
- **AND** 小月历 SHALL 不使用随视口保持可见的 fixed 或 sticky 行为

#### Scenario: 有事件日期被圈出
- **WHEN** 当前月某日期存在日历事件
- **THEN** 小月历 SHALL 用明显颜色或圈选样式标记该日期

### Requirement: 小月历事件列表悬浮展开
系统 SHALL 默认只显示小月历，并通过箭头展开本月事件悬浮层。

#### Scenario: 默认收起事件列表
- **WHEN** 用户打开首页
- **THEN** 小月历 SHALL 默认不展示本月事件列表
- **AND** 展开箭头 SHALL 显示为向上状态

#### Scenario: 展开本月事件
- **WHEN** 用户点击小月历箭头
- **THEN** 箭头 SHALL 切换为向下状态
- **AND** 系统 SHALL 以悬浮层展示本月事件列表
- **AND** 该悬浮层 SHALL 不挤压快写、博客或其他首页内容

#### Scenario: 再次点击收起事件
- **WHEN** 用户在事件列表展开后再次点击箭头
- **THEN** 系统 SHALL 收起本月事件悬浮层
- **AND** 箭头 SHALL 恢复向上状态

### Requirement: 本月事件按状态排序
系统 SHALL 在小月历事件悬浮层中将未到达事件按日期先后展示，并将已过去事件置灰放到底部。

#### Scenario: 未到达事件排序
- **WHEN** 本月存在多个今天或未来日期的事件
- **THEN** 事件列表 SHALL 按日期从近到远排序

#### Scenario: 已过去事件置底
- **WHEN** 本月存在早于今天的事件
- **THEN** 这些事件 SHALL 使用灰色弱化样式
- **AND** 这些事件 SHALL 显示在未到达事件之后

### Requirement: 首页上方快写与日历并列
系统 SHALL 在首页上方将快写区域与小月历并列展示，并让快写尽可能占满可用宽度。

#### Scenario: 桌面端上方布局
- **WHEN** 用户在桌面宽度打开首页
- **THEN** 快写区域 SHALL 显示在上方左侧主区域
- **AND** 小月历 SHALL 显示在上方右侧
- **AND** 快写区域 SHALL 尽可能填满左侧可用空间

#### Scenario: 移动端上方布局
- **WHEN** 用户在移动宽度打开首页
- **THEN** 快写区域和小月历 SHALL 纵向排列
- **AND** 页面 SHALL 不出现横向溢出
