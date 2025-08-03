import os
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
#BASE_FOLDER = r"D:\Wassel\Reports\Monthly_Report"
#DAILY_TASK_SCRIPT = r"d:\VC_project\AI_test\daily_task.py"

# === CONFIG ===
PROJECT_ROOT = Path(r"W:\VC_project\AI_test")
HOME = Path.home()
DOCUMENTS = HOME / "Documents"
BASE_FOLDER = DOCUMENTS / "Reports" / "Monthly_Report"

DAILY_TASK_SCRIPT = PROJECT_ROOT / "daily_task.py"

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

def main():
    missing_days = check_missing_days()
    if not missing_days:
        print("All days are reported for this week!")
        return
    print("Missing reports for:", ", ".join(str(d) for d in missing_days))
    for day in missing_days:
        print(f"Launching daily_task.py for {day}...")
        subprocess.run(["python", DAILY_TASK_SCRIPT, "--date", str(day)])

if __name__ == "__main__":
    main()