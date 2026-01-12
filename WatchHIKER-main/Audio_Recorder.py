#  -*- coding: UTF-8 -*-

# MindPlus
# Python
from unihiker import Audio
import tkinter as tk
from tkinter import ttk
import time
import threading
from datetime import datetime
import os

class AudioRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Audio Recorder")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.audio = Audio()
        self.recording = False
        self.elapsed_time = 0
        self.recordings_dir = "recordings"
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)
        self.setup_ui()

    def setup_ui(self):
        # Main container frame
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both")
        
        # Toggle button for start/stop
        self.toggle_btn = tk.Button(
            main_frame,
            text="START",
            command=self.toggle_recording,
            bg="#00ff00",
            fg="#000000",
            width=20,
            height=2,
            font=("Arial", 16, "bold")
        )
        self.toggle_btn.pack(pady=10)
        
        # Status text
        self.status_label = tk.Label(
            main_frame,
            text="Ready to Record",
            font=("Arial", 16),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.status_label.pack(pady=10)
        
        # Recording indicator
        self.canvas = tk.Canvas(
            main_frame,
            width=100,
            height=100,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        self.indicator = self.canvas.create_oval(
            25, 25, 75, 75,
            fill="#1e1e1e",
            outline="#ff0000",
            width=2
        )
        
        # Timer display
        self.timer_label = tk.Label(
            main_frame,
            text="00:00",
            font=("Arial", 24),
            bg="#1e1e1e",
            fg="#ffffff"
        )
        self.timer_label.pack(pady=10)

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

    def update_timer(self):
        while self.recording:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
            time.sleep(1)
    
    def animate_indicator(self):
        pulse_state = True
        while self.recording:
            self.canvas.itemconfig(
                self.indicator,
                fill="#ff0000" if pulse_state else "#1e1e1e"
            )
            pulse_state = not pulse_state
            time.sleep(0.5)
    
    def toggle_recording(self):
        if not self.recording:
            # Start Recording
            self.recording = True
            self.elapsed_time = 0
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_file = os.path.join(self.recordings_dir, f"recording_{timestamp}.wav")
            
            self.status_label.config(text="Recording...")
            self.toggle_btn.config(
                text="STOP",
                bg="#ff0000",
                fg="#ffffff"
            )
            
            # Start recording in separate thread
            threading.Thread(target=self.audio.start_record, args=(self.current_file,), daemon=True).start()
            
            # Start timer and animation
            threading.Thread(target=self.update_timer, daemon=True).start()
            threading.Thread(target=self.animate_indicator, daemon=True).start()
        else:
            # Stop Recording
            self.recording = False
            self.audio.stop_record()
            self.status_label.config(text=f"Saved: {os.path.basename(self.current_file)}")
            self.toggle_btn.config(
                text="START",
                bg="#00ff00",
                fg="#000000"
            )
            self.canvas.itemconfig(self.indicator, fill="#1e1e1e")

        print("当前录音保存路径：", os.path.abspath(self.recordings_dir))

    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AudioRecorder()
    app.run()