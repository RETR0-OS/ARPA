import spacy
import datetime
import random
from youtubesearchpython import VideosSearch as vidSearch
import webbrowser
from googlesearch import search as gSearch
import wikipedia
import IntentClassifiers.IntentClassifier as IntentClassifier
import warnings
import os
import pickle
from getpass import getpass
import DevCommands as adminCommands
import pyautogui
import time

ASSISTANT_NAME = None
ADMIN_PASS = None
ADMIN_USERNAME = None
user_authenticated = False

current_vars = {"Current_user": None, "Window_stack": None, "Current_tab": None, "Registered_users": {}}

def realtime_vars():
    global current_vars
    try:
        f = open("realTimeVars.dat", "rb")
        current_vars = pickle.load(f)
        return current_vars
    except Exception as e:
        f = open("realTimeVars.dat", "wb")
        pickle.dump(current_vars, f)

        f = open("realTimeVars.dat", "rb")
        current_vars = pickle.load(f)
        return current_vars
        ##Create and load vars

current_vars = realtime_vars()

def get_current_windows():
    windows = pyautogui.getAllWindows()
    windows = [x.title for x in windows if
               x.title not in ['', 'Mail', 'Add an account', 'Settings', 'Windows Input Experience', 'Program Manager']]
    return windows

def preprocess_and_santitize(text):
    global nlp
    doc = nlp(text)
    processed_text = [x.text for x in doc if not x.is_stop and not x.is_punct]
    return " ".join(processed_text)
def exit_arpa():
    adminCommands.admin_commands_toggle = False
    current_vars["Current_user"] = None
    current_vars["Window_stack"] = None
    current_vars["Current_tab"] = None

    f = open("realTimeVars.dat", "wb")
    pickle.dump(current_vars, f)

    logout()

    print("Goodbye. I hope I helped!")
    exit()
def greet():
    global nlp
    global current_vars
    ##Process windows
    windows = get_current_windows()
    current_vars["Window_stack"] = windows
    update_realtime_vars()
    current_vars = realtime_vars()
    IMPORTANT_WORDS = {"who", "is", "what", "how", "where", "make", "neither", "give", "all", "before", "into", "ten",
                       "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "until", "nothing",
                       "sixty", "fifty", "for", "no", "not", "eleven", "twelve", "forty", "first", "least", "by", "of"}
    nlp.Defaults.stop_words -= IMPORTANT_WORDS
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    print("Greetings. I am ARPA, your personal assistant.")
    print(f"It is {days[datetime.date.today().weekday()]}, {datetime.date.today()}")
    print(f"It is now {datetime.datetime.now().strftime('%H:%M')}")
    print("What would you like to do today?")
def load_model():
    try:
        intent_classifier_model = pickle.load(open("D:/ARPA/ARPA/IntentClassifiers/IntentClassifier.dat", "rb"))
        return intent_classifier_model
    except Exception as e:
        IntentClassifier.train_model()
        intent_classifier_model = pickle.load(open("D:/ARPA/ARPA/IntentClassifiers/IntentClassifier.dat", "rb"))
        print(intent_classifier_model)
        return intent_classifier_model

##General functions
def update_realtime_vars():
    global current_vars
    pickle.dump(current_vars, open("realTimeVars.dat", "wb"))
def introduce_yourself():
    introductions = [
        "Hi there! I'm ARPA, your personal assistant. ARPA means Advanced Research and Projects Assistant. Say 'help' to see what I can do.",
        "Hello! I'm ARPA, your assistant. ARPA is short for Advanced Research and Projects Assistant. Type 'help' to learn more about my capabilities.",
        "Greetings! I'm ARPA, your personal assistant. ARPA stands for Advanced Research and Projects Assistant. Say 'help' to discover what I can assist you with.",
        "Hey! I'm ARPA, your assistant. ARPA means Advanced Research and Projects Assistant. Say 'help' to know what I can do.",
        "Hello, I'm ARPA, your assistant. ARPA stands for Advanced Research and Projects Assistant. Type 'help' to see my functions.",
        "Hi, I’m ARPA, your personal assistant. ARPA stands for Advanced Research and Projects Assistant. Say 'help' to find out my features.",
        "Hey there! I’m ARPA, your personal assistant. ARPA means Advanced Research and Projects Assistant. Say 'help' to learn more about my skills.",
        "Hi, I'm ARPA, here to assist you. ARPA stands for Advanced Research and Projects Assistant. Type 'help' to see how I can help.",
        "Hello! I'm ARPA, your personal assistant. ARPA means Advanced Research and Projects Assistant. Type 'help' to know more about my abilities.",
        "Greetings! I’m ARPA, your assistant. ARPA is short for Advanced Research and Projects Assistant. Say 'help' to find out what I can do."
    ]
    greeting_number = random.randint(0, len(introductions) - 1)
    print(introductions[greeting_number])
