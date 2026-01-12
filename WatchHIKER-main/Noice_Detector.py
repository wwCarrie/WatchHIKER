#  -*- coding: UTF-8 -*-

# MindPlus
# Python
from pinpong.extension.unihiker import *
from pinpong.board import Board,Pin
from unihiker import Audio
import tkinter as tk
from tkinter import ttk
import time
import threading
import math

class NoiseMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Noise Monitor")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.audio = Audio()
        self.setup_ui()
        self.start_monitoring()
    
    def setup_ui(self):
        # Title
        self.title_label = tk.Label(
            self.root,
            text="NOISE MONITOR",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.title_label.pack(pady=10)
        
        # Canvas for visualization
        self.canvas = tk.Canvas(
            self.root,
            width=200,
            height=150,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Create bars with peak indicators
        self.bars = []
        self.peaks = []
        self.peak_speeds = []
        num_bars = 16
        
        for i in range(num_bars):
            # Create main bar
            bar = self.canvas.create_rectangle(
                i*12 + 5, 150,
                i*12 + 13, 150,
                fill="#00ff00"
            )
            self.bars.append(bar)
            
            # Create peak indicator
            peak = self.canvas.create_rectangle(
                i*12 + 5, 150,
                i*12 + 13, 148,
                fill="#ffffff"
            )
            self.peaks.append(peak)
            self.peak_speeds.append(0)
        
        # Numerical display
        self.level_label = tk.Label(
            self.root,
            text="0",
            font=("Arial", 36, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.level_label.pack(pady=10)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Monitoring...",
            bg="#1e1e1e",
            fg="#ffffff",
            bd=1,
            relief=tk.SUNKEN
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.root.bind("<ButtonPress-1>", self.start_swipe)
        self.root.bind("<B1-Motion>", self.swipe)
        self.root.bind("<ButtonRelease-1>", self.end_swipe)

    def show_menu(self):
        import menu
        menu.MenuWindow(self.root)
    
    def start_swipe(self, event):
        self.start_x = event.x
        self.start_y = event.y 

    def swipe(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if dy > 80:
            self.show_menu()
            self.start_x = event.x
            self.start_y = event.y

    def end_swipe(self, event):
        self.start_x = 0
    
    def update_visualization(self, level):
        max_height = 150
        peak_fall_speed = 0.5
        
        for i, (bar, peak) in enumerate(zip(self.bars, self.peaks)):
            # Calculate bar height with some randomness
            variation = math.sin(time.time() * 10 + i) * 5
            adjusted_level = max(0, min(100, level + variation))
            
            # Calculate height and color
            height = max_height - (adjusted_level * 1.2)
            
            # Rainbow color effect
            hue = (i / len(self.bars)) * 360
            rgb = self.hsv_to_rgb(hue, 1, 1 if adjusted_level > 0 else 0.2)
            color = f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
            
            # Update bar
            self.canvas.coords(bar, i*12 + 5, height, i*12 + 13, max_height)
            self.canvas.itemconfig(bar, fill=color)
            
            # Update peak
            peak_y = float(self.canvas.coords(peak)[1])
            if height < peak_y:  # New peak
                self.canvas.coords(peak, i*12 + 5, height, i*12 + 13, height + 2)
                self.peak_speeds[i] = 0
            else:  # Peak falling
                self.peak_speeds[i] += peak_fall_speed
                new_y = min(max_height, peak_y + self.peak_speeds[i])
                self.canvas.coords(peak, i*12 + 5, new_y, i*12 + 13, new_y + 2)
        
        # Update level display
        self.level_label.config(text=str(int(level)))
        
        # Update status with smooth color transition
        if level > 80:
            status = "Very Loud!"
            color = "#ff0000"
        elif level > 60:
            status = "Loud"
            color = "#ffff00"
        else:
            status = "Normal"
            color = "#00ff00"
        
        self.status_bar.config(text=status, fg=color)
    
    def hsv_to_rgb(self, h, s, v):
        h = float(h)
        s = float(s)
        v = float(v)
        h60 = h / 60.0
        h60f = math.floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0: r, g, b = v, t, p
        elif hi == 1: r, g, b = q, v, p
        elif hi == 2: r, g, b = p, v, t
        elif hi == 3: r, g, b = p, q, v
        elif hi == 4: r, g, b = t, p, v
        elif hi == 5: r, g, b = v, p, q
        return (
            int(r * 255),
            int(g * 255),
            int(b * 255)
        )
    
    def monitor_audio(self):
        while True:
            try:
                level = self.audio.sound_level()
                self.root.after(0, self.update_visualization, level)
                time.sleep(0.1)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
    
    def start_monitoring(self):
        threading.Thread(target=self.monitor_audio, daemon=True).start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NoiseMonitor()
    app.run()