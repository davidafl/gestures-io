import cv2
import numpy as np
import math
import webbrowser as wb
import os

# keyboard simulator from
# https://stackoverflow.com/questions/13564851/how-to-generate-keyboard-events

# --- Setup ---#
from ctypes import *
from time import sleep

user32 = windll.user32
kernel32 = windll.kernel32
delay = 0.01


####################################
###---KEYBOARD CONTROL SECTION---###
####################################

# --- Key Code Variables ---#
class key:
    cancel = 0x03
    backspace = 0x08
    tab = 0x09
    enter = 0x0D
    shift = 0x10
    ctrl = 0x11
    alt = 0x12
    capslock = 0x14
    esc = 0x1B
    space = 0x20
    pgup = 0x21
    pgdown = 0x22
    end = 0x23
    home = 0x24
    leftarrow = 0x26
    uparrow = 0x26
    rightarrow = 0x27
    downarrow = 0x28
    select = 0x29
    print = 0x2A
    execute = 0x2B
    printscreen = 0x2C
    insert = 0x2D
    delete = 0x2E
    help = 0x2F
    num0 = 0x30
    num1 = 0x31
    num2 = 0x32
    num3 = 0x33
    num4 = 0x34
    num5 = 0x35
    num6 = 0x36
    num7 = 0x37
    num8 = 0x38
    num9 = 0x39
    a = 0x41
    b = 0x42
    c = 0x43
    d = 0x44
    e = 0x45
    f = 0x46
    g = 0x47
    h = 0x48
    i = 0x49
    j = 0x4A
    k = 0x4B
    l = 0x4C
    m = 0x4D
    n = 0x4E
    o = 0x4F
    p = 0x50
    q = 0x51
    r = 0x52
    s = 0x53
    t = 0x54
    u = 0x55
    v = 0x56
    w = 0x57
    x = 0x58
    y = 0x59
    z = 0x5A
    leftwin = 0x5B
    rightwin = 0x5C
    apps = 0x5D
    sleep = 0x5F
    numpad0 = 0x60
    numpad1 = 0x61
    numpad3 = 0x63
    numpad4 = 0x64
    numpad5 = 0x65
    numpad6 = 0x66
    numpad7 = 0x67
    numpad8 = 0x68
    numpad9 = 0x69
    multiply = 0x6A
    add = 0x6B
    seperator = 0x6C
    subtract = 0x6D
    decimal = 0x6E
    divide = 0x6F
    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87
    numlock = 0x90
    scrolllock = 0x91
    leftshift = 0xA0
    rightshift = 0xA1
    leftctrl = 0xA2
    rightctrl = 0xA3
    leftmenu = 0xA4
    rightmenu = 0xA5
    browserback = 0xA6
    browserforward = 0xA7
    browserrefresh = 0xA8
    browserstop = 0xA9
    browserfavories = 0xAB
    browserhome = 0xAC
    volumemute = 0xAD
    volumedown = 0xAE
    volumeup = 0xAF
    nexttrack = 0xB0
    prevoustrack = 0xB1
    stopmedia = 0xB2
    playpause = 0xB3
    launchmail = 0xB4
    selectmedia = 0xB5
    launchapp1 = 0xB6
    launchapp2 = 0xB7
    semicolon = 0xBA
    equals = 0xBB
    comma = 0xBC
    dash = 0xBD
    period = 0xBE
    slash = 0xBF
    accent = 0xC0
    openingsquarebracket = 0xDB
    backslash = 0xDC
    closingsquarebracket = 0xDD
    quote = 0xDE
    play = 0xFA
    zoom = 0xFB
    PA1 = 0xFD
    clear = 0xFE


# --- Keyboard Control Functions ---#

# Category variables
letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
shiftsymbols = "~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"


# Presses and releases the key
def press(key):
    user32.keybd_event(key, 0, 0, 0)
    sleep(delay)
    user32.keybd_event(key, 0, 2, 0)
    sleep(delay)


# Holds a key
def hold(key):
    user32.keybd_event(key, 0, 0, 0)
    sleep(delay)


# Releases a key
def release(key):
    user32.keybd_event(key, 0, 2, 0)
    sleep(delay)


