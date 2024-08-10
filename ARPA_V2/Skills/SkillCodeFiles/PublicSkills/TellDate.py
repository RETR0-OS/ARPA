from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import datetime
import random

class TellDate(Skill):

    triggerIntent = "tell_date"
    date = None
    skillType = "public"

    def __init__(self):
        super(TellDate, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    def run(self, param):
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
        self.date = date_sentences[random.randint(0, len(date_sentences) - 1)]

    def endSkill(self):
        print(self.date)

