from Tkinter import *
from PIL import Image, ImageTk
from SimpleCV import Camera, VideoStream, Color, Display


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
    fname = 'test.avi'

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        w_label = Label(self, text="We will now check your vitals. Please stand still and look into the camera.")
        w_label.pack()

        vs = VideoStream(fps=20, filename=fname, framefill=False)
        cam = Camera()
        disp = Display((800, 600))
        while disp.isNotDone():
            img = cam.getImage()
            img = img.edges()
            vs.writeFrame(img)
            img.save(disp)

if __name__ == "__main__":
    app = App()
    app.mainloop()
