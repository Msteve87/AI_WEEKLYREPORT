# AI Weekly Report Generator 🚀

This project provides an automated set of tools to seamlessly collect your daily Python/Git task logs, review them via a Graphical User Interface (GUI), and compile them into a neat weekly Excel report.

## 🛠️ Features

- **Automated Git Hook Logging**: Tracks and logs your full Git commit messages automatically.
- **Date Backfilling**: Retrieve previous day's commits directly from your git history.
- **Daily Task Manager**: An intuitive GUI to review your day's commits, append manual tasks, and save daily summaries locally.
- **Weekly Excel Compiler**: Automatically takes daily notes and aggregates them into an `.xlsx` template mapped to a Sunday-to-Thursday work week.

## 📦 Requirements & Installation

1. First, make sure your Python dependencies are installed using the newly created `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install the Git Hook**:
   Run the installation script to attach the automatic commit logger to your Git workflow:
   ```bash
   python install_git_logger.py
   ```

## 💻 Usage Instructions

### 1. Daily Tracking (Automatic & Manual)
Once the Git hook is installed, commits are logged automatically behind the scenes into your `Documents/Reports/Monthly_Report/git-daily-reports` directory whenever you commit code.

To manually fetch/backfill commits for a past date, use:
```bash
python log_commit.py --date 2026-04-01
```

### 2. Daily Task Review GUI
Run the Daily Task app at the end of your day. It will instantly pull in the day's git commits and give you space to add extra non-code tasks or explanations.
```bash
python daily_task.py
```
*(You can also use `--date YYYY-MM-DD` to edit a specific past date).*

### 3. Generate Weekly Report
When the week is done, run the weekly script. It automatically gathers all daily text reports from the current week (Sunday up to Thursday), processes them, and outputs a formatted `.xlsx` Weekly Report based on `Template.xlsx`.
```bash
python weekly_Report.py
```

## 📁 File Structure Overview
- `daily_task.py`: Tkinter UI to summarize daily activities.
- `weekly_Report.py`: Generates the compiled `.xlsx` file using `openpyxl`.
- `log_commit.py`: The core Git logger functionality (callable standalone or via hook).
- `install_git_logger.py`: Script to set up automation.
- `Template.xlsx` / `success.png`: Assets required by the script and UI generation.
