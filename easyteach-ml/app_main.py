#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import itertools
from collections import Counter
from collections import deque

import cv2 as cv
import numpy as np
import mediapipe as mp

from ActionMapping import ActionMapping
from utils import CvFpsCalc
from model import KeyPointClassifier
from model import PointHistoryClassifier


class AppMain:
    """
    Main class for the application.
    """
    def __init__(self, tkUI):
        """
        Constructor
        :param tkUI: the tkinter UI instance
        """
        self.run = True
        self.tk = tkUI
        self.altTabIsPress = False

        # keystrokes for changing mode - k to add new hand, s to stop, h to add finger points
        self.mode = -1
        self.tk.bind("k", lambda event: self.handle_key_event(event.char))
        self.tk.bind("n", lambda event: self.handle_key_event(event.char))
        self.tk.bind("h", lambda event: self.handle_key_event(event.char))
        self.tk.bind("0", lambda event: self.handle_key_event(event.char))
        self.tk.bind("1", lambda event: self.handle_key_event(event.char))
        self.tk.bind("2", lambda event: self.handle_key_event(event.char))
        self.tk.bind("3", lambda event: self.handle_key_event(event.char))
        self.tk.bind("4", lambda event: self.handle_key_event(event.char))
        self.tk.bind("5", lambda event: self.handle_key_event(event.char))
        self.tk.bind("6", lambda event: self.handle_key_event(event.char))
        self.tk.bind("7", lambda event: self.handle_key_event(event.char))
        self.tk.bind("8", lambda event: self.handle_key_event(event.char))
        self.tk.bind("9", lambda event: self.handle_key_event(event.char))

        self.is_teaching = False
        self.currentAction = None

        # init params from config
        self.get_args()

        # Camera preparation ###############################################################
        self.cap = cv.VideoCapture(self.cap_device, cv.CAP_DSHOW) # cv.CAP_DSHOW for windows 10 # cv.CAP_ANY for mac os x # cv.CAP_V4L for linux # cv.CAP_GSTREAMER for linux # cv.CAP_FIREWIRE for linux
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, self.cap_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, self.cap_height)

        # Mediapipe Hand Model load #############################################################
        mp_hands = mp.solutions.hands
        # store the model in a member variable
        self.hands = mp_hands.Hands(
            static_image_mode=self.use_static_image_mode,
            max_num_hands=2,
            min_detection_confidence=self.min_detection_confidence, # param in json file
            min_tracking_confidence=self.min_tracking_confidence, # param in json file
        )

        self.init_tensorflow()

        # Coordinate history #################################################################
        self.history_length = 16
        self.point_history = deque(maxlen=self.history_length)

        # Finger gesture history ################################################
        self.finger_gesture_history = deque(maxlen=self.history_length)

        self.mode = 0
        self.debug_image = None

    def init_tensorflow(self):
        """
        Initialize tensorflow model - needed each time we teach a new gesture
        :return:
        """
        self.is_teaching = False
        # create classifier
        self.keypoint_classifier = KeyPointClassifier(num_threads = self.tk.config["classifier"]["num_threads"])
        self.point_history_classifier = PointHistoryClassifier()

        # Read labels ###########################################################
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            self.keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in self.keypoint_classifier_labels
            ]
            f.close()

        self.number_of_gestures = len(self.keypoint_classifier_labels)
        self.new_gesture_index = -1

        with open(
                'model/point_history_classifier/point_history_classifier_label.csv',
                encoding='utf-8-sig') as f:
            self.point_history_classifier_labels = csv.reader(f)
            self.point_history_classifier_labels = [
                row[0] for row in self.point_history_classifier_labels
            ]
            f.close()

        # FPS Measurement ########################################################
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)

        # Action Mapping ########################################################
        self.actionMapping = ActionMapping(self.keypoint_classifier_labels)


    def get_args(self):
        """
        Get arguments from config file
        :return:
        """
        self.cap_device = self.tk.config["cap_device"]
        self.cap_width = self.tk.config["classifier"]["width"]
        self.cap_height = self.tk.config["classifier"]["height"]

        self.use_static_image_mode = self.tk.config["classifier"]["use_static_image_mode"] == "True"
        self.min_detection_confidence = self.tk.config["classifier"]["min_detection_confidence"]
        self.min_tracking_confidence = self.tk.config["classifier"]["min_tracking_confidence"]
        self.use_brect = True

    def handle_key_event(self, key):
        """
        Handle key event, k to start teaching gesture, s to stop, 0 to record a gesture
        :param key:
        :return:
        """
        #print("key event")
        self.new_gesture_index = -1
        if key == 'k':
            self.mode = 1
            # append "gesture" + self.number_of_gestures to the file keypoint_classifier_label.csv
            self.keypoint_classifier_labels.append("gesture" + str(self.number_of_gestures))
            # open the file keypoint_classifier_label.csv and apend the new label at last line
            with open('model/keypoint_classifier/keypoint_classifier_label.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["gesture" + str(self.number_of_gestures)])
            f.close()

        elif key == 's':
            self.mode = 0
        elif key == 'h':
            self.mode = 2
        # is it a digit
        elif key.isdigit():
            self.new_gesture_index = self.number_of_gestures
            self.is_teaching = True
        else:
            self.mode = -1

    # def select_mode(self, key):
    #     number = -1
    #     print("key:", key)
    #     if 48 <= key <= 57:  # 0 ~ 9
    #         number = key - 48
    #     if key == 110:  # n
    #         self.mode = 0
    #     if key == 107:  # k - teaching mode
    #         self.mode = 1
    #     if key == 104:  # h
    #         self.mode = 2
    #     self.mode = number
    #     return number

    def get_video(self):
        return self.cap

    def stopLoop(self):
        self.run = False

    def startLoop(self):
        self.run = True

    def is_running(self):
        return self.run

    def get_frame(self):
        return self.debug_image;

    def get_action_labels(self):
        return self.keypoint_classifier_labels

    def run_video(self):
        """
        capture video from camera and process the image with mediapipe, then
        run the classifier to get the action label
        :return:
        """

        fps = self.cvFpsCalc.get()
        number = self.mode

        # Camera capture #####################################################
        ret, image = self.cap.read()
        if not ret:
            return

        image = cv.flip(image, 1)  # Mirror display
        self.debug_image = copy.deepcopy(image) # copy the image for debug

        # Detection implementation #############################################################
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB) # Convert to RGB

        image.flags.writeable = False
        results = self.hands.process(image)
        image.flags.writeable = True
        self.recognizedSigns = []

        #  ####################### GEST recognition ############################
        if results.multi_hand_landmarks is not None: # if mediapipe detect hands
            # loop over all hands
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # Bounding box calculation
                brect = calc_bounding_rect(self.debug_image, hand_landmarks)
                # 1 - Mediapipe Landmark calculation
                landmark_list = calc_landmark_list(self.debug_image, hand_landmarks)

                # 2 - Mediapipe Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = pre_process_landmark(landmark_list)
                pre_processed_point_history_list = pre_process_point_history(self.debug_image, self.point_history)

                # Write to the dataset file (of we are recording a new gesture)
                logging_csv(self.new_gesture_index, self.mode, pre_processed_landmark_list, pre_processed_point_history_list)

                ############### 3 = TENSORFLOW Hand sign classification
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list) # execute tensorflow model

                # 4 - process the hand sign id
                if hand_sign_id == 2:  # Point gesture
                    self.point_history.append(landmark_list[8])
                else:
                    self.point_history.append([0, 0])

                # Finger gesture classification
                finger_gesture_id = 0
                point_history_len = len(pre_processed_point_history_list)
                if point_history_len == (self.history_length * 2):
                    finger_gesture_id = self.point_history_classifier(pre_processed_point_history_list)

                # Calculates the gesture IDs in the latest detection
                self.finger_gesture_history.append(finger_gesture_id)
                most_common_fg_id = Counter(self.finger_gesture_history).most_common()

                # Drawing part
                self.debug_image = draw_bounding_rect(self.use_brect, self.debug_image, brect)
                self.debug_image = draw_landmarks(self.debug_image, landmark_list)
                self.debug_image = draw_info_text(
                    self.debug_image,
                    brect,
                    handedness,
                    self.keypoint_classifier_labels[hand_sign_id],
                    self.point_history_classifier_labels[most_common_fg_id[0][0]],
                )
                # Add the sign ID to the list of recognized signs
                self.recognizedSigns.append([hand_sign_id,
                                self.keypoint_classifier_labels[hand_sign_id],
                                handedness.classification[0].label])

                # if size of signIds is 2 then gesture using both hands is detected

            ############### convert gestures to action ###################
            key = str(self.actionMapping.convert_signs_to_array(self.recognizedSigns))
            # remove spaces from key
            key = key.replace(" ", "") # remove spaces from key

            # if self.config['actions'][key] is defined we recognize the gesture
            if key in self.tk.config['actions']:
                print (self.tk.config['actions'][key])
                # execute a timer to slow down actions
                # set a timer to execute the action
                if self.currentAction is None:
                    self.actionMapping.execute_action(self.tk.config['actions'][key])
                    self.currentAction = self.tk.after(self.tk.config['actions_delay'], self.cancelCurrentAction)
                    #self.after_cancel(self.currentAction)
                #self.currentAction = self.tk.after(self.tk.config['actions_delay'], self.actionMapping.execute_action(self.tk.config['actions'][key]))


            else:
                #print ("No action defined for this gesture")
                self.actionMapping.reset()


        else:
            self.point_history.append([0, 0]) # if no hand is detected, add a zero to the point history

        self.debug_image = draw_point_history(self.debug_image, self.point_history)
        self.debug_image = draw_info(self.debug_image, fps, self.mode, self.new_gesture_index)

    def cancelCurrentAction(self):
        self.currentAction = None


