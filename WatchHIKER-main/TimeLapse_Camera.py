import cv2
import tkinter as tk
from tkinter import ttk, messagebox
import time
import os
from datetime import datetime

class TimeLapseGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Lapse Generator")
        self.root.geometry("240x320")
        self.root.configure(bg="#2c3e50")
        
        self.cap = None
        self.is_recording = False
        self.frame_count = 0
        self.frames_folder = "timelapse_frames"
        self.output_file = None

        
        self.setup_ui()
        
    def setup_ui(self):
        # Interval input
        ttk.Label(self.root, text="Interval (seconds):").pack(pady=5)
        self.interval_var = tk.StringVar(value="1")
        ttk.Entry(self.root, textvariable=self.interval_var, width=10).pack()
        
        # Duration input
        ttk.Label(self.root, text="Duration (minutes):").pack(pady=5)
        self.duration_var = tk.StringVar(value="60")
        ttk.Entry(self.root, textvariable=self.duration_var, width=10).pack()
        
        # Control buttons
        ttk.Button(self.root, text="Start Recording", command=self.start_recording).pack(pady=5)
        ttk.Button(self.root, text="Stop & Generate", command=self.stop_and_generate).pack(pady=5)
        # ttk.Button(self.root, text="Play Video", command=self.play_video).pack(pady=5)
        # ttk.Button(self.root, text="Stop Video", command=self.stop_video).pack(pady=5)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="Ready")
        self.status_label.pack(pady=5)

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

    def start_recording(self):
        try:
            if not os.path.exists(self.frames_folder):
                os.makedirs(self.frames_folder)
                
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                raise Exception("Could not open camera")
                
            self.is_recording = True
            self.frame_count = 0
            interval = float(self.interval_var.get())
            duration = float(self.duration_var.get()) * 60
            
            def capture_frame():
                if self.is_recording and self.frame_count < (duration / interval):
                    ret, frame = self.cap.read()
                    if ret:
                        filename = f"{self.frames_folder}/frame_{self.frame_count:04d}.jpg"
                        cv2.imwrite(filename, frame)
                        self.frame_count += 1
                        self.status_label.config(text=f"Frames: {self.frame_count}")
                        self.root.after(int(interval * 1000), capture_frame)
                    
            capture_frame()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.is_recording = False
            if self.cap:
                self.cap.release()

    def stop_and_generate(self):
        if self.is_recording:
            self.is_recording = False
            self.status_label.config(text="Generating video...")
            
            frame = cv2.imread(f"{self.frames_folder}/frame_0000.jpg")
            height, width, _ = frame.shape
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_file = f"timelapse_{timestamp}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.output_file, fourcc, 30, (width, height))
            
            for i in range(self.frame_count):
                frame = cv2.imread(f"{self.frames_folder}/frame_{i:04d}.jpg")
                out.write(frame)
                
            out.release()
            if self.cap:
                self.cap.release()
                
            self.status_label.config(text="Video generated!")

    def run(self):
        self.root.mainloop()
    
    def __del__(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        if self.is_playing:
            self.player.stop()

if __name__ == "__main__":
    app = TimeLapseGenerator()
    app.run()