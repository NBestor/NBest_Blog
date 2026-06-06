## MODIFIED Requirements

### Requirement: Blog List Sorted by Create Time
博客列表页 SHALL 按文章发布时间（`create_time`）降序排列，而非按最后编辑时间（`update_time`）。编辑已发布文章后，文章 MUST 保持原有排序位置，不会因为编辑操作而重新置顶到列表顶部。

#### Scenario: 新发布文章排在列表顶部
- **WHEN** 用户发布一篇新文章
- **THEN** 该文章出现在博客列表的顶部（最新发布在最前）

#### Scenario: 编辑后文章不置顶
- **WHEN** 用户编辑一篇已发布的旧文章并保存
- **THEN** 该文章在博客列表中的排序位置不变，仍然保持原发布时间的位置

#### Scenario: 草稿列表排序不变
- **WHEN** 用户查看草稿箱
- **THEN** 草稿列表排序不受影响（草稿列表已有自己的排序逻辑）

## ADDED Requirements

### Requirement: Article Detail Page Show Create and Update Time
文章详情页（`BlogDetailPage.jsx`）SHALL 在文章正文底部、互动按钮上方显示发布时间。当 `update_time` 与 `create_time` 不同时，MUST 同时显示最后编辑时间。

#### Scenario: 未编辑过的文章只显示发布时间
- **WHEN** 用户查看一篇从未编辑过的文章详情
- **THEN** 底部显示「发布于 YYYY-MM-DD HH:MM:SS」，不显示编辑时间

#### Scenario: 编辑过的文章显示两个时间
- **WHEN** 用户查看一篇编辑过的文章详情
- **THEN** 底部显示「发布于 YYYY-MM-DD HH:MM:SS」和「最后编辑于 YYYY-MM-DD HH:MM:SS」

#### Scenario: 时间格式为北京时间
- **WHEN** 文章底部显示发布时间和编辑时间
- **THEN** 时间以 `YYYY-MM-DD HH:MM:SS` 格式显示，且为北京时间