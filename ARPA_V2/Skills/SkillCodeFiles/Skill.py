from abc import ABC, abstractmethod, abstractproperty

class Skill(ABC):
    triggerIntent = None
    skillType = None

    def __init__(self, trigger_intent, skill_type="public"):
        if trigger_intent is None:
            raise ValueError("trigger_intent cannot be none!")
        else:
            self.triggerIntent = trigger_intent
            self.skillType = skill_type

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    @abstractmethod
    def endSkill(self):
        pass