if __name__ == "__AppMain__":
    my_main = AppMain()
    show_window_of_hand_tracing = True
    while show_window_of_hand_tracing:
        my_main.run_video()

    my_main.cap.release()
    cv.destroyAllWindows()


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]

def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # Keypoint
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # Convert to a one-dimensional list
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # Normalization
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list


def pre_process_point_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] -
                                        base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] -
                                        base_y) / image_height

    # Convert to a one-dimensional list
    temp_point_history = list(
        itertools.chain.from_iterable(temp_point_history))

    return temp_point_history


def logging_csv(number, mode, landmark_list, point_history_list):
    if mode == 0:
        pass
    if mode == 1 and (0 <= number <= 9):
        csv_path = 'model/keypoint_classifier/keypoint.csv'
        if number > 0:
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *landmark_list])
            f.close()

    if mode == 2 and (0 <= number <= 9):
        csv_path = 'model/point_history_classifier/point_history.csv'
        if number > 0:
            with open(csv_path, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([number, *point_history_list])
            f.close()

    return

def draw_landmarks(image, landmark_point):
    if len(landmark_point) > 0:
        # Thumb
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[3]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[3]), tuple(landmark_point[4]),
                (255, 255, 255), 2)

        # Index finger
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[6]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[6]), tuple(landmark_point[7]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[7]), tuple(landmark_point[8]),
                (255, 255, 255), 2)

        # Middle finger
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[10]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[10]), tuple(landmark_point[11]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[11]), tuple(landmark_point[12]),
                (255, 255, 255), 2)

        # Ring finger
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[14]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[14]), tuple(landmark_point[15]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[15]), tuple(landmark_point[16]),
                (255, 255, 255), 2)

        # Little finger
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[18]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[18]), tuple(landmark_point[19]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[19]), tuple(landmark_point[20]),
                (255, 255, 255), 2)

        # Palm
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[0]), tuple(landmark_point[1]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[1]), tuple(landmark_point[2]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[2]), tuple(landmark_point[5]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[5]), tuple(landmark_point[9]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[9]), tuple(landmark_point[13]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[13]), tuple(landmark_point[17]),
                (255, 255, 255), 2)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (0, 0, 0), 6)
        cv.line(image, tuple(landmark_point[17]), tuple(landmark_point[0]),
                (255, 255, 255), 2)

    # Key Points
    for index, landmark in enumerate(landmark_point):
        if index == 0:  # Wrist 1
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 1:  # Wrist 2
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 2:  # Thumb: Root
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 3:  # Thumb: 1st joint
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 4:  # Thumb: fingertip
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 5:  # Index finger: Root
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 6:  # Index finger: 2nd joint
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 7:  # 人差指：第1関節
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 8:  # 人差指：指先
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 9:  # 中指：付け根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 10:  # 中指：第2関節
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 11:  # 中指：第1関節
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 12:  # 中指：指先
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 13:  # 薬指：付け根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 14:  # Ring finger: 2nd joint
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 15:  # Ring finger: 1st joint
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 16:  # 薬指：指先
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)
        if index == 17:  # 小指：付け根
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 18:  # 小指：第2関節
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 19:  # 小指：第1関節
            cv.circle(image, (landmark[0], landmark[1]), 5, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 5, (0, 0, 0), 1)
        if index == 20:  # 小指：指先
            cv.circle(image, (landmark[0], landmark[1]), 8, (255, 255, 255),
                      -1)
            cv.circle(image, (landmark[0], landmark[1]), 8, (0, 0, 0), 1)

    return image


