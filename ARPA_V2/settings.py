import os
import pickle


def load_user_profiles():
    global REGISTERED_USER_PROFILES
    directory = "UserProfiles"
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        # Open and read the file
        with open(file_path, 'rb') as file:
            if REGISTERED_USER_PROFILES is None:
                REGISTERED_USER_PROFILES = []
            data = pickle.load(file)
            REGISTERED_USER_PROFILES.append({'username':data["username"], 'password':data["password", 'user_id':data["user_id"]]})


ASSISTANT_NAME = None

CURRENT_USER = None
USER_AUTH_LEVEL = None

REGISTERED_USER_PROFILES = None

load_user_profiles()

