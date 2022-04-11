import cv2
import mediapipe as mp
import math


class HandDetector:
    """
    Finds Hands using the mediapipe library. Exports the landmarks
    in pixel format. Adds extra functionalities like finding how
    many fingers are up or the distance between two fingers. Also
    provides bounding box info of the hand found.
    """

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param maxHands: Maximum number of hands to detect
        :param detectionCon: Minimum Detection Confidence Threshold
        :param minTrackCon: Minimum Tracking Confidence Threshold
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        """
        Finds hands in a BGR image.
        :param img: Image to find the hands in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)

                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    ## box around the hand
                    # cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                    #               (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                    #               (255, 0, 255), 2)

                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, img
        else:
            return allHands

    def returnLeftRightHand(self, myHand1, myHand2):
        """
        Returns the left and right hand.
        :param myHand1: Hand 1
        :param myHand2: Hand 2
        :return: Left and right hand
        """
        if myHand1["type"] == "Right":
            return myHand2, myHand1
        else:
            return myHand1, myHand2

    def fingersUp(self, myHand):
        """
        Finds how many fingers are open and returns in a list.
        Considers left and right hands separately
        :return: List of which fingers are up
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []
            # Thumb
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if myLmList[self.tipIds[id]][1] < myLmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def pointToLeft(self, myHand):
        """
        function to find if hand point to left side of screen
        :return: True if left, False if right
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    return True
                else:
                    return False
            else:
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    return True
                else:
                    return False

    def pointToRight(self, myHand):
        """
        function to find if hand point to right side of screen
        :return: True if right, False if left
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            if myHandType == "Right":
                if myLmList[self.tipIds[0]][0] < myLmList[self.tipIds[0] - 1][0]:
                    return True
                else:
                    return False
            else:
                if myLmList[self.tipIds[0]][0] > myLmList[self.tipIds[0] - 1][0]:
                    return True
                else:
                    return False

    def checkLeftRight(self, myHand):
        """
        function to find if hand point to left side of screen
        :return: True if left, False if right
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            if myHandType == "Right":
                if myLmList[self.tipIds[1]][0] < myLmList[self.tipIds[1] - 1][0]:
                    return "right"
                else:
                    return "left"
            else:
                if myLmList[self.tipIds[1]][0] > myLmList[self.tipIds[1] - 1][0]:
                    return "left"
                else:
                    return "right"

    def checkUpDown(self, myHand):
        """
        function to find if hand point to left side of screen
        :return: True if left, False if right
        """

        myHandType = myHand["type"]
        myLmList = myHand["lmList"]

        if self.results.multi_hand_landmarks:
            if myHandType == "Right":
                if myLmList[self.tipIds[1]][1] < myLmList[self.tipIds[1] - 1][1]:
                    return "up"
                else:
                    return "down"
            else:
                if myLmList[self.tipIds[1]][1] > myLmList[self.tipIds[1] - 1][1]:
                    return "down"
                else:
                    return "up"

    def checkDirection(self, myHand, index : int = 1):
        """
        function to find if hand point to left side of screen
        https://mudgalvaibhav.medium.com/real-time-gesture-recognition-using-googles-mediapipe-hands-add-your-own-gestures-tutorial-1-dd7f14169c19
        :return: True if left, False if right
        """
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]

        x5 = myLmList[self.tipIds[index] - 2][0]
        y5 = myLmList[self.tipIds[index] - 2][1]
        x8 = myLmList[self.tipIds[index]][0]
        y8 = myLmList[self.tipIds[index]][1]

        if abs(x8 - x5) < 0.05:  # since tan(0) --> ∞
            m = 1000000000
        else:
            m = abs((y8 - y5) / (x8 - x5))

        if myHandType == "Left":
            if m > 1:
                if y8 < y5:  # since, y decreases upwards
                    return "Up"
            return " "

        else:
            if m >= 0 and m <= 1:
                if x8 > x5:
                    print("left 243")
                    return "Left"
                else:
                    print("right 246")
                    return "Right"
            if m > 1:
                if y8 < y5:  # since, y decreases upwards
                    print("up 250")
                    return "Up"
                else:
                    print("down 253")
                    return "Down"

    def findDistance(self, p1, p2, img=None):
        """
        Find the distance between two landmarks based on their
        index numbers.
        :param p1: Point1
        :param p2: Point2
        :param img: Image to draw on.
        :param draw: Flag to draw the output on the image.
        :return: Distance between the points
                 Image with output drawn
                 Line information
        """

        x1, y1, z1 = p1
        x2, y2, z2 = p2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return length, info, img
        else:
            return length, info

    def ifHandIs_AltTab(self, myHand):
        if myHand["type"] == "Left":
            return self.fingersUp(myHand) == [1, 1, 1, 1, 1] and self.checkDirection(myHand) == "Up"
        return False

    def ifHandIs_Close(self, myHand):
        if myHand["type"] == "Left":
            return self.fingersUp(myHand) == [0, 0, 0, 0, 0]
        return False


