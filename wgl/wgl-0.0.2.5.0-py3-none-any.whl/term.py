# IMPORTS

import os
import math
from wTermUi.widgets import *
from wTermUi.wErrors import wTermException
from pynput.keyboard import Key, Listener, Events
import string

# MAIN CODE


class TermWin:
    """
    Base class for wTermUi, this is the main class that handles widgets and rendering.
    Create a new window using:
    TermWin([size x, size y], "Name of window")
    It also accepts more parameters, so a fully customized
    TermWin would look like this:
    TermWin([100, 40], "Example TermWin", 2, True, True, None)
    For more info look at the documentation:
    https://pypi.org/project/wgl/
    """
    def __init__(self, win_size: list, win_title: str, max_pages: int = 1, allow_scaling: bool = True, adjust_term_size: bool = False, key_events: list = None, border_letters: str = "╚╔╩╦╠═╬╝╗║╣"):
        self.max_pages = max_pages
        self.adjust_term_size = adjust_term_size
        self.page = 1
        self.allow_scaling = allow_scaling
        if key_events is None:
            key_events = [self.key_down, self.key_up]
        self.key_events = key_events
        self.border_letters = border_letters
        os.system(f'mode con: cols={win_size[0]-1} lines={win_size[1]}')
        os.system(f"title {win_title}")
        self.win_size = win_size
        self.win_title = win_title
        self.widgets = []
        self.pointer = 0
        self.editing = False

    def update_list(self, key):
        """
        Handles all key events and updates widgets.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        self.listener.stop()
        if key == Key.down:
            self.pointer += 1
        if key == Key.up:
            self.pointer -= 1
            if self.pointer < 0:
                self.pointer = 0
        if key == Key.left:
            self.page -= 1
            if self.page < 1:
                self.page = 1
            self.pointer = 0
        if key == Key.right:
            self.page += 1
            if self.page > self.max_pages:
                self.page = self.max_pages
            self.pointer = 0
        if key == Key.enter:
            if not self.editing:
                for widget in self.widgets:
                    if isinstance(widget, TextBox):
                        if widget.active:
                            self.editing = True
                            input("Modify text to:")
                            data_ = input("> ")
                            if widget.type == WGL_TYPES_STRING:
                                widget.text = str(data_[:widget.max_len])
                            elif widget.type == WGL_TYPES_INT:
                                widget.text = int(data_[:widget.max_len])
                            elif widget.type == WGL_TYPES_FLOAT:
                                widget.text = float(data_[:widget.max_len])
                            if widget.callback is not None:
                                widget.callback()
                            self.editing = False

                    if isinstance(widget, Button):
                        if widget.active:
                            if widget.callback is not None:
                                widget.callback()
                            break

                    if isinstance(widget, Switch):
                        if widget.active:
                            widget.toggled = not widget.toggled
                            if widget.callback is not None:
                                widget.callback()
                            break
                return False

    def key_down(self, key):
        """
        key_down calls update_list and renders
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        self.update_list(key)
        self.render()

    def key_up(self, key):
        """
        key_up does nothing
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        # self.render()
        pass

    def main_loop(self):
        """
        main_loop handles all key inputs and calls all the functions
        necessary to use wTermUi.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        while True:
            self.render()
            self.wait_for_input()

    def wait_for_input(self):
        """
        Creates a listener. Does nothing more.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        with Listener(on_press=self.key_down, on_release=self.key_up) as listener:
            self.listener = listener
            self.listener.join()

    def render(self):
        """
        Creates a buffer for every line and appends any
        widgets to said buffer. Rendering happens on
        updates only to make the windows look more clean.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        os.system("cls")
        if not self.allow_scaling:
            os.system(f'mode con: cols={self.win_size[0] - 1} lines={self.win_size[1]}')
        else:
            if self.adjust_term_size:
                self.win_size = [os.get_terminal_size()[0], os.get_terminal_size()[1]]
        tblen = self.win_size[0] - 2
        tblen -= (str.__len__(self.win_title)+2)
        print(" " + self.border_letters[1] + self.border_letters[5]*(str.__len__(self.win_title)+2) + self.border_letters[3] + self.border_letters[5]*(9 + str.__len__(str(self.max_pages))) + self.border_letters[8])
        print(self.border_letters[1] + self.border_letters[10] + " " + self.win_title + " " + self.border_letters[9] + " Page " + str(self.page) + "/" + str(self.max_pages) + " " + self.border_letters[4] + self.border_letters[5]*(math.floor(tblen)-4-(9 + str.__len__(str(self.max_pages)))) + self.border_letters[8])
        print(self.border_letters[9] + self.border_letters[0] + self.border_letters[5] * (str.__len__(self.win_title) + 2) + self.border_letters[2] + self.border_letters[5]*(9 + str.__len__(str(self.max_pages))) + self.border_letters[7] + " " * (math.floor(tblen)-4-(9 + str.__len__(str(self.max_pages)))) + self.border_letters[9])
        inputs = []
        for i in range(self.max_pages):
            page_inputs = []
            inputs.append(page_inputs)
        for widget in self.widgets:
            if isinstance(widget, (TextBox, Button, Switch)):
                inputs[widget.pos[2] - 1].append(widget)
                widget.active = False
        selected_input = False
        if len(inputs[self.page-1]) > 0:
            try:
                selected_input = inputs[self.page - 1][self.pointer]
            except IndexError:
                selected_input = inputs[self.page - 1][len(inputs[self.page - 1]) - 1]
                self.pointer = len(inputs[self.page - 1]) - 1
        if selected_input:
            selected_input.active = True
        buffer_data = []
        for page in range(0, self.max_pages):
            c_page = []
            buffer_data.append(c_page)
            for line in range(0, self.win_size[1] - 7):
                c_page.append(self.border_letters[9] + " ")

        for line in range(0, self.win_size[1] - 7):
            for widget in self.widgets:
                if widget.pos[1] == line:
                    if widget.pos[2] == self.page:
                        if not isinstance(widget, Divider):
                            buffer_data[self.page-1][line] = widget.render(
                                [self.page, line, buffer_data[self.page-1][line]])
                        else:
                            buffer_data[self.page - 1][line] = widget.render(
                                [self.page, line, buffer_data[self.page - 1][line]], self)
            buffer_data[self.page-1][line] += (" " * (self.win_size[0] - (str.__len__(buffer_data[self.page-1][line]) + 2))) + self.border_letters[9]
            print(buffer_data[self.page-1][line])

        print(self.border_letters[0] + (self.border_letters[5] * (self.win_size[0] - 3)) + self.border_letters[7])

    def add_widget(self, widget: Widget) -> Widget:
        """
        Creates and returns a widget. This widget
        has readable and writable data that can
        be accessed by any external code.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        if isinstance(widget, (Label, TextBox, Button, Switch, Divider)):
            self.widgets.append(widget)
            return widget
        else:
            raise wTermException(f"Passed argument '{widget}' is not a valid wTerm widget")

    def quick_ui_gen(self, data):
        """
        This function will take any data that looks like this:
        'Name: [INSERT NAME]'
        and converts it to 2 widgets
        Label([0,0,1], "Name:"), TextBox([7,0,1], "INSERT NAME")
        and replaces all current widgets.
        Probably will support for pages later.
        For more info look at the documentation:
        https://pypi.org/project/wgl/
        """
        idx = 0
        line = 0
        label_text = string.ascii_lowercase+string.ascii_uppercase+string.digits+" :-+=!\"#¤%&/.,<>"
        x = 0
        try:
            current_char = data[idx]
        except IndexError:
            raise wTermException("Data passed isn't long enough to generate widgets")
        while current_char is not None:
            if current_char in label_text:
                label_data = ""
                pos = x+0
                while current_char in label_text:
                    label_data += current_char
                    idx += 1
                    x += 1
                    try:
                        current_char = data[idx]
                    except IndexError:
                        break
                self.widgets.append(Label([pos, line, 1], label_data))

            if current_char in "[":
                input_data = ""
                pos = x+0
                idx += 1
                x += 1
                try:
                    current_char = data[idx]
                except IndexError:
                    break
                while current_char not in "]":
                    input_data += current_char
                    idx += 1
                    x += 1
                    try:
                        current_char = data[idx]
                    except IndexError:
                        break
                self.widgets.append(TextBox([pos, line, 1], input_data))

            if current_char in "(":
                print("Button")
                button_data = ""
                pos = x+0
                idx += 1
                x += 1
                try:
                    current_char = data[idx]
                except IndexError:
                    break
                while current_char not in ")":
                    button_data += current_char
                    idx += 1
                    x += 1
                    try:
                        current_char = data[idx]
                    except IndexError:
                        break
                self.widgets.append(Button([pos, line, 1], button_data))

            if current_char == "{":
                self.widgets.append(Switch([x, line, 1]))
                idx += 2
                x += 2
                try:
                    current_char = data[idx]
                except IndexError:
                    break

            if current_char in "\n;":
                line += 1
                x = -1

            idx += 1
            x += 1
            try:
                current_char = data[idx]
            except IndexError:
                break

# Local testing so I don't have to upload broken functions


if __name__ == "__main__":
    new_term = TermWin([80, 20], "qui testing", allow_scaling=True)

    new_term.quick_ui_gen("""Test input: [Input1]
Switch: {}
close inputs: [inp1][inp2][inp3][inp4]""")

    new_term.main_loop()