import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime
import time
import threading

class CryptoMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crypto Monitor")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        # API Configuration
        self.api_key = "YOUR_API_KEY"  # Get from CryptoCompare
        self.base_url = "https://min-api.cryptocompare.com/data"
        self.symbols = ["BTC", "ETH", "DOGE"]
        self.prices = {}
        self.changes = {}
        
        self.setup_ui()
        self.start_updates()

    def fetch_crypto_data(self):
        try:
            # Get current prices
            price_url = f"{self.base_url}/pricemultifull"
            params = {
                "fsyms": ",".join(self.symbols),
                "tsyms": "USD",
                "api_key": self.api_key
            }
            
            response = requests.get(price_url, params=params)
            data = response.json()
            
            for symbol in self.symbols:
                raw_data = data["RAW"][symbol]["USD"]
                self.prices[symbol] = raw_data["PRICE"]
                self.changes[symbol] = raw_data["CHANGEPCT24HOUR"]
            
            self.update_ui()
            
        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}")
    
    def update_ui(self):
        for symbol in self.symbols:
            price = self.prices.get(symbol, 0)
            change = self.changes.get(symbol, 0)
            
            self.price_labels[symbol].config(
                text=f"$ {price:,.2f}"
            )
            
            change_color = "#00ff00" if change >= 0 else "#ff0000"
            self.change_labels[symbol].config(
                text=f"24h: {change:+.2f}%",
                fg=change_color
            )
        
        self.status_bar.config(
            text=f"Last update: {datetime.now().strftime('%H:%M:%S')}",
            fg="#00ff00"
        )
    
    def setup_ui(self):
        # Title
        title = tk.Label(
            self.root,
            text="CRYPTO MONITOR",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        title.pack(pady=10)
        
        # Create frames for each crypto
        self.price_labels = {}
        self.change_labels = {}
        
        for symbol in self.symbols:
            frame = ttk.LabelFrame(self.root, text=symbol)
            frame.pack(fill="x", padx=5, pady=5)
            
            price_label = tk.Label(
                frame,
                text="$ --",
                font=("Arial", 14),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            price_label.pack(pady=2)
            
            change_label = tk.Label(
                frame,
                text="24h: --",
                font=("Arial", 12),
                bg="#1e1e1e",
                fg="#ffffff"
            )
            change_label.pack(pady=2)
            
            self.price_labels[symbol] = price_label
            self.change_labels[symbol] = change_label
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Initializing...",
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

    def start_updates(self):
        def update_loop():
            while True:
                self.fetch_crypto_data()
                time.sleep(30)  # Update every 30 seconds
        
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CryptoMonitor()
    app.run()