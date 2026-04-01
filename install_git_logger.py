import shutil
import subprocess
from pathlib import Path


def main():
    home = Path.home()
    project_root = Path(__file__).resolve().parent

    source_script = project_root / "log_commit.py"
    target_script_dir = home / "git-tools"
    target_script = target_script_dir / "log_commit.py"

    hooks_dir = home / "git-hooks"
    hook_file = hooks_dir / "post-commit"

    target_script_dir.mkdir(parents=True, exist_ok=True)
    hooks_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_script, target_script)

    hook_contents = """#!/bin/bash
python "$HOME/git-tools/log_commit.py"
"""
    hook_file.write_text(hook_contents, encoding="utf-8", newline="\n")

    subprocess.run(
        ["git", "config", "--global", "core.hooksPath", str(hooks_dir)],
        check=True,
    )

    print(f"Installed logger script to: {target_script}")
    print(f"Installed global hook to: {hook_file}")
    print(f"Configured Git global hooks path: {hooks_dir}")


if __name__ == "__main__":
    main()
