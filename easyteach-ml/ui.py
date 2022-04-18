import json
from tkinter import *
import tkinter
from PIL import ImageTk, Image
import cv2
import customtkinter
import tkinter.messagebox
import sys
import numpy as np
import keyboard_module as kbm

#https://www.youtube.com/watch?v=UdCSiZR8xYY
from app_main import AppMain


class App(customtkinter.CTk):

    # WIDTH = 1000 replaced by JSON file
    # HEIGHT = 600
    live = ""

    def __init__(self):
        super().__init__()
        self.config_file = "config.json"

        # load config.json
        with open(self.config_file, 'r') as f:
            self.config = json.loads(f.read())

        self.mymain = AppMain(self, self.config)
        self.settings_window = None

        self.title("EasyTeach")
        print("width: ", self.winfo_screenwidth())
        print(f"{self.config['window_width']}x{self.config['window_height']}")

        self.geometry(f"{self.config['window_width']}x{self.config['window_height']}")
        self.resizable(False, False)
        
        # Setting icon of master window
        icon = PhotoImage(file = self.config["logo_file"])
        self.iconphoto(False, icon)

        self.radio_var = tkinter.IntVar(value=0)

        self.protocol("WM_DELETE_WINDOW", self.on_closing) # close window with x

        if sys.platform == "darwin": # for mac
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)
            self.createcommand('tk::mac::Quit', self.on_closing)
        else:
            self.bind("<Alt-F4>", self.on_closing)
            self.bind("<Control-w>", self.on_closing)

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

        # ============ frame_right ============
        self.lmain = Label(self.frame_right, bg = "black")
        self.lmain.grid(padx=20, pady=20)
        # ============ frame_right -> frame_info ============

        # self.switch_2.select()

    def update_display_mode(self):
        customtkinter.set_appearance_mode("light") if self.radio_var.get() == 0 else customtkinter.set_appearance_mode("dark")
    

    def on_closing(self, event=0):
        # stop the thread
        self.stop_function()
        # close the window
        self.destroy()
        # exit the program
        exit()


    def start(self):
        self.video_stream() # starts a timer thread for video streaming
        # starts the mainloop as a thread with timer
        self.the_loop()
        #self.the_loop_timer_id = self.after(self.config['loop_delay'], self.the_loop)
        self.mainloop()


    def start_function(self):
        """
        Start function triggered by button_start
        :return:
        """
        App.live = "LIVE"
        # set run flag true
        self.mymain.startLoop()
        # set a timer to run run_video if run flag is true
        self.the_loop()


    def stop_function(self):
        """
        Stop function triggered by button_stop
        :return:
        """
        App.live = ""
        kbm.closeAltTab()
        # cancel current timer
        self.after_cancel(self.the_loop_timer_id);
        # stop video
        self.mymain.stopLoop()


    def settings_function(self):

        self.stop_function()

        self.settings_window = customtkinter.CTkToplevel(self, name="settings")
        self.settings_window.resizable(width = True, height = True)
        #self.settings_window.geometry("500x300")
        self.settings_window.title("Settings")
        self.settings_window.grid_columnconfigure(3, weight=1)
        self.settings_window.grid_rowconfigure(7, weight=1)

        #label = customtkinter.CTkLabel(window, text="BLABLABLABLABLA")

        label_radio_group = customtkinter.CTkLabel(master=self.settings_window,
                                                        text="Select display mode:")
        radio_button_0 = customtkinter.CTkRadioButton(master=self.settings_window,
                                                           variable=self.radio_var,
                                                           value=0,
                                                           text="Light Mode")
        radio_button_1 = customtkinter.CTkRadioButton(master=self.settings_window,
                                                           variable=self.radio_var,
                                                           value=1,
                                                           text="Dark Mode")

        label_radio_group.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        radio_button_0.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        radio_button_1.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        #label_radio_group.pack(side=TOP, fill=X, padx=10, pady=10)
        #radio_button_0.pack(side=TOP, fill=X, padx=10, pady=10)
        #radio_button_1.pack(side=TOP, fill=X, padx=10, pady=10)

        # add label and input field for setting the timer delay
        label_timer_delay = customtkinter.CTkLabel(master=self.settings_window,text="Set timer delay:")
        label_timer_delay.grid(row=3, column=0, sticky=W, padx=10, pady=10)

        self.input_loop_delay = customtkinter.CTkEntry(master=self.settings_window, width=100)
        self.input_loop_delay.grid(row=3, column=1, sticky=W, padx=10, pady=10)

        # set input value to current timer delay
        self.input_loop_delay.insert(0, str(self.config['loop_delay']))

        # label_action_altab = customtkinter.CTkLabel(master=self.settings_window, text="Gesture for alt-tab:")
        # label_action_altab.grid(row=4, column=0, sticky=W, padx=10, pady=10)
        # self.input_action_altab  = customtkinter.CTkEntry(master=self.settings_window, width=100)
        # self.input_action_altab.grid(row=4, column=1, sticky=W, padx=10, pady=10)
        #
        # # set input value to current timer delay
        # # find key with value 'openAltTab' in self.config['actions'] array
        # key = list(filter(lambda x: self.config['actions'][x] == 'openAltTab', self.config['actions'].keys()))[0]
        # self.input_action_altab.insert(0, key)


        #gestures
        # left hand on row 5
        label = customtkinter.CTkLabel(master=self.settings_window, text="Gestures:")
        label.grid(row=5, column=0, sticky=W, padx=5, pady=1)
        label = customtkinter.CTkLabel(master=self.settings_window, text="Action:")
        label.grid(row=6, column=0, sticky=W, padx=5, pady=1)
        label = customtkinter.CTkLabel(master=self.settings_window, text="Left hand:")
        label.grid(row=6, column=1, sticky=W, padx=5, pady=1)
        label = customtkinter.CTkLabel(master=self.settings_window, text="Right hand:")
        label.grid(row=6, column=2, sticky=W, padx=5, pady=1)

        # actions
        self.actionVar = tkinter.StringVar(app)
        self.actionVar.set(list(self.config['actions'].values())[0])
        self.actionVar.trace("w", lambda name, index, mode, actionVar=self.actionVar: self.action_changed(self.actionVar))
        optionlist = list(self.config['actions'].values())
        dropdown = tkinter.OptionMenu(self.settings_window, self.actionVar, *optionlist)
        dropdown.grid(row=7, column=0, sticky=W, padx=5, pady=1)
        #right hand
        self.actionVarLeft = tkinter.StringVar(app)
        self.actionVarLeft.set(self.mymain.get_action_labels()[0])
        #self.actionVarLeft.trace("w", lambda name, index, mode, actionVar=self.actionVarLeft: self.action_changed(self.actionVarLeft))
        optionlist = self.mymain.get_action_labels()
        dropdown = tkinter.OptionMenu(self.settings_window, self.actionVarLeft, *optionlist)
        dropdown.grid(row=7, column=1, sticky=W, padx=5, pady=1)
        #right hand
        self.actionVarRight = tkinter.StringVar(app)
        self.actionVarRight.set(self.mymain.get_action_labels()[0])
        #self.actionVarRight.trace("w", lambda name, index, mode, actionVar=self.actionVarRight: self.action_changed(self.actionVarRight))
        optionlist = self.mymain.get_action_labels()
        dropdown = tkinter.OptionMenu(self.settings_window, self.actionVarRight, *optionlist)
        dropdown.grid(row=7, column=2, sticky=W, padx=5, pady=1)

        # ok button
        button_ok = customtkinter.CTkButton(master=self.settings_window, text="Save",fg_color=("gray75", "gray30"),
                                            command =lambda: self.save_settings_window(self.settings_window))
        button_ok.grid(row=8, column=3, sticky=E, padx=30, pady=10)
        # cancel button
        button_cancel = customtkinter.CTkButton(master=self.settings_window, text="Cancel",fg_color=("gray75", "gray30"),
                                                command =lambda: self.exit_settings_window(self.settings_window))
        button_cancel.grid(row=8, column=2, sticky=E, padx=10, pady=10)

    def help_function(self):
        #self.wm_state('iconic')
        window = customtkinter.CTkToplevel(self)
        window.geometry("500x500")
        window.title("Help")
        label = customtkinter.CTkLabel(window, text="BLABLABLABLABLA")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
        b = customtkinter.CTkButton(master=window, text="Okay",fg_color=("gray75", "gray30"), command =lambda: self.exit_top_window(window))
        b.pack(padx=20, pady=20)


    def about_function(self):
        #self.wm_state('iconic')
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

    def save_settings_window(self, window):
        # save settings
        self.config['loop_delay'] = self.input_loop_delay.get()

        # update gesture
        # first remove gesture already defined
        # find index of value self.actionVar.get()
        index = list(self.config['actions'].values()).index(self.actionVar.get())
        # remove from config
        del self.config['actions'][list(self.config['actions'].keys())[index]]
        # add new gesture
        # create a str like "['Close', 'Open']" as an index to the action
        indexgesture = str([self.actionVarLeft.get(), self.actionVarRight.get()]).replace(" ", "")
        self.config['actions'][indexgesture] = self.actionVar.get()

        self.update_display_mode()
        self.save_config()

        self.exit_settings_window(window)

    def exit_settings_window(self, window):
        window.destroy()
        self.settings_window = None

    def save_config(self):
        with open(self.config_file, 'w') as outfile:
            json.dump(self.config, outfile)
        # flush buffer
        outfile.close()


    def the_loop(self):
        # print("the loop")
        if self.mymain.is_running():
            self.mymain.run_video()

        self.the_loop_timer_id = self.after(self.config['loop_delay'], self.the_loop)

    def video_stream(self):
        """
        This function is used to start the video stream and acts as a timer
        :return:
        """
        # print("video stream")
        # cap = self.mymain.get_video()
        # _, frame = cap.read()

        # if frame is None system is not running yet
        if self.mymain.get_frame() is None:
            print ("frame is None")
            self.lmain.after(self.config['video_delay'], self.video_stream)
            return

        frame = self.mymain.get_frame()

        #set the size of the image to be displayed in the window in percent of the window size (0.0 - 1.0)
        frame = cv2.resize(frame, (self.config["window_width"] - 180 -20 - 20 -20 -2 ,
                                   self.config["window_height"] - 20 - 20 - 20 - 20),
                                   interpolation = cv2.INTER_AREA)

        #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # insert the logo

        logo = cv2.imread(self.config["logo_file"])
        size = 100
        logo = cv2.resize(logo,(size,size))

        img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        # Region of Interest (ROI), where we want to insert logo
        roi = frame[-size-10:-10, -size-10:-10]
        # Set an index of where the mask is
        roi[np.where(mask)] = 0
        roi += logo

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = Image.fromarray(cv2image)
        #img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)

        # restart the timer
        self.lmain.after(self.config['video_delay'], self.video_stream)

    def action_changed(self, actionVar):
        """
        update the 2 other action variables according to the selected action
        :param actionVar:
        :return:
        """
        # find key of value self.actionVar.get() in self.config['actions']
        for key, value in self.config['actions'].items():
            if value == actionVar.get():
                # extract the 2 actions from the key
                gestures = str(key).replace(" ", "").replace("[", "").replace("]", "").replace("'","").split(",")
                self.actionVarLeft.set(gestures[0])
                self.actionVarRight.set(gestures[1])
                break



if __name__ == "__main__":
    print("start UI")
    app = App()
    app.start()


 
