import tkinter as tk
from tkinter import messagebox
import threading
import pystray
from PIL import Image, ImageDraw
import pyperclip
import sys
import os
import keyboard

from snipper import SnippingTool
from ocr_engine import extract_text, setup_tesseract

class TextExtractorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide main window
        self.root.title("Text Extractor")
        
        # Initialize snipper
        self.snipper = SnippingTool(self.root, self.on_capture)
        
        # Status variable
        self.tesseract_ready = setup_tesseract()
        if not self.tesseract_ready:
            print("Warning: Tesseract not found. OCR will fail until installed.")
            # We can show a message box here, but let's do it on first snip to not block startup
        
        self.advanced_mode = False # Default to standard
            
        self.icon = None
        self.setup_tray()

    def setup_tray(self):
        # Create a simple icon image
        image = Image.new('RGB', (64, 64), color = (73, 109, 137))
        d = ImageDraw.Draw(image)
        d.text((10,10), "OCR", fill=(255,255,0))
        
        # Define menu with toggle
        menu = pystray.Menu(
            pystray.MenuItem("Snip Text from Screen", self.on_snip_request),
            pystray.MenuItem("Enable Advanced Mode (High Accuracy / RapidOCR)", self.toggle_advanced, checked=lambda item: self.advanced_mode),
            pystray.MenuItem("Exit", self.on_exit)
        )
        
        self.icon = pystray.Icon("name", image, "Text Extractor", menu)

    def toggle_advanced(self, icon, item):
        self.advanced_mode = not self.advanced_mode
        state = "Enabled" if self.advanced_mode else "Disabled"
        self.icon.notify(f"Advanced Mode (RapidOCR) {state}", "Settings Updated")

    def run(self):
        # Setup Global Hotkey
        try:
            keyboard.add_hotkey('ctrl+alt+s', lambda: self.root.after(0, self.start_snip_main_thread))
            print("Shortcut registered: Ctrl+Alt+S")
        except Exception as e:
            print(f"Failed to register hotkey: {e}")

        # Run tray icon in a separate thread because Tkinter needs the main thread
        threading.Thread(target=self.icon.run, daemon=True).start()
        
        # Start Tkinter loop
        self.root.mainloop()

    def on_snip_request(self, icon, item):
        # Trigger snip from thread -> needs to be thread safe for Tkinter
        # Tkinter method calls should be safe if using after or virtual events, 
        # but simple root.deiconify usually works if careful. 
        # Best practice: use root.after to schedule it on main thread.
        self.root.after(0, self.start_snip_main_thread)

    def start_snip_main_thread(self):
        # Only check Tesseract if in Standard Mode
        if not self.advanced_mode and not self.tesseract_ready:
            # Recheck just in case user installed it while app was running
            self.tesseract_ready = setup_tesseract()
            if not self.tesseract_ready:
                messagebox.showerror("Error", "Tesseract-OCR is not found!\nPlease install it to use this feature.\nhttps://github.com/UB-Mannheim/tesseract/wiki")
                return

        self.snipper.start_snip()

    def on_capture(self, image: Image.Image):
        # print("Image captured. Extracting text...")
        
        # Run OCR in a separate thread so UI doesn't freeze
        mode = "advanced" if self.advanced_mode else "standard"
        threading.Thread(target=self.process_image, args=(image, mode), daemon=True).start()

    def process_image(self, image, mode):
        text = extract_text(image, mode=mode)

        # print(f"Extracted: {text}")
        
        if text:
            pyperclip.copy(text)
            # Notify user
            self.show_notification(text)
        else:
            self.show_notification("No text detected.")

    def show_notification(self, text):
        # Schedule notification on main thread logic if needed, 
        # but icon.notify is usually thread-safe or handles itself.
        # However, to be safe and keep UI logic clean:
        if len(text) > 100:
            display_text = text[:100] + "..."
        else:
            display_text = text
            
        self.icon.notify(f"{display_text}", "Text Copied to Clipboard")

    def _show_result_window(self, text):
        # Legacy: Removed in favor of notification
        pass

    def on_exit(self, icon, item):
        self.icon.stop()
        self.root.quit()
        # Force kill to ensure all threads (keyboard listener, etc.) die
        os._exit(0)

if __name__ == "__main__":
    app = TextExtractorApp()
    app.run()
