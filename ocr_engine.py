import pytesseract
from PIL import Image
import os
import sys

# Common default install locations for Tesseract on Windows
TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\mhars\AppData\Local\Tesseract-OCR\tesseract.exe',
    # Add more if needed
]

def setup_tesseract():
    """Attempts to locate Tesseract executable and configure pytesseract."""
    # Check if 'tesseract' is in PATH
    try:
        # This is a basic check. If this doesn't raise, it's in PATH.
        # However, checking specific paths is more robust on Windows data science envs.
        pytesseract.get_tesseract_version()
        return True
    except pytesseract.TesseractNotFoundError:
        pass # Not in path, search manually

    found_path = None
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            found_path = path
            break
    
    if found_path:
        pytesseract.pytesseract.tesseract_cmd = found_path
        return True
    
    return False



# Global variable for lazy loading RapidOCR
_RAPIDOCR = None

def get_rapidocr():
    global _RAPIDOCR
    if _RAPIDOCR is None:
        # print("Loading RapidOCR Model...")
        from rapidocr_onnxruntime import RapidOCR
        _RAPIDOCR = RapidOCR()
    return _RAPIDOCR

def extract_text(image: Image.Image, mode="standard") -> str:
    """
    Extracts text from a PIL Image object.
    mode: 'standard' (Tesseract) or 'rapid' (RapidOCR/Advanced)
    """
    if mode == "advanced": # Renamed from handwriting
        try:
            ocr = get_rapidocr()
            import numpy as np
            # RapidOCR expects numpy array (OpenCV format BGR)
            # PIL is RGB, but for OCR grayscale/RGB usually fine.
            img_np = np.array(image)
            
            # rapidocr returns list of [dt_boxes, rec_res, score]
            result, elapse = ocr(img_np)
            
            if result:
                # Combine all text segments
                text_content = [line[1] for line in result]
                return "\n".join(text_content)
            else:
                return ""
        except Exception as e:
            return f"Error during RapidOCR: {str(e)}"
    
    # Standard Mode (Tesseract)
    if not setup_tesseract():
        return "Error: Tesseract-OCR is not installed or not found. Please install Tesseract."

    try:
        # --psm 6 is usually good for sparse text blocks, but keeping default is safer generally
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Error during OCR: {str(e)}"


if __name__ == "__main__":
    print("Testing Tesseract setup...")
    if setup_tesseract():
        print(f"Tesseract found! Version: {pytesseract.get_tesseract_version()}")
    else:
        print("Tesseract NOT found.")
