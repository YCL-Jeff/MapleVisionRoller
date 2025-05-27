import pytesseract

# 請將這裡的路徑替換為您實際安裝 Tesseract OCR 的路徑
# 確保路徑完全符合，包括大小寫和斜線方向 (Windows 通常用反斜線 '\'，但 Python 建議用 r'...' 處理)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 接著您的原有程式碼
print(pytesseract.get_tesseract_version())
# ... 其他使用 pytesseract 的程式碼 ...