from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill

class ShowHelp(Skill):

    triggerIntent = "show_help"
    skillType = "public"

    def __init__(self):
        super(ShowHelp, self).__init__(trigger_intent = self.triggerIntent, skill_type=self.skillType)

    def run(self):
        help_message = '''
        ##### Help Menu #####
        This assistant is capable of the following tasks
        1) Telling time: Try, "Tell me the time."
        2) Telling date: Try, "Tell me the date."
        3) Playing Music: Try, "Play <song name> by <artist>."
        4) Web search: Try, "find flights from new delhi to london", or "how to make an omelette", or "what is the capital of France?"
        5) Get Information: Try, "Who is Elon Musk?", "Who is Shawn Mendes?", "Tell me about world war 2", "What is Apple Inc.?", "Tell me about Delhi."
        6) Do calculations: Try, "what is (5 + 4) - 3 into sin(pi) plus cos(pi/4) multiply 3?"
        '''
        print(help_message)

    def endSkill(self):
        pass
