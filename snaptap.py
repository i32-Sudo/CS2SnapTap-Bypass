import keyboard
import random
import time
import ctypes
import pygetwindow as gw
from colorama import Fore

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

def is_window_in_focus(window_title):
    focused_window = gw.getActiveWindow()
    return focused_window and focused_window.title == window_title

def SnapTap(event):
    time.sleep(0.001)  # prevent CPU overload
    if event.event_type == 'down':
        pressed_keys.add(event.name)
        
        if event.name == 'a' and 'd' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('d')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Release ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}{delayms / 1000.0}ms")
        
        elif event.name == 'd' and 'a' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('a')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Release ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}{delayms / 1000.0}ms")
        
    elif event.event_type == 'up':
        pressed_keys.discard(event.name)
        
        if event.name == 'd' and 'a' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('a')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}0.02ms")
        
        elif event.name == 'a' and 'd' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('d')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}0.02ms")


def CounterStrafe(event):
    time.sleep(0.001)  # prevent CPU overload
    if 'a' in pressed_keys and 'd' in pressed_keys:
        return
    if event.event_type == 'up' and COUNTER_STRAFE_KEY in pressed_keys and is_window_in_focus("Counter-Strike 2"):
        # If both keys were previously pressed, do nothing
        if 'a' in pressed_keys and 'd' in pressed_keys:
            return

        # If 'A' is released and 'D' is not still held down, counterstrafe with 'D'
        if event.name == 'a' and 'd' not in pressed_keys and is_window_in_focus("Counter-Strike 2"):
            keyboard.press('d')
            delayms = random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS) / 1000.0
            time.sleep(delayms)
            keyboard.release('d')
            print(f"{Fore.LIGHTBLUE_EX}[CounterStrafe]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}{COUNTER_STRAFE_KEY} {Fore.YELLOW}{delayms}ms")

        # If 'D' is released and 'A' is not still held down, counterstrafe with 'A'
        elif event.name == 'd' and 'a' not in pressed_keys and is_window_in_focus("Counter-Strike 2"):
            print(f"{Fore.LIGHTBLUE_EX}[CounterStrafe]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}{COUNTER_STRAFE_KEY}")
            keyboard.press('a')
            delayms = random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS) / 1000.0
            time.sleep(delayms)
            print(f"{Fore.LIGHTBLUE_EX}[CounterStrafe]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}{COUNTER_STRAFE_KEY} {Fore.YELLOW}{delayms}ms")
            keyboard.release('a')
        pressed_keys.discard(event.name) # Remove if you have delay issues but this ensures the CounterStrafing & SnapTap Dont interfere with eachother

def main():
    keyboard.unhook_all()
    keyboard.unhook_all_hotkeys()
    ctypes.windll.kernel32.SetConsoleTitleW(str("Notepad - " + str(random.randint(5, 5000)) + ".txt"))
    # Add exit hotkey
    keyboard.add_hotkey(exit_key, lambda: exit())
    
    # Hook keyboard events for SnapTap
    keyboard.hook(SnapTap)
    keyboard.hook(CounterStrafe)

    while True:
        if keyboard.is_pressed(activation_key) and mode == 'SnapTap' and is_window_in_focus("Counter-Strike 2"):
            print(f"{Fore.LIGHTMAGENTA_EX}[BHOP]{Fore.LIGHTBLACK_EX} Send Key (space) Input {Fore.WHITE}{activation_key} {Fore.YELLOW}{TICK_64_MS}/tps")
            keyboard.send("space")
            time.sleep(TICK_64_MS * 1)
            while keyboard.is_pressed(activation_key):
                print(f"{Fore.LIGHTMAGENTA_EX}[BHOP]{Fore.LIGHTBLACK_EX} Send Key (space) Input {Fore.WHITE}{activation_key} {Fore.YELLOW}{TICK_64_MS}/tps")
                keyboard.send("space")
                time.sleep(TICK_64_MS * 2)
        else:
            time.sleep(0.001)  # prevent CPU overload

if __name__ == "__main__":
    main()
