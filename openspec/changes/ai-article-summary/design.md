## Context

当前文章系统已有 `summary` 字段（DB 限制 300 字符，`buildArticleSummary` 截取 140 字符），用户可在编辑器中手动填写简介。当 summary 为空时，系统自动从正文剥离 Markdown 后截取前 140 字符，质量不稳定。

项目已安装 `openai==1.109.1`，可直接兼容 DeepSeek API（DeepSeek 遵循 OpenAI SDK 接口规范）。用户选择 DeepSeek 作为 AI 提供商，要求手动触发 + 空 summary 时提示。

## Goals / Non-Goals

**Goals:**
- 提供后端 API，输入文章内容 → 返回 AI 生成的中文简介（不超过 300 字符）及所用模型名称
- 前端编辑器中添加「🤖 AI 生成」按钮，用户点击触发
- AI 生成后显示模型来源标注「由 {模型名} 生成」
- summary 为空时，按钮旁显示温和提示
- 配置项通过 `.env` 管理，支持切换 AI 提供商
- AI 调用超时 15 秒，超时返回友好错误

**Non-Goals:**
- 不自动生成（不侵入保存/发布流程）
- 不覆盖已有 summary（用户手写优先）
- 不支持批量生成
- 不支持用户自定义 prompt
- 不做调用频率限制（单用户博客场景无必要）

## Decisions

### 1. 后端架构：独立 service + api 模块

```
backend/app/
├── api/
│   └── ai.py              ← 新建：POST /api/ai/summary
├── services/
│   └── ai_service.py      ← 新建：封装 DeepSeek API 调用
├── core/
│   └── config.py          ← 修改：新增 AI 配置项
└── api/
    └── router.py          ← 修改：注册 aiRouter
```

**理由**: 保持项目现有分层模式（`api/` 处理 HTTP 请求，`services/` 处理业务逻辑）。AI 调用细节隔离在 `ai_service.py`，方便测试和替换提供商。

### 2. API 设计

```
POST /api/ai/summary
  Content-Type: application/json
  Auth: Bearer <token>

  Request:
  {
    "content": "文章 Markdown 正文..."
  }

  Response (200):
  {
    "summary": "AI 生成的中文简介",
    "model": "deepseek-chat"
  }

  Error (401): 未登录
  Error (422): content 为空或超长 (>50000 字符)
  Error (502): AI 服务不可用
  Error (504): AI 响应超时
```

**理由**: RESTful 风格，与项目现有 API 一致。无需单独鉴权——复用现有 `getCurrentUser` 依赖（防止未登录用户消耗额度）。

### 3. DeepSeek API 调用封装

```python
# ai_service.py
from openai import OpenAI

def generateSummary(content: str, apiKey: str, baseUrl: str, model: str) -> dict:
    client = OpenAI(api_key=apiKey, base_url=baseUrl)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是一个专业的文章编辑。为给定的文章生成一个简洁的中文简介。"
                    "必须严格遵守以下规则："
                    "1. 简介不超过300个字符，超出视为不合格；"
                    "2. 直接描述文章的核心内容和观点；"
                    "3. 不要使用'本文介绍了'、'这篇文章讲述了'等开头语；"
                    "4. 语言精炼，避免冗余修辞。"
                ),
            },
            {"role": "user", "content": content},
        ],
        max_tokens=250,
        temperature=0.3,
        timeout=15,
    )
    return {
        "summary": response.choices[0].message.content.strip(),
        "model": model,
    }
```

**备选方案及排除理由**:
- ~~本地模型 (torch + transformers)~~: 你的机器 GPU 资源不可控，部署到服务器更难保证
- ~~LangChain~~: 杀鸡用牛刀，一个简单的 API 调用不需要额外抽象层
- ~~流式响应 (streaming)~~: 简介生成极短（< 3 秒），流式无体验增益，反而增加复杂度

### 4. 配置项设计

```bash
# .env
AI_API_KEY=sk-your-deepseek-key
AI_BASE_URL=https://api.deepseek.com
AI_MODEL=deepseek-chat
```

`config.py` 中新增:
- `AI_API_KEY`: 默认 `""`，为空时跳过 AI 初始化
- `AI_BASE_URL`: 默认 `https://api.deepseek.com`
- `AI_MODEL`: 默认 `deepseek-chat`

**理由**: 这三个参数覆盖了 API Key、端点、模型名，足够切换到任意 OpenAI 兼容的提供商（OpenAI、DeepSeek、Ollama、通义千问等）。`AI_API_KEY` 为空时优雅降级，不会导致启动报错。

### 5. 前端交互设计

在文章编辑页的「简介」字段旁添加按钮：

```
┌─────────────────────────────────────────┐
│  标题：[___________________________]    │
│                                         │
│  简介：[___________________________]    │
│        [🤖 AI 生成]  ← 提示文案：       │
│        "用 AI 帮你生成？"（空时显示）      │
│        "重新生成"（有内容时显示）        │
│                                         │
│  正文：[...]                             │
└─────────────────────────────────────────┘
```

交互流程：
1. 用户点击按钮 → 按钮显示 loading（禁用 + 转圈）
2. 调用 `POST /api/ai/summary` 传入正文内容
3. 成功 → 返回的 summary 填入简介输入框，下方显示「由 {model} 生成」标注，按钮恢复
4. 失败 → toast 提示错误信息，按钮恢复

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| AI API 调用失败（网络/额度/超时） | 后端 try/except 捕获，返回 `502` + 友好错误消息；前端 toast 提示，不影响编辑 |
| 文章内容过长超出 API context | 后端校验 `content` 长度 ≤ 50000 字符（约 DeepSeek 32K context 的安全值），超长返回 422 |
| AI 返回的简介可能不理想 | 用户可以手动编辑 AI 生成结果，不满意点「重新生成」 |
| API Key 泄露到前端或日志 | Key 仅存储在服务端 `.env`；不在日志中打印请求/响应内容 |
| 用户内容发送到第三方（隐私） | 用户主动点击触发，非自动发送；已知风险，用户知情 |

## Open Questions

- 是否需要在后端缓存 AI 生成结果？（初步判断不需要，生成成本低且每次可不同）
- 是否需要支持 DeepSeek V3 或其他模型切换？（当前配置灵活，`.env` 改 `AI_MODEL` 即可）