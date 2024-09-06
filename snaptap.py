import keyboard
import random
import time
import ctypes
import pygetwindow as gw
from pynput.mouse import Controller, Button    
from colorama import Fore

pressed_keys = set()

# Constants
RELEASE_MIN_MS = 20 # Lower Values results in quicker movements
RELEASE_MAX_MS = 30
COUNTER_STRAFE_MIN_MS = 7 # Lower values results in quicker movements but less counter-strafe snapping
COUNTER_STRAFE_MAX_MS = 7 # 0.5x - 7=700ms
COUNTER_STRAFE_KEY = 'alt'
TICK_64_MS = 0.0156 # This is set for a Ping of 40~, For every 10ms ping above this add 0.0005 to it, Do not use if you are above 80ms ping
key_press_times = {}

exit_key = "end"
activation_key = "space"  # Adjust based on your bhop button

# Set default mode
mode = 'SnapTap'

SnapTapIRQ = False
CounterStrafeIRQ = False

def is_window_in_focus(window_title):
    focused_window = gw.getActiveWindow()
    return focused_window and focused_window.title == window_title

def SnapTap(event):
    time.sleep(0.001)  # prevent CPU overload
    global SnapTapIRQ
    if event.event_type == 'down':
        #pressed_keys.add(event.name)
        #print(f"{Fore.LIGHTBLACK_EX}[KeyDetection] {event.name} / {event.event_type}")
        if (CounterStrafeIRQ == True):
            return

        if event.name == 'a' and 'd' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys and activation_key not in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('d')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Release ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}{delayms / 1000.0}ms")
        
        elif event.name == 'd' and 'a' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys and activation_key not in pressed_keys:
            delayms = random.randint(RELEASE_MIN_MS, RELEASE_MAX_MS)
            time.sleep(delayms / 1000.0)
            keyboard.release('a')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Release ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}{delayms / 1000.0}ms")
        
    elif event.event_type == 'up':
        #pressed_keys.discard(event.name)
        if (CounterStrafeIRQ == True):
            return
        #print(f"{Fore.LIGHTBLACK_EX}[KeyDetection] {event.name} / {event.event_type}")

        if event.name == 'd' and 'a' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys and activation_key not in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('a')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}0.02ms")
        
        elif event.name == 'a' and 'd' in pressed_keys and is_window_in_focus("Counter-Strike 2") and COUNTER_STRAFE_KEY not in pressed_keys and activation_key not in pressed_keys:
            #delayms = random.randint(SetminMs, SetmaxMs)
            keyboard.press('d')
            print(f"{Fore.LIGHTRED_EX}[SnapTap]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}A/D {Fore.YELLOW}0.02ms")


def CounterStrafe(event):
    global CounterStrafeIRQ
    time.sleep(0.001)  # prevent CPU overload

    if 'a' in pressed_keys and 'd' in pressed_keys:
        return
    if event.event_type == 'up' and COUNTER_STRAFE_KEY in pressed_keys and is_window_in_focus("Counter-Strike 2") and activation_key not in pressed_keys:
        #print(f"{Fore.LIGHTBLACK_EX}[KeyDetection] {event.name} / {event.event_type}")

        #if event.name == 'alt' and is_window_in_focus("Counter-Strike 2"):
            #keyboard.release("ctrl")
            #keyboard.send("ctrl")

        # If both keys were previously pressed, do nothing
        if 'a' in pressed_keys and 'd' in pressed_keys:
            return
        if 'shift' in pressed_keys or 'ctrl' in pressed_keys:
            return
        
        # If 'A' is released and 'D' is not still held down, counterstrafe with 'D'
        if event.name == 'a' and 'd' not in pressed_keys and is_window_in_focus("Counter-Strike 2"):
            CounterStrafeIRQ = True
            RNG = random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS)
            for i in range(1, RNG):
                if ('a' in pressed_keys) or ('a' in pressed_keys and 'd' in pressed_keys):
                    print(f"{Fore.BLACK}[WATCHDOG] IRQ Interrupt in CounterStrafe.")
                    return
                keyboard.press('d')
                time.sleep(0.01)
                keyboard.release('d')
            print(f"{Fore.LIGHTBLUE_EX}[CounterStrafe]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}{COUNTER_STRAFE_KEY} {Fore.YELLOW}0.{RNG}ms")

        # If 'D' is released and 'A' is not still held down, counterstrafe with 'A'
        elif event.name == 'd' and 'a' not in pressed_keys and is_window_in_focus("Counter-Strike 2"):
            CounterStrafeIRQ = True
            RNG = random.randint(COUNTER_STRAFE_MIN_MS, COUNTER_STRAFE_MAX_MS)
            for i in range(1, RNG):
                if ('d' in pressed_keys) or ('d' in pressed_keys and 'a' in pressed_keys):
                    print(f"{Fore.BLACK}[WATCHDOG] IRQ Interrupt in CounterStrafe.")
                    return
                keyboard.press('a')
                time.sleep(0.01)
                keyboard.release('a')
            print(f"{Fore.LIGHTBLUE_EX}[CounterStrafe]{Fore.LIGHTBLACK_EX} Send Hold ({event.name}) Input {Fore.WHITE}{COUNTER_STRAFE_KEY} {Fore.YELLOW}0.{RNG}ms")
        CounterStrafeIRQ = False
        #pressed_keys.discard(event.name) # Remove if you have delay issues but this ensures the CounterStrafing & SnapTap Dont interfere with eachother

def watchdog(event):
    if (event.event_type == 'down'):
        pressed_keys.add(event.name)
    if (event.event_type == 'up'):
        pressed_keys.discard(event.name)

def main():
    keyboard.unhook_all()
    keyboard.unhook_all_hotkeys()
    print(f"{Fore.RED}Unhooked All\nUnhooked All Hotkeys")
    ctypes.windll.kernel32.SetConsoleTitleW(str("Notepad - " + str(random.randint(5, 5000)) + ".txt"))
    # Add exit hotkey
    keyboard.add_hotkey(exit_key, lambda: exit())
    
    # Hook keyboard events for SnapTap
    keyboard.hook(watchdog)
    keyboard.hook(CounterStrafe)
    keyboard.hook(SnapTap)

    mouse = Controller()
    while True:
        if keyboard.is_pressed(activation_key) and mode == 'SnapTap' and is_window_in_focus("Counter-Strike 2"):
            #print(f"{Fore.LIGHTBLACK_EX}[KeyDetection] space / down")
            print(f"{Fore.LIGHTMAGENTA_EX}[BHOP]{Fore.LIGHTBLACK_EX} Send Key (space) Input {Fore.WHITE}{activation_key} {Fore.YELLOW}{TICK_64_MS}/tps")
            mouse.scroll(0, -1) # Mouse Scroll is better because spacebar can get stuck on its own inputs
            #keyboard.send('space')
            time.sleep(TICK_64_MS * 1)
            while keyboard.is_pressed(activation_key):
                print(f"{Fore.LIGHTMAGENTA_EX}[BHOP]{Fore.LIGHTBLACK_EX} Send Key (space) Input {Fore.WHITE}{activation_key} {Fore.YELLOW}{TICK_64_MS}/tps")
                mouse.scroll(0, -1) # Mouse Scroll is better because spacebar can get stuck on its own inputs
                #keyboard.send('space')
                time.sleep(TICK_64_MS * 2)
        else:
            time.sleep(0.001)  # prevent CPU overload

if __name__ == "__main__":
    main()
