# Screen Text Extractor 📝

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

A lightweight, system-tray application for Windows that allows you to extract text from anywhere on your screen—including videos, images, and protected documents—and copies it directly to your clipboard.

Think of it as the Windows Snipping Tool, but for text.

## ✨ Features

*   **Snipping Tool Interface**: Familiar click-and-drag overlay to select text.
*   **System Tray Integration**: runs silently in the background.
*   **Instant OCR**: Powered by Google's Tesseract Engine for high-accuracy text recognition.
*   **Advanced Mode (RapidOCR)**: Uses ONNX Runtime for blazing fast, high-accuracy extraction of handwriting and complex text.
*   **Global Shortcut**: Trigger a snip instantly with `Ctrl + Alt + S`.
*   **Silent Clipboard Copy**: Automatically copies extracted text to clipboard without annoying popups.
*   **Video Support**: Works perfectly on paused or playing videos (YouTube, etc.).

## 🚀 Installation

### Run from Source (Developers)
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This includes `rapidocr_onnxruntime` for high-performance OCR.*
3.  Run the app:
    ```bash
    python main.py
    ```

### 📦 Prerequisites (Tesseract OCR)
This tool relies on the Tesseract OCR engine for "Standard Mode".
1.  **Download**: [UB-Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2.  **Install**: Run the installer and use default settings.

## 🛠️ Usage

### 1. The Basics
1.  Run the app. It will appear in your **System Tray** (bottom right).
2.  **Right-Click** and select **"Snip Text from Screen"**.
3.  **Drag** your mouse to draw a box around the text.
4.  **Release** to capture. The text is copied to your clipboard! 📋

### 2. Global Shortcut ⌨️
*   Press **`Ctrl + Alt + S`** anywhere to instantly trigger the snipping tool.

### 3. Advanced Mode (Handwriting/Complex Text) 🧠
For higher accuracy (e.g., handwriting):
1.  Right-click the tray icon.
2.  Check **"Enable Advanced Mode (High Accuracy / RapidOCR)"**.
3.  Snip as usual. It uses a Neural Network model (RapidOCR) for superior results.

## 🤝 Contributing

Contributions are welcome!
1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
