# Todo Agent 操作说明 (Todo Agent Manual)

## 1. 核心理念 (Core Philosophy)
Todo Agent 旨在建立代码待办事项 (TODO/FIXME/URGENT) 与 GitHub Issue 之间的自动化联动机制。通过将代码中的待办标记转化为可追踪的任务，确保每一个技术债务或紧急需求都有据可查，并与 Git 工作流深度集成。

## 2. 自动化同步机制 (Sync Mechanism)

### 扫描与解析 (Scan & Parse)
- **触发时机**: 定期或在 `main` 分支代码更新时。
- **解析对象**: `main/` 目录下的所有源文件。
- **标记格式**: 遵循标准的代码注释风格，例如：
  - `// TODO: 任务描述`
  - `# FIXME: 问题描述`
  - `// URGENT: 紧急任务描述`

### Issue 创建与回写 (Issue Creation & Back-write)
1. **自动创建**: 发现新标记且未关联 Issue 时，自动通过 GitHub MCP 创建 Issue。
2. **回写 ID**: 将生成的 `[issue-{id}]` 自动回写到源文件注释中。
   - 示例：`// TODO: 任务描述 [issue-123]`
3. **建立链接**: 在 `README.md` 的 todo 区域自动添加任务条目及 GitHub Issue 链接。

## 3. 协同闭环流程 (Collaboration Lifecycle)

### 状态联动
- **开发中**: 当 Git Agent 为该 Issue 创建了 `dev/` 物理隔离目录时，Issue 状态自动更新为 `in-progress`。
- **已完成**:
  1. Git Agent 提交 PR 并合并至 `main`。
  2. GitHub Issue 被关闭并标注 `closed/merged-to-main`。
  3. Todo Agent 自动将 `main/` 目录源文件中的标记更新为 `[DONE]`。
     - 示例：`// TODO: 任务描述 [issue-123] [DONE]`

## 4. 路径与引用规则 (Path Rules)
- **统一根目录**: 所有在 Issue 或 `README.md` 中记录的路径必须相对于 `main/` 物理目录，**禁止**包含 `main/` 前缀。
- **映射表更新**: 每次同步操作后，Todo Agent 需更新 `docs/git_agent_mapping.md` 中的 `Todo 唯一标识` 和 `状态`。

---
*注：本手册受 `.trae/rules/project_rules.md` 约束。*