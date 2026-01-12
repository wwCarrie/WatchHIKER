import tkinter as tk
from tkinter import ttk
import requests
import json
from datetime import datetime

class AirQualityApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Air Quality Monitor")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.API_KEY = "8f22641ee48fb8697204f20fdc4c359d"
        self.cities = {
            "广州": {"lat": 23.1291, "lon": 113.2644}
        }

        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for city tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")
        
        # Create tabs for each city
        self.city_frames = {}
        for city in self.cities:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=city)
            self.city_frames[city] = self.create_city_frame(frame, city)
            
        # Refresh button
        tk.Button(self.root, text="Refresh Data", command=self.update_all_data).pack(pady=5)

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

    def create_city_frame(self, parent, city):
        frame = ttk.Frame(parent)
        frame.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Air Quality Index
        aqi_label = tk.Label(frame, text="AQI: --", font=("Arial", 16, "bold"))
        aqi_label.pack()
        
        # PM Values
        pm_frame = ttk.LabelFrame(frame, text="Particulate Matter")
        pm_frame.pack(fill="x", padx=5, pady=5)
        
        pm25_label = tk.Label(pm_frame, text="PM2.5: -- µg/m³")
        pm25_label.pack()
        
        pm10_label = tk.Label(pm_frame, text="PM10: -- µg/m³")
        pm10_label.pack()
        
        # Other Pollutants
        poll_frame = ttk.LabelFrame(frame, text="Other Pollutants")
        poll_frame.pack(fill="x", padx=5, pady=5)
        
        co_label = tk.Label(poll_frame, text="CO: -- µg/m³")
        no2_label = tk.Label(poll_frame, text="NO₂: -- µg/m³")
        so2_label = tk.Label(poll_frame, text="SO₂: -- µg/m³")
        o3_label = tk.Label(poll_frame, text="O₃: -- µg/m³")
        
        for label in [co_label, no2_label, so2_label, o3_label]:
            label.pack()
        
        return {
            "aqi": aqi_label,
            "pm25": pm25_label,
            "pm10": pm10_label,
            "co": co_label,
            "no2": no2_label,
            "so2": so2_label,
            "o3": o3_label
        }

    
    def update_city_data(self, city):
        try:
            lat = self.cities[city]["lat"]
            lon = self.cities[city]["lon"]
            url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={self.API_KEY}"
            
            response = requests.get(url)
            data = json.loads(response.text)
            
            if 'list' in data and len(data['list']) > 0:
                air_data = data['list'][0]
                components = air_data['components']
                aqi = air_data['main']['aqi']
                
                labels = self.city_frames[city]
                
                # Update AQI with color coding
                aqi_colors = ["#00e400", "#ffff00", "#ff7e00", "#ff0000", "#8f3f97"]
                labels["aqi"].config(
                    text=f"AQI: {aqi}",
                    fg=aqi_colors[aqi-1]
                )
                
                # Update PM values
                labels["pm25"].config(text=f"PM2.5: {components['pm2_5']:.1f} µg/m³")
                labels["pm10"].config(text=f"PM10: {components['pm10']:.1f} µg/m³")
                
                # Update other pollutants
                labels["co"].config(text=f"CO: {components['co']:.1f} µg/m³")
                labels["no2"].config(text=f"NO₂: {components['no2']:.1f} µg/m³")
                labels["so2"].config(text=f"SO₂: {components['so2']:.1f} µg/m³")
                labels["o3"].config(text=f"O₃: {components['o3']:.1f} µg/m³")
                
        except Exception as e:
            print(f"Error updating {city} data: {e}")
    
    def update_all_data(self):
        for city in self.cities:
            self.update_city_data(city)
    
    def run(self):
        self.update_all_data()
        self.root.mainloop()

def main():
    app = AirQualityApp()
    app.run()

if __name__ == "__main__":
    main()