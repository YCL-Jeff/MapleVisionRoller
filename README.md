# MapleVisionRoller

<a href="https://github.com/YCL-Jeff/MapleVisionRoller/blob/main/README_zh-TW.md">繁體中文Readme</a>

A computer vision-based tool for automating UI interactions by recognising numerical values in application interfaces using OCR and DirectX screenshot capture.

**⚠️ Note**: This project is for **educational purposes only**. It demonstrates computer vision and automation techniques in a controlled, non-production environment.

## Features
- Captures UI elements with `mss` to handle DirectX-rendered interfaces.
- Recognises numerical values using `pytesseract` and OpenCV.
- Automates mouse interactions based on recognised values.
- Configurable screen coordinates for flexible UI adaptation.

## Prerequisites
- Python 3.12
- Tesseract OCR installed at `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Python packages listed in `requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YCL-Jeff/MapleVisionRoller.git
   cd MapleVisionRoller
   ```
2. Install Tesseract OCR:
   - Download from [UB-Mannheim Tesseract Releases](https://github.com/UB-Mannheim/tesseract/wiki).
   - Install to `C:\Program Files\Tesseract-OCR\`.
   - If Tesseract is installed elsewhere, update `tesseract_cmd` in `prog/LUCY.py`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Scripts

| Script | Purpose |
|---|---|
| `prog/LUCY.py` | Main script: capture the two value regions, read them with OCR and click the interaction point |
| `prog/PointPosetion.py` | Prints the mouse position every second, for measuring coordinates |
| `prog/test_run.py` | Saves screenshots of the value regions to check the capture areas |
| `prog/test_tesseract.py` | Checks that Tesseract is installed and reachable |

## Usage
1. Update coordinates in `prog/LUCY.py`:
   - Run `python prog/PointPosetion.py` and hover over each target to read its coordinates.
   - Update in `prog/LUCY.py`:
     ```python
     region_luck = (1759, 884, 60, 40)   # First value region
     region_int = (1759, 830, 60, 40)    # Second value region
     dice_position = (1942, 885)         # Interaction point (replace with measured value)
     ```
2. Run the script:
   ```bash
   python prog/LUCY.py
   ```
3. Ensure the target application is open and positioned on the main monitor.

## Debugging
Debug images are written to `D:\Jeff\python\` by default; change the paths in `prog/LUCY.py` and `prog/test_run.py` to a folder on your machine. Examples are in `png/`.

- **OCR Issues**: Check `thresh_debug.png` for preprocessed images. Adjust `recognize_number` parameters (e.g., blur kernel, threshold block size) if numbers are unclear.
- **Screenshot Issues**: Verify `luck_mss.png` and `dex_mss.png` contain correct regions.
- **Coordinate Issues**: Ensure `dice_position` is within screen resolution (e.g., 2560x1600).

## Disclaimer
This project is for **educational purposes only** to explore computer vision and automation techniques. It should not be used in production environments or applications where automation is prohibited.

## Licence
MIT License
