## ADDED Requirements

### Requirement: Editor Reset on New Article
文章编辑器（`BlogEditPage.jsx`）SHALL 在 URL 参数中既无 `draftId` 也无 `articleId` 时，将表单重置为空白新建状态。当用户从导航栏点击「写文章」或直接访问 `/blog/edit` 时，编辑器 MUST 显示初始内容（`"# 新草稿\n\n开始写点什么吧。"`），表单字段 SHALL 全部清空为默认值。

#### Scenario: 从已编辑状态切换回新建
- **WHEN** 用户先编辑 `/blog/edit?articleId=5`，再从导航栏点击「写文章」（`/blog/edit` 无参数）
- **THEN** 编辑器表单重置为初始状态：标题为空、简介为空、内容为 `"# 新草稿\n\n开始写点什么吧。"`、分类为无、可见范围为仅自己可见、标签为空

#### Scenario: 从草稿编辑切换回新建
- **WHEN** 用户先编辑 `/blog/edit?draftId=3`，再从导航栏点击「写文章」无参数
- **THEN** 编辑器表单重置为初始空白状态

#### Scenario: 直接访问 /blog/edit 新建
- **WHEN** 用户从导航栏点击「写文章」或访问 `/blog/edit`
- **THEN** 编辑器显示空白新建状态，`isLoading` 为 `false`

#### Scenario: 有 draftId 时不重置
- **WHEN** 用户访问 `/blog/edit?draftId=3`
- **THEN** 编辑器正常加载对应草稿，不触发重置

#### Scenario: 有 articleId 时不重置
- **WHEN** 用户访问 `/blog/edit?articleId=5`
- **THEN** 编辑器正常加载对应已发布文章，不触发重置