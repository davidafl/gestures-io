import cv2
import hand_tracking_module as htm
import keyboard_module as kbm
import time

show_window_of_hand_tracing = False

class main:

    def __init__(self):

        self.run = False   
        self.DELAY_TIME = 0.75
        self.cap = cv2.VideoCapture(0)
        self.detector = htm.HandDetector(detectionCon=0.8, maxHands=2)
        self.altTabIsPress = False

    def get_video(self):
        return self.cap

    def stopLoop(self):
        self.run = False

    def startLoop(self):
        self.run = True

    def is_running(self):
        return self.run

    def run_video(self):
        success, img = self.cap.read()
        hands, img = self.detector.findHands(img)  # With Draw

        # fingers1, fingers2 = 0, 0
        #
        if hands:
            
            hand1 = hands[0]
            fingers1 = self.detector.fingersUp(hand1)

            if len(hands) == 2:
                hand2 = hands[1]

                leftHand, rightHand = self.detector.returnLeftRightHand(hand1, hand2)

                if self.altTabIsPress:
                    if not self.detector.ifHandIs_AltTab(leftHand):
                        self.altTabIsPress = False
                        kbm.closeAltTab()
                    else:
                        kbm.pressArrowByString(self.detector.checkDirection(rightHand, 1))
                        time.sleep(self.DELAY_TIME)

                else:
                    if self.detector.ifHandIs_AltTab(leftHand):
                        self.altTabIsPress = True
                        kbm.openAltTab()

                if self.detector.ifHandIs_Close(leftHand):

                    lmList1 = rightHand["lmList"]  # List of 21 Landmarks points

                    if self.detector.checkDirection(rightHand, 1) == self.detector.checkDirection(rightHand, 2):
                        kbm.scrollMouseByString(self.detector.checkDirection(rightHand, 1))
                        time.sleep(self.DELAY_TIME * 0.75)

                    else:
                        kbm.pressArrowByString(self.detector.checkDirection(rightHand, 1))
                        time.sleep(self.DELAY_TIME)

        # if no hands in video
        else:
            if self.altTabIsPress:
                altTabIsPress = False
                kbm.closeAltTab()
        
        if show_window_of_hand_tracing:
            cv2.imshow("Image", img)
            cv2.waitKey(1)

        
if __name__ == "__main__":
    my_main = main()
    show_window_of_hand_tracing = True
    while show_window_of_hand_tracing:
        my_main.run_video()