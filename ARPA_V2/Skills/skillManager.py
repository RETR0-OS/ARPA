#from ARPAv2 import Assistant
import settings
from Skills.SkillCodeFiles.Skill import Skill
from Skills.SkillCodeFiles.PublicSkills.PlayMusic import PlayMusic
from Skills.SkillCodeFiles.PublicSkills.TellDate import TellDate
from Skills.SkillCodeFiles.PublicSkills.TellTime import TellTime
from Skills.SkillCodeFiles.PublicSkills.W2Math import W2Math
from Skills.SkillCodeFiles.PublicSkills.SayGoodBye import SayGoodBye
from Skills.SkillCodeFiles.PublicSkills.ShowHelp import ShowHelp
from Skills.SkillCodeFiles.PublicSkills.WebSearch import WebSearch
from Skills.SkillCodeFiles.PublicSkills.WikiSearch import WikiSearch
from Skills.SkillCodeFiles.PublicSkills.IndroduceBot import IntroduceBot
from Skills.SkillCodeFiles.PublicSkills.SetTimer import SetTimer
from Skills.SkillCodeFiles.PublicSkills.AlarmManager import AlarmManager
from Skills.SkillCodeFiles.PublicSkills.AuthenticateUser import AuthenticateUser

class SkillManager:
    availableSkills = None
    selectedSkill = None

    def __init__(self):
        self.availableSkills = Skill.__subclasses__()

    def __matchSkill__(self, intent):
        for skill in self.availableSkills:
            if skill.triggerIntent == intent:
                self.selectedSkill = skill
                return
        self.selectedSkill = None

    def __runSkill__(self, params):
        if self.selectedSkill is None:
            print("Sorry, I could not understand you.")
            return
        skill = self.selectedSkill()
        if skill.skillType == "public":
            skill.run(params)
            skill.endSkill()
        elif skill.skillType == "authenticated" and settings.CURRENT_USER is not None:
            skill.run(params)
            skill.endSkill()
        else:
            print("You are not authorized to do that!")

    def executeCommand(self, intent, params):
        self.__matchSkill__(intent)
        self.__runSkill__(params)
