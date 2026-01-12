import tkinter as tk
import requests
import math
import smtplib
from email.mime.text import MIMEText
from email.header import Header


BOT_TOKEN = ''
CHAT_ID = ''


def send_email_alert(sender_email, auth_code, receiver_email, subject, content):
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = Header(subject, 'utf-8')

        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        smtp.login(sender_email, auth_code)
        smtp.sendmail(sender_email, [receiver_email], msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print("邮件发送失败：", e)
        return False


class SosApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SOS Alert")
        self.root.geometry("300x400")
        self.root.configure(bg="#2c3e50")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="Emergency SOS", font=("Arial", 20), bg="#2c3e50", fg="white")
        title.pack(pady=20)
        
        # SOS Button
        self.sos_button = RoundButton(self.root, 200, 200, "#ff0000", self.send_alert)
        self.sos_button.pack(pady=20)
        
        # Status Label
        self.status = tk.Label(self.root, text="Ready", font=("Arial", 12), bg="#2c3e50", fg="white")
        self.status.pack(pady=10)

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

    def send_alert(self):
        self.status.config(text="Sending alert...", fg="yellow")

        # 设置你的邮箱信息
        sender = "2458369534@qq.com" # 换成自己的邮箱
        auth_code = "" # 换成自己的
        receiver = "2458369534@qq.com"
        subject = "SOS ALERT"
        content = "这是一个来自紧急按钮的SOS求助消息！"

        success = send_email_alert(sender, auth_code, receiver, subject, content)

        if success:
            self.status.config(text="Alert sent!", fg="green")
        else:
            self.status.config(text="Failed to send!", fg="red")

        self.root.after(3000, lambda: self.status.config(text="Ready", fg="white"))


class RoundButton(tk.Canvas):
    def __init__(self, parent, width, height, color, command):
        super().__init__(parent, width=width, height=height, bg="#2c3e50", highlightthickness=0)
        self.command = command
        self.color = color
        self.pulse_size = 0
        
        # Create button elements
        self.circle = self.create_oval(30, 30, width-30, height-30, fill=color, outline=color)
        self.pulse = self.create_oval(0, 0, width, height, outline=color, width=2)
        self.text = self.create_text(width//2, height//2, text="SOS", fill="white", font=("Arial Bold", 24))
        
        # Start animation and bind click
        self.bind("<Button-1>", self.on_click)
        self.animate_pulse()
        
    def animate_pulse(self):
        self.pulse_size = (self.pulse_size + 1) % 20
        scale = self.pulse_size / 20
        
        # Update pulse circle
        self.coords(self.pulse, 
                   20 - self.pulse_size * 2,
                   20 - self.pulse_size * 2,
                   180 + self.pulse_size * 2,
                   180 + self.pulse_size * 2)
        
        # Update opacity
        alpha = hex(int(255 * (1 - scale)))[2:].zfill(2)
        self.itemconfig(self.pulse, outline=f"#{alpha}0000")
        
        self.after(50, self.animate_pulse)
        
    def on_click(self, event):
        # Click animation
        self.itemconfig(self.circle, fill="#cc0000")
        self.after(100, lambda: self.itemconfig(self.circle, fill=self.color))
        if self.command:
            self.command()

if __name__ == "__main__":
    app = SosApp()
    app.root.mainloop()