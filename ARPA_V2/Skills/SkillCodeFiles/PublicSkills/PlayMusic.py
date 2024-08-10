from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
from selenium import webdriver
from chromedriver_py import binary_path
from youtubesearchpython import VideosSearch as vidSearch
from pyautogui import getAllWindows, getWindowsWithTitle
import time
from selenium.webdriver.chrome.service import Service

class PlayMusic(Skill):
    driver = None
    brave_path = None
    driver_path = None
    triggerIntent = "play_music"
    skillType = "public"

    def __init__(self):
        super(PlayMusic, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)
        self.brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/Brave.exe"
        self.driver_path = Service(executable_path=binary_path)

    @staticmethod
    def manageWindows():
        windows = getAllWindows()
        windows = [x.title for x in windows if x.title not in ['', 'Mail', 'Add an account', 'Settings', 'Windows Input Experience', 'Program Manager']]
        getWindowsWithTitle(windows[0])[0].minimize()

    @staticmethod
    def sanitizeInput(raw_query):
        raw_query = raw_query.split()
        redundancies = ["Play", "music", "tunes", "song", "beats"]
        processed_query = [x for x in raw_query if x not in redundancies]
        return " ".join(processed_query)

    def run(self, search_string):
        option = webdriver.ChromeOptions()
        option.binary_location = self.brave_path
        option.add_experimental_option("detach", True)

        browser = webdriver.Chrome(service=self.driver_path, options=option)

        query = self.sanitizeInput(search_string)

        v_search = vidSearch(query, limit=1)
        link = v_search.result()["result"][0]["link"]

        try:
            browser.get(link)
            time.sleep(2)
            self.manageWindows()
        except TimeoutError:
            print("[!] Error connecting to the internet. Please check your internet connection!")
        except Exception as e:
            print("[!] An unidentified error occurred! Error message:\n")
            print(e)
        finally:
            browser.close()

    def endSkill(self):
        pass