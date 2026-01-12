import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class VideoStreamApp:
    def __init__(self, root, stream_url):
        self.root = root
        self.root.title("Video Stream")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.stream_url = stream_url
        self.cap = cv2.VideoCapture(self.stream_url)
        
        self.setup_ui()
        self.update_frame()
        
    def setup_ui(self):
        self.video_frame = ttk.LabelFrame(self.root, text="Video Stream")
        self.video_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(self.video_frame, width=240, height=320, bg="#1e1e1e")
        self.canvas.pack()

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
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (240, 320))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.imgtk = imgtk
        
        self.root.after(10, self.update_frame)
        
    def run(self):
        self.root.mainloop()
        self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoStreamApp(root, "http://10.181.34.185:8080/video")
    app.run()
