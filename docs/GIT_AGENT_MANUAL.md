# Git Agent 操作说明 (Git Agent Manual)

## 1. 核心理念 (Core Philosophy)
Git Agent 采用 **“物理隔离开发”** 模式，旨在解决 Trae 环境下多任务并行开发时的代码冲突和上下文污染问题。

- **Main 目录**: 仅存放 `main` 分支的基线代码，作为所有开发的起点和最终合并的目标。
- **Dev 目录**: 存放各功能分支的物理副本，每个副本都是一个独立的 Git 工作区。

## 2. 目录结构规范 (Directory Structure)
```text
/mnt/e/WSL2/agent-server-sample/
├── main/               # 主基线工作区 (Root of main branch)
└── dev/                # 开发工作区根目录
    ├── feat/issue-1-xxx/   # 功能开发物理目录
    └── bugfix/issue-2-xxx/ # Bug 修复物理目录
```

## 3. 核心操作流程 (Workflow)

### 第一步：创建开发环境 (Create Environment)
当接收到新的任务（关联 Issue）时，Git Agent 会：
1. 在 `dev/` 下创建以分支名为命名的子目录。
2. 在该子目录下执行 `git clone` 或 `git init` 关联远端仓库。
3. 创建并切换到对应的功能分支。
4. 更新 `docs/git_agent_mapping.md` 映射表。

### 第二步：物理隔离开发 (Isolated Development)
- 开发者（或 Agent）必须切换到 `dev/` 下对应的子目录进行代码编写和测试。
- **严禁**直接在 `main/` 目录下修改代码。

### 第三步：提交 PR (Submit Pull Request)
- 在 `dev/` 子目录下完成 `git add` 和 `git commit`。
- 推送代码到远端仓库。
- 通过 GitHub MCP 发起 Pull Request (PR)，目标分支为 `main`。

### 第四步：合并与清理 (Merge & Cleanup)
1. PR 在 GitHub 端通过评审后执行合并。
2. 在 `main/` 目录下执行 `git pull` 同步最新的基线。
3. 删除 `dev/` 下对应的物理目录以释放空间。
4. 在映射表中更新状态为“已合并/已删除”。

## 4. 路径引用准则 (Path Reference Rules)
- **绝对禁止前缀**: 在 Issue、Todo 备注或文档中引用文件时，统一使用相对于分支根目录的路径。
  - 错误：`main/README.md`
  - 正确：`README.md`
- **Agent 自动适配**: Git Agent 会根据当前所处的物理目录自动解析相对路径。

---
*注：本说明受 `.trae/rules/project_rules.md` 约束。*