def draw_bounding_rect(use_brect, image, brect):
    if use_brect:
        # Outer rectangle
        cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[3]),
                     (0, 0, 0), 1)

    return image


def draw_info_text(image, brect, handedness, hand_sign_text,
                   finger_gesture_text):
    cv.rectangle(image, (brect[0], brect[1]), (brect[2], brect[1] - 22),
                 (0, 0, 0), -1)

    info_text = handedness.classification[0].label[0:]
    if hand_sign_text != "":
        info_text = info_text + ':' + hand_sign_text
    cv.putText(image, info_text, (brect[0] + 5, brect[1] - 4),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    if finger_gesture_text != "":
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(image, "Finger Gesture:" + finger_gesture_text, (10, 60),
                   cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2,
                   cv.LINE_AA)

    return image


def draw_point_history(image, point_history):
    for index, point in enumerate(point_history):
        if point[0] != 0 and point[1] != 0:
            cv.circle(image, (point[0], point[1]), 1 + int(index / 2),
                      (152, 251, 152), 2)

    return image


def draw_info(image, fps, mode, number):
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (0, 0, 0), 4, cv.LINE_AA)
    cv.putText(image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX,
               1.0, (255, 255, 255), 2, cv.LINE_AA)

    mode_string = ['Logging Key Point', 'Logging Point History']
    if 1 <= mode <= 2:
        cv.putText(image, "MODE:" + mode_string[mode - 1], (10, 90),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                   cv.LINE_AA)
        if 0 <= number <= 9:
            cv.putText(image, "NUM:" + str(number), (10, 110),
                       cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1,
                       cv.LINE_AA)
    return image

