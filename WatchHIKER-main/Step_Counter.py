import tkinter as tk
from tkinter import ttk
from pinpong.extension.unihiker import *
from pinpong.board import Board,Pin
from unihiker import GUI
import time

class StepCounterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Step Counter")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.steps = 0
        self.setup_ui()
        Board().begin()
        self.update_values()
        
    def setup_ui(self):
        # Accelerometer Frame
        acc_frame = ttk.LabelFrame(self.root, text="Accelerometer")
        acc_frame.pack(fill="x", padx=5, pady=5)
        
        self.acc_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(
                acc_frame,
                text=f"{axis}: 0.00",
                font=("Arial", 12),
                bg="#1e1e1e",
                fg="#00ff00"
            )
            label.pack(pady=2)
            self.acc_labels[axis] = label
            
        # Gyroscope Frame
        gyro_frame = ttk.LabelFrame(self.root, text="Gyroscope")
        gyro_frame.pack(fill="x", padx=5, pady=5)
        
        self.gyro_labels = {}
        for axis in ['X', 'Y', 'Z']:
            label = tk.Label(
                gyro_frame,
                text=f"{axis}: 0.00",
                font=("Arial", 12),
                bg="#1e1e1e",
                fg="#00ff00"
            )
            label.pack(pady=2)
            self.gyro_labels[axis] = label
            
        # Steps Frame
        steps_frame = ttk.LabelFrame(self.root, text="Steps")
        steps_frame.pack(fill="x", padx=5, pady=5)
        
        self.steps_label = tk.Label(
            steps_frame,
            text="0",
            font=("Arial", 24, "bold"),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.steps_label.pack(pady=10)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Running",
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
    
    def update_values(self):
        try:
            # Update accelerometer values
            acc_x = accelerometer.get_x()
            acc_y = accelerometer.get_y()
            acc_z = accelerometer.get_z()
            
            self.acc_labels['X'].config(text=f"X: {acc_x:.2f}")
            self.acc_labels['Y'].config(text=f"Y: {acc_y:.2f}")
            self.acc_labels['Z'].config(text=f"Z: {acc_z:.2f}")
            
            # Update gyroscope values
            gyro_x = gyroscope.get_x()
            gyro_y = gyroscope.get_y()
            gyro_z = gyroscope.get_z()
            
            self.gyro_labels['X'].config(text=f"X: {gyro_x:.2f}")
            self.gyro_labels['Y'].config(text=f"Y: {gyro_y:.2f}")
            self.gyro_labels['Z'].config(text=f"Z: {gyro_z:.2f}")
            
            # Update step count
            if accelerometer.get_strength() > 1.5:
                self.steps += 1
                self.steps_label.config(text=str(self.steps))
            
            self.status_bar.config(text=f"Last update: {time.strftime('%H:%M:%S')}")
            
        except Exception as e:
            self.status_bar.config(text=f"Error: {str(e)}")
            
        self.root.after(100, self.update_values)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StepCounterGUI()
    app.run()