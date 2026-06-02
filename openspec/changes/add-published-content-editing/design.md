## Context

当前系统已有成熟的草稿编辑流程：`createDraft` / `updateDraft` / `publishDraft` 三个 service 函数和对应的 `POST/PUT /api/articles/drafts` 路由。这些函数都加了 `is_draft = 1` 的 SQL 条件限制。已发布文章（`is_draft = 0`）的 `GET /api/articles/{id}` 已支持，但无对应的 `PUT` 端点和编辑 UI 入口。

快写类似：`createQuickPost` / `deleteQuickPost` 已实现，但无 `updateQuickPost`。

前端编辑器 `BlogEditPage.jsx` 已通过 `draftId` URL 参数加载草稿，有完整的标题/简介/内容/分类/标签编辑能力，且已集成 AI 生成简介按钮。因此编辑已发布文章的最佳方案是复用此编辑器，新增 `articleId` 参数支持。

## Goals / Non-Goals

**Goals:**
- 已发布博客文章：作者可编辑标题、简介、内容、分类、标签、可见范围
- 已发布快写：作者可编辑内容和可见范围
- 前端编辑器复用：已发布文章通过 `?articleId=X` 参数加载到现有编辑器
- 鉴权：仅作者本人可编辑自己的内容
- 编辑后保留 AI 生成简介按钮

**Non-Goals:**
- 不涉及草稿编辑流程变更
- 不对编辑器 UI 做大幅调整
- 不支持管理员代编辑他人文章（管理员只有删除权限）
- 不添加版本历史/编辑记录

## Decisions

### 1. 后端：新增独立 service 函数而非复用 updateDraft

**选择**：为已发布文章新增 `updatePublishedArticle(userId, articleId, ...)`，不修改现有 `updateDraft`。

**理由**：
- `updateDraft` 有 `WHERE is_draft = 1` 硬约束，去掉会改变现有语义
- 已发布文章和草稿的 SQL 不同（草稿用 `is_draft = 1`，已发布用 `is_draft = 0`），混用易出 bug
- 保持最小改动原则，不触现有逻辑

**备选方案及排除理由**：
- ~~直接修改 `updateDraft` 去掉 `is_draft = 1`~~：可能影响草稿编辑逻辑，测试范围变大
- ~~写一个通用 `updateArticle` 统一草稿和已发布~~：过度设计，两个场景差异仅在一行 SQL 条件

### 2. API 设计

#### 2.1 已发布文章编辑
```
PUT /api/articles/{article_id}
  Auth: Bearer <token>

  Request (与 DraftRequest 相同):
  {
    "title": "string",
    "summary": "string | null",
    "content": "string",
    "category_id": "int | null",
    "visible_type": "public|friend|self",
    "tags": ["string", ...]
  }

  Response (200): ArticleDetailResponse
  Error (401): 未登录
  Error (403): 不是作者
  Error (404): 文章不存在
```

#### 2.2 已发布快写编辑
```
PUT /api/quick-posts/{quick_post_id}
  Auth: Bearer <token>

  Request:
  {
    "content": "string",
    "visible_type": "public|friend|self"
  }

  Response (200): QuickPostResponse
  Error (401): 未登录
  Error (403): 不是作者
  Error (404): 快写不存在
```

### 3. 前端编辑器复用设计

```
BlogEditPage.jsx 现有逻辑：
  ?draftId=X  → 加载草稿（已有）
  ?articleId=X → 加载已发布文章（新增）

  两者共用同一个编辑器组件，区别仅在：
  ├── 数据源不同（/drafts/{id} vs /{id}）
  ├── 保存时调用的 API 不同（PUT /drafts/{id} vs PUT /articles/{id}）
  └── 发布按钮：articleId 时隐藏（已发布），draftId 时显示
```

### 4. 快写编辑交互：内联编辑

快写内容短，不需要跳转到独立编辑器。设计为：

```
┌─────────────────────────────────────┐
│ 用户A · 2分钟前                     │
│ 这是一条快写内容...                  │
│ ♡ 3  💬 2                          │
│              [✏️ 编辑] (仅自己的可见) │
└─────────────────────────────────────┘
           ↓ 点击编辑
┌─────────────────────────────────────┐
│ ┌─────────────────────────────────┐ │
│ │ textarea（预填原内容）           │ │
│ │ ...                              │ │
│ └─────────────────────────────────┘ │
│ 可见范围: [公开 ▾]                  │
│ [保存] [取消]                       │
└─────────────────────────────────────┘
```

**理由**：快写 ≤500 字符，内联编辑比跳页面快；复用现有卡片 UI 空间，改动最小。

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| 已发布文章被编辑后，原内容丢失 | 前端在编辑页提示「正在编辑已发布文章」；用户手动保存确认 |
| 编辑期间其他用户看到半成品 | 后端 `UPDATE` 是原子操作，瞬间生效 |
| 分类/标签变更可能导致列表筛选问题 | 标签用 `syncArticleTags` 已处理多对多关系，无副作用 |
| 前端复用 draftId + articleId 可能状态混乱 | 同一时间只允许一个模式（优先级：articleId > draftId），互斥 |

## Open Questions

- 编辑已发布文章时是否需要保留「发布」按钮？初步决定隐藏，用「保存修改」替代
- 快写编辑时是否需要支持重新 AI 生成？初步不加入（快写内容短、无需简介）