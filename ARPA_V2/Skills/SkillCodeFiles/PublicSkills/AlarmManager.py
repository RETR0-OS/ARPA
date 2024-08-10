from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import pickle
import datetime
import time
import ctypes
import winsound
import threading
import re

class AlarmManager(Skill):

    triggerIntent = "set_alarm"
    skillType = "public"
    file = None

    def __init__(self):
        super(AlarmManager, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)
        self.file = "D:/ARPA/ARPA_V2/Skills/SkillCodeFiles/PublicSkills/ExtraDataFiles/alarms.dat"
        f = open(self.file, "wb")
        pickle.dump([], f)
        f.close()
        self.__checkAlarms__()


    @staticmethod
    def __ringAlarm__(alarm):
        winsound.PlaySound("Skills/SkillCodeFiles/PublicSkills/ExtraDataFiles/alarm.wav", winsound.SND_ASYNC)
        # winsound.PlaySound("ExtraDataFiles/alarm.wav", winsound.SND_ASYNC)
        ctypes.windll.user32.MessageBoxW(0, f"This is your alarm for {alarm}", "Time Up!", 0x1000)
        winsound.PlaySound(None, winsound.SND_ASYNC)

    def __checkAlarms__(self):
            while True:
                with open(self.file, "rb") as f:
                    alarms = pickle.load(f)
                if len(alarms) > 0:
                    for alarm in alarms:
                        if alarm == datetime.datetime.now().strftime("%H:%M"):
                            f = open(self.file, "wb")
                            alarms.remove(alarm)
                            pickle.dump(alarms, f)
                            f.close()
                            alarm_ring_thread = threading.Thread(target=self.__ringAlarm__, args=(alarm,))
                            alarm_ring_thread.daemon = True
                            alarm_ring_thread.start()
                    time.sleep(2)
                else:
                    break

    def __writeAlarm__(self, new_alarm):
        f = open(self.file, "rb")
        alarms = pickle.load(f)
        alarms.append(new_alarm)
        f.close()
        f = open(self.file, "wb")
        pickle.dump(alarms, f)
        f.close()

    def __addAlarm__(self, time_list):
        if "now" in time_list:
            delta_hrs = 0
            delta_mins = 0
            if "hours" in time_list or "hour" in time_list:
                try:
                    if time_list[time_list.index("hours")-1].isdigit():
                        delta_hrs += int(time_list[time_list.index("hours")-1])
                except ValueError:
                    if time_list[time_list.index("hour") - 1].isdigit():
                        delta_hrs += int(time_list[time_list.index("hour") - 1])
            if "minutes" in time_list or "minute" in time_list:
                try:
                    if time_list[time_list.index("minutes") - 1].isdigit():
                        delta_mins += int(time_list[time_list.index("minutes") - 1])
                except ValueError:
                    if time_list[time_list.index("minute") - 1].isdigit():
                        delta_mins += int(time_list[time_list.index("minute") - 1])
            if delta_hrs == 0 and delta_mins == 0:
                print("[!] Error setting alarm. Please rephrase your query.")
            else:
                new_alarm = (datetime.datetime.now() + datetime.timedelta(hours=delta_hrs, minutes=delta_mins)).strftime("%H:%M")
                self.__writeAlarm__(new_alarm)
                return

        elif ":" in time_list:
            colon_ind = time_list.index(":")
            print(colon_ind)
            hrs = time_list[colon_ind-1]
            if hrs.isdigit():
                num_hrs = int(hrs)
                if len(hrs) == 1:
                    hrs = "0"+hrs
                if "am" in time_list and (0 > num_hrs or num_hrs > 12):
                    print("[!] Error setting alarm. Please rephrase your query.")
                elif "pm" in time_list:
                    if not 0 < num_hrs <= 12:
                        print("[!] Error setting alarm. Please rephrase your query.")
                    else:
                        if num_hrs == 12:
                            hrs = "12"
                        else:
                            num_hrs += 12
                            hrs = str(num_hrs)
                        mins = time_list[colon_ind +1]
                        if mins.isdigit() and 0 < int(mins) <= 59:
                            new_alarm = hrs + ":" + mins
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query.")
                elif num_hrs < 0 or num_hrs >= 24:
                    print("[!] Error setting alarm. Please rephrase your query.")
                else:
                    mins = time_list[colon_ind + 1]
                    if not mins.isdigit() or not len(mins) == 2:
                        print("[!] Error setting alarm. Please rephrase your query.")
                    else:
                        new_alarm = hrs+":"+mins
                        self.__writeAlarm__(new_alarm)
                        return
            else:
                print("[!] Error setting alarm. Please rephrase your query.")

        elif "am" in time_list:
            time_list.pop("am")
            num_elements = len(time_list)
            new_alarm = ""
            if num_elements == 1:
                alarm_time = time_list[0]
                if alarm_time.isdigit():
                    if 2 >= len(alarm_time) >= 1:
                        if alarm_time == "12":
                            new_alarm = "00:00"
                            self.__writeAlarm__(new_alarm)
                            return
                        elif len(alarm_time) == 1:
                            new_alarm = "0"+alarm_time+":00"
                            self.__writeAlarm__(new_alarm)
                            return
                        elif 0 < int(alarm_time) <= 12:
                            new_alarm = alarm_time + ":00"
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query")
                    elif 4 >= len(alarm_time) >= 3:
                        mins = alarm_time[-2:]
                        if len(alarm_time) == 3:
                            hrs = "0" + alarm_time[0]
                        else:
                            hrs = alarm_time[0:2]
                        if mins.isdigit() and hrs.isdigit():
                            new_alarm = hrs + ":" + mins
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query")
                    else:
                        print("[!] Error setting alarm. Please rephrase your query")
                else:
                    print("[!] Error setting alarm. Please rephrase your query")

            elif num_elements == 2:
                hrs = time_list[0]
                mins = time_list[1]
                if hrs.isdigit():
                    num_hrs = int(hrs)
                    if not (0 < num_hrs <= 12):
                        print("[!] Error setting alarm. Please rephrase your query.")
                    else:
                        if len(hrs) == 1:
                            hrs = "0"+hrs
                        if mins.isdigit() and len(mins) == 2 and 0 <= int(mins) <= 59:
                            new_alarm = hrs + ":" + mins
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query.")
                else:
                    print("[!] Error setting alarm. Please rephrase your query.")
            else:
                print("[!] Error setting alarm. Please rephrase your query.")

        elif "pm" in time_list:
            time_list.pop("pm")
            num_elements = len(time_list)
            new_alarm = ""
            if num_elements == 1:
                alarm_time = time_list[0]
                if alarm_time.isdigit():
                    if 2 >= len(alarm_time) >= 1:
                        if alarm_time == "12":
                            new_alarm = "12:00"
                            self.__writeAlarm__(new_alarm)
                            return
                        elif 0 < int(alarm_time) <= 12:
                            alarm_time = str(int(alarm_time) + 12)
                            new_alarm = alarm_time+":00"
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query")
                    elif 4 >= len(alarm_time) >= 3:
                        mins = alarm_time[-2:]
                        if len(alarm_time) == 3:
                            hrs = str(12 + int(alarm_time[0]))
                        else:
                            hrs = str(12 + int(alarm_time[0:2]))
                        if mins.isdigit() and hrs.isdigit():
                            if 12 < int(hrs) < 24:
                                new_alarm = hrs + ":" + mins
                                self.__writeAlarm__(new_alarm)
                                return
                            elif int(hrs) == 24:
                                new_alarm = "12:"+mins
                                self.__writeAlarm__(new_alarm)
                                return
                            else:
                                print("[!] Error setting alarm. Please rephrase your query")
                        else:
                            print("[!] Error setting alarm. Please rephrase your query")
                    else:
                        print("[!] Error setting alarm. Please rephrase your query")
                else:
                    print("[!] Error setting alarm. Please rephrase your query")

            elif num_elements == 2:
                hrs = time_list[0]
                mins = time_list[1]
                if hrs.isdigit():
                    num_hrs = int(hrs)
                    if not (0 < num_hrs <= 12):
                        print("[!] Error setting alarm. Please rephrase your query.")
                    else:
                        hrs = str(num_hrs + 12)
                        if hrs == 24:
                            hrs = "12"
                        if mins.isdigit() and len(mins) == 2 and 0 <= int(mins) <= 59:
                            new_alarm = hrs + ":" + mins
                            self.__writeAlarm__(new_alarm)
                            return
                        else:
                            print("[!] Error setting alarm. Please rephrase your query.")
                else:
                    print("[!] Error setting alarm. Please rephrase your query.")
            else:
                print("[!] Error setting alarm. Please rephrase your query.")



    @staticmethod
    def __sanitizeCommand__(raw_string):
        filtered_command = '''([0-9]+)|(\:)|(am)|(pm)|(hours)|(minutes)(hour)|(minute)|(now)'''
        p = re.compile(filtered_command)
        useful_words = ["hours", "minutes", "hour", "minute", "now", "am", "pm", ":"]
        captures = list(p.finditer(raw_string.lower()))
        time_maker = [x.group() for x in captures if x.group() in useful_words or x.group().isdigit()]
        return time_maker

    def run(self, params):
        time_tokens = self.__sanitizeCommand__(params)
        self.__addAlarm__(time_tokens)

    def endSkill(self):
        pass


##Tests
'''test_obj = AlarmManager()
test_obj.run("set alarm for 1 minute from now")
test_obj.__checkAlarms__()'''