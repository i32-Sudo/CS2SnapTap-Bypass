import keyboard
import random
import time
import ctypes

pressed_keys = set()

# Constants
ReleaseminMs = 30
ReleasemaxMs = 70
TICK_64_MS = 0.0156 # Change as needed to account for Ping & FPS, If you have High FPS & Low Ping do not change

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
            delayms = random.randint(ReleaseminMs, ReleasemaxMs)
            time.sleep(delayms / 1000.0)
            keyboard.release('d')
        
        elif event.name == 'd' and 'a' in pressed_keys:
            delayms = random.randint(ReleaseminMs, ReleasemaxMs)
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

def main():
    ctypes.windll.kernel32.SetConsoleTitleW(str("Notepad - " + str(random.randint(5, 5000)) + ".txt"))
    # Add exit hotkey
    keyboard.add_hotkey(exit_key, lambda: exit())
    
    # Hook keyboard events for SnapTap
    keyboard.hook(SnapTap)


    while True:
        if keyboard.is_pressed(activation_key) and mode == 'SnapTap':
            send_space(TICK_64_MS * 1)
            while keyboard.is_pressed(activation_key):
                send_space(TICK_64_MS * 2)
        else:
            time.sleep(0.001)  # prevent CPU overload

if __name__ == "__main__":
    main()
