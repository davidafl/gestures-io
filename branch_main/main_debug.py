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
        # hands = detector.findHands(img, draw=False)  # No Draw

        fingers2 = 0
        fingers1 = 0
        if hands:
            # Hand 1
            hand1 = hands[0]
            # lmList1 = hand1["lmList"]  # List of 21 Landmarks points
            # bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
            # centerPoint1 = hand1["center"]  # center of the hand cx,cy
            # handType1 = hand1["type"]  # Hand Type Left or Right

            fingers1 = detector.fingersUp(hand1)
            # length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
            # length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw

            if len(hands) == 2:
                hand2 = hands[1]
                # lmList2 = hand2["lmList"]  # List of 21 Landmarks points
                # bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
                # centerPoint2 = hand2["center"]  # center of the hand cx,cy
                # handType2 = hand2["type"]  # Hand Type Left or Right

                leftHand, rightHand = detector.returnLeftRightHand(hand1, hand2)

                if altTabIsPress:
                    if not detector.ifHandIs_AltTab(leftHand):
                        altTabIsPress = False
                        print("alttab")
                        kbm.closeAltTab()

                else:
                    if detector.ifHandIs_AltTab(leftHand):
                        altTabIsPress = True
                        print("open")
                        kbm.openAltTab()

                if altTabIsPress:
                    kbm.pressArrowByString(detector.checkDirection(rightHand, 1))
                    time.sleep(DELAY_TIME)

                if detector.ifHandIs_Mouse(leftHand):
                    print("mouse")

                    kbm.scrollMouseByString(detector.checkDirection(rightHand, 0))
                    # t_myLmList = rightHand["lmList"]
                    # kbm.moveMousePosition(t_myLmList[8][0],t_myLmList[8][1])
                    time.sleep(DELAY_TIME * 0.75)

            # if no 2 hands in video
            # else:
            #
        # if no hands in video
        else:
            if altTabIsPress:
                altTabIsPress = False
                kbm.closeAltTab()


                # length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
                # length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)  # with draw
            # print(fingers1, fingers2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
