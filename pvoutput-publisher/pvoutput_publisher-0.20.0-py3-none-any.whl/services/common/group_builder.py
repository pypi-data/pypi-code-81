class Builder:
    def __init__(self, value_separator = ",", group_separator = ";"):
        self.group_separator = group_separator
        self.value_separator = value_separator
        self.text = ""
        self.first_value = True
        self.new_group = True

    def add_value(self, value: str = None):
        self.add_value_separator()
        self.add_group_separator()
        if value is not None:
            self.text += str(value)
        self.first_value = False

    def add_value_separator(self):
        if not self.first_value and not self.new_group:
            self.text += self.value_separator
            self.first_value = False

    def add_group_separator(self):
        if self.new_group and self.text != "":
            self.text += self.group_separator
        self.new_group = False

    def next_group(self):
        self.first_value = True
        self.new_group = True