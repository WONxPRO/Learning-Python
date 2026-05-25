from pynput import keyboard, mouse

# =========================
# KEYBOARD HANDLER
# =========================
def on_press(key):
    try:
        # Normal keys (letters, numbers)
        print(f'Pressed Keyboard "{key.char}"')
    except AttributeError:
        # Special keys (shift, ctrl, etc.)
        print(f'Pressed Special Key "{key}"')

# =========================
# MOUSE HANDLER
# =========================
def on_click(x, y, button, pressed):
    if pressed:
        print(f'Mouse Clicked {button} at ({x}, {y})')

# =========================
# LISTENERS
# =========================
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

keyboard_listener.join()
mouse_listener.join()