## Implementation Tasks

### Phase 1: 后端 — 日志系统

- [ ] Task 1.1: 新建 `backend/app/core/logging.py`
  - `setupLogging()` 函数：配置 root logger + RotatingFileHandler
  - 日志格式：`%(asctime)s [%(levelname)s] %(name)s: %(message)s`
  - 文件轮转：5MB / 3 个文件
  - 控制台级别：WARNING

- [ ] Task 1.2: 在 `backend/app/main.py` 启动时调用 `setupLogging()`

- [ ] Task 1.3: 在关键 API 路由添加错误日志
  - `articles.py` — HTTPException 处理中添加 logger.error
  - `ai.py` — 每个路由的异常处理中添加 logger.error
  - `users.py` — 异常处理中添加 logger.error
  - `quick_posts.py` — 异常处理中添加 logger.error
  - `comments.py` — 异常处理中添加 logger.error

- [ ] Task 1.4: 在 `ai_service.py` 的 `_callAI()` 中添加调用日志
  - 调用前：记录 model, contentLen, maxTokens
  - 调用后：记录 elapsed, responseLen
  - 失败：记录 elapsed, error

### Phase 2: 后端 — 牛宝对话 API

- [ ] Task 2.1: 在 `ai_service.py` 中新增 `chatWithNiubao(messages, api_key, base_url, model)` 函数
  - System prompt: "你是牛宝，一个温暖、幽默的好朋友..."
  - 将 messages 拼接到 API 调用中
  - 返回 `{ reply, model }`

- [ ] Task 2.2: 在 `ai.py` 中新增 `POST /ai/chat` 路由
  - 请求 Schema：`{ messages: list[{role, content}] }`
  - 响应 Schema：`{ reply: str, model: str }`
  - 鉴权：`getCurrentUser`

### Phase 3: 前端 — 牛宝对话页面

- [ ] Task 3.1: 新建 `frontend/src/pages/NiuBaoChatPage.jsx`
  - 左右分栏布局（左侧对话列表，右侧聊天区域）
  - 对话列表：新建对话 / 切换对话 / 删除对话
  - 聊天区域：消息气泡（用户右侧蓝色，牛宝左侧灰色）
  - 输入框 + 发送按钮
  - localStorage 持久化对话历史
  - 消息发送时调用 `POST /ai/chat`

- [ ] Task 3.2: 在 `App.jsx` 中添加路由
  - import NiuBaoChatPage
  - 添加 `{ path: 'niubao', element: <ProtectedRoute><NiuBaoChatPage /></ProtectedRoute> }`

- [ ] Task 3.3: 在 `route-config.js` 中添加路由配置
  - `{ path: '/niubao', label: '牛宝', visibility: 'auth', showInNav: false }`

- [ ] Task 3.4: 在 `global.css` 添加聊天页面样式
  - `.chat-layout` — 左右分栏
  - `.chat-sidebar` — 对话列表
  - `.chat-main` — 聊天区域
  - `.chat-bubble-user` / `.chat-bubble-bot` — 消息气泡
  - `.chat-input-row` — 输入框行

### Phase 4: 前端 — 电子宠物入口

- [ ] Task 4.1: 修改 `HomePage.jsx`
  - 左下角添加固定定位按钮
  - 登录用户可见，游客隐藏
  - 占位符：🐮 emoji + 预留 img 标签

- [ ] Task 4.2: 在 `global.css` 添加电子宠物样式
  - `.niubao-pet` — 固定定位、圆形、阴影、hover 效果

### 验证清单

- [ ] 后端启动后 `logs/app.log` 文件存在
- [ ] API 异常时日志文件中能查到错误记录
- [ ] AI 调用（摘要/润色/评论/对话）有完整的调用前/后日志
- [ ] 主页左下角显示 🐮 按钮，游客不显示
- [ ] 点击 🐮 跳转到 `/niubao`
- [ ] `/niubao` 页面显示左右布局
- [ ] 可以新建对话并发送消息
- [ ] 牛宝回复正常显示
- [ ] 刷新后对话历史保留
- [ ] 切换/删除对话正常