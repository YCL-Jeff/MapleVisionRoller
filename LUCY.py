import cv2
import numpy as np
import pyautogui
import pytesseract
import mss
from PIL import Image # 新增這一行
import time

# 設置 Tesseract 可執行檔路徑（確認正確路徑）
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
            
            # **關鍵修正：將 mss 截圖轉換為 PIL Image，再從 PIL Image 轉換為 NumPy 陣列**
            img_pil = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            img = np.array(img_pil) # PIL Image to NumPy array (RGB format)
            
            # 將 RGB 轉換為 BGR (OpenCV 預設)
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
        
        # --- 預處理調整區域 ---
        # 1. 縮放：根據數字大小調整 fx, fy。如果數字很小，可以嘗試更大倍數。
        #    interpolation 選擇 INTER_LANCZOS4 能夠保持較高的圖片品質。
        gray = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_LANCZOS4) 
        
        # 2. 高斯模糊去噪：
        #    如果您在 thresh_debug.png 中看到數字周圍有許多小點（噪點），才需要模糊。
        #    如果數字邊緣本身就模糊，嘗試更小核或移除這一步。
        #    這裡先將其註釋掉，除非您看到明顯的噪點。
        gray = cv2.GaussianBlur(gray, (3, 3), 0) 
        
        # 3. 自適應二值化：這是最關鍵的一步。
        #    - blockSize (第三個參數，奇數，大於1): 決定了計算閾值的鄰域大小。
        #      如果數字比較大，或者背景變化較大，可以嘗試更大的值 (如 21, 31)。
        #      如果數字較小且背景相對均勻，可以嘗試小一點的值 (如 9, 11)。
        #    - C (第四個參數): 從平均值中減去的值。可以用來微調亮度對比。
        #      正值會讓周圍區域更亮，負值會讓周圍區域更暗。通常在 2-10 之間調整。
        #    - THRESH_BINARY_INV: 讓數字變成白色（前景），背景變成黑色。這通常是 OCR 喜歡的格式。
        
        # 建議嘗試：
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5) 
        
        # 如果自適應二值化效果不好，可以嘗試簡單閾值 (如果背景均勻且對比度高)
        # ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV) # 180 可以調整
        
        # --- 預處理調整結束 ---

        # 保存預處理影像以供除錯
        cv2.imwrite("D:\\Jeff\\python\\thresh_debug.png", thresh) 
        
        # Tesseract 數字白名單
        # config='--psm 7 -c tessedit_char_whitelist=0123456789'
        # --psm 7: 將圖片視為單行文字。這通常對辨識單個數字更有利。
        # --psm 6: 將圖片視為單一均勻的文字區塊。也可以繼續使用。
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
    
    # 定義幸運和敏捷的區域（請更新為正確座標）
    # 請再次確認這些寬高是否準確。
    # 定義幸運和敏捷的區域
    region_luck = (1759, 884, 60, 40) # Luck region: (X, Y, Width, Height)
    region_dex =  (1759, 830, 60, 40) # Dex region: (X, Y, Width, Height)
    dice_position = (1942, 885)      # Dice button (請確認是否正確)
    
    # 驗證座標是否在螢幕範圍內
    screen_width, screen_height = pyautogui.size()
    
    # 檢查 luck 區域的右下角
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
    
    # 檢查 dex 區域的右下角
    if region_dex[0] + region_dex[2] > screen_width or region_dex[1] + region_dex[3] > screen_height:
        print(f"錯誤：敏捷區域 ({region_dex}) 超出螢幕範圍 ({screen_width}, {screen_height})")
        print("請使用以下程式重新測量座標：")
        print("""
import pyautogui
import time
while True:
    print(pyautogui.position())
    time.sleep(1)
""")
        return

    # 檢查擲骰按鈕座標
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
    target_luck_1, target_dex_1 = 5, 12
    target_luck_2, target_dex_2 = 4, 13
    
    while True:
        # 截取幸運和敏捷區域
        screenshot_luck = capture_screen(region_luck)
        screenshot_dex = capture_screen(region_dex)
        
        if screenshot_luck is None or screenshot_dex is None:
            print("截圖失敗，可能座標超出螢幕範圍或遊戲反截圖機制生效。請檢查控制台錯誤訊息。")
            break # 截圖失敗直接跳出循環，避免無限循環
        
        # 識別數字
        luck = recognize_number(screenshot_luck)
        dex = recognize_number(screenshot_dex)
        
        print(f"Luck: {luck}, Dex: {dex}")
        
        # 檢查是否達到目標
        if luck is not None and dex is not None:
            if (luck == target_luck_1 and dex == target_dex_1) or \
               (luck == target_luck_2 and dex == target_dex_2):
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