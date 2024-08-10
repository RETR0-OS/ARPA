from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import threading
import time
import ctypes
import winsound

class SetTimer(Skill):
    time_left = 0
    timer_thread = None
    triggerIntent = "set_timer"
    skillType = "public"

    def __init__(self):
        super(SetTimer, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    @staticmethod
    def sanitizeInput(params):
        important_words = ["second", "hour", "minute", "half", "an"]


    @staticmethod
    def trackTime(timer):
        time.sleep(timer)
        winsound.PlaySound("Skills/SkillCodeFiles/PublicSkills/ExtraDataFiles/alarm.wav", winsound.SND_ASYNC)
        ctypes.windll.user32.MessageBoxW(0, "Your time is up!", "Time Up!", 1)
        winsound.PlaySound(None, winsound.SND_ASYNC)

    def run(self, params):
        print("Timer started.")
        self.timer_thread = threading.Thread(target=self.trackTime, args=(params,))
        self.timer_thread.daemon = True
        self.timer_thread.start()
        self.endSkill()
    
    def endSkill(self):
        pass

# timer = SetTimer()
# timer.run(2)