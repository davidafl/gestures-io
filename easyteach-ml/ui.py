import json
from tkinter import *
import tkinter

from PIL import ImageTk, Image
import cv2
import customtkinter
import tkinter.messagebox
import sys
import numpy as np
from tkvideo import tkvideo

# our packages
import keyboard_module as kbm
import keypoint_classification as kpc

#https://www.youtube.com/watch?v=UdCSiZR8xYY
from app_main import AppMain


class App(customtkinter.CTk):

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.config_file = "config.json"

        # load config.json
        with open(self.config_file, 'r') as f:
            self.config = json.loads(f.read())
            f.close()

        # build and set the gesture recognition engine and pass the UI (self)
        self.mymain = AppMain(self)

        self.settings_window = None # we will build it later when needed
        # load images
        self.button_img = PhotoImage(file ="resources/button.png")
        self.help_img = PhotoImage(file="resources/header.png")
        self.about_img = PhotoImage(file="resources/about.png")

        self.title("Gestures.io")
        #print(f"{self.config['window_width']}x{self.config['window_height']}")

        self.geometry(f"{self.config['window_width']}x{self.config['window_height']}")
        self.resizable(False, False)
        
        # Setting icon of master window
        icon = PhotoImage(file = self.config["logo_file"])
        self.iconphoto(False, icon)

        # the variable bound to the radio buttons (display mode)
        self.radio_var = tkinter.IntVar(value=0)

        # listener for delete window event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

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


        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Gestures.io",
                                              text_font=("Roboto Medium", -25))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        #self.img = self.img.subsample(2, 2) # scale image to 50%

        self.button_start = Button(master=self.frame_left,
                                   text="Start",
                                   compound=tkinter.CENTER,
                                   image = self.button_img,
                                   borderwidth=0,
                                   command=self.start_button)
        self.button_start.grid(row=2, column=0, pady=10, padx=20)

        self.button_stop = Button(master=self.frame_left,
                                  text="Stop",
                                  compound=tkinter.CENTER,
                                  image = self.button_img,
                                  borderwidth=0,
                                  command=self.stop_button)
        self.button_stop.grid(row=3, column=0, pady=10, padx=20)

        self.button_settings = Button(master=self.frame_left,
                                      text="Settings",
                                      compound=tkinter.CENTER,
                                      image = self.button_img,
                                      borderwidth=0,
                                      command=self.settings_button)
        self.button_settings.grid(row=4, column=0, pady=10, padx=20)

        self.button_help = Button(master=self.frame_left,
                                  text="Help",
                                  compound=tkinter.CENTER,
                                  image = self.button_img,
                                  borderwidth=0,
                                  command=self.help_button)
        self.button_help.grid(row=5, column=0, pady=10, padx=20)

        self.button_about = Button(master=self.frame_left,
                                   #self.button_about = Button(master=self.frame_left,
                                   text="About",
                                   compound=tkinter.CENTER,
                                   image = self.button_img,
                                   borderwidth=0,
                                   command=self.about_button)
        self.button_about.grid(row=6, column=0, pady=10, padx=20)

        self.button_quit = Button(master=self.frame_left,
                                  text="Quit",
                                  compound=tkinter.CENTER,
                                  image = self.button_img,
                                  borderwidth=0,
                                  command=self.on_closing)
        self.button_quit.grid(row=7, column=0, pady=10, padx=20)


        # ============ frame_right ============
        self.lmain = Label(self.frame_right, bg = "black")  # background color
        self.lmain.grid(padx=20, pady=20)

        # display a video window on top of main window
        self.video_label = Label(self.frame_right, bg = "grey")
        self.video_label.grid(row=0, column=0, columnspan=8, rowspan=15, sticky="nswe")
        player = tkvideo("resources/splash.mp4", self.video_label, loop=1, size=(1100, 600))
        player.play()
        # destroy the label after the video is done playing
        self.after(10000, self.video_label.destroy) # destroy after 10 seconds

    def update_display_mode(self):
        """
        Update the display mode of the main window
        :return:
        """
        customtkinter.set_appearance_mode("light") if self.radio_var.get() == 0 else customtkinter.set_appearance_mode("dark")
    

    def on_closing(self):
        """
        Close the main window and exit the program
        :return:
        """
        # stop the gesture recognition and video capture
        self.stop_button()
        # close the window
        self.destroy()
        # exit the program
        exit(0)


    def start(self):
        """
        Start the gesture recognition and video capture
        :return:
        """
        self.video_stream() # starts a timer thread for video streaming
        # starts the mainloop as a thread with timer
        self.the_loop()
        # start in stopped state - let the splash video play!
        # self.stop_function() - UNDER DEVELOPMENT - not working yet
        self.mainloop()


    def start_button(self):
        """
        Start function triggered by button_start
        :return:
        """
        self.mymain.startLoop() # set run flag true
        self.the_loop() # set a timer to run run_video if run flag is true


    def stop_button(self):
        """
        Stop function triggered by button_stop
        :return:
        """
        kbm.closeAltTab() # release the keyboard alt-tab
        self.after_cancel(self.the_loop_timer_id) # cancel current timer
        self.mymain.stopLoop() # stop video


    def settings_button(self):

        self.stop_button() # stop the video

        if (self.settings_window == None):

            self.settings_window = customtkinter.CTkToplevel(self, name="settings") # create a new window
            self.settings_window.resizable(width = True, height = True) # make the window resizable
            # attach self.exit_settings_window(window) to the window's close button
            self.settings_window.protocol("WM_DELETE_WINDOW", self.cancel_settings_button)

            # add an image background
            #self.settings_window.img_background = ImageTk.PhotoImage(Image.open("resources/bg-tech.png"))
            #bg_label = Label(self.settings_window, image=self.settings_window.img_background)
            #bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            self.settings_window.title("Settings") # set the title of the window
            self.settings_window.grid_columnconfigure(3, weight=1) # make the column 3 stretchable
            self.settings_window.grid_rowconfigure(len(self.config["actions"]) + 12, weight=1) # make the row stretchable

            # mode light/dark radio button
            label_radio_group = Label(master=self.settings_window,text="Select display mode:", font=("Helvetica", 12))
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

            # add label and input field for setting the timer delay
            label_timer_delay = Label(master=self.settings_window,text="Set main delay:", font=("Helvetica", 12), anchor=W)
            label_timer_delay.grid(row=3, column=0, sticky=W, padx=10, pady=10)
            self.input_loop_delay = Entry(master=self.settings_window, width=30)
            self.input_loop_delay.grid(row=3, column=1, sticky=W, padx=10, pady=10)
            self.input_loop_delay.insert(0, str(self.config['loop_delay']))

            # actions delay
            label_actions_delay = Label(master=self.settings_window,text="Set actions delay:", font=("Helvetica", 12), anchor=W)
            label_actions_delay.grid(row=4, column=0, sticky=W, padx=10, pady=10)
            self.input_actions_delay = Entry(master=self.settings_window, width=30)
            self.input_actions_delay.grid(row=4, column=1, sticky=W, padx=10, pady=10)
            self.input_actions_delay.insert(0, str(self.config['actions_delay']))

            # video delay
            label_video_delay = Label(master=self.settings_window,text="Set video delay:", font=("Helvetica", 12), anchor=W)
            label_video_delay.grid(row=5, column=0, sticky=W, padx=10, pady=10)
            self.input_video_delay = Entry(master=self.settings_window, width=30)
            self.input_video_delay.grid(row=5, column=1, sticky=W, padx=10, pady=10)
            self.input_video_delay.insert(0, str(self.config['video_delay']))

            #gestures
            #label = customtkinter.CTkLabel(master=self.settings_window, text="Configure your gestures:") # this is old custom tkinter code.
            label = Label(master=self.settings_window, text="Configure your gestures:", font=("Helvetica", 14))
            label.grid(row=6, column=0, sticky=W, padx=0, pady=1)
            label = Label(master=self.settings_window, text="Action:", anchor=W, font=("Helvetica", 12))
            label.grid(row=7, column=0, sticky=W, padx=0, pady=1)
            label = Label(master=self.settings_window, text="Left hand:", anchor=W, font=("Helvetica", 12))
            label.grid(row=7, column=1, sticky=W, padx=0, pady=1)
            label = Label(master=self.settings_window, text="Right hand:", anchor=W, font=("Helvetica", 12))
            label.grid(row=7, column=2, sticky=W, padx=0, pady=1)

            # actions
            self.actionVar = tkinter.StringVar(app)
            # get the list of actions from the actionsDefault key (we assume all of them are there)
            self.actionVar.set(list(self.config['actionsDefault'].values())[0])
            # update other dropdowns upon change
            self.actionVar.trace("w", lambda name, index, mode, actionVar=self.actionVar: self.action_changed(self.actionVar))
            optionlist = list(self.config['actionsDefault'].values()) # make a copy of the list of actions
            dropdown = tkinter.OptionMenu(self.settings_window, self.actionVar, *optionlist)
            dropdown.grid(row=8, column=0, sticky=W, padx=5, pady=1)

            #left hand
            self.actionVarLeft = tkinter.StringVar(app)
            self.actionVarLeft.set(self.mymain.get_action_labels()[0])
            # optionlist is a copy of  self.mymain.get_action_labels() because we add "None" to the list
            optionlist = list(self.mymain.get_action_labels()) # make a copy of the list of actions
            optionlist.insert(0, "None") # add "None" to the list

            dropdown = tkinter.OptionMenu(self.settings_window, self.actionVarLeft, *optionlist)
            dropdown.grid(row=8, column=1, sticky=W, padx=5, pady=1)

            #right hand
            self.actionVarRight = tkinter.StringVar(app)
            self.actionVarRight.set(self.mymain.get_action_labels()[0])

            dropdown = tkinter.OptionMenu(self.settings_window, self.actionVarRight, *optionlist)
            dropdown.grid(row=8, column=2, sticky=W, padx=5, pady=1)

            self.action_changed(self.actionVar) # trigger initial action update
            self.display_gestures_config_table(fromrow=9) # display a table of all gestures in config

            nextrow = 9 + len(self.config["actionsDefault"]) + 1 # hack to get the row number of the next row to be added

            # button to run the training
            button = Button(master=self.settings_window, text="Train gestures", command=self.train_gestures)
            button.grid(row=nextrow, column=0, sticky=W, padx=10, pady=10)

            # save button
            save_settings_button = Button(master=self.settings_window, text="Save",
                                          compound=tkinter.CENTER,
                                          image = self.button_img,
                                          borderwidth=0,
                                          command =lambda: self.save_settings(self.settings_window))
            save_settings_button.grid(row=nextrow+1, column=3, sticky=E, padx=30, pady=10)

            # cancel button
            cancel_settings_button = Button(master=self.settings_window, text="Cancel",
                                            compound=tkinter.CENTER,
                                            image = self.button_img,
                                            borderwidth=0,
                                            command =self.cancel_settings_button)
            cancel_settings_button.grid(row=nextrow+1, column=2, sticky=E, padx=10, pady=10)

        else:
            # window already exists, show window
            self.display_gestures_config_table(fromrow=9) # rebuild the table of gestures
            self.settings_window.deiconify()

    def display_gestures_config_table(self, fromrow=0):
        """
        Display a table of all gestures in the settings window
        :param fromrow: index of the first row to be displayed
        :return: nothing
        """
        rows = []
        i = 1
        for key, value in self.config['actions'].items():
            gestures = str(key).replace(" ", "").replace("[", "").replace("]", "").replace("'","").split(",")
            cols = []
            for j in range(3):
                e = Entry(self.settings_window, width=10)
                e.grid(row=fromrow+i, column=j, sticky=NSEW, padx=5, pady=1)
                if j == 0:
                    e.insert(j, value)
                elif j == 1:
                    e.insert(j, gestures[0])
                elif j == 2:
                    e.insert(j, gestures[1])
                e.config(state=DISABLED) # disable editing
                cols.append(e)
            rows.append(cols)
            i = i + 1

    def help_button(self):
        """
        Display the help window
        :return:
        """
        self.stop_button()
        self.help_window = customtkinter.CTkToplevel(self)
        self.help_window.title("Help")
        label = Label(self.help_window, image=self.help_img, bg="black", bd=0)

        label.pack(expand=YES, fill=BOTH) # fill the window with the image

        # load the text file resources/help.txt and display the text under the label image with a scrollbar
        with open("resources/help.txt", "r") as f:
            text = f.read()
            f.close()
        text_widget = Text(self.help_window, height=20, width=60, bg="white", fg="black", bd=0)
        text_widget.insert(END, text)
        # set font
        text_widget.config(font=("Helvetica", 12))
        text_widget.config(state=DISABLED)
        text_widget.pack(expand=YES, fill=BOTH)

        # scrollbar in case text is too long
        scrollbar = Scrollbar(self.help_window, orient=VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_widget.config(yscrollcommand=scrollbar.set)

        # close button of help window
        b = Button(master=self.help_window, text="Close",
                   compound=tkinter.CENTER,
                   image=self.button_img,
                   command =lambda: self.exit_and_destroy_window(self.help_window))
        b.pack(side="bottom", fill="both", expand=True)


    def about_button(self):
        """
        Display the about window
        :return:
        """
        self.stop_button()
        self.about_window = customtkinter.CTkToplevel(self)
        self.about_window.title("About")
        label = Label(self.about_window, image=self.about_img, bg="black", bd=0)

        label.pack(expand=YES, fill=BOTH)
        b = Button(master=self.about_window, text="Close",
                   compound=tkinter.CENTER,
                   image=self.button_img,
                   command =lambda: self.exit_and_destroy_window(self.about_window))
        b.pack(side="bottom", fill="both", expand=True)


    def exit_and_destroy_window(self, window):
        """
        Destroy the window and start the program again
        :param window:
        :return:
        """
        window.destroy()
        self.update_display_mode()

    def save_settings(self, window):
        """
        Save the settings to the config.json file
        :param window:
        :return:
        """
        self.config['loop_delay'] = self.input_loop_delay.get()
        self.config['video_delay'] = self.input_video_delay.get()
        self.config['actions_delay'] = self.input_actions_delay.get()

        # update gesture
        # first remove gesture already defined
        # find index of value self.actionVar.get()
        index = list(self.config['actionsDefault'].values()).index(self.actionVar.get())
        # remove from config
        try:
            del self.config['actions'][list(self.config['actions'].keys())[index]]
        except:
            pass # ignore if not found


        # create a str like "['Close', 'Open']" as an index to the action
        indexgesture = str([self.actionVarLeft.get(), self.actionVarRight.get()]).replace(" ", "")
        # save new gesture definition
        self.config['actions'][indexgesture] = self.actionVar.get()

        self.update_display_mode() # needed for tk
        self.save_json() # save config file
        self.cancel_settings_button() # close window

    def cancel_settings_button(self):
        """
        Close the settings window (don't destroy it)
        :return:
        """
        self.settings_window.withdraw()

    def save_json(self):
        """
        Save the self.config dictionary to the config.json file
        :return:
        """
        with open(self.config_file, 'w') as outfile:
            json.dump(self.config, outfile)
            outfile.close()


    def the_loop(self):
        """
        The main loop of the program handling the video and actions
        runs as a infinite loop
        :return:
        """
        if self.mymain.is_running():
            self.mymain.run_video()

        self.the_loop_timer_id = self.after(self.config['loop_delay'], self.the_loop)

    def video_stream(self):
        """
        This function is used to start the video stream runs as a periodic timer (infinite loop)
        :return:
        """

        # if frame is None system is not running yet
        if self.mymain.get_frame() is None:
            self.lmain.after(self.config['video_delay'], self.video_stream) # wait and try again
            return

        frame = self.mymain.get_frame()

        #set the size of the image to be displayed in the window in percent of the window size (0.0 - 1.0)
        frame = cv2.resize(frame, (self.config["window_width"] - 180 -20 - 20 -20 -2 ,
                                   self.config["window_height"] - 20 - 20 - 20 - 20),
                                   interpolation = cv2.INTER_AREA)

        #insert the logo
        logo = cv2.imread(self.config["logo_file"])
        size = 100
        logo = cv2.resize(logo,(size,size))
        img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
        # Region of Interest (ROI), where we want to insert logo
        # define a region at bottom right corner
        rows,cols,channels = frame.shape
        roi = frame[rows-size:rows, 0:size]
        # Set an index of where the mask is
        roi[np.where(mask)] = 0
        roi += logo
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk) # display the image

        # restart the timer to call the video stream
        self.lmain.after(self.config['video_delay'], self.video_stream)

    def action_changed(self, actionVar):
        """
        update the 2 other action variables (dropdowns) according to the selected action
        :param actionVar:
        :return:
        """
        # find key of value self.actionVar.get() in self.config['actions']
        for key, value in self.config['actions'].items():
            if value == actionVar.get():
                # extract the 2 actions from the key
                gestures = str(key).replace(" ", "").replace("[", "").replace("]", "").replace("'","").split(",")
                self.actionVarLeft.set(gestures[0]) # set the left action
                self.actionVarRight.set(gestures[1]) # set the right action
                break

    def train_gestures(self):
        """
        run the classifier training to train new gesture.
        (ex jupyter file): keypoints_classification.py
        :return:
        """
        num_gestures = self.mymain.number_of_gestures # number of gestures
        if (self.mymain.is_teaching): # if we added data in keypoints.csv
            num_gestures = num_gestures+1 # add 1 to the number of gestures

        print("Training " + str(num_gestures) + " gestures.")
        print("Please wait...")
        kpc.run_training(num_gestures)

        self.settings_window.destroy() # force reload gestures ? to check if it works ##############
        self.settings_window = None

        print("Training complete!")




if __name__ == "__main__":
    print("start UI")
    app = App() # create the app
    app.start() # start the app


 
