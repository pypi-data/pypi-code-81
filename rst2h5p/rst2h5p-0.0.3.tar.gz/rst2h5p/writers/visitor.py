from ..elements import SingleChoice, MultiChoice

class VisitorSpecialState():
    def get_element(self):
        pass

class VisitorSpecialSingleChoice(VisitorSpecialState):
    def __init__(self, **kwargs):
        self.element = SingleChoice(**kwargs)
        self.current_question = None
    def close_question(self):
        if self.current_question:
            return self.element.add_question(self.current_question["question"], self.current_question["answers"])
        self.current_question = None
    def add_option(self, content):
        assert self.current_question
        self.current_question["answers"].append(content)
    def set_question(self, text):
        self.close_question()
        self.current_question = {"question": text, "answers": []}
    def get_element(self):
        self.close_question()
        return self.element

class VisitorSpecialMultiChoice(VisitorSpecialState):
    def __init__(self, correct, **kwargs):
        self.element = MultiChoice(**kwargs)
        self.correct = correct
        self.counter = 1
    def add_option(self, content):
        self.element.add_option(content, self.counter in self.correct)
        self.counter += 1
    def set_question(self, text):
        self.element.set_question(text)
    def get_element(self):
        return self.element

