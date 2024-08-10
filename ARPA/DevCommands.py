import IntentClassifiers.IntentClassifier as IntentClassifier
from getpass import getpass
import pickle
import os

def update_realtime_vars(update_values):
    pickle.dump(update_values, open("realTimeVars.dat", "wb"))
def load_assistant_vars():
    return pickle.load(open("realTimeVars.dat", "rb"))
def retrain_model():
    print("[+] Updating assistant model. Please wait for the updates to finish....")
    print()
    IntentClassifier.train_model()

def register_user():
    assistant_vars = load_assistant_vars()
    if assistant_vars["Registered_users"][assistant_vars["Current_user"]][1] == "admin":
        username = input("Enter username>> ")
        if username in assistant_vars["Registered_users"].keys():
            print("Username taken! Try a different username!")
            return register_user()
        else:
            password = getpass("Enter password>> ")
            confirm_pass = getpass("Confirm password>> ")
            if password == confirm_pass:
                auth_level = input("Enter authorization level (admin/ user)>> ")
                if auth_level not in ["admin", "user"]:
                    print("Invalid authorization level! Try again!")
                    return register_user()
                else:
                    assistant_vars["Registered_users"][username] = [password, auth_level]
                    update_realtime_vars(assistant_vars)
                    print("User registered successfully!")
            else:
                print("Passwords did not match! Try again!")
                return register_user()
    else:
        print("You are not authorized to register new users!")
def delete_user():
    assistant_vars = load_assistant_vars()
    if assistant_vars["Registered_users"][assistant_vars["Current_user"]][1] == "admin":
        print("[!]Account deletion console!! Deleted accounts cannot be recovered! Proceed with caution!!")
        del_user = input("Enter username to delete>> ")
        admin_pass = getpass("Enter YOUR password>> ")
        if del_user in assistant_vars["Registered_users"].keys():
            confirmation = input(f"Are you sure you wish to delete user {del_user} (Enter yes to confirm)?>> ")
            if confirmation.lower() == "yes":
                del assistant_vars["Registered_users"][del_user]
                update_realtime_vars(assistant_vars)
                print(f"[!] User {del_user} deleted!")
            else:
                print("[!] Cancelling deletion process!")
        else:
            print(f"[!] User {del_user} not found!")
    else:
        print("[!] You are not authorized to delete users! Ask your admin to delete the account!")

def change_password(username):
    assistant_vars = load_assistant_vars()
    current_pass = getpass("Enter your current password>> ")
    if current_pass == assistant_vars["Registered_users"][username][0]:
        new_pass = getpass("Enter new password>> ")
        confirm_new_pass = getpass("Re enter new password for confirmation>> ")
        if new_pass == confirm_new_pass:
            assistant_vars["Registered_users"][username][0] = new_pass
            update_realtime_vars(assistant_vars)
            print("[!] Password updated successfully!")
        else:
            print("[!] The entered passwords do not match!")
    else:
        print("[!] Invalid password!")

def list_users():
    assistant_vars = load_assistant_vars()
    if assistant_vars["Registered_users"][assistant_vars["Current_user"]][1] == "admin":
        print()
        print("[!] User list: ")
        print()
        for key in assistant_vars["Registered_users"].keys():
            print(f"Username: {key}")
            print(f"Auth Level: {assistant_vars['Registered_users'][key][1]}")
            print()
    else:
        print("[!] You are not authorized to list system users!")
def change_auth_level():
    assistant_vars = load_assistant_vars()
    if assistant_vars["Registered_users"][assistant_vars["Current_user"]][1] == "admin":
        user = input("Enter username to alter>> ")
        if user in assistant_vars["Registered_users"].keys():
            pass_confirm = getpass("Enter your password to confirm this action>> ")
            if pass_confirm == assistant_vars["Registered_users"]["Current_user"][0]:
                new_auth = input("Enter new authorization level (admin/user)>> ")
                if new_auth in ["admin", "user"]:
                    assistant_vars["Registered_users"][user][1] = new_auth
                    update_realtime_vars(assistant_vars)
                    print("[!] Authorization level updated!")
                else:
                    print("[!] Invalid authorization level!")
            else:
                print("[!] In valid password!")
        else:
            print("[!] This user does not exist!")
    else:
        print("[!] You are not authorized to change authorization levels!")
def start_user_directory():
    assistant_vars = load_assistant_vars()
    user = assistant_vars["Current_user"]
    ##Check for existence
    if not os.path.isdir(f"D:/ARPA/ARPA/UserData/{user}"):
        os.mkdir(f"D:/ARPA/ARPA/UserData/{user}")
def read_to_do_list(user):
    if not os.path.isfile(f"D:/ARPA/ARPA/UserData/{user}/toDoList.dat"):
        print("[!] You do not have an active to do list!")
        print("[!] Starting a new to do list!")
        to_do_list(user)

    else:
        print("[!] your current to do list is as follows: ")
        f = open(f"D:/ARPA/ARPA/UserData/{user}/toDoList.dat", "rb")
        tasks = pickle.load(f)
        for task in tasks:
            print(task)
        f.close()

def to_do_list(user):
    ##Check path:
    if not os.path.isdir(f"D:/ARPA/ARPA/UserData/{user}"):
        start_user_directory()
    if not os.path.isfile(f"D:/ARPA/ARPA/UserData/{user}/toDoList.dat"):
        print("[!] Starting new to do list!")
        print()
    else:
        print("[!] Adding to this list:")
        print()
        read_to_do_list(user)
    f = open(f"D:/ARPA/ARPA/UserData/{user}/toDoList.dat", "ab")
    tasks = []
    while True:
        t = input("Enter your task>> ")
        tasks.append(t)
        c = input("Add more tasks (enter yes/no)?>> ")
        if c.lower() != "yes":
            break
    pickle.dump(tasks, f)
    print("[!] To do list updated!")
    f.close()





