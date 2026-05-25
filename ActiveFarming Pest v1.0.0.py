import threading
import time
import random
import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from pynput.keyboard import Controller, KeyCode, Key
from pynput.mouse import Controller as MouseController, Button

# =========================
# CONTROLLERS
# =========================
kb = Controller()
mouse = MouseController()

# =========================
# GLOBAL STATE
# =========================
running = False
paused = False
mode = "IDLE"

step_index = 0
step_remaining = 0.0
current_keys = []

start_time = None
last_reset_time = None

lock = threading.RLock()

# =========================
# KEYS
# =========================
A = KeyCode.from_char('a')
S = KeyCode.from_char('s')
R = KeyCode.from_char('r')
D = KeyCode.from_char('d')
W = KeyCode.from_char('w')
Z = KeyCode.from_char('z')

STEP_NAMES = ["S + R", "A + R", "S + R", "A + R"]
BASE = [20.0, 20.0, 20.0, 20.0]

# =========================
# COORDINATES
# =========================
EQUIP_BTN = (966, 467)
SLOT_1 = (814, 599)
SLOT_2 = (861, 596)
SLOT_3 = (880, 597)
SLOT_4 = (927, 600)

# =========================
# HELPERS
# =========================
def rand_duration(base):
    return base + random.uniform(0, 1)

def press_keys(keys):
    for k in keys:
        kb.press(k)

def release_keys(keys):
    for k in keys:
        kb.release(k)

def tap(k, d=0.1):
    kb.press(k)
    kb.release(k)
    time.sleep(d)

def press_char(c, d=0.1):
    tap(KeyCode.from_char(c), d)

def click(x, y, pre=0.0, post=0.0):
    if pre > 0:
        time.sleep(pre)
    mouse.position = (x, y)
    mouse.click(Button.left, 1)
    if post > 0:
        time.sleep(post)

def rclick(d=0.1):
    mouse.click(Button.right, 1)
    time.sleep(d)

def get_step_keys(idx):
    return [[S, R], [A, R], [R, S], [A, R]][idx]

