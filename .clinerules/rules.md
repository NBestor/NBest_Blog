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

- **文件夹**: 小写、中横线分隔
- **文件命名**: 组件 `UpperCamelCase.jsx`，工具 `lower-snake-case.js`，页面 `PageName.jsx`
- **变量**: `lowerCamelCase`，函数 `handleXxx`/`fetchXxx`，布尔 `isXxx`，常量 `UPPER_SNAKE_CASE`
- **接口**: RESTful，小写复数中横线，如 `/api/articles`
- **CSS**: 沿用项目现有风格，新增样式追加到现有 CSS 文件末尾

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