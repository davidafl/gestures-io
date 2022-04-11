import cv2
import hand_tracking_module as htm
import keyboard_module as kbm
import time


DELAY_TIME = 0.75

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    detector = htm.HandDetector(detectionCon=0.8, maxHands=2)
    run = True
    altTabIsPress = False

    while run:
        success, img = cap.read()
        hands, img = detector.findHands(img)  # With Draw

        # fingers1, fingers2 = 0, 0
        #
        if hands:
            # Hand 1
            hand1 = hands[0]
            fingers1 = detector.fingersUp(hand1)

            if len(hands) == 2:
                hand2 = hands[1]

                leftHand, rightHand = detector.returnLeftRightHand(hand1, hand2)

                if altTabIsPress:
                    if not detector.ifHandIs_AltTab(leftHand):
                        altTabIsPress = False
                        kbm.closeAltTab()
                    else:
                        kbm.pressArrowByString(detector.checkDirection(rightHand, 1))
                        time.sleep(DELAY_TIME)

                else:
                    if detector.ifHandIs_AltTab(leftHand):
                        altTabIsPress = True
                        kbm.openAltTab()

                if detector.ifHandIs_Close(leftHand):

                    lmList1 = rightHand["lmList"]  # List of 21 Landmarks points

                    if detector.checkDirection(rightHand, 1) == detector.checkDirection(rightHand, 2):
                        kbm.scrollMouseByString(detector.checkDirection(rightHand, 1))
                        time.sleep(DELAY_TIME * 0.75)

                    else:
                        kbm.pressArrowByString(detector.checkDirection(rightHand, 1))
                        time.sleep(DELAY_TIME)

        # if no hands in video
        else:
            if altTabIsPress:
                altTabIsPress = False
                kbm.closeAltTab()

        cv2.imshow("Image", img)
        cv2.waitKey(1)
