import cv2
import ttkbootstrap as tk
from PIL import Image, ImageTk
from model import check_if_waste

class CameraApp:
    def __init__(self, window, window_title):
        
        self.window = window

        self.window.title(window_title)

        self.video_source = 0  # Use the default camera (you can change this if needed)

        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(3), height=self.vid.get(4))
        self.canvas.pack(pady=50, padx=100)

        # self.btn_snapshot = tk.Button(window, text="Snapshot", width=10, command=self.snapshot)
        # self.btn_snapshot.pack(padx=20, pady=10)

        self.window.after(1000, self.snapshot)

        self.label = tk.Label(text="", font=("Arial",16,"bold"))
        self.label.pack()

        self.btn_exit = tk.Button(window, text="Exit", width=50, command=self.exit_app)
        self.btn_exit.pack(pady=50)

        self.update()
        self.window.mainloop()

    #cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", frame)
            val = check_if_waste(frame)
            if(val==True):
                self.label.config(text="Waste")
            else:
                self.label.config(text="Not a Waste")

        self.window.after(10000, self.snapshot)

    def exit_app(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

if __name__ == "__main__":
    root = tk.Window(themename="darkly", size=(800,800))
    app = CameraApp(root, "Waste Detector")