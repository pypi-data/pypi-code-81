from uuid import uuid4

class Element():
    def __init__(self, *, x = 0, y = 0, width = 100, height = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = None
        self.alwaysDisplayComments = False
        self.backgroundOpacity = 0
        self.displayAsButton = False
        self.buttonSize = "big"
        self.goToSlideType = "specified"
        self.invisible = False
        self.solution = ""
    def get_object(self):
        return vars(self)

class AdvancedText(Element):
    def __init__(self, text = None, *, x = 0, y = 0, width = 100, height = 100):
        super().__init__(x = x, y = y, width = width, height = height)
        self.action = {
            "library": "H5P.AdvancedText 1.1",
            "params": {
                "text": text
            },
            "subContentId": str(uuid4()),
            "metadata": {
                "contentType": "Text",
                "license": "U",
                "title": "Untitled Text"
            }
        }

class SingleChoice(Element):
    def __init__(self, question = "", *, x = 0, y = 0, width = 100, height = 100):
        super().__init__(x = x, y = y, width = width, height = height)
        self.action = {
            "library": "H5P.SingleChoiceSet 1.11",
            "params": {
                "choices": [],
                "overallFeedback": [{ "from": 0, "to": 100 }],
                "behaviour": {
                    "timeoutCorrect": 1000,
                    "timeoutWrong": 1000,
                    "soundEffectsEnabled": True,
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "passPercentage": 100,
                    "autoContinue": True
                },
            },
            "subContentId": str(uuid4()),
            "metadata": {
                "contentType": "Single Choice Set",
                "license": "U",
                "title": "Untitled Single Choice Set"
            }
        }
    def add_question(self, text, answers):
        self.action["params"]["choices"].append({
            "question": text,
            "answers": answers,
            "subContentId": str(uuid4())
        })

    def set_behaviour(self, key, value):
        self.action["params"]["behaviour"][key] = value
class MultiChoice(Element):
    def __init__(self, question = "", *, x = 0, y = 0, width = 100, height = 100):
        super().__init__(x = x, y = y, width = width, height = height)
        self.action = {
            "library": "H5P.MultiChoice 1.14",
            "params": {
                "question": question,
                "answers": [],
                "overallFeedback": [{ "from": 0, "to": 100 }],
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "type": "auto",
                    "singlePoint": False,
                    "randomAnswers": True,
                    "showSolutionsRequiresInput": True,
                    "confirmCheckDialog": False,
                    "confirmRetryDialog": False,
                    "autoCheck": False,
                    "passPercentage": 100,
                    "showScorePoints": True
                },
            },
            "subContentId": str(uuid4()),
            "metadata": {
                "contentType": "Multiple Choice",
                "license": "U",
                "title": "Untitled Multiple Choice"
            }
        }

    def add_option(self, text, correct):
        self.action["params"]["answers"].append({
            "correct": correct,
            "text": text
        })

    def set_behaviour(self, key, value):
        self.action["params"]["behaviour"][key] = value

    def set_question(self, text):
        self.action["params"]["question"] = text
