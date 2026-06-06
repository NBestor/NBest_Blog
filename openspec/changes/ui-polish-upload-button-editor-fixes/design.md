## Context

当前项目的前端页面存在6个用户体验缺陷，其中4个纯前端改动、2个涉及后端：

1. **BlogEditPage** — 文件上传按钮无显式文字标签
2. **BlogEditPage** — 从编辑模式切回"写文章"时不重置状态
3. **BlogDetailPage** — 无法查看原始 Markdown 源码
4. **AppLayout** — 导航栏无头像显示
5. **博客列表** — 编辑后文章重新置顶（`ORDER BY update_time DESC` 问题）
6. **时间显示** — SQLite `CURRENT_TIMESTAMP` 为 UTC，未转北京时间

## Goals / Non-Goals

**Goals:**
- 上传图片按钮添加显式可见文字标签"上传图片"
- 编辑器在无 `draftId` / `articleId` 参数时重置为空白新建状态
- 文章详情页添加 Markdown 渲染/源码切换按钮
- 导航栏用户区域在用户名左侧显示头像
- 博客列表按 `create_time DESC` 排序，编辑不改变排序
- 全局 `create_time` / `update_time` 转换为北京时间 (UTC+8)
- 文章详情页底部显示发布时间和最后编辑时间

**Non-Goals:**
- 不修改 API 接口定义
- 不修改编辑器核心逻辑
- 不新增路由
- 不添加头像上传功能（已有头像上传在 ProfilePage）

## Decisions

### 1. 上传图片按钮：label 内嵌文字

**选择**：在 `<label className="file-button">` 内保留文字"上传图片" + `title` tooltip，input 保持 `display: none`。

**理由**：
- 文字"上传图片"就是按钮的可见标签，`.file-button` 样式已定义按钮外观
- `<input>` 内嵌在 `<label>` 中，点击 label 任意位置即可触发文件选择
- 结构不变，只加文字，改动最小

### 2. 编辑器状态重置

**选择**：在 BlogEditPage 的 `useEffect` 中，当 `draftId` 和 `articleId` 均为 `null` 时，直接重置 `formData` 为初始状态。

```javascript
useEffect(() => {
  if (!draftId && !articleId) {
    setFormData({ title: '', summary: '', content: '# 新草稿\n\n开始写点什么吧。', ... });
    setCurrentDraftId(null);
    setSearchParams({});
    setIsLoading(false);
  }
}, [draftId, articleId]);
```

**理由**：组件不卸载时 URL 参数变化，用 `useEffect` 检测重置。

### 3. Markdown 源码切换

**选择**：在 BlogDetailPage 的 `article-body` 上方添加一个 `secondary-button`，切换 `showSource` 状态。

```jsx
{showSource ? (
  <pre className="markdown-source">{article.content}</pre>
) : (
  <div className="markdown-body article-body">
    <Viewer plugins={plugins} value={article.content} />
  </div>
)}
```

### 4. 导航栏头像

**选择**：在 `AppLayout.jsx` 中 `<span className="user-chip">` 之前插入头像图片。

```jsx
{user?.avatar_url ? (
  <img className="navbar-avatar" src={user.avatar_url} alt={displayName} />
) : (
  <span className="navbar-avatar-placeholder">{displayName?.charAt(0)}</span>
)}
```

### 5. 博客列表排序改为按发布时间

**选择**：修改 `article_service.py` 中 `listVisibleArticles()` 的 SQL 排序：`ORDER BY articles.create_time DESC, articles.id DESC`。

**理由**：
- 问题根源：当前 `ORDER BY articles.update_time DESC`，编辑后 `update_time` 更新导致文章置顶
- 改为 `create_time DESC` 后，编辑只更新 `update_time` 但不影响排序
- 文章发布时间保持不变，符合用户期望

### 6. 时间转换为北京时间

**选择**：在后端各 service 的 `formatArticle()`/`formatQuickPost()` 等格式化函数中添加北京时间转换。

```python
from datetime import datetime, timedelta, timezone

BEIJING_TZ = timezone(timedelta(hours=8))

def toBeijingTime(utcStr: str) -> str:
    """将 UTC 时间字符串转为北京时间字符串（YYYY-MM-DD HH:MM:SS）"""
    if not utcStr:
        return utcStr
    dt = datetime.strptime(utcStr, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    beijing = dt.astimezone(BEIJING_TZ)
    return beijing.strftime("%Y-%m-%d %H:%M:%S")
```

在产品代码中使用：

```python
def formatArticle(row):
    article = {
        ...
        "create_time": toBeijingTime(row["create_time"]),
        "update_time": toBeijingTime(row["update_time"]),
    }
```

**理由**：
- SQLite `CURRENT_TIMESTAMP` 返回 UTC 格式 `YYYY-MM-DD HH:MM:SS`
- 在 service 层格式化时统一转换，避免前端重复处理时区
- 所有时间字段（文章、快写、评论、待办等）统一转换

### 7. 文章详情页显示发布/编辑时间

**选择**：在 BlogDetailPage 底部 `.article-body` 之后、`.editor-actions` 按钮之前添加时间标签行。

```jsx
<div className="article-time-info">
  <span>发布于 {article.create_time}</span>
  {article.update_time !== article.create_time && (
    <span>最后编辑于 {article.update_time}</span>
  )}
</div>
```

**理由**：
- `create_time` 和 `update_time` 从后端返回（已转北京时间）
- 仅当两时间不同时显示编辑时间

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 排序改 `create_time` 后新发布文章和旧文章混杂 | 新发布的文章 create_time 为最新，自然排在前面 |
| 北京时间转换依赖 `datetime` 字符串解析 | SQLite 时间格式固定为 `YYYY-MM-DD HH:MM:SS`，parse 安全 |
| 编辑器重置可能清空用户未保存内容 | 只有导航栏点击"写文章"时触发，此时 draftId/aricleId=null |
| Markdown 源码含特殊字符影响 <pre> 渲染 | React 自动转义 `{article.content}` |
| 头像 URL 可能失效 | 后端 static 文件固定路径，与 ProfilePage 一致 |

## Open Questions

- 无