class Widget:
    def __init__(self, pos: list, text: str, placeholder_text: str, toggled: bool = False, callback=None):
        self.callback = callback
        self.placeholder_text = placeholder_text
        self.text = text
        self.pos = pos
        self.toggled = toggled

    def __repr__(self):
        return f"Generic Widget"


class Label(Widget):
    def __init__(self, pos, text):
        self.pos = pos
        self.text = text

    def render(self, data):
        if data[0] == self.pos[2]:
            if data[1] == self.pos[1]:
                new_data = data[2]
                try:
                    if str.__len__(new_data) - 2 > self.pos[0]:
                        new_data = new_data[:self.pos[0]]
                    else:
                        new_data = new_data + " "*(self.pos[0] - (str.__len__(new_data)-2))
                except TypeError:
                    return new_data
                new_data += self.text
                new_data = new_data + data[2][str.__len__(new_data):]
                return new_data
        return data[2]

    def __repr__(self):
        return self.text


class TextBox(Widget):
    def __init__(self, pos, placeholder_text, callback=None):
        self.pos = pos
        self.placeholder_text = placeholder_text
        self.active = False
        self.text = ""
        self.callback = callback

    def render(self, data):
        if data[0] == self.pos[2]:
            if data[1] == self.pos[1]:
                new_data = data[2]
                if str.__len__(new_data)-2 > self.pos[0]:
                    new_data = new_data[:self.pos[0]]
                else:
                    new_data = new_data + " "*(self.pos[0] - (str.__len__(new_data)-2))
                if not self.active:
                    if not self.text:
                        new_data += "["+self.placeholder_text+"]"
                    else:
                        new_data += "[" + self.text + "]"
                else:
                    if not self.text:
                        new_data += ">" + self.placeholder_text + "<"
                    else:
                        new_data += ">" + self.text + "<"
                new_data = new_data + data[2][str.__len__(new_data):]
                return new_data

    def __repr__(self):
        return "["+self.placeholder_text+"]"


class Button(Widget):
    def __init__(self, pos, text, callback=None):
        self.pos = pos
        self.active = False
        self.text = text
        self.callback = callback

    def render(self, data):
        if data[0] == self.pos[2]:
            if data[1] == self.pos[1]:
                new_data = data[2]
                if str.__len__(new_data)-2 > self.pos[0]:
                    new_data = new_data[:self.pos[0]]
                else:
                    new_data = new_data + " "*(self.pos[0] - (str.__len__(new_data)-2))
                if not self.active:
                    new_data += "(" + self.text + ")"
                else:
                    new_data += ">" + self.text + "<"
                new_data = new_data + data[2][str.__len__(new_data):]
                return new_data

    def __repr__(self):
        return "["+self.text+"]"


class Switch(Widget):
    def __init__(self, pos, callback=None):
        self.pos = pos
        self.active = False
        self.toggled = False
        self.callback = callback

    def render(self, data):
        if data[0] == self.pos[2]:
            if data[1] == self.pos[1]:
                new_data = data[2]
                if str.__len__(new_data)-2 > self.pos[0]:
                    new_data = new_data[:self.pos[0]]
                else:
                    new_data = new_data + " "*(self.pos[0] - (str.__len__(new_data)-2))
                if not self.active:
                    if self.toggled:
                        new_data += "[x]"
                    else:
                        new_data += "[ ]"
                else:
                    if self.toggled:
                        new_data += ">x<"
                    else:
                        new_data += "> <"
                new_data = new_data + data[2][str.__len__(new_data):]
                return new_data

    def __repr__(self):
        return "[ ]"
