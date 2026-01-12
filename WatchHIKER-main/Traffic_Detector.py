import tkinter as tk
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk
import io
import webbrowser

class TrafficMonitor:
    def __init__(self):
        # Window setup
        self.root = tk.Tk()
        self.root.title("Traffic Monitor")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        # Cities data
        self.cities = {
            "Coimbatore": {
                "roads": ["Avinashi Road", "Trichy Road", "Sathy Road"]
            }
        }
        
        self.setup_ui()
        self.update_traffic()
    
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="TRAFFIC STATUS",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        title.pack(pady=10)
        
        # Create frames for each road
        self.road_frames = {}
        self.status_labels = {}
        
        for city, data in self.cities.items():
            city_frame = ttk.LabelFrame(self.root, text=city)
            city_frame.pack(fill="x", padx=5, pady=5)
            
            for road in data["roads"]:
                road_frame = ttk.Frame(city_frame)
                road_frame.pack(fill="x", padx=5, pady=2)
                
                road_label = tk.Label(
                    road_frame,
                    text=road,
                    font=("Arial", 12),
                    bg="#1e1e1e",
                    fg="white"
                )
                road_label.pack(side=tk.LEFT)
                
                status_label = tk.Label(
                    road_frame,
                    text="Checking...",
                    font=("Arial", 12),
                    bg="#1e1e1e",
                    fg="yellow"
                )
                status_label.pack(side=tk.RIGHT)
                
                self.status_labels[road] = status_label
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Monitoring traffic...",
            bg="#1e1e1e",
            fg="white",
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
    
    def update_traffic(self):
        # Simulated traffic updates
        import random
        statuses = ["Light", "Moderate", "Heavy"]
        colors = {"Light": "#00ff00", "Moderate": "#ffff00", "Heavy": "#ff0000"}
        
        for road in self.status_labels:
            status = random.choice(statuses)
            self.status_labels[road].config(
                text=status,
                fg=colors[status]
            )
        
        self.root.after(30000, self.update_traffic)  # Update every 30 seconds
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TrafficMonitor()
    app.run()