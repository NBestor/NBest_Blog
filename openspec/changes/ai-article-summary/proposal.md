## Why

当前文章简介只能从正文剥离 Markdown 语法后截取前 140 字符，生成质量高度依赖文章开头是否恰好包含概括性语句，大部分情况下简介要么信息不全要么毫无意义。引入 AI 自动生成可大幅提升简介质量，让文章列表页的预览更有吸引力。

## What Changes

- 新增后端 API `POST /api/ai/summary`，接收文章内容，调用 DeepSeek API 返回 AI 生成的中文简介
- Prompt 强制要求简介 **不超过 300 字符**，确保简介精炼
- API 响应中携带 `model` 字段，标注生成所用的 AI 模型名称，前端展示给用户
- 新增配置项 `AI_API_KEY`、`AI_BASE_URL`、`AI_MODEL` 支持灵活切换 AI 提供商
- 前端编辑器在「简介」字段旁添加「🤖 AI 生成」按钮，仅在用户点击时触发
- 当用户未填写简介时，按钮旁显示温和提示「用 AI 帮你生成？」
- 简介生成后显示「由 {模型名} 生成」来源标注

## Capabilities

### New Capabilities

- `ai-article-summary`: AI 驱动的文章简介自动生成功能，包括后端 API 和前端编辑器按钮

### Modified Capabilities

<!-- No existing specs are modified by this change -->

## Impact

- **新增文件**: `backend/app/api/ai.py`（AI 路由）、`backend/app/services/ai_service.py`（AI 调用封装）
- **修改文件**: `backend/app/core/config.py`（新增 AI 配置项）、`backend/app/api/router.py`（注册 aiRouter）、`backend/.env.example`（新增 AI 配置示例）
- **前端修改**: 文章编辑器中增加 AI 生成按钮及交互逻辑
- **依赖**: `openai` 库（已安装，版本 1.109.1），无需新增依赖