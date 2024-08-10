from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import datetime
import random

class TellTime(Skill):

    triggerIntent = "tell_time"
    time = None
    skillType = "public"

    def __init__(self):
        super(TellTime, self).__init__(self.triggerIntent, skill_type=self.skillType)

    def run(self, param):
        current_time = datetime.datetime.now().strftime("%H:%M")
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
        self.time = time_sentences[random.randint(0, len(time_sentences)-1)]

    def endSkill(self):
        print(self.time)

