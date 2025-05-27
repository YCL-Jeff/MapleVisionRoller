import pyautogui
import time

while True:
    x, y = pyautogui.position()
    print(f"滑鼠座標: ({x}, {y})")
    time.sleep(1)