from re import match

from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController

keyboard = KeyboardController()
mouse = MouseController()


import time

keyboard = KeyboardController()
mouse = MouseController()


DELAY_TIME = 1

# https://nitratine.net/blog/post/simulate-keypresses-in-python/

def pressDownArrow():
    keyboard.press(Key.down)
    keyboard.release(Key.down)
    print("down---")

def pressUpArrow():
    keyboard.press(Key.up)
    keyboard.release(Key.up)
    print("up---")


def pressLeftArrow():
    keyboard.press(Key.left)
    keyboard.release(Key.left)
    print("left---")

def pressSpace():
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    print("space---")

def pressRightArrow():
    keyboard.press(Key.right)
    keyboard.release(Key.right)
    print("right---")

def openAltTab():
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    #pressRightArrow()


def closeAltTab():
    keyboard.release(Key.alt)


def pressArrowByString(arrow: str):

    if arrow == "Up":
        pressUpArrow()
    elif arrow == "Down":
        pressDownArrow()
    elif arrow == "Left":
        pressLeftArrow()
    elif arrow == "Right":
        pressRightArrow()
    else:
        pass


def scrollMouseByString(arrow: str):

    if arrow == "Up":
        scrollUpByMouse()
    elif arrow == "Down":
        scrollDownByMouse()
    else:
        pass


def scrollUpByMouse():
    mouse.scroll(0, 1)


def scrollDownByMouse():
    mouse.scroll(0, -1)


def moveMousePosition(x:int , y:int):
    # Set pointer position
    mouse.position = (x, y)
    # print('Now we have moved it to {0}'.format(mouse.position))