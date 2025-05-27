import mss
import cv2
import numpy as np
with mss.mss() as sct:
    monitor = {"left": 1756, "top": 834, "width": 54, "height": 41}
    screenshot = sct.grab(monitor)
    img = np.array(screenshot, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    cv2.imwrite("D:\\Jeff\\python\\luck_mss.png", img)
    monitor = {"left": 1759, "top": 884, "width": 58, "height": 30}
    screenshot = sct.grab(monitor)
    img = np.array(screenshot, dtype=np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    cv2.imwrite("D:\\Jeff\\python\\dex_mss.png", img)