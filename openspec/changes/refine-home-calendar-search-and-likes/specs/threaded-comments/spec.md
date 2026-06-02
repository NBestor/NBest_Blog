## ADDED Requirements

### Requirement: 评论点赞显示为爱心状态
系统 SHALL 使用空心爱心和红色实心爱心展示评论点赞状态。

#### Scenario: 评论未点赞
- **WHEN** 当前用户未点赞某条评论
- **THEN** 评论点赞按钮 SHALL 显示空心爱心
- **AND** 按钮 SHALL 保留点赞数量

#### Scenario: 评论已点赞
- **WHEN** 当前用户已点赞某条评论
- **THEN** 评论点赞按钮 SHALL 显示红色实心爱心
- **AND** 按钮 SHALL 保留点赞数量

#### Scenario: 切换评论点赞
- **WHEN** 已登录用户点击评论爱心按钮
- **THEN** 系统 SHALL 切换点赞状态
- **AND** 爱心视觉状态 SHALL 随接口结果更新
