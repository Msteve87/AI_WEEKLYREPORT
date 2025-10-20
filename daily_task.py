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

# === CONFIG ===
#PROJECT_ROOT = Path(r"D:\VC_project\AI_test")
PROJECT_ROOT = Path(__file__).resolve().parent

HOME = Path.home()
DOCUMENTS = HOME / "Documents"


#BASE_FOLDER = r"D:\Wassel\Reports\Monthly_Report"
#BASE_FOLDER = PROJECT_ROOT / "Reports" / "Monthly_Report"
BASE_FOLDER = DOCUMENTS / "Reports" / "Monthly_Report"
BASE_FOLDER.mkdir(parents=True, exist_ok=True)

MODEL_NAME = "mistral"

#CUSTOM_SOUND = r"D:\VC_project\AI_test\among-us-roundstart.mp3"
CUSTOM_SOUND = PROJECT_ROOT / "among-us-roundstart.mp3"

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

# === Run Ollama to summarize + detect status ===
def analyze_tasks(user_text):
    prompt = f"""
You are a productivity assistant. The user will give you a messy list of work activities they did today. Your job is to extract and summarize each task clearly, and assign a status:

- If the task seems completed (e.g. "fixed", "finished", "deployed", "helped"), mark it as "Completed".
- If the task is ongoing, in progress, or uncertain (e.g. "working on", "planning", "starting"), mark it as "In_Progress".

Return the result in this exact format:

- Task: [summary]
  Status: Completed

Only return plain text using that structure.

Tasks:
{user_text}
"""
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.stdout.decode().strip()

# === Main submit: triggers AI and shows preview ===
def generate_summary():
    user_input = text_entry.get("1.0", tk.END).strip()

    if not user_input:
        messagebox.showwarning("Empty Input", "Please enter your tasks for today!")
        return

    # Call Ollama
    ai_result = analyze_tasks(user_input)

    # Open preview window
    show_preview_window(ai_result)

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

# Play sound right when app starts
play_startup_sound()

label = tk.Label(root, text=f"What did you do on {selected_date}? (List or paragraph is fine)")
label.pack(padx=10, pady=10)

text_entry = tk.Text(root, width=60, height=15)
text_entry.pack(padx=10, pady=10)

generate_btn = tk.Button(root, text="Generate Summary", command=generate_summary)
generate_btn.pack(padx=10, pady=10)

root.mainloop()