from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service

class WebSearch(Skill):
    targetIntent = "web_search"
    brave_path = None
    driver_path = None
    driver = None
    skillType = "public"

    def __init__(self):
        super(WebSearch, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)
        self.brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/Brave.exe"
        self.driver_path = Service(executable_path=binary_path)

    @staticmethod
    def sanitizeInput(raw_query):
        raw_query = raw_query.split()
        redundancies = ["search", "find", "look"]
        processed_query = [x for x in raw_query if x not in redundancies]
        return " ".join(processed_query)

    def run(self, search_string):
        option = webdriver.ChromeOptions()
        option.binary_location = self.brave_path
        option.add_experimental_option("detach", True)

        browser = webdriver.Chrome(service=self.driver_path, options=option)

        query = self.sanitizeInput(search_string)

        try:
            browser.get(f"https://google.com/search?q={query}")
        except TimeoutError:
            print("[!] Error connecting to the internet. Please check your internet connection!")
        except Exception as e:
            print("[!] An unidentified error occurred! Error message:\n")
            print(e)
        finally:
            browser.close()

    def endSkill(self):
        pass