# Cline 全局行为规则

## 核心原则

1. **任何功能变更必须走 OpenSpec 流程** — 无论是新建功能、修改现有功能、还是 bug 修复，都先创建 change（proposal → design → specs → tasks），再按 tasks 逐步实现。禁止直接跳到编码。
2. **逐步确认** — 每个 OpenSpec artifact 创建/修改后，等待用户确认再继续下一步。不可一次性批量生成所有文件。
3. **编码阶段按任务顺序** — 严格按 tasks.md 的顺序逐项实现，每完成一项标记 `[x]`。

## OpenSpec 流程

```
用户提出需求
    ↓
openspec new change "<name>"           # 创建 change
    ↓
逐个生成/修改 artifact（每步等确认）：
  ① proposal.md     → 等待确认
  ② design.md       → 等待确认
  ③ specs/*.md      → 等待确认
  ④ tasks.md        → 等待确认
    ↓
用户说 "开始实现" 或 /opsx:apply
    ↓
按 tasks.md 逐项编码
```

## 工程规范（来自 .codex/agent.md）

### 命名规范
- **文件夹**: 小写、中横线分隔，功能内聚、单一职责，禁止中文/特殊符号
- **文件命名**: 组件 `UpperCamelCase.jsx`，工具 `lower-snake-case.js`，页面 `PageName.jsx`，配置 `config.js` / `.env`
- **变量**: `lowerCamelCase`，函数 `handleXxx`/`fetchXxx`，布尔 `isXxx`，常量 `UPPER_SNAKE_CASE`
- **数据库**: 表名小写复数下划线（`articles`、`quick_posts`），字段小写语义化
- **接口**: RESTful，小写复数中横线，如 `/api/articles`、`/api/quick-posts`

### 后端架构模式
```
backend/app/
├── api/         # HTTP 路由 + request/response Schema（薄层，只做参数校验和调用 service）
├── services/    # 业务逻辑（数据库操作、外部 API 调用等）
├── core/        # 配置（config.py）+ 安全（security.py）
├── db/          # 数据库连接（database.py）
└── schemas/     # Pydantic 响应模型（仅声明结构，不含业务逻辑）
```
- 依赖注入：FastAPI `Depends(getCurrentUser)` / `Depends(getSettings)`
- 鉴权：`app/api/auth.py` 提供 `getCurrentUser`（强制登录）和 `getOptionalCurrentUser`（可选）
- 错误处理：`HTTPException(status_code=status.HTTP_404_NOT_FOUND, ...)` 返回标准状态码

### 前端架构模式
```
frontend/src/
├── pages/       # 页面组件（PageName.jsx），每个路由一个页面
├── components/  # 可复用组件（ProtectedRoute、CommentThread 等）
├── layouts/     # 布局组件（AppLayout）
├── contexts/    # React Context（AuthContext）
└── api/         # Axios 实例（http-client.js，统一 baseURL + token 注入）
```
- 状态管理：`useState` + `useEffect` + `useMemo`，不引入 Redux
- 路由守卫：`ProtectedRoute` 组件包裹需要登录的页面
- 错误处理：API 调用包裹在 `try/catch` 中，失败时 `setMessage("xxx 失败")` 展示给用户

### 权限模型
- **游客 visitor**: 仅浏览公开内容
- **用户 user**: 登录后的默认角色，可发布/互动/管理自己内容
- **管理员 admin**: 可删除任意内容（`getCurrentSupervisor` 鉴权）

### CSS 规范
- 沿用项目现有风格：`global.css`（主要样式）+ `standard.css`（补充）
- 新增样式追加到 `global.css` 文件末尾，不修改已有样式
- 风格特征：简约白灰基调、圆角 5px、轻微阴影、hover 过渡

### 迭代开发原则
- 每个阶段/模块完成后必须可独立运行、可验收
- 后端接口和前端页面同步完成，不可只做一端
- 阶段验收通过后再进入下一阶段

## 禁止行为

- ❌ 用户提出需求后直接写代码
- ❌ 一次性生成多个 OpenSpec artifact 不等确认
- ❌ 跳过 OpenSpec 流程做任何功能变更
- ❌ 修改代码时不更新对应的 OpenSpec 文件
- ❌ 主动猜测用户意图做额外改动

## 例外

以下情况可以不走 OpenSpec：
- 纯 bug 修复（单行/少量改动，不涉及需求变更）
- 用户明确说 "直接改"
- 回答技术问题、配置指导等非编码任务