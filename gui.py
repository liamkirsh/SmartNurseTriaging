from Tkinter import *
from PIL import Image, ImageTk
import cv2
import multiprocessing
import threading


class App(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.wm_title("Smart Nurse")
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (WelcomePage, VitalsPage,):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        w_label = Label(self, text="Welcome to the Belleville Hospital!", font=("Helvetica", 24))
        w_label.pack()

        d_image = Image.open("res/doctor.jpg")
        d_photo = ImageTk.PhotoImage(d_image)
        p_label = Label(self, image=d_photo)
        p_label.image = d_photo
        p_label.pack()

        w_button = Button(self, text="Check In", command=lambda: controller.show_frame("VitalsPage"))
        w_button.pack(fill=BOTH, expand=1, padx=2, pady=2)

class VitalsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        fname = 'test.avi'
        w_label = Label(self, text="We will now check your vitals. Please stand still and look into the camera.")
        w_label.pack()

        cap = cv2.VideoCapture(0)
        lmain = Label(self)
        lmain.pack()
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        def show_frame():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, show_frame)

        show_frame()


if __name__ == "__main__":
    app = App()
    app.mainloop()
