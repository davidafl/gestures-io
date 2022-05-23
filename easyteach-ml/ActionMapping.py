import keyboard_module as kbm
import time

class ActionMapping:
    def __init__(self, action_labels):
        self.altTabIsPressed = False
        self.count = 0
        self.action_labels = action_labels
        print ("labels: " , self.action_labels)
        # load CSV file model/keyboard_classifier_label.csv file

    def reset(self):
        self.count+= 1
        if (self.count > 10):
            self.altTabIsPressed = False
            kbm.closeAltTab()
            self.count = 0


    def convert_signs_to_array(self, signs):
        """
        builds an array of left and right hands signs
        :param signs: an array of signs
        :return: an array of hands
        """
        hands = []
        #loop over self.recognizedSigns and add the sign id to hands
        for sign in signs:
            if (sign[2] == "Left"):
                hands.append(self.action_labels[sign[0]])
        if (len(hands) == 0):
            hands.append("None")

        for sign in signs:
            if (sign[2] == "Right"):
                hands.append(self.action_labels[sign[0]])
        if (len(hands) == 1):
            hands.append("None")

        return hands

    def execute_action(self, action):

        if (action =="openAltTab" and self.altTabIsPressed == False):
            self.altTabIsPressed = True
            kbm.openAltTab()

        if (action =="closeAltTab" and self.altTabIsPressed == True):
            self.altTabIsPressed = False
            kbm.closeAltTab()

        if (self.altTabIsPressed and action == "nextTab"):
            kbm.pressRightArrow()

        if (self.altTabIsPressed and action == "prevTab"):
            kbm.pressLeftArrow()

        if (self.altTabIsPressed and action == "upTab"):
            kbm.pressUpArrow()

        if (self.altTabIsPressed and action == "downTab"):
            kbm.pressDownArrow()

        if(action == "downArrow"):
            kbm.pressDownArrow()

        if(action == "upArrow"):
            kbm.pressUpArrow()

        if (action == "space"):
            kbm.pressSpace()



