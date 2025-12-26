import tkinter as tk
from PIL import ImageGrab
import ctypes

class SnippingTool:
    def __init__(self, root, on_capture_callback):
        self.root = root
        self.on_capture_callback = on_capture_callback
        self.root.withdraw() # Hide the main window initially
        
        self.snip_window = None
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None
        self.rect_id = None
        self.is_snipping = False

    def start_snip(self):
        if self.is_snipping:
            return
            
        self.is_snipping = True
        self.snip_window = tk.Toplevel(self.root)
        self.snip_window.attributes("-fullscreen", True)
        self.snip_window.attributes("-topmost", True)
        self.snip_window.attributes("-alpha", 0.3) # Make it semi-transparent
        self.snip_window.config(cursor="cross")
        
        # Windows specific: make it white and transparent key
        # On Windows, to make a "clear" hole, we usually use a specific color and set it as transparent
        # But for simple highlighting, just alpha is often enough.
        # Let's try simple alpha first: grey overlay.
        self.snip_window.configure(background='black')

        self.canvas = tk.Canvas(self.snip_window, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Escape>", self.cancel_snip)
        
        # Force update to ensure it's drawn
        self.snip_window.update()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2, fill="white", stipple="gray50") 
        # Note: stippling might not look great on all OS, but works for "selection" effect usually.
        # Alternatively, we just draw a red box.

    def on_mouse_drag(self, event):
        self.current_x, self.current_y = (event.x, event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, self.current_x, self.current_y)

    def on_button_release(self, event):
        if self.start_x is None or self.start_y is None:
            return

        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        
        self.close_snip()
        
        # Ensure non-zero size
        if (x2 - x1) > 5 and (y2 - y1) > 5:
            self.capture_screen(x1, y1, x2, y2)

    def cancel_snip(self, event=None):
        self.close_snip()

    def close_snip(self):
        self.is_snipping = False
        if self.snip_window:
            self.snip_window.destroy()
            self.snip_window = None
        self.start_x = None
        self.start_y = None
        self.rect_id = None

    def capture_screen(self, x1, y1, x2, y2):
        # We need to grab screen coordinates. Toplevel coordinates are screen coords in fullscreen.
        # However, ImageGrab uses screen coordinates.
        try:
            # Depending on DPI scaling, this might be off.
            # Windows DPI awareness is often needed.
            # For now, let's assume 100% or that ImageGrab aligns with Tkinter.
            
            # Hide the overlay fully before grabbing (though it's destroyed, give it a ms)
            # destroy() is usually synchronous enough, but update_idletasks handles pending events.
            self.root.update_idletasks()
            
            image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            if self.on_capture_callback:
                self.on_capture_callback(image)
        except Exception as e:
            pass # print(f"Capture failed: {e}")

# DPI Awareness (Windows)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass
