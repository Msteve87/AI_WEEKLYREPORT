# AI_test

Brief tools for entering daily tasks and generating weekly/monthly reports.

## Overview
- `daily_task.py` — Tkinter GUI to enter tasks for a day, summarize via Ollama, and save a dated text file.
- `weekly_report_checker.py` — (optional) checks for missing daily reports (Sunday–Thursday) and launches `daily_task.py` for each missing day.
- `weekly_Report.py` — reads saved daily text files and writes a weekly summary into an Excel template (`Template.xlsx`).

## Requirements
- Python 3.8+
- Windows (tested)
- Install required Python packages:
```powershell
pip install openpyxl playsound
```
- Optional: Ollama CLI and your chosen model (e.g. `mistral`) if you want AI summarization.
- Ensure `Template.xlsx` exists in the project root.

## Project layout
- d:\VC_project\AI_test\
  - daily_task.py
  - weekly_report_checker.py
  - weekly_Report.py
  - Template.xlsx
  - among-us-roundstart.mp3 (optional)
  - README.md

## Configuration
Edit top of scripts if needed:
- `PROJECT_ROOT`, `TEMPLATE_PATH`, `OUTPUT_PATH`, `BASE_FOLDER`
- In `daily_task.py` set `CUSTOM_SOUND` path or leave blank to use system beep.
- Work week is Sunday–Thursday (functions `get_week_start` / `get_week_dates`).

Daily files are saved to:
`%USERPROFILE%\Documents\Reports\Monthly_Report\YYYY_MM\YYYY-MM-DD.txt`

## Usage

1. Run daily GUI for today:
```powershell
python d:\VC_project\AI_test\daily_task.py
```

2. Run daily GUI for a specific date:
```powershell
python d:\VC_project\AI_test\daily_task.py --date 2025-08-01
```

3. Check for missing days (Sunday–Thursday) and open daily GUI for them:
```powershell
python d:\VC_project\AI_test\weekly_report_checker.py
```

4. Generate weekly/monthly Excel report (uses `Template.xlsx`):
```powershell
python d:\VC_project\AI_test\weekly_Report.py
```

## Troubleshooting
- ModuleNotFoundError: No module named 'openpyxl'  
  Run `pip install openpyxl`.

- ModuleNotFoundError: No module named 'pandas'  
  Comment out or remove any unused `import pandas as pd` lines since this project does not require pandas.

- Ollama errors: ensure Ollama CLI is installed and the model name in `daily_task.py` is available.

- Sound not playing: confirm `CUSTOM_SOUND` path is correct and `playsound` is installed; Windows fallback uses `winsound`.

## Notes
- Report generation expects daily `.txt` files in the correct month folder. Use the GUI to create them or run the checker to prompt for missing days.
- Adjust `get_week_dates` if your workweek or week-start logic changes.
