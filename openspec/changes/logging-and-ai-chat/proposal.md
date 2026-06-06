## Why

当前存在两个待改进/新增的功能点：

### 增强日志系统
7. **缺少全面统一的日志记录**：项目目前没有集中的日志系统，无法追踪 API 错误、渲染异常、AI 调用失败等运行时问题。排查 bug 只能依赖浏览器控制台或终端输出，效率低下。

### AI Chat Bot「牛宝」
8. **缺少 AI 对话入口**：虽然已有牛宝 AI 评论功能，但用户无法直接与牛宝进行自由对话。需要一个类似 DeepSeek 网页聊天版的对话界面。

## What Changes

### A. 增强日志系统
- 后端：添加 Python `logging` 模块，配置日志格式（时间戳、日志级别、模块名、详细信息）
- 后端：在关键 API 路由（`articles.py`, `ai.py`, `users.py`, `quick_posts.py`, `comments.py`）中添加错误日志
- 后端：在 AI 服务层（`ai_service.py`）添加调用日志（请求内容长度、响应结果、耗时）
- 后端：日志输出到文件 + 控制台（可配置日志级别）
- 前端：捕获渲染错误、API 请求错误，记录到 console + 后端日志接口

### B. AI Chat Bot「牛宝」— 对话页面
- 前端新增 `NiuBaoChatPage.jsx`：对话界面
  - 左侧：历史对话列表
  - 右侧：聊天区域（消息气泡 + 输入框）
  - 支持 Markdown 渲染（类似 DeepSeek 网页聊天版）
- 后端新增 `POST /ai/chat` 路由：
  - 支持多轮对话（传入 `messages` 数组）
  - 牛宝 system prompt 设定为温暖、幽默的好朋友
- 前端路由：`/niubao` → `NiuBaoChatPage`
- 路由配置：`showInNav: false`（通过电子宠物入口进入）

### C. AI Chat Bot「牛宝」— 主页电子宠物入口
- 主页左下角添加**固定悬浮按钮**：电子宠物形象的**占位符**
- 占位符样式：圆形按钮，显示「🐮」emoji 或牛宝首字母
- 预留 `src` 属性，后续可替换为图片
- 点击后跳转 `/niubao` 对话页面
- 前端路由保护：需要登录

## Capabilities

### New Capabilities

- `logging-system`: 增强日志系统，记录后端 API 和前端关键错误
- `niubao-chat-page`: 牛宝 AI 对话页面
- `niubao-pet-entry`: 主页电子宠物入口（占位符）

## Impact

| 层级 | 文件 | 改动 |
|------|------|------|
| 后端 core | `logging.py` | **新建** 日志配置模块 |
| 后端 API | `articles.py`, `ai.py`, `users.py`, `quick_posts.py`, `comments.py` | 添加错误日志 |
| 后端 service | `ai_service.py` | 添加 AI 调用日志；新增 `chatWithNiubao()` 函数 |
| 后端 API | `ai.py` | 新增 `POST /ai/chat` 路由 |
| 前端 | `NiuBaoChatPage.jsx` | **新建** 牛宝对话页面 |
| 前端 | `HomePage.jsx` | 左下角添加电子宠物入口 |
| 前端 | `App.jsx` | 添加 `/niubao` 路由 |
| 前端 | `route-config.js` | 添加路由配置 |
| 前端 | `global.css` | 电子宠物样式 + 聊天页面样式 |