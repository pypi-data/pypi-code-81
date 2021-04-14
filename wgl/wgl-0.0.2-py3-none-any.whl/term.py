# IMPORTS

import ctypes
import os
import math
from wTermUi.widgets import *
from wTermUi.wErrors import wTermException
from pynput.keyboard import Key, Listener

# MAIN CODE


class TermWin:
    def __init__(self, win_size: list, win_title: str, max_pages: int = 1, key_events: list = None, border_letters: str = "╚╔╩╦╠═╬╝╗║╣"):
        self.max_pages = max_pages
        self.page = 1
        if key_events is None:
            key_events = [self.key_down, self.key_up]
        self.key_events = key_events
        self.border_letters = border_letters
        # ctypes.windll.kernel32.SetConsoleTitleA(win_title)
        os.system(f'mode con: cols={win_size[0]-1} lines={win_size[1]}')
        os.system(f"title {win_title}")
        self.win_size = win_size
        self.win_title = win_title
        self.widgets = []
        self.pointer = 0

    def update_list(self, key):
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
            for widget in self.widgets:
                if isinstance(widget, TextBox):
                    if widget.active:
                        input()
                        widget.text = input("Set text: ")
                        if widget.callback is not None:
                            widget.callback()
                        break
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

    def key_down(self, key):
        self.update_list(key)
        self.render()

    def key_up(self, key):
        # self.render()
        pass

    def main_loop(self):
        self.render()
        self.wait_for_input()
        while True:
            pass

    def wait_for_input(self):
        with Listener(on_press=self.key_down, on_release=self.key_up) as listener:
            listener.join()

    def render(self):
        os.system("cls")
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
                        buffer_data[self.page-1][line] = widget.render([self.page, line, buffer_data[self.page-1][line]])
            buffer_data[self.page-1][line] += (" " * (self.win_size[0] - (str.__len__(buffer_data[self.page-1][line]) + 2))) + self.border_letters[9]
            print(buffer_data[self.page-1][line])

        print(self.border_letters[0] + (self.border_letters[5] * (self.win_size[0] - 3)) + self.border_letters[7])

    def add_widget(self, widget: Widget) -> Widget:
        if isinstance(widget, (Label, TextBox, Button, Switch)):
            self.widgets.append(widget)
            return widget
        else:
            raise wTermException(f"Passed argument {widget} is not a valid wTerm widget")
