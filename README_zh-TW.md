# MapleVisionRoller

一個基於電腦視覺的工具，透過 OCR 和 DirectX 截圖技術，自動化數值識別。

**⚠️ 注意**：本專案僅用於**學習用途**。

## 功能
- 使用 `mss` 截圖。
- 透過 `pytesseract` 和 OpenCV 識別數值。
- 自動擲骰直到達到目標屬性。
- 可自訂螢幕座標，適應不同 UI 配置。

## 前置條件
- Python 3.12
- Tesseract OCR 安裝於 `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Python 套件見 `requirements.txt`

## 安裝
1. 複製儲存庫：
   ```bash
   git clone https://github.com/YCL-Jeff/MapleVisionRoller.git
   cd MapleVisionRoller
   ```
2. 安裝 Tesseract OCR：
   - 從 [UB-Mannheim Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki) 下載。
   - 安裝至 `C:\Program Files\Tesseract-OCR\`。
   - 若安裝在其他位置，請修改 `prog/LUCY.py` 中的 `tesseract_cmd`。
3. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```

## 程式說明

| 檔案 | 用途 |
|---|---|
| `prog/LUCY.py` | 主程式：截取兩個數值區域、OCR 辨識並點擊擲骰按鈕 |
| `prog/PointPosetion.py` | 每秒印出滑鼠座標，用來量測位置 |
| `prog/test_run.py` | 儲存數值區域截圖，確認截取範圍 |
| `prog/test_tesseract.py` | 測試 Tesseract 是否安裝正確 |

## 使用方法
1. 更新 `prog/LUCY.py` 中的座標：
   - 執行 `python prog/PointPosetion.py`，將滑鼠移到幸運、智力和擲骰按鈕上讀取座標。
   - 在 `prog/LUCY.py` 中更新：
     ```python
     region_luck = (1759, 884, 60, 40)   # 幸運區域
     region_int = (1759, 830, 60, 40)    # 智力區域
     dice_position = (1942, 885)         # 擲骰按鈕（請替換為測量值）
     ```
2. 執行腳本：
   ```bash
   python prog/LUCY.py
   ```
3. 確保環境處於擲骰介面，且位於主螢幕。

## 除錯
除錯圖片預設寫入 `D:\Jeff\python\`，請將 `prog/LUCY.py` 和 `prog/test_run.py` 中的路徑改成自己電腦上的資料夾。範例圖片在 `png/`。

- **OCR 問題**：檢查 `thresh_debug.png`，若數字不清晰，調整 `recognize_number` 參數（例如模糊核、閾值塊大小）。
- **截圖問題**：確認 `luck_mss.png` 和 `dex_mss.png` 包含正確區域。
- **座標問題**：確保 `dice_position` 在螢幕解析度範圍內（例如 2560x1600）。

## 免責聲明
本專案僅用於**學習目的**，探索電腦視覺和自動化技術。請勿在生產環境或禁止自動化的應用中使用。

## 授權
MIT 授權
