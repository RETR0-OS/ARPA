import pickle

f = open("realTimeVars.dat", "wb")
pickle.dump({"Current_user": None, "Window_stack": None, "Current_tab": None, "Registered_users": {'r3tr0':['AadityaJ12@', "admin"]}}, f)
f.close()