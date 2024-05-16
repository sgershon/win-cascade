import sys
import time

import pygetwindow
from screeninfo import get_monitors

wins = sorted(pygetwindow.getAllWindows(), key=lambda x: x.left)

window_gap = 30
window_index = 0
width, height = 900, 400

monitors = get_monitors()

def debug(msg):
    if "debug" in sys.argv:
        print(msg)

for monitor in monitors:
    fr = monitor.x
    to = monitor.x + monitor.width

    wins_here = [win for win in wins if fr < win.centerx < to]
    
    fr_x = fr
    fr_y = 0
    window_index = 0

    for i, win in enumerate(wins_here):
        debug(f"{i}, {win}")
        if win.title:
            if win.title in ["Windows Input Experience", "Settings", "Setup", "Cascade", "MobaXterm"]:
                debug(f"\t\t- Skipping {win.title}, excepted window")
                continue
            if not win.visible:
                debug(f"\t\t- Skipping {win.title}, not visible")
                continue

            debug(f"\t {(win.title, win.left, win.centerx, win.right, win.isActive, win.visible, win.isMinimized, win.isMaximized, win.size)}")
        
            try:
                win.activate()
                pass
            except pygetwindow.PyGetWindowException as e:
                debug(f"\t\t- Can't activate {win.title}")
                continue
            time.sleep(1)
        
            win.restore()
            time.sleep(0.5)

            win.resizeTo(width, height)
            new_x, new_y = fr_x + (window_index * window_gap), fr_y + (window_index * window_gap)
            debug(f"\t\t {new_x}, {new_y}")
            win.moveTo(new_x, new_y)
            print(f"* ({i}/{len(wins)}) cascading to {new_x},{new_y}: {win.title}")

            window_index += 1

print()
