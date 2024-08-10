from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill

class SayGoodBye(Skill):
    triggerIntent = "exit"
    skillType = "public"

    def __init__(self):
        super(SayGoodBye, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    def run(self, params):
        print("Goodbye. I hope I helped!")

    def endSkill(self):
        exit()