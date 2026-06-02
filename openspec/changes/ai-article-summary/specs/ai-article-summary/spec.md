## ADDED Requirements

### Requirement: AI Summary Generation API
系统 SHALL 提供 `POST /api/ai/summary` 接口，接收文章 Markdown 内容，调用 DeepSeek API 生成不超过 300 字符的中文简介。响应 MUST 包含 `summary` 字段（简介文本）和 `model` 字段（所用模型名称）。该接口 MUST 要求用户登录认证。当 `AI_API_KEY` 未配置时，接口 SHALL 返回 503 错误提示 AI 服务未启用。

#### Scenario: 成功生成简介
- **WHEN** 已登录用户发送包含有效 content 的请求
- **THEN** 系统返回 `200` 及 `{ "summary": "AI 生成的简介文本", "model": "deepseek-chat" }`，响应中 `model` 字段标注所用 AI 模型

#### Scenario: 未登录用户请求
- **WHEN** 未登录用户请求该接口
- **THEN** 系统返回 `401` 未授权错误

#### Scenario: content 为空
- **WHEN** 请求中 content 字段为空字符串或只含空白字符
- **THEN** 系统返回 `422` 校验错误，提示内容不能为空

#### Scenario: content 过长
- **WHEN** 请求中 content 字段超过 50000 字符
- **THEN** 系统返回 `422` 校验错误，提示内容过长

#### Scenario: AI API Key 未配置
- **WHEN** `AI_API_KEY` 环境变量为空且收到请求
- **THEN** 系统返回 `503` 错误，提示 AI 服务未启用

#### Scenario: AI 服务调用超时
- **WHEN** DeepSeek API 在 15 秒内未响应
- **THEN** 系统返回 `504` 错误，提示 AI 服务超时请重试

#### Scenario: AI 服务返回错误
- **WHEN** DeepSeek API 返回非正常响应（如额度用尽、网络错误）
- **THEN** 系统返回 `502` 错误，携带可读的错误描述

### Requirement: AI Configuration Management
系统 MUST 通过 `.env` 文件支持以下 AI 配置项：`AI_API_KEY`（API 密钥，默认空字符串）、`AI_BASE_URL`（API 端点，默认 `https://api.deepseek.com`）、`AI_MODEL`（模型名称，默认 `deepseek-chat`）。当 `AI_API_KEY` 为空时，AI 功能优雅降级，不影响系统正常启动。

#### Scenario: 完整配置可用
- **WHEN** `.env` 中正确设置了 `AI_API_KEY`、`AI_BASE_URL`、`AI_MODEL`
- **THEN** 系统启动后 AI 接口可正常调用

#### Scenario: 缺少 API Key 时启动
- **WHEN** `.env` 中 `AI_API_KEY` 为空
- **THEN** 系统正常启动，AI 接口返回 503 表示服务未启用

#### Scenario: 使用默认端点
- **WHEN** `.env` 中未设置 `AI_BASE_URL` 和 `AI_MODEL`
- **THEN** 系统使用 `https://api.deepseek.com` 和 `deepseek-chat` 作为默认值

### Requirement: AI Generate Button in Editor
前端文章编辑器的「简介」字段旁 MUST 显示「🤖 AI 生成」按钮。当简介为空时，按钮旁 SHALL 显示提示「用 AI 帮你生成？」。用户点击按钮后，系统 SHALL 调用后端 AI API，将返回结果填入简介输入框。生成期间按钮 MUST 显示 loading 状态并禁用。

#### Scenario: 简介为空时显示提示
- **WHEN** 用户在编辑器中且简介字段为空
- **THEN** 按钮旁显示「用 AI 帮你生成？」提示文案

#### Scenario: 简介有内容时显示重新生成
- **WHEN** 用户在编辑器中且简介字段已有内容
- **THEN** 按钮旁不显示提示文案，按钮仍可点击重新生成

#### Scenario: 点击生成按钮成功
- **WHEN** 用户点击按钮且正文内容不为空
- **THEN** 按钮变为 loading 状态，AI 返回结果后自动填入简介输入框，下方显示「由 {模型名} 生成」标注，按钮恢复

#### Scenario: AI 生成后显示模型来源
- **WHEN** AI 成功生成简介并填入输入框
- **THEN** 简介输入框下方显示「由 {模型名} 生成」的来源标注

#### Scenario: 正文为空时点击按钮
- **WHEN** 用户点击按钮但正文内容为空
- **THEN** 前端提示用户「请先编写文章内容」，不发送 API 请求

#### Scenario: AI 生成失败
- **WHEN** API 返回错误
- **THEN** 按钮恢复可用状态，显示 toast 错误提示，简介内容不被覆盖