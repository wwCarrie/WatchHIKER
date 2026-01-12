import tkinter as tk
from tkinter import ttk
import requests
import json
from PIL import Image, ImageTk
import datetime

class WeatherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        # OpenWeatherMap configuration
        self.API_KEY = "8f22641ee48fb8697204f20fdc4c359d"
        self.cities = {
            "Guangzhou": {"code": "CN", "frame": None},
            "Hangzhou": {"code": "CN", "frame": None}
        }
        self.current_city = "Guangzhou"
        
        self.setup_ui()
        self.update_weather()
        
    def setup_ui(self):
        # Create frames for each city
        for city in self.cities:
            frame = tk.Frame(self.root, bg="#1e1e1e")
            self.cities[city]["frame"] = frame
            
            # City label
            tk.Label(
                frame,
                text=city.upper(),
                font=("Arial", 16, "bold"),
                bg="#1e1e1e",
                fg="white"
            ).pack(pady=10)
            
            # Temperature frame
            temp_frame = tk.Frame(frame, bg="#1e1e1e")
            temp_frame.pack(pady=5)
            
            temp_label = tk.Label(
                temp_frame,
                text="--°C",
                font=("Arial", 32, "bold"),
                bg="#1e1e1e",
                fg="#00ff00"
            )
            temp_label.pack()
            
            # Weather description
            desc_label = tk.Label(
                frame,
                text="Loading...",
                font=("Arial", 12),
                bg="#1e1e1e",
                fg="white"
            )
            desc_label.pack(pady=5)
            
            # Weather details frame
            details_frame = tk.Frame(frame, bg="#1e1e1e")
            details_frame.pack(pady=10, fill="x", padx=20)
            
            # Humidity
            humidity_label = tk.Label(
                details_frame,
                text="Humidity: --%",
                font=("Arial", 10),
                bg="#1e1e1e",
                fg="white"
            )
            humidity_label.pack(pady=2)
            
            # Wind speed
            wind_label = tk.Label(
                details_frame,
                text="Wind: -- m/s",
                font=("Arial", 10),
                bg="#1e1e1e",
                fg="white"
            )
            wind_label.pack(pady=2)
            
            # Store labels for updating
            self.cities[city].update({
                "temp_label": temp_label,
                "desc_label": desc_label,
                "humidity_label": humidity_label,
                "wind_label": wind_label
            })
        
        # Navigation buttons frame
        nav_frame = tk.Frame(self.root, bg="#1e1e1e")
        nav_frame.pack(side=tk.BOTTOM, pady=5)
        
        ttk.Button(
            nav_frame,
            text="PREV",
            command=self.show_previous
        ).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(
            nav_frame,
            text="REF",
            command=self.update_weather
        ).pack(side=tk.LEFT, padx=1)
        
        ttk.Button(
            nav_frame,
            text="NXT",
            command=self.show_next
        ).pack(side=tk.LEFT, padx=1)
        
        # Show initial city
        self.show_city(self.current_city)

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
        
    def show_city(self, city):
        # Hide all frames
        for c in self.cities:
            self.cities[c]["frame"].pack_forget()
        
        # Show selected city
        self.cities[city]["frame"].pack(expand=True, fill="both")
        self.current_city = city
        
    def show_next(self):
        cities = list(self.cities.keys())
        current_index = cities.index(self.current_city)
        next_index = (current_index + 1) % len(cities)
        self.show_city(cities[next_index])
        self.update_weather()
        
    def show_previous(self):
        cities = list(self.cities.keys())
        current_index = cities.index(self.current_city)
        prev_index = (current_index - 1) % len(cities)
        self.show_city(cities[prev_index])
        self.update_weather()
        
    def update_weather(self):
        try:
            city = self.current_city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{self.cities[city]['code']}&appid={self.API_KEY}&units=metric"
            response = requests.get(url)
            data = json.loads(response.text)
            
            # Update labels
            temp = round(data['main']['temp'])
            desc = data['weather'][0]['description'].capitalize()
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            self.cities[city]["temp_label"].config(text=f"{temp}°C")
            self.cities[city]["desc_label"].config(text=desc)
            self.cities[city]["humidity_label"].config(text=f"Humidity: {humidity}%")
            self.cities[city]["wind_label"].config(text=f"Wind: {wind_speed} m/s")
            
        except Exception as e:
            self.cities[city]["desc_label"].config(text="Error updating weather")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WeatherApp()
    app.run()