def format_time(sec):
    m = int(sec // 60)
    s = int(sec % 60)
    return f"{m:02d}:{s:02d}"

def full_stop():
    global running, paused, step_index, step_remaining, current_keys, mode
    with lock:
        running = False
        paused = False
        mode = "IDLE"
        release_keys([S, A, R, D, W, Z])
        step_index = 0
        step_remaining = 0.0
        current_keys = []

# =========================
# MODE 1 — FARM LOOP
# =========================
def worker():
    global running, paused, step_index, step_remaining, current_keys, last_reset_time, mode

    last_tick = time.time()

    while True:
        time.sleep(0.005)
        now = time.time()
        dt = now - last_tick
        last_tick = now

        with lock:
            if not running:
                break

            mode = "FARM"

            if paused:
                release_keys(current_keys)
                continue

            if last_reset_time and (now - last_reset_time) >= 600:
                release_keys(current_keys)
                tap(Z)
                step_index = 0
                step_remaining = 0
                current_keys = []
                last_reset_time = now
                continue

            if step_remaining <= 0:
                step_remaining = rand_duration(BASE[step_index])
                current_keys = get_step_keys(step_index)
                press_keys(current_keys)

            step_remaining -= dt

            if step_remaining <= 0:
                release_keys(current_keys)
                step_index = (step_index + 1) % 4
                step_remaining = 0

    full_stop()

def toggle_running():
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
    global paused
    with lock:
        if running:
            paused = not paused

def switch_step(direction):
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
# MODE 2 — FARM → KILL (1s delays)
# =========================
def to_kill():
    global mode
    full_stop()
    time.sleep(0.2)
    mode = "KILL"

    # numpad +
    kb.press(KeyCode.from_vk(107))
    kb.release(KeyCode.from_vk(107))
    time.sleep(1.0)

    # E
    kb.press(KeyCode.from_char('e'))
    kb.release(KeyCode.from_char('e'))
    time.sleep(1.0)

    # equipment + slots
    mouse.position = EQUIP_BTN
    mouse.click(Button.left, 1)
    time.sleep(1.0)

    mouse.position = SLOT_1
    mouse.click(Button.left, 1)
    time.sleep(1.0)

    mouse.position = SLOT_2
    mouse.click(Button.left, 1)
    time.sleep(1.0)

    mouse.position = SLOT_3
    mouse.click(Button.left, 1)
    time.sleep(1.0)

    mouse.position = SLOT_4
    mouse.click(Button.left, 1)
    time.sleep(1.0)

    # ESC
    kb.press(Key.esc)
    kb.release(Key.esc)
    time.sleep(1.0)

    # 8
    kb.press(KeyCode.from_char('8'))
    kb.release(KeyCode.from_char('8'))
    time.sleep(1.0)

    # right click
    mouse.click(Button.right, 1)
    time.sleep(1.0)


# =========================
# MODE 3 — KILL → FARM (1s delays)
# =========================
def to_farm():
    global mode
    full_stop()
    time.sleep(0.2)
    mode = "FARM"

    # E
    kb.press(KeyCode.from_char('e'))
    kb.release(KeyCode.from_char('e'))
    time.sleep(0.5)

    # equipment + slots
    mouse.position = EQUIP_BTN
    mouse.click(Button.left, 1)
    time.sleep(0.7)

    mouse.position = SLOT_1
    mouse.click(Button.right, 1)
    time.sleep(0.7)

    mouse.position = SLOT_2
    mouse.click(Button.left, 1)
    time.sleep(0.7)

    mouse.position = SLOT_3
    mouse.click(Button.right, 1)
    time.sleep(0.7)

    mouse.position = SLOT_4
    mouse.click(Button.left, 1)
    time.sleep(0.7)

    # ESC
    kb.press(Key.esc)
    kb.release(Key.esc)

    # 8 + right click
    kb.press(KeyCode.from_char('8'))
    kb.release(KeyCode.from_char('8'))
    time.sleep(0.2)

    mouse.click(Button.right, 1)
    time.sleep(0.2)

    # remaining actions
    kb.press(KeyCode.from_char('z'))
    kb.release(KeyCode.from_char('z'))

    kb.press(KeyCode.from_char('4'))
    kb.release(KeyCode.from_char('4'))

    kb.press(Key.space)
    time.sleep(0.3)
    kb.release(Key.space)
    mouse.click(Button.left, 1)
    time.sleep(0.5)

    kb.press(KeyCode.from_char('2'))
    kb.release(KeyCode.from_char('2'))
    time.sleep(1.0)

# =========================
# UI
# =========================
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.88)
        self.root.geometry("260x200+0+0")
        self.root.configure(bg="#0f1115")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#0f1115", foreground="#e6edf3", font=("Segoe UI", 9))

        frame = tk.Frame(self.root, bg="#0f1115")
        frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.status = ttk.Label(frame, text="MODE: IDLE")
        self.status.pack(anchor="w")

        self.runtime = ttk.Label(frame, text="TIME: 00:00")
        self.runtime.pack(anchor="w")

        self.step = ttk.Label(frame, text="STEP: -")
        self.step.pack(anchor="w")

        self.keys = ttk.Label(frame, text="KEYS: -")
        self.keys.pack(anchor="w")

        ttk.Label(frame, text="").pack()

        ttk.Label(frame, text="[NUM0] Start/Stop").pack(anchor="w")
        ttk.Label(frame, text="[NUM1] Pause").pack(anchor="w")
        ttk.Label(frame, text="[NUM+] Kill Mode").pack(anchor="w")
        ttk.Label(frame, text="[NUM-] Farm Mode").pack(anchor="w")
        ttk.Label(frame, text="[NUM*] Stop").pack(anchor="w")

        self.update()

    def update(self):
        with lock:
            self.status.config(text=f"MODE: {mode}")

            if running and start_time:
                self.runtime.config(text=f"TIME: {format_time(time.time()-start_time)}")

            self.step.config(text=f"STEP: {STEP_NAMES[step_index]}")

            if current_keys:
                names = [k.char.upper() if hasattr(k, 'char') else str(k) for k in current_keys]
                self.keys.config(text="KEYS: " + " + ".join(names))
            else:
                self.keys.config(text="KEYS: -")

        self.root.after(50, self.update)

    def run(self):
        self.root.mainloop()

# =========================
# HOTKEYS
# =========================
def on_press(key):
    try:
        vk = key.vk
    except:
        return

    if vk == 96:
        toggle_running()
    elif vk == 97:
        toggle_pause()
    elif vk == 107:
        threading.Thread(target=to_kill, daemon=True).start()
    elif vk == 109:
        threading.Thread(target=to_farm, daemon=True).start()
    elif vk == 106:
        full_stop()

    elif key == Key.right:
        switch_step(+1)
    elif key == Key.left:
        switch_step(-1)

# =========================
# MAIN
# =========================
app = App()

threading.Thread(
    target=lambda: keyboard.Listener(on_press=on_press).run(),
    daemon=True
).start()

app.run()