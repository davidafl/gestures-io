from doctest import master
from tkinter import *
import tkinter
from turtle import begin_fill, position, width
from PIL import ImageTk, Image
from matplotlib import backends
import cv2
from main import main
import customtkinter
import tkinter.messagebox
import sys
from tkinter import messagebox
import numpy as np


#https://www.youtube.com/watch?v=UdCSiZR8xYY

class App(customtkinter.CTk):

    WIDTH = 1000
    HEIGHT = 600
    live = ""

    # WIDTH = 666
    # HEIGHT = 400 
    # live = ""

    def __init__(self):
        super().__init__()

        self.mymain = main()

        self.title("EasyTeach")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        
        # Setting icon of master window
        icon = PhotoImage(file = "resources\EasyTeachLogo.png")
        self.iconphoto(False, icon)
        self.radio_var = tkinter.IntVar(value=0)
        

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)

        # ============ create two frames ============

        # configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        # #############################
        # img = ImageTk.PhotoImage(file = "EasyTeachLogo.png")
    
        # self.logo = Label(self.frame_left, image=img , borderwidth = 0 , highlightthickness = 0)
        # self.logo.image = img
        # self.logo.grid(row=0, column=0, columnspan=2, sticky="nswe")
        # #############################

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="EasyTeach",
                                              text_font=("Roboto Medium", -25))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_start = customtkinter.CTkButton(master=self.frame_left,
                                                text="Start",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.start_function)
        self.button_start.grid(row=2, column=0, pady=10, padx=20)

        self.button_stop = customtkinter.CTkButton(master=self.frame_left,
                                                text="Stop",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.stop_function)
        self.button_stop.grid(row=3, column=0, pady=10, padx=20)

        self.button_settings = customtkinter.CTkButton(master=self.frame_left,
                                                text="Settings",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.settings_function)
        self.button_settings.grid(row=4, column=0, pady=10, padx=20)

        self.button_help = customtkinter.CTkButton(master=self.frame_left,
                                                text="Help",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.help_function)
        self.button_help.grid(row=5, column=0, pady=10, padx=20)

        self.button_about = customtkinter.CTkButton(master=self.frame_left,
                                        text="About",
                                        fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                        command=self.about_function)
        self.button_about.grid(row=6, column=0, pady=10, padx=20)

        #video frame
        self.lmain = Label(self.frame_right, bg = "black")
        self.lmain.grid(padx=20, pady=20)

    
    def update_display_mode(self):
       customtkinter.set_appearance_mode("light") if self.radio_var.get() == 0 else customtkinter.set_appearance_mode("dark")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.video_stream()    
        self.after(1000, self.the_loop)
        self.mainloop()

    def start_function(self):
        print("start button")
        App.live = "LIVE"
        self.mymain.startLoop()
        self.the_loop()

    def stop_function(self):   
        App.live = ""
        self.mymain.stopLoop()

    def settings_function(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("500x500")
        window.title("Setings")
        label = customtkinter.CTkLabel(window, text="BLABLABLABLABLA")

        label_radio_group = customtkinter.CTkLabel(master=window,
                                                        text="Select display mode:")

        radio_button_0 = customtkinter.CTkRadioButton(master=window,
                                                           variable=self.radio_var,
                                                           value=0,
                                                           text="Light Mode")

        radio_button_1 = customtkinter.CTkRadioButton(master=window,
                                                           variable=self.radio_var,
                                                           value=1,
                                                           text="Dark Mode")


        b = customtkinter.CTkButton(master=window, text="Okay",fg_color=("gray75", "gray30"), command =lambda: self.exit_top_window(window))
        
        label_radio_group.pack(side=TOP, fill=X, padx=10, pady=10)
        radio_button_0.pack(side=TOP, fill=X, padx=10, pady=10)
        radio_button_1.pack(side=TOP, fill=X, padx=10, pady=10)
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        b.pack(padx=20, pady=20)
        self.update()

    def help_function(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("500x500")
        window.title("Help")
        label = customtkinter.CTkLabel(window, text="BLABLABLABLABLA")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        b = customtkinter.CTkButton(master=window, text="Okay",fg_color=("gray75", "gray30"), command =lambda: self.exit_top_window(window))
        b.pack(padx=20, pady=20)
        self.update()

    def about_function(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("500x500")
        window.title("About")
        label = customtkinter.CTkLabel(window, text="BLABLABLABLABLA")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        b = customtkinter.CTkButton(master=window, text="Okay",fg_color=("gray75", "gray30"), command = lambda: self.exit_top_window(window))
        b.pack(padx=20, pady=20)

    def exit_top_window(self, window):
        window.destroy()
        self.update_display_mode()

    def the_loop(self):
        if self.mymain.is_running():
            self.mymain.run_video()
        self.after(1000, self.the_loop) 

    def video_stream(self):

        cap = self.mymain.get_video()
        _, frame = cap.read()
        
        #set the size of the image to be displayed in the window in percent of the window size (0.0 - 1.0)
        frame = cv2.resize(frame, (App.WIDTH - 180 -20 - 20 -20 -2 ,
                                   App.HEIGHT - 20 - 20 - 20 - 20),
                                   interpolation = cv2.INTER_AREA)


        #############
        
        logo = cv2.imread("resources\EasyTeachLogo.png")
        size = 100
        logo = cv2.resize(logo,(size,size))

        img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

        
        # Region of Interest (ROI), where we want
        # to insert logo
        roi = frame[-size-10:-10, -size-10:-10]
        
        # Set an index of where the mask is
        roi[np.where(mask)] = 0
        roi += logo
        
        ##########

        # font = cv2.FONT_HERSHEY_TRIPLEX
        # cv2.putText(frame, 
        #         f'{App.live}', 
        #         (50, 50), 
        #         font, 1, 
        #         (0, 0 , 255), 
        #         3, 
        #         cv2.LINE_4)

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(1, self.video_stream) 


if __name__ == "__main__":
    print("start UI")
    app = App()
    app.start()


 
