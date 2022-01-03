from pynput.keyboard import Key, Controller
import time

keyboard = Controller()


# ============ Functions ============= #
def printstring(str):
    time.sleep(1)

    openAltTab()
    time.sleep(0.5)
    pressLeftArrow()
    time.sleep(0.5)
    pressLeftArrow()
    time.sleep(0.15)
    closeAltTab()

    time.sleep(2)

    for c in str:
        keyboard.press(c)
        keyboard.release(c)
        time.sleep(0.15)

    pressRightArrow()
    pressRightArrow()
    pressRightArrow()
    pressRightArrow()

    keyboard.press(")")
    keyboard.release(")")
    time.sleep(2)

    openAltTab()
    pressLeftArrow()
    closeAltTab()

    time.sleep(0.5)


def pressDownArrow():
    keyboard.press(Key.down)
    keyboard.release(Key.down)
    time.sleep(0.5)


def pressUpArrow():
    keyboard.press(Key.up)
    keyboard.release(Key.up)
    time.sleep(0.5)


def pressLeftArrow():
    keyboard.press(Key.left)
    keyboard.release(Key.left)
    time.sleep(0.5)


def pressRightArrow():
    keyboard.press(Key.right)
    keyboard.release(Key.right)
    time.sleep(0.5)


def openAltTab():
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    keyboard.release(Key.tab)
    time.sleep(0.06)
    pressRightArrow()


def closeAltTab():
    keyboard.release(Key.alt)


# https://nitratine.net/blog/post/simulate-keypresses-in-python/
# ============ main ============= #

printstring("Liron Farzam is the king! :    ")
