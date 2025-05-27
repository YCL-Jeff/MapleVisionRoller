import cv2
import numpy as np
import pyautogui
import pytesseract
import mss
from PIL import Image
import time

# 設置 Tesseract 可執行檔路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 確保滑鼠操作的安全性
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.6

def capture_screen(region):
    """使用 mss 截取螢幕指定區域，透過 PIL 轉換為 OpenCV 格式"""
    try:
        with mss.mss() as sct:
            monitor = {"left": region[0], "top": region[1], "width": region[2], "height": region[3]}
            screenshot = sct.grab(monitor)
            img_pil = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            img = np.array(img_pil)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            return img
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return None

def recognize_number(image):
    """使用 OCR 識別數字"""
    if image is None:
        return None
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)
        cv2.imwrite("D:\\Jeff\\python\\thresh_debug.png", thresh)
        text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        print(f"Tesseract raw output: '{text}'")
        print(f"Tesseract output type: {type(text)}")
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='ignore')
        cleaned_text = ''.join(filter(str.isdigit, text))
        return int(cleaned_text) if cleaned_text else None
    except Exception as e:
        print(f"OCR failed: {e}")
        return None

def click_dice(x, y):
    """點擊擲骰按鈕"""
    try:
        pyautogui.click(x, y)
        print(f"Clicked dice at ({x}, {y})")
    except Exception as e:
        print(f"Dice click failed: {e}")

def main():
    print("程式將在 3 秒後開始，請將遊戲窗口準備好...")
    print("確保遊戲在主螢幕，且座標正確！")
    print(f"螢幕解析度: {pyautogui.size()}")
    time.sleep(3)
    
    # 定義幸運和智力的區域
    region_luck = (1759, 884, 60, 40)  # Luck region
    region_int = (1759, 830, 60, 40)   # Int region
    dice_position = (1942, 885)        # Dice button (請確認是否正確)
    
    # 驗證座標是否在螢幕範圍內
    screen_width, screen_height = pyautogui.size()
    if region_luck[0] + region_luck[2] > screen_width or region_luck[1] + region_luck[3] > screen_height:
        print(f"錯誤：幸運區域 ({region_luck}) 超出螢幕範圍 ({screen_width}, {screen_height})")
        print("請使用以下程式重新測量座標：")
        print("""
import pyautogui
import time
while True:
    print(pyautogui.position())
    time.sleep(1)
""")
        return
    if region_int[0] + region_int[2] > screen_width or region_int[1] + region_int[3] > screen_height:
        print(f"錯誤：智力區域 ({region_int}) 超出螢幕範圍 ({screen_width}, {screen_height})")
        print("請使用以下程式重新測量座標：")
        print("""
import pyautogui
import time
while True:
    print(pyautogui.position())
    time.sleep(1)
""")
        return
    if dice_position[0] >= screen_width or dice_position[1] >= screen_height:
        print(f"錯誤：擲骰按鈕座標 ({dice_position[0]}, {dice_position[1]}) 超出螢幕範圍 ({screen_width}, {screen_height})")
        print("請使用以下程式重新測量座標：")
        print("""
import pyautogui
import time
while True:
    print(pyautogui.position())
    time.sleep(1)
""")
        return
    
    # 目標條件
    target_luck_1, target_int_1 = 5, 12
    target_luck_2, target_int_2 = 0, 13
    
    while True:
        # 截取幸運和智力區域
        screenshot_luck = capture_screen(region_luck)
        screenshot_int = capture_screen(region_int)
        
        if screenshot_luck is None or screenshot_int is None:
            print("截圖失敗，可能座標超出螢幕範圍或遊戲反截圖機制生效。請檢查控制台錯誤訊息。")
            break
        
        # 識別數字
        luck = recognize_number(screenshot_luck)
        int_val = recognize_number(screenshot_int)
        
        print(f"Luck: {luck}, Int: {int_val}")
        
        # 檢查是否達到目標
        if luck is not None and int_val is not None:
            if (luck == target_luck_1 and int_val == target_int_1) or \
               (luck == target_luck_2 and int_val == target_int_2):
                print("達到目標！停止擲骰")
                break
            else:
                print("未達目標，繼續擲骰...")
                click_dice(dice_position[0], dice_position[1])
        else:
            print("數字辨識失敗，檢查 D:\\Jeff\\python\\thresh_debug.png 或原始截圖是否清晰。")
        
        # 等待 0.6 秒
        time.sleep(0.6)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程式終止")
    except Exception as e:
        print(f"程式錯誤: {e}")