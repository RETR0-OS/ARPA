from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import datetime
import pickle
import settings

class MakeToDoList(Skill):

    triggerIntent = ""
    user = None
    file = None

    def __init__(self):
        super(MakeToDoList, self).__init__(trigger_intent=self.triggerIntent)

        self.user = settings.CURRENT_USER
        self.file = f"UserData/ToDoLists/{self.user}"

    @staticmethod
    def __getListItem__():
        item = input("Enter task to add (Leave blank if you are done)>>")
        if item != "":
            return item
        else:
            return None

    def run(self, params):
        task_list = []
        while True:
            task = self.__getListItem__()
            if task is not None:
                task_list.append(task)
            else:
                break

        f = open(self.file, "rb")
        data = pickle.load(f)
        data.extend(task_list)
        f.close()
        f = open(self.file, "wb")
        pickle.dump(data, f)

        self.endSkill()

    def endSkill(self):
        print("Tasks added!")