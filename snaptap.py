import keyboard
import random
import time
import ctypes

pressed_keys = set()

# Constants
RELEASE_MIN_MS = 30
RELEASE_MAX_MS = 70
COUNTER_STRAFE_MIN_MS = 30
COUNTER_STRAFE_MAX_MS = 75
COUNTER_STRAFE_KEY = 'alt'
TICK_64_MS = 0.0156 # Change as needed to account for Ping & FPS, If you have High FPS & Low Ping do not change
key_press_times = {}

exit_key = "end"
activation_key = "space"  # Adjust based on your bhop button

# Set default mode
mode = 'SnapTap'

def send_space(duration):
    keyboard.send("space")
    time.sleep(duration)

def SnapTap(event):
    if event.event_type == 'down':
        pressed_keys.add(event.name)
        
        if event.name == 'a' and 'd' in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('d')
        
        elif event.name == 'd' and 'a' in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('a')
        
    elif event.event_type == 'up':
        pressed_keys.discard(event.name)
        
        if event.name == 'd' and 'a' in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('a')
        
        elif event.name == 'a' and 'd' in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('d')

def CounterStrafe(event):
    if 'a' in pressed_keys and 'd' in pressed_keys:
        return
    if event.event_type == 'up' and COUNTER_STRAFE_KEY in pressed_keys:
        # If both keys were previously pressed, do nothing
        if 'a' in pressed_keys and 'd' in pressed_keys:
            return

        # If 'A' is released and 'D' is not still held down, counterstrafe with 'D'
        if event.name == 'a' and 'd' not in pressed_keys:
            keyboard.press('d')
            time.sleep(random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS) / 1000.0)
            keyboard.release('d')

        # If 'D' is released and 'A' is not still held down, counterstrafe with 'A'
        elif event.name == 'd' and 'a' not in pressed_keys:
            keyboard.press('a')
            time.sleep(random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS) / 1000.0)
            keyboard.release('a')
        pressed_keys.discard(event.name) # Remove if you have delay issues but this ensures the CounterStrafing & SnapTap Dont interfere with eachother

def main():
    ctypes.windll.kernel32.SetConsoleTitleW(str("Notepad - " + str(random.randint(5, 5000)) + ".txt"))
    # Add exit hotkey
    keyboard.add_hotkey(exit_key, lambda: exit())
    
    # Hook keyboard events for SnapTap
    keyboard.hook(SnapTap)
    keyboard.hook(CounterStrafe)

    while True:
        if keyboard.is_pressed(activation_key) and mode == 'SnapTap':
            send_space(TICK_64_MS * 1)
            while keyboard.is_pressed(activation_key):
                send_space(TICK_64_MS * 2)
        else:
            time.sleep(0.001)  # prevent CPU overload

if __name__ == "__main__":
    main()