def play_music(search_param):
    global current_vars
    v_search = vidSearch(search_param, limit=1)
    link = v_search.result()["result"][0]["link"]
    webbrowser.open(link, new=1)
    time.sleep(2)
    windows = get_current_windows()
    current_vars["Window_stack"] = windows
    update_realtime_vars()
    current_vars = realtime_vars()
    pyautogui.getWindowsWithTitle(current_vars["Window_stack"][0])[0].minimize()
    return
def calculate(equation):
    try:
        results = gSearch(equation, num_results=1)
        for i in results:
            print(i)
    except Exception as e:
        print(f"An error occurred. Error message: \n {e} \nIs your internet on?")
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=7, auto_suggest=False)
        print(summary)
        more = input("Do you wish to learn more? \n>> ")
        more = nlp(preprocess_and_santitize(more))
        confirm = {
            "yes": ["yes", "yup", "yeah", "yes, tell me more", "yes tell me more", "more", "tell me", "yes I want to",
                    "yes I want to learn more", "yes arpa", "tell me more arpa", "arpa tell me more", "yes arpa"],
            "no": ["no", "nope", "no thank you", "no I don't want to", "that's all", "no i do not want to", "no need",
                   "that's all i need", "non"]}
        confirmation = ""
        cur_max_confirm = 0
        for key in confirm.keys():
            for i in confirm[key]:
                similarity = more.similarity(nlp(i))
                if similarity > cur_max_confirm:
                    confirmation = key
                    cur_max_confirm = similarity
        if confirmation == "yes":
            print("Ok! Here is some more information: \n")
            result = wikipedia.summary(query, sentences=50, auto_suggest=False)
            print(result)
            print()
            print()
            print("For additional information, might I suggest looking at: ", wikipedia.page(query, auto_suggest=False).url)
            print("Source: Wikipedia")
        elif confirmation == "no":
            print("Ok.")
    except wikipedia.exceptions.DisambiguationError as e:
        print("The query was too ambiguous. It was interpreted in the following contexts: \n")
        print(e.options)
        print()
        print("Please try a fresh query with a little more detail.")
    except wikipedia.exceptions.PageError:
        print("Sorry, I could not understand you. Perhaps you made a spelling error?")
        print("Perhaps these results can help you better.")
        search_the_web(query)
    except wikipedia.exceptions.HTTPTimeoutError:
        print("Sorry, your request wasn't processed correctly. Please retry in a while.")
    except wikipedia.exceptions.RedirectError:
        print("Sorry, there was some error. Please try again.")
    except Exception:
        print("An unidentified error occurred. Please try again.")
