from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import random

class IntroduceBot(Skill):
    triggerIntent = "introduce_"
    introduction = None
    skillType = "public"

    def __init__(self):
        super(IntroduceBot, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    def run(self, params):
        introductions = [
            "Hi there! I'm your personal assistant. Say 'help' to see what I can do.",
            "Hello! I'm your assistant.  Type 'help' to learn more about my capabilities.",
            "Greetings! I'm your personal assistant. Say 'help' to discover what I can assist you with.",
            "Hey! I'm your assistant. Say 'help' to know what I can do.",
            "Hello, I'm your assistant. Type 'help' to see my functions.",
            "Hi, I’m your personal assistant. Say 'help' to find out my features.",
            "Hey there! I’m your personal assistant. Say 'help' to learn more about my skills.",
            "Hi, I'm here to assist you. Type 'help' to see how I can help.",
            "Hello! I'm your personal assistant. Type 'help' to know more about my abilities.",
            "Greetings! I’m your assistant. Say 'help' to find out what I can do."
        ]
        greeting_number = random.randint(0, len(introductions) - 1)
        self.introduction = introductions[greeting_number]

    def endSkill(self):
        print(self.introduction)