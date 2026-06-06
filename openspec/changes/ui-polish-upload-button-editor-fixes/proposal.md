## Why

当前存在6个用户体验缺陷：

1. BlogEditPage 中"上传图片"按钮只有灰色背景，无可见文字标签，用户不清楚其功能
2. BlogEditPage 复用同一页面处理"写文章"和"编辑文章"，再次点击导航栏"写文章"时不会重置状态
3. 文章详情页只能看渲染后的 Markdown，无法查看原始 Markdown 源码
4. 导航栏右上角只显示用户名，缺少头像，无法快速识别当前登录账号
5. 编辑已发布文章后 `update_time` 变更，导致文章重新置顶到博客列表顶部
6. 所有时间字段使用 SQLite `CURRENT_TIMESTAMP`（UTC），未转换为北京时间显示

## What Changes

### 上传图片按钮显式文字
- 将 BlogEditPage 中 `.file-button` 添加显式按钮文字"上传图片" + tooltip

### 编辑器页面状态重置
- 修复 BlogEditPage：当 URL 参数既无 `articleId` 也无 `draftId` 时，重置表单为初始状态

### 文章详情页 Markdown 源码切换
- BlogDetailPage 添加「显示原始 Markdown」切换按钮，点击后展示未渲染的 Markdown 源码

### 导航栏头像显示
- 导航栏右上角用户区域，在用户名左侧显示用户头像

### 博客列表排序改为按发布时间
- 修改 `listVisibleArticles()` 的 SQL 排序字段：从 `update_time DESC` 改为 `create_time DESC`，使编辑不再改变文章排序位置
- 在文章详情页底部显示发布时间和最后编辑时间

### 时间转换为北京时间
- 后端所有 service 返回的 `create_time` / `update_time` 统一从 UTC 转为北京时间 (UTC+8)
- 博客列表页、详情页、快写列表/详情页的时间均显示为北京时间

## Capabilities

### New Capabilities

- `upload-button-label`: 文章编辑器中上传图片按钮的显式文字标签
- `editor-reset-on-new`: 无参数进入编辑器时重置为空白状态
- `markdown-source-toggle`: 文章详情页 Markdown 渲染/源码切换
- `navbar-avatar`: 导航栏用户头像显示
- `sort-by-create-time`: 博客列表按发布时间排序，编辑不改变排序
- `beijing-timezone`: 全局时间从 UTC 转换为北京时间

## Impact

| 层级 | 文件 | 改动 |
|------|------|------|
| 后端 service | `article_service.py` | `listVisibleArticles()` 排序改为 `create_time DESC`；`formatArticle()` / `formatReadableArticle()` 添加北京时间转换 |
| 后端 service | `quick_post_service.py` | `formatQuickPost()` 添加北京时间转换 |
| 后端 service | `comment_service.py` | comment `create_time` 添加北京时间转换 |
| 前端 | `BlogEditPage.jsx` | 上传按钮添加显式文字；修复无参数时状态重置 |
| 前端 | `BlogDetailPage.jsx` | 添加 Markdown 源码切换按钮；底部显示发布/编辑时间 |
| 前端 | `AppLayout.jsx` | 用户名左侧显示头像 |
| 前端 | `BlogListPage.jsx` | 文章卡片时间显示更新（如有需要） |
| 前端 | `global.css` | 新增少量样式支持（头像、源码区、时间标签） |