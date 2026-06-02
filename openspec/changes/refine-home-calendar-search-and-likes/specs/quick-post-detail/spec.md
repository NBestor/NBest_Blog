## ADDED Requirements

### Requirement: 快写点赞显示为爱心状态
系统 SHALL 使用空心爱心和红色实心爱心展示快写点赞状态。

#### Scenario: 快写未点赞
- **WHEN** 当前用户未点赞某条快写
- **THEN** 快写点赞按钮 SHALL 显示空心爱心
- **AND** 按钮 SHALL 保留点赞数量

#### Scenario: 快写已点赞
- **WHEN** 当前用户已点赞某条快写
- **THEN** 快写点赞按钮 SHALL 显示红色实心爱心
- **AND** 按钮 SHALL 保留点赞数量

#### Scenario: 切换快写点赞
- **WHEN** 已登录用户点击快写爱心按钮
- **THEN** 系统 SHALL 切换点赞状态
- **AND** 爱心视觉状态 SHALL 随接口结果更新

### Requirement: 博客点赞显示为爱心状态
系统 SHALL 使用空心爱心和红色实心爱心展示博客点赞状态。

#### Scenario: 博客未点赞
- **WHEN** 当前用户未点赞某篇博客
- **THEN** 博客点赞按钮 SHALL 显示空心爱心
- **AND** 按钮 SHALL 保留点赞数量

#### Scenario: 博客已点赞
- **WHEN** 当前用户已点赞某篇博客
- **THEN** 博客点赞按钮 SHALL 显示红色实心爱心
- **AND** 按钮 SHALL 保留点赞数量
