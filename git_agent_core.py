import os
import subprocess
from typing import Optional

class GitAgent:
    """
    负责 Git 版本管理与物理隔离工作区管理的 Agent。
    实现：todo-agent 提交 Issue -> git-agent 创建 dev 目录分支 -> PR 合并至 main -> 关闭 Issue。
    """

    def __init__(self, root_path: str = "/mnt/e/WSL2/agent-server-sample"):
        self.root_path = root_path
        self.main_path = os.path.join(root_path, "main")
        self.dev_root_path = os.path.join(root_path, "dev")
        self.mapping_file = os.path.join(self.main_path, "docs/git_agent_mapping.md")

    def create_dev_workspace(self, issue_id: str, type: str, todo_group: str, short_desc: str):
        """
        基于 Issue ID 创建物理隔离的开发工作区。
        格式: {type}/{issue_id}-{todo_group}-{short_desc}
        """
        branch_name = f"{type}/{issue_id}-{todo_group}-{short_desc}"
        dev_dir = os.path.join(self.dev_root_path, branch_name.replace("/", "_"))

        print(f"[*] 正在为 Issue #{issue_id} 创建物理工作区...")
        
        # 1. 确保 dev 根目录存在
        if not os.path.exists(self.dev_root_path):
            os.makedirs(self.dev_root_path, mode=0o755)

        # 2. 同步 main 目录基线 (从远程拉取最新)
        print(f"[*] 同步 main 分支基线...")
        subprocess.run(["git", "-C", self.root_path, "checkout", "main"], check=True)
        subprocess.run(["git", "-C", self.root_path, "pull", "origin", "main"], check=True)

        # 3. 创建远程分支
        print(f"[*] 创建远程分支: {branch_name}")
        subprocess.run(["git", "-C", self.root_path, "push", "origin", f"main:refs/heads/{branch_name}"], check=True)

        # 4. 创建物理目录并克隆/拉取代码
        print(f"[*] 创建物理目录: {dev_dir}")
        if not os.path.exists(dev_dir):
            os.makedirs(dev_dir, mode=0o755)
        
        # 这种方式避免了嵌套仓库问题，直接将指定分支检出到物理目录
        subprocess.run(["git", "clone", "-b", branch_name, "https://github.com/alanyao91168/agent-server-sample.git", dev_dir], check=True)

        print(f"[+] 工作区创建成功: {dev_dir}")
        self._update_mapping(issue_id, branch_name, dev_dir)
        return dev_dir

    def _update_mapping(self, issue_id: str, branch_name: str, dev_path: str):
        """更新映射表"""
        # 简单追加到文件末尾，实际应用中可能需要更复杂的解析
        with open(self.mapping_file, "a", encoding="utf-8") as f:
            f.write(f"| - | - | {issue_id} | {branch_name} | {dev_path} | 已创建 | - |\n")

if __name__ == "__main__":
    # 测试代码
    agent = GitAgent()
    # 示例调用
    # agent.create_dev_workspace("1", "feat", "todo", "init-framework")
