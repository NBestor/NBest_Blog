## 1. 后端配置

- [ ] 1.1 在 `backend/app/core/config.py` 中新增 `AI_API_KEY`、`AI_BASE_URL`、`AI_MODEL` 配置项，提供默认值
- [ ] 1.2 在 `backend/.env.example` 中添加 AI 配置项示例（注释状态，值为占位符）

## 2. AI 服务层

- [ ] 2.1 新建 `backend/app/services/ai_service.py`，封装 `generateSummary(content)` 函数，返回 `{ summary, model }`，prompt 强制简介不超过 300 字符，处理超时和异常

## 3. AI API 路由

- [ ] 3.1 新建 `backend/app/api/ai.py`，定义请求/响应 Schema（含 `model` 字段）和 `POST /ai/summary` 路由，复用 `getCurrentUser` 鉴权
- [ ] 3.2 在 `backend/app/api/router.py` 中注册 aiRouter

## 4. 前端 AI 生成按钮

- [ ] 4.1 在文章编辑器中简介输入框旁添加「🤖 AI 生成」按钮，空简介时显示「用 AI 帮你生成？」提示
- [ ] 4.2 实现按钮点击逻辑：校验正文非空 → loading 状态 → 调用 API → 填入结果 + 显示「由 {model} 生成」标注 / 错误 toast
- [ ] 4.3 处理 loading 态样式、按钮禁用/恢复交互，以及模型来源标注的样式

## 5. 本地配置与验证

- [ ] 5.1 在项目本地的 `backend/.env` 文件中配置有效的 `AI_API_KEY`
- [ ] 5.2 启动前后端，验证 AI 生成按钮功能完整可用