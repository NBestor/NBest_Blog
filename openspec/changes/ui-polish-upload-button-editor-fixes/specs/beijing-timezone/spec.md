## ADDED Requirements

### Requirement: All Time Fields Converted to Beijing Time
系统 SHALL 在所有后端 API 响应中将 `create_time` 和 `update_time` 字段从 UTC 时间转换为北京时间 (UTC+8)。转换 MUST 在 service 层的格式化函数中统一完成，所有返回给前端的 `YYYY-MM-DD HH:MM:SS` 格式字符串 SHALL 表示北京时间。

#### Scenario: 文章列表时间显示为北京时间
- **WHEN** 用户浏览博客文章列表
- **THEN** 所有文章的 `create_time` 字段值为北京时间（比 UTC 快 8 小时）

#### Scenario: 文章详情时间显示为北京时间
- **WHEN** 用户查看文章详情
- **THEN** 文章的 `create_time` 和 `update_time` 均为北京时间

#### Scenario: 快写列表时间显示为北京时间
- **WHEN** 用户浏览首页快写列表
- **THEN** 所有快写的 `create_time` 和 `update_time` 均为北京时间

#### Scenario: 评论时间显示为北京时间
- **WHEN** 用户查看文章或快写的评论
- **THEN** 所有评论的 `create_time` 为北京时间

#### Scenario: 编辑后 update_time 更新为当前北京时间
- **WHEN** 用户编辑文章或快写后保存
- **THEN** 返回的 `update_time` 为当前北京时间，由后端 `CURRENT_TIMESTAMP` 写入后经转换得到

### Requirement: Beijing Time Conversion Utility
后端 SHALL 提供一个统一的北京时间转换函数 `toBeijingTime(utcStr: str) -> str`，集中处理 UTC → UTC+8 转换逻辑，供所有 service 格式化函数复用。

#### Scenario: UTC 时间正确转换
- **WHEN** 输入 `"2026-06-02 06:00:00"` (UTC)
- **THEN** 输出 `"2026-06-02 14:00:00"` (北京时间)

#### Scenario: 空值安全处理
- **WHEN** 输入 `None` 或空字符串
- **THEN** 返回原值不变，不抛出异常