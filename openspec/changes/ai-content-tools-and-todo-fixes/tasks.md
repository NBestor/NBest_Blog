## Implementation Tasks

### Phase 1: 后端 — AI 润色 API

- [x] Task 1.1: 在 `ai_service.py` 中新增 `polishContent(content, style, customPrompt)` 函数
  - 根据 `style` 选择对应 system prompt
  - 调用 AI API，超时 30s
  - 返回 `{ polished, model }`

- [x] Task 1.2: 在 `ai.py` 中新增 `POST /ai/polish` 路由
  - 请求 Schema：`{ content: str, style: str = "formatting", custom_prompt: str | None = None }`
  - 复用 `getCurrentUser` 鉴权

### Phase 2: 后端 — AI 简介模式扩展

- [x] Task 2.1: 修改 `ai_service.py` 中 `generateSummary()` 函数
  - 增加 `style` 和 `custom_prompt` 参数
  - 根据 style 选择对应的 system prompt（formal/marketing/academic/casual/humorous/custom）
  - 默认 style 为 "formal"

- [x] Task 2.2: 修改 `ai.py` 中 `POST /ai/summary` 路由
  - 请求 Schema 增加 `style` 和 `custom_prompt` 可选字段

### Phase 3: 后端 — AI 评论 API + 牛宝账号

- [x] Task 3.1: 在 `ai_service.py` 中新增 `generateComment(content)` 函数
  - System prompt：牛宝温暖幽默朋友风格
  - 返回 `{ comment, model }`

- [x] Task 3.2: 在 `ai.py` 中新增 `POST /ai/comment` 路由
  - 请求 Schema：`{ content: str, target_type: str, target_id: int }`
  - 鉴权 `getCurrentUser`
  - 以牛宝（ID=666）身份调用 `comment_service` 创建评论

- [x] Task 3.3: 修改 `database.py`
  - 在 `initializeDatabase()` 中确保 ID=666 牛宝账号存在
  - 自动加为所有用户双向好友
  - 新用户注册时自动与牛宝建立好友关系

### Phase 4: 前端 — 代办功能微调

- [x] Task 4.1: 修改 `HomePage.jsx`
  - 待办按 `due_date` 排序（有截止日期升序，无截止日期排最后）
  - `due_date` 为空时不显示"无截止日期"
  - 每条待办添加 checkbox，勾选调用 `PUT /todos/{id}` 完成

### Phase 5: 前端 — AI 模式选择面板组件

- [x] Task 5.1: 在 `BlogEditPage.jsx` 中新增模式选择面板
  - 提取公共模态面板逻辑（简介和润色共用）
  - 简介模式面板：6 种选项（正式/营销/学术/轻松/幽默/自定义）
  - 润色模式面板：5 种选项（排版/错别字/学术/青春文学/自定义）
  - 自定义模式显示文本输入框
  - 面板关闭按钮

- [x] Task 5.2: 修改 AI 生成简介按钮逻辑
  - 点击后弹出模式选择面板而非直接生成
  - 选择后调用 API 传入 `style` 参数

- [x] Task 5.3: 编辑器新增「🤖 AI 润色」按钮
  - 放在编辑器操作区（`editor-actions`）
  - 正文为空时禁用
  - 点击弹出润色模式面板
  - 成功后替换编辑器内容

### Phase 6: 前端 — AI 评论勾选

- [x] Task 6.1: 修改 `BlogEditPage.jsx`
  - 编辑器底部添加 checkbox「🤖 牛宝评论」
  - 发布/保存时若勾选，调用 `POST /ai/comment`

- [x] Task 6.2: 修改 `HomePage.jsx`
  - 快写发布框添加 checkbox「🤖 牛宝评论」
  - 发布时若勾选，调用 `POST /ai/comment`

### Phase 7: 样式

- [x] Task 7.1: 在 `global.css` 添加模式选择面板样式
  - `.ai-mode-panel` — 模态面板遮罩
  - `.ai-mode-options` — 选项按钮列表
  - `.ai-mode-option` — 单个选项样式
  - `.ai-mode-custom-input` — 自定义输入框

### 验证清单

- [ ] 主页待办按截止日期排序，无日期排最后
- [ ] 主页待办无日期时不显示"无截止日期"
- [ ] 主页待办可勾选完成，完成后消失
- [ ] AI 生成简介弹出模式选择，6 种模式均可用
- [ ] AI 润色按钮可见，5 种模式均可用
- [ ] 排版模式不修改原文文字
- [ ] 勾选"牛宝评论"后文章发布，牛宝自动评论
- [ ] 勾选"牛宝评论"后快写发布，牛宝自动评论
- [ ] 牛宝账号 ID=666，所有用户好友