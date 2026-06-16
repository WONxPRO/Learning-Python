import threading
import time
import random
import tkinter as tk
from tkinter import ttk

import win32gui
import win32process
import win32con
import win32api
import psutil

from pynput import keyboard
from pynput.keyboard import Key

# =========================
# STATE
# =========================
running = False
paused = False

step_index = 0
step_remaining = 0.0
current_keys = []

start_time = None
last_reset_time = None

target_hwnd = None
mode = "BACKGROUND"  # or "ACTIVE"

lock = threading.Lock()

# =========================
# CONFIG
# =========================
STEP_NAMES = ["A + R", "W", "R + D", "W"]
BASE = [26.0, 1.0, 26.0, 1.0]

KEY_SEQUENCE = [
    ['a', 'r'],
    ['w'],
    ['r', 'd'],
    ['w']
]

VK_MAP = {
    'a': 0x41,
    'r': 0x52,
    'd': 0x44,
    'w': 0x57,
    'z': 0x5A
}

# =========================
# WINDOW ENUM
# =========================
def get_windows():
    windows = []

    def enum_handler(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return

        try:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            name = psutil.Process(pid).name()
        except:
            return

        title = win32gui.GetWindowText(hwnd)
        windows.append((hwnd, title if title else "[No Title]", name))

    win32gui.EnumWindows(enum_handler, None)
    return windows


def set_target(hwnd):
    global target_hwnd
    target_hwnd = hwnd


# =========================
# INPUT METHODS
# =========================
def send_post(hwnd, vk, down=True):
    msg = win32con.WM_KEYDOWN if down else win32con.WM_KEYUP
    win32gui.PostMessage(hwnd, msg, vk, 0)


def send_input(vk, down=True):
    flag = 0 if down else win32con.KEYEVENTF_KEYUP
    win32api.keybd_event(vk, 0, flag, 0)


def press_keys(keys):
    if target_hwnd is None:
        return

    if mode == "BACKGROUND":
        for k in keys:
            send_post(target_hwnd, VK_MAP[k], True)

    else:  # ACTIVE MODE
        prev = win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(target_hwnd)

        for k in keys:
            send_input(VK_MAP[k], True)

        win32gui.SetForegroundWindow(prev)


def release_keys(keys):
    if target_hwnd is None:
        return

    if mode == "BACKGROUND":
        for k in keys:
            send_post(target_hwnd, VK_MAP[k], False)

    else:
        prev = win32gui.GetForegroundWindow()
        win32gui.SetForegroundWindow(target_hwnd)

        for k in keys:
            send_input(VK_MAP[k], False)

        win32gui.SetForegroundWindow(prev)


def tap_key(k):
    press_keys([k])
    release_keys([k])


# =========================
# CORE LOGIC
# =========================
def rand_duration(base):
    return base + random.uniform(0, 0.5)


def full_stop():
    global running, paused, step_index, step_remaining, current_keys
    with lock:
        running = False
        paused = False
        release_keys(['a', 'r', 'd', 'w', 'z'])
        step_index = 0
        step_remaining = 0.0
        current_keys = []


def worker():
    global running, paused, step_index, step_remaining, current_keys, last_reset_time

    while True:
        time.sleep(0.01)

        with lock:
            if not running:
                break

            if paused:
                continue

            # reset cycle
            if last_reset_time and (time.time() - last_reset_time) >= 900:
                release_keys(current_keys)
                tap_key('z')
                step_index = 0
                step_remaining = 0.0
                current_keys = []
                last_reset_time = time.time()
                continue

            if step_remaining <= 0:
                step_remaining = rand_duration(BASE[step_index])
                current_keys = KEY_SEQUENCE[step_index]
                press_keys(current_keys)

        time.sleep(0.01)

        with lock:
            if not running:
                break

            step_remaining -= 0.01

            if step_remaining <= 0:
                release_keys(current_keys)
                step_index = (step_index + 1) % 4
                step_remaining = 0

    full_stop()


# =========================
# CONTROLS
# =========================
def toggle_running():
    global running, paused, start_time, last_reset_time

    with lock:
        if running:
            full_stop()
            return

        if target_hwnd is None:
            return

        running = True
        paused = False
        start_time = time.time()
        last_reset_time = time.time()

    threading.Thread(target=worker, daemon=True).start()


def toggle_pause():
    global paused
    with lock:
        if running:
            paused = not paused


# =========================
# UI
# =========================
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Automation Controller")
        self.root.geometry("520x420")
        self.root.configure(bg="#0e1117")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#0e1117")
        style.configure("TLabel", background="#0e1117", foreground="#c9d1d9")
        style.configure("TButton", background="#21262d", foreground="#c9d1d9")
        style.configure("TEntry", fieldbackground="#161b22", foreground="#c9d1d9")

        main = ttk.Frame(self.root)
        main.pack(fill="both", expand=True, padx=16, pady=12)

        # window selection
        ttk.Label(main, text="Target Window").pack(anchor="w")
        self.dropdown = ttk.Combobox(main)
        self.dropdown.pack(fill="x", pady=5)

        ttk.Button(main, text="Refresh", command=self.refresh).pack()
        ttk.Button(main, text="Set Target", command=self.set_target).pack(pady=5)

        # mode
        ttk.Label(main, text="Mode").pack(anchor="w")
        self.mode_var = tk.StringVar(value="BACKGROUND")
        ttk.Combobox(main, textvariable=self.mode_var,
                     values=["BACKGROUND", "ACTIVE"]).pack(fill="x", pady=5)

        # durations
        ttk.Label(main, text="Durations").pack(anchor="w")
        self.entries = []
        for i in range(4):
            e = ttk.Entry(main)
            e.insert(0, str(BASE[i]))
            e.pack(fill="x", pady=2)
            self.entries.append(e)

        ttk.Button(main, text="Apply", command=self.apply).pack(pady=6)

        # controls
        ttk.Button(main, text="Start / Stop (\\)", command=toggle_running).pack(fill="x")
        ttk.Button(main, text="Pause (])", command=toggle_pause).pack(fill="x", pady=4)
        ttk.Button(main, text="FULL STOP (Numpad -)", command=full_stop).pack(fill="x")

        # debug
        self.status = ttk.Label(main, text="OFF")
        self.status.pack(anchor="w", pady=6)

        self.runtime = ttk.Label(main, text="Runtime: 00:00")
        self.runtime.pack(anchor="w")

        self.update_ui()

    def refresh(self):
        self.windows = get_windows()
        self.dropdown['values'] = [
            f"{name} | {title} | {hwnd}"
            for hwnd, title, name in self.windows
        ]

    def set_target(self):
        idx = self.dropdown.current()
        if idx >= 0:
            hwnd, title, name = self.windows[idx]
            set_target(hwnd)

    def apply(self):
        global BASE, mode
        with lock:
            for i in range(4):
                try:
                    BASE[i] = float(self.entries[i].get())
                except:
                    pass
            mode = self.mode_var.get()

    def update_ui(self):
        with lock:
            if running:
                self.status.config(text="PAUSED" if paused else "RUNNING")
                if start_time:
                    t = int(time.time() - start_time)
                    self.runtime.config(text=f"Runtime: {t//60:02}:{t%60:02}")
            else:
                self.status.config(text="OFF")

        self.root.after(100, self.update_ui)

    def run(self):
        self.root.mainloop()


# =========================
# HOTKEYS
# =========================
def on_press(key):
    try:
        if key.char == '\\':
            toggle_running()
        elif key.char == ']':
            toggle_pause()
    except:
        if hasattr(key, "vk") and key.vk == 109:
            full_stop()


# =========================
# MAIN
# =========================
app = App()

threading.Thread(
    target=lambda: keyboard.Listener(on_press=on_press).run(),
    daemon=True
).start()

app.run()