# Types out a string
def typestr(sentence):
    for letter in sentence:
        shift = letter in shiftsymbols
        fixedletter = "space"
        if letter == "`" or letter == "~":
            fixedletter = "accent"
        elif letter == "1" or letter == "!":
            fixedletter = "num1"
        elif letter == "2" or letter == "@":
            fixedletter = "num2"
        elif letter == "3" or letter == "#":
            fixedletter = "num3"
        elif letter == "4" or letter == "$":
            fixedletter = "num4"
        elif letter == "5" or letter == "%":
            fixedletter = "num5"
        elif letter == "6" or letter == "^":
            fixedletter = "num6"
        elif letter == "7" or letter == "&":
            fixedletter = "num7"
        elif letter == "8" or letter == "*":
            fixedletter = "num8"
        elif letter == "9" or letter == "(":
            fixedletter = "num9"
        elif letter == "0" or letter == ")":
            fixedletter = "num0"
        elif letter == "-" or letter == "_":
            fixedletter = "dash"
        elif letter == "=" or letter == "+":
            fixedletter = "equals"
        elif letter in letters:
            fixedletter = letter.lower()
        elif letter == "[" or letter == "{":
            fixedletter = "openingsquarebracket"
        elif letter == "]" or letter == "}":
            fixedletter = "closingsquarebracket"
        elif letter == "\\" or letter == "|":
            fixedletter == "backslash"
        elif letter == ";" or letter == ":":
            fixedletter = "semicolon"
        elif letter == "'" or letter == "\"":
            fixedletter = "quote"
        elif letter == "," or letter == "<":
            fixedletter = "comma"
        elif letter == "." or letter == ">":
            fixedletter = "period"
        elif letter == "/" or letter == "?":
            fixedletter = "slash"
        elif letter == "\n":
            fixedletter = "enter"
        keytopress = eval("key." + str(fixedletter))
        if shift:
            hold(key.shift)
            press(keytopress)
            release(key.shift)
        else:
            press(keytopress)


# --- Mouse Variables ---#

class mouse:
    left = [0x0002, 0x0004]
    right = [0x0008, 0x00010]
    middle = [0x00020, 0x00040]


# --- Mouse Control Functions ---#

# Moves mouse to a position
def move(x, y):
    user32.SetCursorPos(x, y)

# Presses and releases mouse
def click(button):
    user32.mouse_event(button[0], 0, 0, 0, 0)
    sleep(delay)
    user32.mouse_event(button[1], 0, 0, 0, 0)
    sleep(delay)

# Holds a mouse button
def holdclick(button):
    user32.mouse_event(button[0], 0, 0, 0, 0)
    sleep(delay)


# Releases a mouse button
def releaseclick(button):
    user32.mouse_event(button[1])
    sleep(delay)

#hold(key.alt)
#press(key.tab)

#####




# end of keyboard simulator

# print ("Enter full website for")

#print ("\n2 fingers")
fingers2='cnn' # input()

#print ("\n3 fingers")
fingers3='cnn'

#print ("\n4 fingers")
fingers4='cnn' #input()

tabs=0
count=0
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    # read image
    ret, img = cap.read()

    # get hand data from the rectangle sub window on the screen
    cv2.rectangle(img, (400,400), (100,100), (0,255,0),0)
    crop_img = img[100:400, 100:400]

    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # thresholdin: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # show thresholded image, not necessary and can be skipped
    cv2.imshow('Thresholded', thresh1)

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    print(cv2.__version__)
    #if version == '3':
    #    image, contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #elif version == '2':
    #    contours, hierarchy =        cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # find contour with max area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)#  return point false to find convexity defects

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)# to draw all contours pass -1

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0] #[ start point, end point, farthest point, approximate distance to farthest point ]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img,start, end, [0,255,0], 2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)
    if count==0:
        cv2.putText(img,"Wait for it :p", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
    # define actions required
    if count_defects == 1 and count!=2 and tabs<=8:
        #wb.open_new_tab('http://www.'+fingers2+'.com')
        hold(key.alt)
        press(key.tab)
        #tabs=tabs+1
        cv2.putText(img,"2."+fingers2, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
        count=2    
    elif count_defects == 2 and count!=3 and tabs<=8:
        #wb.open_new_tab('http://www.'+fingers3+'.com')
        #tabs=tabs+1
        cv2.putText(img, "3."+fingers3, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3)
        count=3
    elif count_defects == 3 and count!=4 and tabs<=8:
        #wb.open_new_tab('http://www.'+fingers4+'.com')
        cv2.putText(img, "4."+fingers4, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,165,0), 3)
        #tabs=tabs+1
        count=4
    elif count_defects == 4 and count!=5:
        cv2.putText(img,"5.Close ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
        #os.system("taskkill /im chrome.exe /f")
        tabs=0
        count=5
    else:
        cv2.putText(img,"", (50, 100),\
                    cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
        
        
    if count==2:
        cv2.putText(img, "2."+fingers2, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 3)
    elif count==3:
        cv2.putText(img, "3."+fingers3, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3)
    elif count==4:
        cv2.putText(img, "4."+fingers4, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,165,0), 3)
    elif count==5:
        cv2.putText(img, "5.WebBrowser", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)



    # show appropriate images in windows
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    #not necessary to show contours and can be skipped
    cv2.imshow('Contours', all_img)

    k = cv2.waitKey(10)
    if k == 27:
        break
