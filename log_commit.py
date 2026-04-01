import subprocess
from datetime import datetime
from pathlib import Path
import socket


def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def main():
    try:
        repo_root = run_git(["rev-parse", "--show-toplevel"])
        repo_name = Path(repo_root).name
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        sha = run_git(["rev-parse", "--short", "HEAD"])
        msg = run_git(["log", "-1", "--pretty=%s"])
    except subprocess.CalledProcessError:
        return

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    host = socket.gethostname()

    report_dir = Path.home() / "Documents" / "Reports" / "Monthly_Report" / "git-daily-reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / f"{date_str}.txt"

    line = f"{time_str} | {host} | {repo_name} | {branch} | {sha} | {msg}"

    if report_file.exists():
        content = report_file.read_text(encoding="utf-8", errors="ignore")
        if sha in content:
            return

    with report_file.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    main()
