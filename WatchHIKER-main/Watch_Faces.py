import tkinter as tk
from tkinter import Canvas
import math
from datetime import datetime
import pytz

class WatchFaces:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Watch Faces")
        self.root.geometry("240x320")
        self.root.configure(bg="#1e1e1e")
        
        self.current_face = 0
        self.faces = ["analog", "binary", "matrix", "emoji"]
        self.start_x = 0
        
        self.setup_ui()
        self.create_analog_face()
        self.update_clock()
    
    def setup_ui(self):
        self.canvas = Canvas(
            self.root,
            width=200,
            height=200,
            bg="#1e1e1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        self.time_label = tk.Label(
            self.root,
            font=('Arial', 30),
            bg="#1e1e1e",
            fg="#00ff00"
        )
        self.time_label.pack(pady=5)
        
        # Bind swipe events
        self.root.bind("<Button-1>", self.start_swipe)
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
        
        if abs(dx) > 50 and abs(dy) < 30:
            if dx > 0:
                self.change_face(1)
            else:
                self.change_face(-1)
            self.start_x = event.x
            self.start_y = event.y
        elif dy > 80: 
            self.show_menu()
            self.start_x = event.x
            self.start_y = event.y
        
    def end_swipe(self, event):
        self.start_x = 0
    
    def change_face(self, direction):
        self.current_face = (self.current_face + direction) % len(self.faces)
        self.canvas.delete("all")
        
        if self.faces[self.current_face] == "analog":
            self.create_analog_face()
        elif self.faces[self.current_face] == "binary":
            self.create_binary_face()
        elif self.faces[self.current_face] == "matrix":
            self.create_matrix_face()
        elif self.faces[self.current_face] == "emoji":
            self.create_emoji_face()
    
    def create_analog_face(self):
        self.canvas.create_oval(10, 10, 190, 190, width=2, outline="#00ff00")
        for i in range(12):
            angle = i * math.pi/6 - math.pi/2
            start_x = 100 + 80 * math.cos(angle)
            start_y = 100 + 80 * math.sin(angle)
            end_x = 100 + 90 * math.cos(angle)
            end_y = 100 + 90 * math.sin(angle)
            self.canvas.create_line(start_x, start_y, end_x, end_y, fill="#00ff00", width=2)
        
        self.second_hand = self.canvas.create_line(100, 100, 100, 30, fill="#ff0000", width=1)
        self.minute_hand = self.canvas.create_line(100, 100, 100, 40, fill="#00ff00", width=2)
        self.hour_hand = self.canvas.create_line(100, 100, 100, 60, fill="#00ff00", width=3)
        self.canvas.create_oval(95, 95, 105, 105, fill="#00ff00")
    
    def create_binary_face(self):
        self.binary_bits = []
        for i in range(6):  # 6 rows
            y = 30 + i * 30
            for j in range(6):  # 6 columns
                x = 30 + j * 30
                bit = self.canvas.create_oval(
                    x-10, y-10,
                    x+10, y+10,
                    fill="#1e1e1e",
                    outline="#00ff00"
                )
                self.binary_bits.append(bit)
    
    def create_matrix_face(self):
        self.matrix_chars = []
        for i in range(12):  # 12 columns of falling digits
            char = {
                'id': self.canvas.create_text(
                    20 * i + 10, 0,
                    text="0",
                    fill="#00ff00",
                    font=('Courier', 16)
                ),
                'y': 0,
                'speed': (i % 3) + 1  # Variable speeds
            }
            self.matrix_chars.append(char)

    def create_emoji_face(self):
        # Base circle
        self.canvas.create_oval(10, 10, 190, 190, width=2, outline="#00ff00")
        
        # Create emoji elements
        self.emoji_eyes = [
            self.canvas.create_oval(60, 60, 80, 80, fill="#00ff00"),
            self.canvas.create_oval(120, 60, 140, 80, fill="#00ff00")
        ]
        
        # Create mouth (arc that changes with time)
        self.emoji_mouth = self.canvas.create_arc(
            50, 50, 150, 150,
            start=0, extent=180,
            fill="#00ff00"
        )
        
        # Hour markers as small dots
        for i in range(12):
            angle = i * math.pi/6
            x = 100 + 80 * math.cos(angle)
            y = 100 + 80 * math.sin(angle)
            self.canvas.create_oval(
                x-3, y-3, x+3, y+3,
                fill="#00ff00"
            )

    def update_clock(self):
        now = datetime.now()
        
        if self.faces[self.current_face] == "emoji":
            # Blink animation (every 3 seconds)
            if now.second % 3 == 0:
                for eye in self.emoji_eyes:
                    self.canvas.itemconfig(eye, fill="#1e1e1e")
            else:
                for eye in self.emoji_eyes:
                    self.canvas.itemconfig(eye, fill="#00ff00")
            
            # Mouth animation based on seconds
            mouth_extent = 180 * abs(math.sin(now.second * math.pi/30))
            self.canvas.itemconfig(
                self.emoji_mouth,
                start=0,
                extent=mouth_extent
            )
        
        elif self.faces[self.current_face] == "analog":
            second = now.second * math.pi/30 - math.pi/2
            minute = (now.minute + now.second/60) * math.pi/30 - math.pi/2
            hour = (now.hour % 12 + now.minute/60) * math.pi/6 - math.pi/2
            
            self.canvas.coords(self.second_hand, 100, 100, 100 + 85 * math.cos(second), 100 + 85 * math.sin(second))
            self.canvas.coords(self.minute_hand, 100, 100, 100 + 70 * math.cos(minute), 100 + 70 * math.sin(minute))
            self.canvas.coords(self.hour_hand, 100, 100, 100 + 50 * math.cos(hour), 100 + 50 * math.sin(hour))
        
        elif self.faces[self.current_face] == "binary":
            # Convert time to binary
            time_bits = (
                format(now.hour, '06b') +    # 6 bits for hours
                format(now.minute, '06b') +  # 6 bits for minutes
                format(now.second, '06b')    # 6 bits for seconds
            )
            
            # Update binary display
            for i, bit in enumerate(time_bits):
                self.canvas.itemconfig(
                    self.binary_bits[i],
                    fill="#00ff00" if bit == '1' else "#1e1e1e"
                )
        
        elif self.faces[self.current_face] == "matrix":
            time_str = now.strftime('%H%M%S')
            for i, char in enumerate(self.matrix_chars):
                # Update vertical position
                char['y'] += char['speed']
                if char['y'] > 200:
                    char['y'] = 0
                
                # Update digit and position
                digit = time_str[i % len(time_str)]
                self.canvas.coords(char['id'], 20 * i + 10, char['y'])
                self.canvas.itemconfig(char['id'], text=digit)

        self.time_label.config(text=now.strftime('%H:%M:%S'))
        self.root.after(50 if self.faces[self.current_face] == "matrix" else 1000, self.update_clock)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WatchFaces()
    app.run()