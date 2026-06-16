import time
import threading
import ctypes
import pyautogui
from mss import mss
import tkinter as tk
from pynput import keyboard

# =========================
# DPI FIX
# =========================
ctypes.windll.user32.SetProcessDPIAware()

# =========================
# CONFIG
# =========================
BOX_SIZE = 10
TARGET_COLOR = (141, 63, 148)
TOLERANCE = 40
DELAY = 0.01

running = False
detected = False

# =========================
# OVERLAY STATE
# =========================
overlay_ready = False
canvas_ref = None
rect_id = None
root_ref = None

status_root = None
status_label = None

# =========================
# COLOR MATCH
# =========================
def color_match(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

# =========================
# SCREEN / REGION
# =========================
screen_width, screen_height = pyautogui.size()
center_x = screen_width // 2
center_y = screen_height // 2

def compute_region():
    return {
        "left": center_x - BOX_SIZE // 2,
        "top": center_y - BOX_SIZE // 2,
        "width": BOX_SIZE,
        "height": BOX_SIZE
    }

region = compute_region()

# =========================
# OVERLAY BOX
# =========================
def create_overlay():
    global canvas_ref, rect_id, overlay_ready, root_ref

    root = tk.Tk()
    root_ref = root

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "white")

    root.geometry(f"{region['width']}x{region['height']}+{region['left']}+{region['top']}")

    canvas = tk.Canvas(root, width=region['width'], height=region['height'],
                       bg="white", highlightthickness=0)
    canvas.pack()

    rect = canvas.create_rectangle(
        0, 0, region['width'], region['height'],
        outline="#550000", width=2
    )

    canvas_ref = canvas
    rect_id = rect
    overlay_ready = True

    root.mainloop()

def update_overlay_visual():
    if not overlay_ready:
        return

    if not running:
        color = "#550000"  # idle (dim red)
    else:
        color = "#00FF00" if detected else "#FF0000"

    canvas_ref.after(0, lambda: canvas_ref.itemconfig(rect_id, outline=color))

def move_overlay():
    if root_ref:
        root_ref.after(0, lambda:
            root_ref.geometry(f"{region['width']}x{region['height']}+{region['left']}+{region['top']}")
        )

# =========================
# STATUS WINDOW
# =========================
def create_status_window():
    global status_root, status_label

    root = tk.Tk()
    status_root = root

    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.geometry("220x60+0+0")

    label = tk.Label(root, text="INIT",
                     font=("Consolas", 10, "bold"),
                     fg="white", bg="black", justify="left", anchor="w")
    label.pack(fill="both", expand=True)

    status_label = label
    root.mainloop()

def update_status():
    if not status_root:
        return

    text = (
        f"{'ON' if running else 'OFF'} | "
        f"{'TRUE' if detected else 'FALSE'}"
    )

    color = "#00FF00" if detected else "#FF0000"

    status_root.after(0, lambda: status_label.config(text=text, fg=color))

threading.Thread(target=create_overlay, daemon=True).start()
threading.Thread(target=create_status_window, daemon=True).start()

# =========================
# MOVEMENT
# =========================
def move_checker(dx, dy):
    global center_x, center_y, region

    center_x += dx
    center_y += dy

    center_x = max(0, min(center_x, screen_width - 1))
    center_y = max(0, min(center_y, screen_height - 1))

    region = compute_region()
    move_overlay()

# =========================
# KEYBOARD
# =========================
def on_press(key):
    global running

    try:
        if key.char == '\\':
            running = not running
    except AttributeError:
        if key == keyboard.Key.up:
            move_checker(0, -1)
        elif key == keyboard.Key.down:
            move_checker(0, 1)
        elif key == keyboard.Key.left:
            move_checker(-1, 0)
        elif key == keyboard.Key.right:
            move_checker(1, 0)

keyboard.Listener(on_press=on_press).start()

# =========================
# MAIN LOOP
# =========================
with mss() as sct:
    while True:

        if not running:
            detected = False
            update_overlay_visual()
            update_status()
            time.sleep(0.05)
            continue

        screenshot = sct.grab(region)
        pixels = screenshot.rgb

        width = screenshot.width
        height = screenshot.height

        cx = width // 2
        cy = height // 2
        i = (cy * width + cx) * 3

        pixel = (pixels[i], pixels[i+1], pixels[i+2])
        detected = color_match(pixel, TARGET_COLOR, TOLERANCE)

        update_overlay_visual()
        update_status()

        time.sleep(DELAY)