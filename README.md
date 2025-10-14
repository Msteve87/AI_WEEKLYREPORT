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

## Install Ollama (Windows)
1. Visit the official install page and follow the Windows instructions:
   - https://ollama.com/install

2. Preferred simple methods:
   - Download the Windows installer (MSI) from the official page and run it as Administrator.
   - OR, if you use winget (Windows Package Manager), try:
     ```powershell
     winget install Ollama.Ollama
     ```
     (If winget package is unavailable on your system, use the installer from the website.)

3. Verify installation:
```powershell
ollama --version
```
You should see version information. If that fails, ensure the Ollama install directory was added to your PATH and reopen the terminal.

4. Download the model you plan to use (example uses `mistral`):
```powershell
ollama pull mistral
```
(If you prefer, `ollama run <model>` will often download the model on first use.)

5. Quick test run:
```powershell
ollama run mistral
```
This should start a session using the model. Your `daily_task.py` uses `subprocess` to call `ollama run <MODEL_NAME>`.

Notes:
- Run the installer as Administrator on Windows if you encounter permission issues.
- See `ollama --help` for more commands and troubleshooting.

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

- Ollama errors: ensure Ollama CLI is installed and the model name in `daily_task.py` is available. Use `ollama pull <model>` to download the model before running the app.

- Sound not playing: confirm `CUSTOM_SOUND` path is correct and `playsound` is installed; Windows fallback uses `winsound`.

## Notes
- Report generation expects daily `.txt` files in the correct month folder. Use the GUI to create them or run the checker to prompt for missing days.
- Adjust `get_week_dates` if your workweek or week-start logic changes.
