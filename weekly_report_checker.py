import sys
import subprocess
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import winsound

#BASE_FOLDER = r"D:\Wassel\Reports\Monthly_Report"
#DAILY_TASK_SCRIPT = r"d:\VC_project\AI_test\daily_task.py"


# === CONFIG ===
#PROJECT_ROOT = Path(r"d:\VC_project\AI_test")
PROJECT_ROOT = Path(__file__).resolve().parent

HOME = Path.home()
DOCUMENTS = HOME / "Documents"
BASE_FOLDER = DOCUMENTS / "Reports" / "Monthly_Report"

DAILY_TASK_SCRIPT = PROJECT_ROOT / "daily_task.py"
WEEKLY_REPORT_SCRIPT = PROJECT_ROOT / "weekly_Report.py"

DAILY_TASK_EXE = PROJECT_ROOT / "dist" / "daily_task.exe"
WEEKLY_REPORT_EXE = PROJECT_ROOT / "dist" / "weekly_Report.exe"
WAIT_TIMEOUT = 300  # seconds to wait for report file (5 minutes)
# ==============

def get_week_dates():
    today = datetime.today().date()
    # Find the most recent Sunday (weekday() == 6 for Sunday)
    days_since_sunday = (today.weekday() + 1) % 7
    start = today - timedelta(days=days_since_sunday)
    # Sunday (start) to Thursday (start + 4)
    return [start + timedelta(days=i) for i in range(5)]

def check_missing_days():
    week_dates = get_week_dates()
    folder_name = f"{week_dates[0].year}_{week_dates[0].month:02d}"
    folder_path = os.path.join(BASE_FOLDER, folder_name)
    missing = []
    for day in week_dates:
        file_path = os.path.join(folder_path, f"{day}.txt")
        if not os.path.exists(file_path):
            missing.append(day)
    return missing

def run_daily_task_for_day(day):
    report_folder = BASE_FOLDER / f"{day.year}_{day.month:02d}"
    report_file = report_folder / f"{day}.txt"

    print(f"\n📝 Launching Daily Task for {day}...")
    subprocess.run([str(DAILY_TASK_EXE), "--date", str(day)])
    
    print("⏳ Waiting for report to be saved...")
    for i in range(WAIT_TIMEOUT):
        if report_file.exists():
            print(f"✅ Report saved successfully: {report_file}")
            return True
        time.sleep(1)
    print(f"⚠️ Timeout: Report for {day} not found after {WAIT_TIMEOUT//60} minutes.")
    return False


# def main():
#     missing_days = check_missing_days()
#     if not missing_days:
#         print("All days are reported for this week!")
#         return
#     print("Missing reports for:", ", ".join(str(d) for d in missing_days))
#     for day in missing_days:
#         print(f"Launching daily_task.py for {day}...")
#         #subprocess.run(["python", DAILY_TASK_SCRIPT, "--date", str(day)])
#         run_program(DAILY_TASK_SCRIPT, ["--date", str(day)])

#     print("Launching weekly_Report.py...")
#     #subprocess.run(["python", WEEKLY_REPORT_SCRIPT])
#     run_program(WEEKLY_REPORT_SCRIPT)

def main():
    print("🔍 Checking weekly reports...")
    missing_days = check_missing_days()

    if not missing_days:
        print("✅ All days are already reported this week.")
    else:
        print("📅 Missing reports for:", ", ".join(str(d) for d in missing_days))
        for day in missing_days:
            run_daily_task_for_day(day)

    print("PROJECT_ROOT:", PROJECT_ROOT)
    print("Daily task path exists:", DAILY_TASK_EXE.exists(), DAILY_TASK_EXE)
    print("Weekly report path exists:", WEEKLY_REPORT_EXE.exists(), WEEKLY_REPORT_EXE)

    print("\n📊 Generating weekly report...")
    if WEEKLY_REPORT_EXE.exists():
        subprocess.run([str(WEEKLY_REPORT_EXE)])
    else:
        # fallback to .py if exe not built yet
        subprocess.run([sys.executable, str(PROJECT_ROOT / "weekly_Report.py")])

    print("\n🎉 All done!")





if __name__ == "__main__":
    main()