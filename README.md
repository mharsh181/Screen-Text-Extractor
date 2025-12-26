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
*   **Silent Clipboard Copy**: Automatically copies extracted text to clipboard without annoying popups.
*   **Video Support**: Works perfectly on paused or playing videos (YouTube, etc.).

## 🚀 Installation

### Option A: Standalone Executable (Easy)
1.  Go to the `Release_Package` folder.
2.  Run `ScreenTextExtractor.exe`.
3.  *Note: You still need Tesseract-OCR installed (see below).*

### Option B: Run from Source (Developers)
1.  Clone this repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    python main.py
    ```

### 📦 Prerequisites (Tesseract OCR)
This tool relies on the Tesseract OCR engine.
1.  **Download**: [UB-Mannheim Tesseract Installer](https://github.com/UB-Mannheim/tesseract/wiki)
2.  **Install**: Run the installer and use default settings.

## 🛠️ Usage

1.  Look for the **OCR Icon** (blue/yellow) in your Windows System Tray.
2.  **Right-Click** and select **"Snip Text from Screen"**.
3.  **Drag** your mouse to draw a box around the text you want.
4.  **Release** to capture. The text is now in your clipboard! 📋

## 🤝 Contributing

Contributions are welcome!
1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
