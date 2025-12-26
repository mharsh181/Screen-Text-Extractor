import tkinter as tk
from tkinter import messagebox
import threading
import pystray
from PIL import Image, ImageDraw
import pyperclip
import sys
import os

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
            # print("Warning: Tesseract not found. OCR will fail until installed.")
            pass
            # We can show a message box here, but let's do it on first snip to not block startup
            
        self.icon = None
        self.setup_tray()

    def setup_tray(self):
        # Create a simple icon image
        image = Image.new('RGB', (64, 64), color = (73, 109, 137))
        d = ImageDraw.Draw(image)
        d.text((10,10), "OCR", fill=(255,255,0))
        
        menu = pystray.Menu(
            pystray.MenuItem("Snip Text from Screen", self.on_snip_request),
            pystray.MenuItem("Exit", self.on_exit)
        )
        
        self.icon = pystray.Icon("name", image, "Text Extractor", menu)

    def run(self):
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
        if not self.tesseract_ready:
            # Recheck just in case user installed it while app was running
            self.tesseract_ready = setup_tesseract()
            if not self.tesseract_ready:
                messagebox.showerror("Error", "Tesseract-OCR is not found!\nPlease install it to use this feature.\nhttps://github.com/UB-Mannheim/tesseract/wiki")
                return

        self.snipper.start_snip()

    def on_capture(self, image: Image.Image):
        # print("Image captured. Extracting text...")
        
        # Run OCR in a separate thread so UI doesn't freeze
        threading.Thread(target=self.process_image, args=(image,), daemon=True).start()

    def process_image(self, image):
        text = extract_text(image)
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

if __name__ == "__main__":
    app = TextExtractorApp()
    app.run()
