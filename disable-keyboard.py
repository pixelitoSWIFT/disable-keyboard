import os
import sys
import ctypes
import tkinter as tk
from tkinter import ttk
import keyboard
import threading

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

def toggle_keyboard():
    global keyboard_disabled
    if not keyboard_disabled:
        for key in range(150):
            keyboard.block_key(key)
        keyboard_disabled = True
        status_label.config(text="Keyboard Disabled")
    else:
        for key in range(150):
            keyboard.unblock_key(key)
        keyboard_disabled = False
        status_label.config(text="Keyboard Enabled")

def threaded_toggle():
    threading.Thread(target=toggle_keyboard, daemon=True).start()

keyboard_disabled = False

root = tk.Tk()

if hasattr(sys, "_MEIPASS"):
    icon_path = os.path.join(sys._MEIPASS, "icon.ico")
else:
    icon_path = "icon.ico"

if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
    
root.resizable(False, False)
root.geometry("200x120")
root.title("Disable Keyboard")

status_label = tk.Label(root, text="Keyboard Enabled", font=("Segoe UI", 14))
status_label.pack(pady=5)

style = ttk.Style()
style.configure("Custom.TButton",  font=("Segoe UI", 12),  padding=10)

toggle_button = ttk.Button(root, text="Toggle Keyboard",  style="Custom.TButton", command=threaded_toggle)
toggle_button.pack(pady=5)

root.mainloop()
