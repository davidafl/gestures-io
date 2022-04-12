from tkinter import *
from PIL import ImageTk, Image
import cv2
from main import main

def start_function():
    global live
    live = "LIVE"
    mymain.startLoop()
    the_loop()


def stop_function():
    global live
    live = ""
    mymain.stopLoop()


def settings_function():
    pass


def help_function():
    print("Help")


def about_function():
    pass


def the_loop():
    if mymain.is_running():
        mymain.run_video()
    root.after(1000, the_loop) 
    
# function for video streaming
def video_stream():
    global live

    cap = mymain.get_video()
    _, frame = cap.read()

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        
    cv2.putText(cv2image, f'{live}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3,cv2.LINE_AA)

    
    img = Image.fromarray(cv2image)
    
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream) 

# def stop_video_stream():
#     cap = mymain.get_video()
#     cap.release()
#     # lmain.destroy()


SIZE_X_BUTTON = 8
SIZE_Y_BUTTON = 4
live = "" 

if __name__ == "__main__":
    #https://www.youtube.com/watch?v=UdCSiZR8xYY

    print("start UI")

    mymain = main()
    root = Tk()
    root.title("EasyTeach")
    root.geometry("700x600")
    

    #new 5 buttons in same size in 1 column 
    button_start = Button(root, text="Start", width=SIZE_X_BUTTON, height=SIZE_Y_BUTTON, command=start_function)
    button_stop = Button(root, text="Stop", width=SIZE_X_BUTTON, height=SIZE_Y_BUTTON, command=stop_function)
    button_settings = Button(root, text="Settings", width=SIZE_X_BUTTON, height=SIZE_Y_BUTTON, command=settings_function)
    button_help = Button(root, text="Help", width=SIZE_X_BUTTON, height=SIZE_Y_BUTTON, command=help_function)
    button_about = Button(root, text="About", width=SIZE_X_BUTTON, height=SIZE_Y_BUTTON, command=about_function)

    button_start.grid(row=2, column=1)
    button_stop.grid(row=3, column=1)
    button_settings.grid(row=4, column=1)
    button_help.grid(row=5, column=1)
    button_about.grid(row=6, column=1)



    app = Frame(root, bg="white")
    app.grid(row=2, column=2, rowspan=5, columnspan=2)
    # Create a label in the frame
    lmain = Label(app)
    lmain.grid()

    video_stream()    
    root.after(1000, the_loop)
    root.mainloop()
