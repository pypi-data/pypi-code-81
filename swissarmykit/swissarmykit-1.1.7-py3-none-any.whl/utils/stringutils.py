import re
from sys import getsizeof
import string
from html.parser import HTMLParser
import html as html_lib
import urllib.parse
import pandas as pd


class StringUtils():

    # https://stackoverflow.com/questions/21842885/python-find-a-substring-in-a-string-and-returning-the-index-of-the-substring/21844040
    @staticmethod
    def find_str(sub_str, string):
        return string.find(sub_str)

    # This used for print or log only. Remove characters outside of the BMP (emoji's) in Python 3
    # Ref: https://stackoverflow.com/questions/36283818/remove-characters-outside-of-the-bmp-emojis-in-python-3
    @staticmethod
    def get_valid_utf_8(text):
        # return ''.join(c for c in unicodedata.normalize('NFC', text) if c <= '\uFFFF')
        return StringUtils.remove_emoji(re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text))

    @staticmethod
    def get_valid_utf_8_v2(text):
        # return ''.join(c for c in unicodedata.normalize('NFC', text) if c <= '\uFFFF')
        return bytes(text, 'utf-8').decode('utf-8', 'ignore')

    @staticmethod
    def get_valid_text_for_excel(x):
        ''' UTF-8, not asscii'''
        return x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x

    @staticmethod
    def get_ascii_only(s):
        return s.encode('ascii', errors='ignore').decode('ascii')

    @staticmethod
    def remove_spaces_into_space(s):
        # https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string
        return ' '.join(s.split())
    
    @staticmethod
    def get_letter_only(s, space=False):
        if space:
            return ''.join(re.findall("[a-zA-Z ]+", s))
        return ''.join(re.findall("[a-zA-Z]+", s))

    @staticmethod
    def get_number_only(s):
        return ''.join(re.findall("[0-9]+", s))

    @staticmethod
    def print_table_in_console(lst, cols_width=None):
        from texttable import Texttable
        t = Texttable()
        if cols_width:
            t.set_cols_width(cols_width)
        t.add_rows(lst)
        print(t.draw())

    @staticmethod
    def crlf_to_lf(content):
        '''https://stackoverflow.com/questions/36422107/how-to-convert-crlf-to-lf-on-a-windows-machine-in-python'''
        return content.replace(b'\r\n', b'\n')

    @staticmethod
    def get_alphanumeric(s, space=False):
        if space:
            return ''.join(ch for ch in s if ch.isalnum() or ch.isspace())
        return ''.join(ch for ch in s if ch.isalnum())

    @staticmethod
    def java_string_hashcode(s):
        h = 0
        for c in s:
            h = (31 * h + ord(c)) & 0xFFFFFFFF
        return ((h + 0x80000000) & 0xFFFFFFFF) - 0x80000000

    @staticmethod
    def remove_emoji(text):
        '''\\xF0\\x9F\\x92\\x96'''
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    @staticmethod
    def remove_empty_line(text):
        return '\n'.join([l.rstrip() for l in text.splitlines() if l.strip()])

    @staticmethod
    def remove_line_where(text, where=None, where_texts=None):
        if where:
            return '\n'.join([l.rstrip() for l in text.splitlines() if where not in l])

        if where_texts:
            def exists(t, w_):
                for w in w_:
                    return w in t
                return False

            lst = []
            for l in text.splitlines():
                if not exists(t, where_texts):
                    lst.append(l)
            return '\n'.join(lst)

        raise Exception('Must have conditions')

    @staticmethod
    def print_pretty_json(parsed):
        import json
        print(json.dumps(parsed, indent=4, sort_keys=True))

    @staticmethod
    def get_list_char(upper_case=False):
        if upper_case:
            return [i for i in string.ascii_uppercase]
        return [i for i in string.ascii_lowercase]


    @staticmethod
    def strip_tags(html):
        ''' https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python '''
        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.fed = []

            def handle_data(self, d):
                self.fed.append(d)

            def get_data(self):
                return ''.join(self.fed)

        s = MLStripper()
        s.feed(html)
        return s.get_data()

    @staticmethod
    def copy(text):
        ''' Avoid use extra 'clipboard' lib '''
        df = pd.DataFrame([text])
        df.to_clipboard(index=False, header=False)

    @staticmethod
    def paste():
        from tkinter import Tk
        return Tk().clipboard_get()

    @staticmethod
    def clone(str):
        return (str + '.')[:-1]

    @staticmethod
    def binary_2_text(text):
        return text.decode('utf-8')

    @staticmethod
    def html_escape(text):
        return html_lib.escape(text)

    @staticmethod
    def html_unescape(text):
        return html_lib.unescape(text)

    @staticmethod
    def url_encode(text, plus=False):
        if plus:
            return urllib.parse.quote_plus(text)
        return urllib.parse.quote(text)

    @staticmethod
    def url_decode(text, plus=False):
        if plus:
            return urllib.parse.unquote_plus(text)
        return urllib.parse.unquote(text)

    @staticmethod
    def get_size(str):
        return getsizeof(str)


if __name__ == '__main__':
    pass