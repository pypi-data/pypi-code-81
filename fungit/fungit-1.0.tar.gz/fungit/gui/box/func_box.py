import os
import time

from fungit.event.key import Key
from ..utils import create_profile
from ..style import Cursor, Symbol
from ..renderer import Renderer
from . import Box


class DynamicPromptBox(Box):

    close: bool = False
    count = 0
    process_symbol = [Symbol.graph_down[key]
                      for key in Symbol.graph_down.keys()]

    @classmethod
    def main(cls, title, prompt):
        f_w, f_h = os.get_terminal_size()

        cls.x = round(f_w / 4)
        cls.w = round(f_w / 2)
        _w = cls.w - 2
        _len = len(prompt)
        idx = 0
        cls.content = []
        if _len > _w:
            while idx + _w < _len:
                cls.content.append(prompt[idx:idx + _w])
                idx += _w
        cls.content.append(prompt[idx:])
        cls.h = len(cls.content) + 2
        cls.y = round(f_h / 2) - round(cls.h / 2)

        cls.box = create_profile(cls.x, cls.y, cls.w, cls.h, title=title)
        Renderer.now(cls.box)

        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        box_content = ''
        for idx, line in enumerate(cls.content):

            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line}'
                box_content += _line
                start_y += 1

        # cls.box_content += cls.process_symbol[cls.count % 4]
        # cls.count += 1
        cls.box_content = box_content + \
            cls.process_symbol[cls.count % len(cls.process_symbol)]
        start_time = time.time()
        while not cls.close:
            if time.time() - start_time > 0.2:
                cls.count += 1
                cls.box_content = box_content + \
                    cls.process_symbol[cls.count % len(cls.process_symbol)]
                start_time = time.time()
            # cls.render()
            Renderer.now(cls.box_content)

            while Key.has_key():
                key = Key.get()

                if key == 'q':
                    pass
                elif key == 'scape':
                    cls.close = True
                    break
                else:
                    continue

        cls.close = False
        cls.count = 0


class ConfirmBox():
    close: bool = False

    @classmethod
    def main(cls, title: str, prompt: str):
        f_w, f_h = os.get_terminal_size()

        # get box `x` and `(w)idth`
        cls.x = round(f_w / 4)
        cls.w = round(f_w / 2)

        line_len = cls.w - 2
        prompt_len = len(prompt)

        # process prompt string.
        idx: int = 0
        cls.content = []
        if prompt_len > line_len:
            while idx + line_len < prompt_len:
                cls.content.append(prompt[idx:idx + line_len])
                idx += line_len
        cls.content.append(prompt[idx:])

        # get box `y` and `(h)eigth`.
        cls.h = len(cls.content) + 2
        cls.y = round(f_h / 2) - round(cls.h / 2)

        # create box profile
        cls.box = create_profile(cls.x, cls.y, cls.w, cls.h, title=title)

        # create the content in box.
        start_x = cls.x + 1
        start_y = cls.y + 1

        cls.box_content = ''
        for idx, line in enumerate(cls.content):

            if idx < cls.h - 2:
                _line = f'{Cursor.to(start_y, start_x)}{line}'
                cls.box_content += _line
                start_y += 1

        # render
        Renderer.now(cls.box, cls.box_content)

        # listen key
        is_confirm: bool = False
        while not cls.close:
            Key.clear()
            while Key.has_key():
                key = Key.get()

                if key == 'q':
                    # TODO
                    pass
                elif key == 'enter' or key == 'y' or key == 'Y':
                    cls.close = True
                    is_confirm = True
                    break
                elif key == 'scape':  # escape
                    cls.close = True
                    break
                else:
                    continue

        cls.close = False
        return is_confirm


class InputBox():
    pass