def search_the_web(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return
    except Exception as e:
        print("Error occurred! Ensure you are connected to the internet!")
def tell_time():
    current_time = datetime.datetime.now().strftime("%H%:%M%")
    time_sentences = [
        f"It is {current_time} right now.",
        f"The current time is {current_time}.",
        f"Right now, it's {current_time}.",
        f"It is {current_time}.",
        f"The time now is {current_time}.",
        f"It's currently {current_time}.",
        f"As of now, it's {current_time}.",
        f"The clock shows {current_time}.",
        f"It's {current_time} at the moment.",
        f"Currently, it is {current_time}."
    ]
    print(time_sentences[random.randint(0, len(time_sentences)-1)])
def tell_date():
    current_date = datetime.date.today()
    weekday = datetime.date.today().weekday()
    date_sentences = [
        f"It is {weekday}, {current_date} today.",
        f"Today is {weekday}, {current_date}.",
        f"It's {weekday}, {current_date}.",
        f"The date is {weekday}, {current_date}.",
        f"It's {weekday}, {current_date}.",
        f"It is {weekday}, {current_date} today.",
        f"The date is {weekday}, {current_date}.",
        f"It's {weekday}, {current_date}.",
        f"Today is {weekday}, {current_date}."
    ]
    print(date_sentences[random.randint(0, len(date_sentences) - 1)])

##Processing functions
def intent_classify(command, intent_classifier):
    return intent_classifier.predict([command])
def process_command(command, intent_classifier):
    intent = intent_classify(command, intent_classifier)[0]
    command = nlp(command)
    if intent == "exit":
        exit_arpa()
    elif intent == "play_music":
        remove_words = ["play", "music", "tunes"]
        search_terms = " ".join([x for x in [i.text for i in command] if x not in remove_words])
        play_music(search_terms)
    elif intent == "introduce_yourself":
        introduce_yourself()
    elif intent == "do_calculations":
        equation = " ".join([i.text for i in command])
        calculate(equation)
        ##Still very buggy...Need to fix.
    elif intent == "web_search":
        remove_words = ["search", "find", "who"]
        query = " ".join([x for x in [i.text for i in command] if x not in remove_words])
        search_the_web(query)
    elif intent == "wiki_search":
        remove_words = ["search", "wikipedia", "who", "find", "for"]
        query = " ".join([x for x in [i.text for i in command] if x not in remove_words])
        search_wikipedia(query)
    elif intent == "read_todo_list":
        if current_vars["Current_user"] is not None:
            adminCommands.read_to_do_list(current_vars["Current_user"])
        else:
            print("[!] you are not logged in! Kindly login to read your to do list!")
    elif intent == "start_todo_list":
        if current_vars["Current_user"] is not None:
            adminCommands.to_do_list(current_vars["Current_user"])
        else:
            print("[!] you are not logged in! Kindly login to create your to do list!")


def authenticate():
    global current_vars
    global user_authenticated
    print()
    print("[!] !!!!Admin command mode authentication! Proceed with caution!!!!! [!]")
    print()
    user = input("Enter username>> ")
    password = getpass("Enter password>> ")
    registered_users = current_vars["Registered_users"].keys()

    if user in registered_users and password == current_vars["Registered_users"][user][0]:
        user_authenticated = True
        print(f"Welcome, {user}")
        current_vars["Current_user"] = user
        update_realtime_vars()
        print("[!] Admin command protocols active. Please proceed with caution. [!]")
        print()
    else:
        print("[!] Credentials invalid! Admin command console locked! [!]")
        exit()
def logout():
    global ADMIN_USERNAME
    global user_authenticated
    global ADMIN_PASS
    global current_vars
    if user_authenticated is True:
        current_vars["Current_user"] = None
        update_realtime_vars()
        current_vars = realtime_vars()
        ADMIN_USERNAME = None
        ADMIN_PASS = None
        user_authenticated = False
        print("[!] User logged out!")
    else:
        return

def check_admin_commands(command, assistant_model):
    global current_vars
    if command == "register new user":
        adminCommands.register_user()
        current_vars = realtime_vars()
    elif command == "update assistant":
        adminCommands.retrain_model()
        assistant_model = load_model()
    elif command == "delete a user":
        adminCommands.delete_user()
        current_vars = realtime_vars()
    elif command == "list users":
        adminCommands.list_users()
    elif command == "change password":
        adminCommands.change_password(current_vars["Current_user"])
        current_vars = realtime_vars()
    elif command == "change authorization level":
        adminCommands.change_auth_level()
        current_vars = realtime_vars()
    else:
        return False
    return True


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    nlp = spacy.load("en_core_web_lg")

    ASSISTANT_NAME = os.environ.get("ASSISTANT_NAME")
    ADMIN_PASS = os.environ.get("ARPA_ADMIN_PASS")
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
    user_authenticated = False
    model = load_model()
    greet()

    while True:
        try:
            user_command = input(">> ").lower()
            if (user_command == "admin command mode" or user_command == "login") and user_authenticated is False:
                authenticate()
            elif user_command == "admin command mode" and user_authenticated is True:
                print("[!] You are already authenticated! Command mode active! [!]")
            elif user_command == "logout" or user_command == "sign out" or user_command == "signout":
                logout()
            else:
                is_admin_command = False
                if user_authenticated is True:
                    is_admin_command = check_admin_commands(user_command, model)
                if is_admin_command is False:
                    preprocess_and_santitize(user_command)
                    process_command(user_command, model)
        except KeyboardInterrupt:
            exit_arpa()
