import sys
import subprocess
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import winsound

# === PATH CONFIG ===
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent

HOME = Path.home()
DOCUMENTS = HOME / "Documents"
BASE_FOLDER = DOCUMENTS / "Reports" / "Monthly_Report"

DAILY_TASK_EXE = PROJECT_ROOT  / "daily_task.exe"
WEEKLY_REPORT_EXE = PROJECT_ROOT  / "weekly_Report.exe"

WAIT_TIMEOUT = 60  # 1 minute max wait
# ====================

def get_week_dates():
    today = datetime.today().date()
    # Sunday as start
    days_since_sunday = (today.weekday() + 1) % 7
    start = today - timedelta(days=days_since_sunday)
    return [start + timedelta(days=i) for i in range(5)]  # Sun–Thu

def check_missing_days():
    week_dates = get_week_dates()
    folder_name = f"{week_dates[0].year}_{week_dates[0].month:02d}"
    folder_path = BASE_FOLDER / folder_name
    missing = []
    for day in week_dates:
        file_path = folder_path / f"{day}.txt"
        if not file_path.exists():
            missing.append(day)
    return missing

def run_daily_task_for_day(day):
    report_folder = BASE_FOLDER / f"{day.year}_{day.month:02d}"
    report_file = report_folder / f"{day}.txt"

    print(f"📝 Launching daily_task.exe for {day}...")
    subprocess.run([str(DAILY_TASK_EXE), "--date", str(day)])
    
    print("⏳ Waiting for report to be saved...")
    for _ in range(WAIT_TIMEOUT):
        if report_file.exists():
            print(f"✅ Report for {day} saved!")
            return True
        time.sleep(1)

    print(f"⚠️ Timeout: Report for {day} not found.")
    return False

def main():
    print("🔍 Checking weekly reports...")
    missing_days = check_missing_days()

    if not missing_days:
        print("✅ All daily reports exist. Generating weekly report...")
    else:
        print("📅 Missing reports:", ", ".join(str(d) for d in missing_days))
        for day in missing_days:
            run_daily_task_for_day(day)

    # === Run weekly report ===
    print("📊 Generating weekly report...")
    subprocess.run([str(WEEKLY_REPORT_EXE)])

    # === Popup & Sound ===
    winsound.MessageBeep(winsound.MB_ICONASTERISK)
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Weekly Checker", "🎉 Weekly process completed successfully!")

if __name__ == "__main__":
    main()
    time.sleep(1)  # short grace period
    os._exit(0)    # forcefully terminate this process (skips lingering Tk threads)
