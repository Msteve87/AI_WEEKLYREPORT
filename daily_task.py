import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import winsound
from datetime import datetime
from playsound import playsound
import threading
import sys
from pathlib import Path
from tkinter import font


# === CONFIG ===
HOME = Path.home()
DOCUMENTS = HOME / "Documents"

BASE_FOLDER = DOCUMENTS / "Reports" / "Monthly_Report"
BASE_FOLDER.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "mistral"

# Detect correct path (works in .py and .exe)
if getattr(sys, 'frozen', False):
    PROJECT_ROOT = Path(sys._MEIPASS)
else:
    PROJECT_ROOT = Path(__file__).resolve().parent

CUSTOM_SOUND = PROJECT_ROOT / "report_bobdyfound_1.mp3"


# Example:
# CUSTOM_SOUND = r"C:\path\to\sound.wav"

# === Parse optional --date argument ===
selected_date = None
if len(sys.argv) > 2 and sys.argv[1] == "--date":
    try:
        selected_date = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
    except Exception:
        selected_date = datetime.today().date()
else:
    selected_date = datetime.today().date()

# === Main submit: shows preview without AI processing ===
def generate_summary():
    user_input = text_entry.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showwarning("Empty Input", "Please enter your tasks for today!")
        return

    # Open preview window
    show_preview_window(user_input)

# === Preview window ===
def show_preview_window(summary_text):
    preview = tk.Toplevel(root)
    preview.title("Review Your Summary")

    label = tk.Label(preview, text="Review and edit your summarized tasks below:")
    label.pack(padx=10, pady=10)

    summary_box = tk.Text(preview, width=70, height=20)
    summary_box.pack(padx=10, pady=10)
    summary_box.insert("1.0", summary_text)

    save_button = tk.Button(
        preview,
        text="Save Summary",
        command=lambda: save_summary(summary_box.get("1.0", tk.END))
    )
    save_button.pack(pady=10)

# === Save final summary ===
def save_summary(final_text):
    # Use selected_date instead of today
    folder_name = f"{selected_date.year}_{selected_date.month:02d}"
    folder_path = os.path.join(BASE_FOLDER, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    file_name = f"{selected_date}.txt"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_text.strip())

    messagebox.showinfo("Saved", f"Summarized tasks saved to:\n{file_path}")
    root.destroy()

# === Play sound when the app opens ===
def play_startup_sound():
    if CUSTOM_SOUND.exists():
        threading.Thread(target=playsound, args=(str(CUSTOM_SOUND),), daemon=True).start()
    else:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

# === GUI layout ===
root = tk.Tk()
root.title(f"Daily Task Entry - {selected_date}")

unicode_font = ("Arial", 12)   # or ("Tahoma", 12) for better Arabic rendering
# Play sound right when app starts
play_startup_sound()



label = tk.Label(root, text=f"What did you do on {selected_date}? (List or paragraph is fine)")
label.pack(padx=10, pady=10)

def load_git_commits():
    git_report_dir = BASE_FOLDER / "git-daily-reports"
    git_file = git_report_dir / f"{selected_date}.txt"
    
    if git_file.exists():
        try:
            content = git_file.read_text(encoding="utf-8", errors="ignore")
            lines = content.strip().split("\n")
            
            commit_list = []
            for line in lines:
                parts = line.split(" | ")
                if len(parts) >= 6:
                    repo = parts[2]
                    msg = parts[5]
                    commit_list.append(f"- Task: Repo: {repo}\n  Commit: {msg}\n  Status: Completed")
            
            if commit_list:
                text_entry.insert("1.0", "\n\n".join(commit_list) + "\n")
        except Exception as e:
            print(f"Error loading git reports: {e}")

text_entry = tk.Text(root, width=90, height=20, font=unicode_font, autoseparators=True,maxundo=-1)
text_entry.pack(padx=10, pady=10)

# Pre-load the data
load_git_commits()


def force_unicode_paste(event=None):
    try:
        # Get raw clipboard text as Unicode
        data = root.clipboard_get()
        
        # Insert manually
        text_entry.insert("insert", data)

    except Exception as e:
        print("Paste error:", e)

    return "break"   # IMPORTANT: stop Tkinter's default behavior


text_entry.bind("<Control-v>", force_unicode_paste)
text_entry.bind("<Control-V>", force_unicode_paste)
text_entry.bind("<Shift-Insert>", force_unicode_paste)
text_entry.bind("<<Paste>>", force_unicode_paste)


generate_btn = tk.Button(root, text="Save Preview", command=generate_summary , width=30)
generate_btn.pack(padx=10, pady=10)

root.mainloop()
os._exit(0)
