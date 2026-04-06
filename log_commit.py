import subprocess
from datetime import datetime
from pathlib import Path
import socket
import sys


def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()


def log_to_file(date_str, time_str, host, repo_name, branch, sha, msg):
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


def main():
    try:
        repo_root = run_git(["rev-parse", "--show-toplevel"])
        repo_name = Path(repo_root).name
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    except subprocess.CalledProcessError:
        return

    host = socket.gethostname()

    # Check for --date argument
    if len(sys.argv) > 2 and sys.argv[1] == "--date":
        target_date = sys.argv[2]
        try:
            user_name = run_git(["config", "user.name"])
            # Format: SHA|Time|RawBody + custom delimiter
            log_format = "%H|%ad|%B======END_COMMIT======"
            commits_raw = run_git([
                "log",
                f"--author={user_name}",
                f"--after={target_date} 00:00:00",
                f"--before={target_date} 23:59:59",
                f"--pretty=format:{log_format}",
                "--date=format:%H:%M:%S"
            ])
            
            if not commits_raw:
                return

            for commit_block in commits_raw.split("======END_COMMIT======"):
                commit_block = commit_block.strip()
                if not commit_block:
                    continue
                sha_full, commit_time, msg = commit_block.split("|", 2)
                msg = msg.strip().replace("\n", "[NEWLINE]")
                log_to_file(target_date, commit_time, host, repo_name, branch, sha_full[:7], msg)
        except Exception:
            return
    else:
        # Default behavior: log current HEAD
        try:
            sha = run_git(["rev-parse", "--short", "HEAD"])
            msg = run_git(["log", "-1", "--pretty=%B"]).strip().replace("\n", "[NEWLINE]")
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")
            log_to_file(date_str, time_str, host, repo_name, branch, sha, msg)
        except subprocess.CalledProcessError:
            return


if __name__ == "__main__":
    main()
