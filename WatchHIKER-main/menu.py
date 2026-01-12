import tkinter as tk

class MenuWindow:
    def __init__(self, master):
        self.menu_window = tk.Toplevel(master)
        self.menu_window.title("Menu")
        self.menu_window.geometry("240x320")
        self.menu_window.configure(bg="#2e2e2e")
        self.menu_window.resizable(False, False)

        self.start_x = 0
        self.start_y = 0

        self.menu_window.bind("<ButtonPress-1>", self.start_swipe)
        self.menu_window.bind("<B1-Motion>", self.swipe)

        self.modules = [
            "AQI_Monitor",
            "Audio_Recorder",
            "Crypto_Monitor",
            "Duco_Coin_Monitor",
            "esp32_cam_viewer",
            "Noice_Detector",
            "Online_WeatherStation",
            "SOS_Trigger",
            "Step_Counter",
            "TimeLapse_Camera",
            "Traffic_Detector",
        ]

        title_label = tk.Label(
            self.menu_window, text="Select Module",
            bg="#2e2e2e", fg="#00ff00", font=("Arial", 14, "bold")
        )
        title_label.pack(pady=10)

        canvas = tk.Canvas(self.menu_window, bg="#2e2e2e", highlightthickness=0)
        frame = tk.Frame(canvas, bg="#2e2e2e")
        scrollbar = tk.Scrollbar(self.menu_window, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        for module in self.modules:
            btn = tk.Button(
                frame,
                text=module,
                command=lambda m=module: self.open_module(m),
                bg="#1e1e1e",
                fg="#00ff00",
                font=("Arial", 12),
                width=25,
                relief="groove"
            )
            btn.pack(pady=4, padx=5)

        self.menu_window.bind("<FocusOut>", lambda e: self.menu_window.destroy())

    def open_module(self, module_name):
        print(f"Opening module: {module_name}")
        self.menu_window.destroy()

        if module_name == "Audio_Recorder":
            import Audio_Recorder
            app = Audio_Recorder.AudioRecorder() 
            app.run()
        elif module_name == "Crypto_Monitor":
            import Crypto_Monitor
            app = Crypto_Monitor.CryptoMonitor() 
            app.run()
        elif module_name == "Duco_Coin_Monitor":
            import Duco_Coin_Monitor
            app = Duco_Coin_Monitor.DucoMonitor()
            app.run()
        elif module_name == "esp32_cam_viewer":
            import esp32_cam_viewer
            app = esp32_cam_viewer.VideoStreamApp()
            app.run()
        elif module_name == "Noice_Detector":
            import Noice_Detector
            app = Noice_Detector.NoiseMonitor()
            app.run()
        elif module_name == "Online_WeatherStation":
            import Online_WeatherStation
            app = Online_WeatherStation.WeatherApp()
            app.run()
        elif module_name == "SOS_Trigger":
            import SOS_Trigger
            app = SOS_Trigger.SosApp()
            app.run()
        elif module_name == "Step_Counter":
            import Step_Counter
            app = Step_Counter.StepCounterGUI()
            app.run()
        elif module_name == "TimeLapse_Camera":
            import TimeLapse_Camera
            app = TimeLapse_Camera.TimeLapseGenerator()
            app.run()
        elif module_name == "Traffic_Detector":
            import Traffic_Detector
            app = Traffic_Detector.TrafficMonitor()
            app.run()
        elif module_name == "AQI_Monitor":
            import AQI_Monitor
            app = AQI_Monitor.AirQualityApp() 
            app.run()

        else:
            print(f"Module '{module_name}' not found or not implemented.")

    def start_swipe(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def swipe(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        print(f"Swipe dx={dx}, dy={dy}")

        if abs(dx) > 50 and abs(dy) < 30 and dx < 0:
            print("Swipe left detected - returning to dial")
            self.return_to_dial()
            self.start_x = event.x
            self.start_y = event.y

    def return_to_dial(self):
        self.menu_window.destroy()
        # TODO: 显示表盘界面相关代码
        print("Returned to dial")