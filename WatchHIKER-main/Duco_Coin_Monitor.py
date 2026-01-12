import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DucoMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Duino-Coin Monitor")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.username = "kyoot"  # Replace with your username
        self.API_URL = "https://server.duinocoin.com/users/"
        self.update_interval = 5000
        self.setup_ui()
        self.update_data()
        
    def setup_ui(self):
        # Balance Display
        self.balance_frame = ttk.LabelFrame(self.root, text="Balance")
        self.balance_frame.pack(fill="x", padx=5, pady=5)
        
        self.balance_label = tk.Label(
            self.balance_frame,
            text="0.000000 DUCO",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.balance_label.pack(pady=5)
        
        # Mining Stats
        self.mining_frame = ttk.LabelFrame(self.root, text="Mining Status")
        self.mining_frame.pack(fill="x", padx=5, pady=5)
        
        self.hashrate_label = tk.Label(
            self.mining_frame,
            text="Hashrate: 0 H/s",
            bg="#1e1e1e",
            fg="white"
        )
        self.hashrate_label.pack()
        
        self.miners_label = tk.Label(
            self.mining_frame,
            text="Miners: 0",
            bg="#1e1e1e",
            fg="white"
        )
        self.miners_label.pack()
        
        # Network Info
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
        
    def update_data(self):
        try:
            response = requests.get(
                f"{self.API_URL}{self.username}",
                headers={"User-Agent": "DucoMonitor/1.0"},
                timeout=10
            )
            logger.debug(f"API Response: {response.text}")
            
            data = response.json()
            if data.get("success"):
                result = data.get("result", {})
                logger.debug(f"Parsed data: {result}")
                
                # Fix balance parsing - it's nested in a dict
                balance_data = result.get("balance", {})
                balance = float(balance_data.get("balance", 0))
                self.balance_label.config(text=f"{balance:.6f} DUCO")
                
                # Update Mining Stats
                miners = result.get("miners", [])
                total_hashrate = sum(float(m.get("hashrate", 0)) for m in miners)
                self.hashrate_label.config(text=f"Hashrate: {total_hashrate:.2f} H/s")
                self.miners_label.config(text=f"Miners: {len(miners)}")
                
                
        except Exception as e:
            logger.error(f"Update error: {str(e)}")
            self.status.config(text=f"Error: {str(e)}", fg="#ff0000")
            
        finally:
            self.root.after(self.update_interval, self.update_data)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DucoMonitor()
    app.run()