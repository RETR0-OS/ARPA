from ARPA_V2.ARPAv2 import Assistant
from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.PlayMusic import PlayMusic
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.TellDate import TellDate
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.TellTime import TellTime
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.W2Math import W2Math
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.SayGoodBye import SayGoodBye
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.ShowHelp import ShowHelp
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.WebSearch import WebSearch
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.WikiSearch import WikiSearch
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.IndroduceBot import IntroduceBot
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.SetTimer import SetTimer
from ARPA_V2.Skills.SkillCodeFiles.PublicSkills.AlarmManager import AlarmManager
class SkillManager:
    availableSkills = None
    selectedSkill = None

    def __init__(self):
        self.availableSkills = Skill.__subclasses__()

    def __matchSkill__(self, intent):
        for skill in self.availableSkills:
            if skill.triggerIntent == intent:
                self.selectedSkill = skill
                break

    def __runSkill__(self, params):
        skill = self.selectedSkill()
        if skill.skillType == "public":
            skill.run(params)
            skill.endSkill()
        elif skill.skillType == "authenticated" and Assistant.currentUser is not None:
            skill.run(params)
            skill.endSkill()
        else:
            print("You are not authorized to do that!")


    def executeCommand(self, intent, params):
        self.__matchSkill__(intent)
        self.__runSkill__(params)
