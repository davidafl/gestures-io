from tkinter import *
import tkinter
from turtle import position
from PIL import ImageTk, Image
import cv2
from main import main
import customtkinter
import tkinter.messagebox
import customtkinter
import sys

# def stop_video_stream():
#     cap = mymain.get_video()
#     cap.release()
#     # lmain.destroy()

#https://www.youtube.com/watch?v=UdCSiZR8xYY

class App(customtkinter.CTk):

    WIDTH = 1000
    HEIGHT = 600
    live = ""

    def __init__(self):
        super().__init__()

        self.mymain = main()

        self.title("EasyTeach")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

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


        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="CustomTkinter",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
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

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        ####################
       
        # Create a label in the frame
       
        ####################

        # configure grid layout (3x7)
        # for i in [0, 1, 2, 3]:
        #     self.frame_right.rowconfigure(i, weight=1)
            
        #self.frame_right.rowconfigure(7, weight=10)
        
        # self.frame_right.columnconfigure(0, weight=1)
        # self.frame_right.columnconfigure(1, weight=1)
        #self.frame_right.columnconfigure(2, weight=0)
        
        # self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        # self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=8, pady=20, padx=20, sticky="nsew")
        #app = Frame(self.frame_right, bg = "black")
        self.lmain = Label(self.frame_right, bg = "black")
        self.lmain.grid()
        # ============ frame_right -> frame_info ============

        # self.frame_info.rowconfigure(0, weight=1)
        # self.frame_info.columnconfigure(0, weight=1)

        self.switch_2.select()

    def button_event(self):
        print("Button pressed")

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.video_stream()    
        self.after(1000, self.the_loop)
        self.mainloop()

        ##################
    def start_function(self):
        
        App.live = "LIVE"
        self.mymain.startLoop()
        self.the_loop()


    def stop_function(self):
    
        App.live = ""
        self.mymain.stopLoop()


    def settings_function(self):
        pass


    def help_function(self):
        print("Help")


    def about_function(self):
        pass

    def the_loop(self):
        if self.mymain.is_running():
            self.mymain.run_video()
        self.after(1000, self.the_loop) 

    def video_stream(self):

        cap = self.mymain.get_video()
        _, frame = cap.read()

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  
        cv2.putText(cv2image, f'{App.live}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3,cv2.LINE_AA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(1, self.video_stream) 
        ##################

if __name__ == "__main__":
    print("start UI")
    app = App()
    app.start()


 

