# 红玲
# TODO:红玲
import os
from sty import fg, bg
from tqdm import tqdm


class Screen:
    def __init__(self, col_size = None, row_size = None):
        if col_size or row_size:
            self.column_size = col_size if col_size else 0
            self.row_size = row_size if row_size else 0
        else:
            sz = os.get_terminal_size()
            self.column_size = col_size if col_size else sz.columns
            self.row_size = row_size if row_size else sz.lines
        pass

    @staticmethod
    def clear_screen():
        os.system("clear")
        return


class Processor:
    def __init__(self, _total):
        self.pbar = tqdm(total=_total)

    def update(self, _derta):
        self.pbar.update(_derta)


class Formator:
    def __init__(self, col_size = None, row_size = None):
        self.screen = Screen(col_size, row_size)

    def in_column_center(self, _string):
        _string = _string.center(self.screen.column_size)
        return _string

    def in_row_center(self, _string):
        row_to_print = int(self.screen.row_size / 2)
        ret = ""
        for i in range(row_to_print):
            ret += "\n"
        ret += _string
        return ret

    def in_half_center(self, _string):
        string = self.in_column_center(_string)
        string = self.in_row_center(string)
        return string

    def in_all_center(self, _string):
        string = self.in_column_center(_string)
        string = self.in_row_center(string)
        string += self.in_row_center("")
        return string

    def in_all_left(self, _string):
        string = self.in_row_center("")
        string += self.in_row_center("")
        string += "\n" + _string
        return string


class Printer:
    def __init__(self):
        pass

    @staticmethod
    def in_fg_color(_string, _color_num):
        return fg(_color_num) + _string + fg.rs

    @staticmethod
    def in_bg_color(_string, _color_num):
        return bg(_color_num) + _string + bg.rs

    @staticmethod
    def p(_string):
        print(_string, end="")

    @staticmethod
    def pln(_string):
        print(_string)

    @staticmethod
    def pp(_string):  # processbar print
        tqdm.write(_string, end="")

    @staticmethod
    def ppln(_string):
        tqdm.write(_string)

    def multi_in_style(self, _multi_line_string, _style_object, _formator=None):
        line_list = _multi_line_string.split('\n')
        if len(line_list) > len(_style_object.colorlist):
            length_per_color = len(line_list) / len(_style_object.colorlist)
            if length_per_color == 0:
                length_per_color += 1
        else:
            length_per_color = len(_style_object.colorlist)

        ret =""
        if not _style_object.center:
            for i, line in enumerate(line_list):
                li_color = _style_object.colorlist[int(i / length_per_color)]
                ret += self.in_fg_color(line, li_color)+"\n"
        elif _style_object.center and not _style_object.cenrow:
            if _formator:
                for i, line in enumerate(line_list):
                    li_color = _style_object.colorlist[int(i / length_per_color)]
                    ret += _formator.in_column_center(self.in_fg_color(line, li_color)) +"\n"
            else:
                print("[-] There's no formator")
                exit(0)
        elif _style_object.center and _style_object.cenrow:
            if _formator:
                for i, line in enumerate(line_list):
                    li_color = _style_object.colorlist[int(i / length_per_color)]
                    ret += _formator.in_column_center(self.in_fg_color(line, li_color)) +"\n"
                ret = _formator.in_row_center(ret)
            else:
                print("[-] There's no formator")
                exit(0)
        return ret





if __name__ == "__main__":
    l = [1,2,3,4]
    for i, k in l:
        print(i,k)






