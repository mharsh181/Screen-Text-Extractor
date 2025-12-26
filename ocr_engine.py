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

def extract_text(image: Image.Image) -> str:
    """
    Extracts text from a PIL Image object.
    """
    if not setup_tesseract():
        return "Error: Tesseract-OCR is not installed or not found. Please install Tesseract."

    try:
        # --psm 6 is usually good for sparse text blocks, but keeping default is safer generally
        # We can optimize config later.
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
