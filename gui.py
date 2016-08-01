from Tkinter import *
from PIL import Image, ImageTk
import cv2
import multiprocessing
import time

RECORD_SECS = 3

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
        self.time = RECORD_SECS

        fname = 'test.avi'
        w_label = Label(self,
                        text="We will now check your vitals. Please stand still and look into the camera.\nPress Start to begin recording.",
                        font=("Helvetica", 24))
        w_label.pack()

        self.cap = cv2.VideoCapture(0)
        self.record = 0

        self.lmain = Label(self)
        self.lmain.pack()
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        self.show_frame()
        self.start_button = Button(self, text="Start", font=("Arial", 20), command=self.event_click)
        self.start_button.pack(fill=BOTH, expand=1, padx=2, pady=2)

    def show_frame(self):
        self._, self.frame = self.cap.read()
        fourcc = cv2.cv.CV_FOURCC(*'MP4V')
        self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (self.frame.shape[1], self.frame.shape[0]))
        if self.record == 1:
            self.start_recording_proc()
            self.record = 2
        frame = cv2.flip(self.frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_frame)

    def event_click(self):
        self.start_button.config(state="disabled")
        self.countdown()
        self.record = 1
            
    def countdown(self):
        if self.time > 0:
            self.start_button.config(text=self.time)
            self.time = self.time - 1
            self.after(1000, self.countdown)
        elif self.time == 0:
            self.time = self.time - 1
            self.start_button.config(text="Done")
            self.stop_recording()

    def start_recording_proc(self):
        global p
        print "starting process"
        p = multiprocessing.Process(target=self.start_recording)
        p.start()

    def start_recording(self):
        while self.out.isOpened() and self.time > 0:
            try:
                stat, frame = self.cap.read()
                if stat == 0:
                    break
                if self.out.isOpened():
                    self.out.write(frame)
                    time.sleep(50) 
            except:
                continue

    def stop_recording(self):
        #self.record = 3
        #self.cap.release()
        p.terminate()
        self.out.release()


if __name__ == "__main__":
    app = App()
    app.mainloop()
