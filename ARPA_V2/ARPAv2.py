'''
This file defines the code for the main assistant.
This file implements the following features:
-> Greeting
-> Input sanitation
-> Intent Classification
'''

import pickle
import IntentClassifier.IntentClassifier as IntentClassifier
import pyautogui
import spacy
import datetime
import pandas as pd
from numerizer import numerize
from Skills.skillManager import SkillManager
import settings
import warnings


class Assistant:
    intentClassifier = None
    windowStack = []
    query = None
    skillManager = None
    '''if spacy.require_gpu():
        __nlp__ = spacy.load("en_core_web_trf")
    else:
        __nlp__ = spacy.load("en_web_core_lg")'''
    __nlp__ = spacy.load("en_core_web_lg")
    __skillCodes__ = None

    def __updateWindows__(self):
        windows = pyautogui.getAllWindows()
        self.windowStack = [x.title for x in windows if x.title not in ['', 'Mail', 'Add an account', 'Settings', 'Windows Input Experience', 'Program Manager']]

    def __init__(self, assistant_name):
        warnings.filterwarnings("ignore", category=UserWarning)
        settings.ASSISTANT_NAME = assistant_name
        self.skillManager = SkillManager()

        try:
            f = open("IntentClassifier/IntentClassifier.dat", "rb")
            self.intentClassifier = pickle.load(f)
        except FileNotFoundError:
            IntentClassifier.train_model()
            f = open("IntentClassifier/IntentClassifier.dat", "rb")
            self.intentClassifier = pickle.load(f)
        f.close()

        try:
            f = open("Data/RegisteredUsers.dat", "rb")
            settings.REGISTERED_USER_PROFILES = pickle.load(f)
            f.close()
        except FileNotFoundError:
            settings.REGISTERED_USER_PROFILES = None

        ##load up windows
        self.__updateWindows__()

        try:
            skill_data = pd.read_csv("Skills/SkillCodes.csv")
        except FileNotFoundError:
            pass

        self.greet()

    def greet(self):
        '''
            This function is meant to greet the user upon initialization of the chatbot.
            This function tells the date, time and day.
        '''
        IMPORTANT_WORDS = {"who", "is", "what", "how", "where", "make", "neither", "give", "all", "before", "into",
                           "ten",
                           "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "until", "nothing",
                           "sixty", "fifty", "for", "no", "not", "eleven", "twelve", "forty", "first", "least", "by",
                           "of"}
        self.__nlp__.Defaults.stop_words -= IMPORTANT_WORDS
        days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        print(f"Greetings. I am {settings.ASSISTANT_NAME}, your personal assistant.")
        print(f"It is {days[datetime.date.today().weekday()]}, {datetime.date.today()}")
        print(f"It is now {datetime.datetime.now().strftime('%H:%M')}")
        print("What would you like to do today?")

    def __getIntent__(self, command):
        intent = self.intentClassifier.predict([command])[0]
        return intent

    def __removeStopWords__(self, command):
        command = self.__nlp__(command)
        command = [x.text for x in command if not x.is_stop]
        command = self.__nlp__(" ".join(command))
        return command

    def __numerizeText__(self, command):
        command = numerize(str(command))
        return command

    def __preprocessing__(self, command):
        filter_command = self.__removeStopWords__(command)
        filter_command = self.__numerizeText__(filter_command)
        return filter_command

    @staticmethod
    def __check_coded_commands__(query):
        if query == "login":
            return "login"
        elif query == "exit":
            print("Goodbye.")
            exit()
        return None

    def takeCommand(self):
        query = input(">> ")
        processed_query = self.__preprocessing__(query)
        intent = self.__check_coded_commands__(query)
        if intent is None:
            intent = self.__getIntent__(query).strip()
        if intent == "calculate":
            self.skillManager.executeCommand(intent, processed_query)
        elif intent == "exit":
            print("Goodbye.")
            exit()
        else:
            self.skillManager.executeCommand(intent, processed_query)


##Tests
assistant = Assistant("ARPA")
#assistant.skillManager.executeCommand("set_timer", 5)
while True:
    assistant.takeCommand()