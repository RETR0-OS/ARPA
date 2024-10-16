from Skills.SkillCodeFiles.Skill import Skill
import settings
import getpass

class AuthenticateUser(Skill):

    def __init__(self):
        triggerIntent = "login"
        skillType = "public"
        super(AuthenticateUser, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)

    def run(self, params):
        username = input("Enter your username>> ")
        passwd = getpass.getpass("Enter your password>> ")

        for user_profile in settings.REGISTERED_USER_PROFILES:
            if user_profile["user"] == username and user_profile["password"] ==passwd:
                settings.CURRENT_USER = username
                settings.USER_AUTH_LEVEL = user_profile["auth_level"]
                return

    def endSkill(self):
        print(f"Welcome, {settings.CURRENT_USER}. What would you like to do today?")
