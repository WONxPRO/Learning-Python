import threading
import time
import random
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode, Key

# =========================
# INPUT CONTROLLER
# =========================
kb = Controller()

# =========================
# GLOBAL STATE
# =========================
running = False          # Main execution flag
paused = False           # Pause flag

step_index = 0           # Current step (0–3)
step_remaining = 0.0     # Remaining time for current step
current_keys = []        # Currently pressed keys

start_time = None        # When script started
last_reset_time = None   # 15-minute reset timer

lock = threading.RLock() # Reentrant lock (prevents deadlocks)

# =========================
# KEY DEFINITIONS
# =========================
A = KeyCode.from_char('a')
S = KeyCode.from_char('s')
R = KeyCode.from_char('r')
D = KeyCode.from_char('d')
W = KeyCode.from_char('w')
Z = KeyCode.from_char('z')

STEP_NAMES = ["S + R", "A + R", "S + R", "A + R"]

# Base durations (seconds)
BASE = [20.0, 20.0, 20.0, 20.0]

# =========================
# HELPER FUNCTIONS
# =========================
def rand_duration(base):
    """
    Adds slight randomness to avoid perfect repetition.
    """
    return base + random.uniform(0, 1)

def press_keys(keys):
    """
    Press multiple keys.
    """
    for k in keys:
        kb.press(k)

def release_keys(keys):
    """
    Release multiple keys.
    """
    for k in keys:
        kb.release(k)

def tap_key(key):
    """
    Press + release (single tap).
    """
    kb.press(key)
    kb.release(key)

def get_step_keys(idx):
    """
    Maps step index → key combination.
    """
    return [[S, R], [A, R], [R, S], [A, R]][idx]

def full_stop():
    """
    Completely stop execution and release all keys.
    Safe to call anytime.
    """
    global running, paused, step_index, step_remaining, current_keys
    with lock:
        running = False
        paused = False

        release_keys([S, A, R, D, W, Z])

        step_index = 0
        step_remaining = 0.0
        current_keys = []

def switch_step(direction):
    """
    Manual step override (left/right arrow).
    """
    global step_index, step_remaining, current_keys

    with lock:
        if not running:
            return

        release_keys(current_keys)

        step_index = (step_index + direction) % 4
        step_remaining = rand_duration(BASE[step_index])
        current_keys = get_step_keys(step_index)

        if not paused:
            press_keys(current_keys)

# =========================
# WORKER THREAD
# =========================
def worker():
    """
    Core execution loop.

    Uses real-time delta (dt) instead of fixed decrement.
    Prevents timing drift caused by sleep inaccuracies.
    """
    global running, paused, step_index, step_remaining, current_keys, last_reset_time

    last_tick = time.time()

    while True:
        time.sleep(0.005)  # yield CPU (not used for timing)

        now = time.time()
        dt = now - last_tick
        last_tick = now

        with lock:
            if not running:
                break

            # Pause handling
            if paused:
                release_keys(current_keys)
                continue

            # 10-minute reset logic
            if last_reset_time and (now - last_reset_time) >= 600:
                release_keys(current_keys)
                tap_key(Z)

                step_index = 0
                step_remaining = 0.0
                current_keys = []
                last_reset_time = now
                continue

            # Start new step if needed
            if step_remaining <= 0:
                step_remaining = rand_duration(BASE[step_index])
                current_keys = get_step_keys(step_index)
                press_keys(current_keys)

            # Decrease using real elapsed time
            step_remaining -= dt

            # Step finished → advance
            if step_remaining <= 0:
                release_keys(current_keys)
                step_index = (step_index + 1) % 4
                step_remaining = 0.0

    # Safe shutdown (no recursive lock calls)
    with lock:
        running = False
        paused = False
        release_keys([S, A, R, D, W, Z])
        step_index = 0
        step_remaining = 0.0
        current_keys = []

# =========================
# CONTROL FUNCTIONS
# =========================
def toggle_running():
    """
    Start or stop the worker thread.
    """
    global running, paused, start_time, last_reset_time

    with lock:
        if running:
            full_stop()
            return

        running = True
        paused = False
        start_time = time.time()
        last_reset_time = time.time()

    threading.Thread(target=worker, daemon=True).start()

def toggle_pause():
    """
    Toggle pause state.
    """
    global paused, current_keys

    with lock:
        if not running:
            return

        paused = not paused

        if not paused and current_keys:
            press_keys(current_keys)

# =========================
# OVERLAY UI
# =========================
class App:
    def __init__(self):
        self.root = tk.Tk()

        # Borderless overlay window
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.geometry("300x180+0+0")
        self.root.configure(bg="#0b0f14")

        # Styling
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel",
            background="#0b0f14",
            foreground="#e6edf3",
            font=("Segoe UI", 9)
        )

        style.configure("Header.TLabel",
            font=("Segoe UI", 10, "bold")
        )

        # Layout
        main = tk.Frame(self.root, bg="#0b0f14")
        main.pack(fill="both", expand=True, padx=8, pady=6)

        self.status = ttk.Label(main, text="STOPPED", style="Header.TLabel")
        self.status.pack(anchor="w")

        self.runtime = ttk.Label(main, text="00:00")
        self.runtime.pack(anchor="w")

        debug = tk.Frame(main, bg="#11161c")
        debug.pack(fill="both", expand=True, pady=(6, 0))

        self.keys_label = ttk.Label(debug, text="Keys: -")
        self.keys_label.pack(anchor="w", padx=6)

        self.step_label = ttk.Label(debug, text="Step: -")
        self.step_label.pack(anchor="w", padx=6)

        self.time_left_label = ttk.Label(debug, text="Remaining: -")
        self.time_left_label.pack(anchor="w", padx=6)

        self.update_ui()

    def format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m:02d}:{s:02d}"

    def update_ui(self):
        """
        Refresh UI every 50ms.
        """
        with lock:
            # Status
            if running:
                state = "PAUSED" if paused else "RUNNING"
            else:
                state = "STOPPED"
            self.status.config(text=state)

            # Runtime
            if start_time and running:
                elapsed = time.time() - start_time
                self.runtime.config(text=self.format_time(elapsed))

            # Active keys
            if current_keys:
                names = []
                for k in current_keys:
                    if hasattr(k, 'char') and k.char:
                        names.append(k.char.upper())
                    else:
                        names.append(str(k))
                self.keys_label.config(text=f"Keys: {' + '.join(names)}")
            else:
                self.keys_label.config(text="Keys: -")

            # Step + time remaining
            self.step_label.config(text=f"Step: {STEP_NAMES[step_index]}")
            self.time_left_label.config(text=f"Remaining: {step_remaining:.2f}s")

        self.root.after(50, self.update_ui)

    def run(self):
        self.root.mainloop()

# =========================
# KEY LISTENER
# =========================
def on_press(key):
    """
    Global hotkeys:
    \   → start/stop
    ]   → pause
    ← → → step control
    numpad - → full stop
    """
    try:
        if key.char == '\\':
            toggle_running()
        elif key.char == ']':
            toggle_pause()
    except AttributeError:
        if key == Key.right:
            switch_step(+1)
        elif key == Key.left:
            switch_step(-1)
        elif key == KeyCode.from_vk(109):
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