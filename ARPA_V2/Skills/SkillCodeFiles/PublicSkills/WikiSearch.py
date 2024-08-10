from ARPA_V2.Skills.SkillCodeFiles.Skill import Skill
import wikipedia
import spacy

class WikiSearch(Skill):
    triggerIntent = "wiki_search"
    nlp = None
    skillType = "public"

    def __init__(self):
        super(WikiSearch, self).__init__(trigger_intent=self.triggerIntent, skill_type=self.skillType)
        self.nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def sanitizeInput(raw_query):
        raw_query = raw_query.split()
        redundancies = ["who", "what", "where", "is", "how", "are", "were", "please", "tell", "about", "me", "when"]
        processed_query = [x for x in raw_query if x not in redundancies]
        return " ".join(processed_query)


    def run(self, search_query):
        try:
            query = self.sanitizeInput(search_query)
            summary = wikipedia.summary(query, sentences=7, auto_suggest=False)
            print(summary)
            more = input("Do you wish to learn more? \n>> ")
            more = self.nlp(self.sanitizeInput(more))
            confirm = {
                "yes": ["yes", "yup", "yeah", "yes, tell me more", "yes tell me more", "more", "tell me",
                        "yes I want to",
                        "yes I want to learn more", "yes arpa", "tell me more arpa", "arpa tell me more", "yes arpa"],
                "no": ["no", "nope", "no thank you", "no I don't want to", "that's all", "no i do not want to",
                       "no need",
                       "that's all i need", "non"]}
            confirmation = ""
            cur_max_confirm = 0
            for key in confirm.keys():
                for i in confirm[key]:
                    similarity = more.similarity(self.nlp(i))
                    if similarity > cur_max_confirm:
                        confirmation = key
                        cur_max_confirm = similarity
            if confirmation == "yes":
                print("Ok! Here is some more information: \n")
                result = wikipedia.summary(query, sentences=100, auto_suggest=False)
                print(result)
                print()
                print()
                print("For additional information, might I suggest looking at: ",
                      wikipedia.page(query, auto_suggest=False).url)
                print("Source: Wikipedia")
            elif confirmation == "no":
                print("Ok.")
        except wikipedia.exceptions.DisambiguationError as e:
            print("The query was too ambiguous. It was interpreted in the following contexts: \n")
            print(e.options)
            print()
            print("Please try a fresh query with a little more detail.")
        except wikipedia.exceptions.PageError:
            print("Sorry, I could not understand you. Perhaps you made a spelling error?")
        except wikipedia.exceptions.HTTPTimeoutError:
            print("Sorry, your request wasn't processed correctly. Please retry in a while.")
        except wikipedia.exceptions.RedirectError:
            print("Sorry, there was some error. Please try again.")
        except Exception as e:
            print("An unidentified error occurred. Please try again.")

    def endSkill(self):
        pass