from jutest.encode.encode import Encode


class EncodeChecker:
    def __init__(self):
        self.encodes = [
            Encode(
                name='html unescape',
                advice='Use `html.unescape` function',
                patterns=('&amp;', '&lt;', '&gt;', '&quot;', '&#x27;'),
            ),
            Encode(
                name='url encode',
                advice='Use `urllib.parse.urldecode` function',
                patterns=('%3D', '%26', '%2B'),
            ),
            Encode(
                name='unicode escape',
                advice='Use `.encode().decode("unicode_escape")` functions',
                patterns=('\\u',),
            ),
        ]

    def check(self, text: str) -> bool:
        return any(
            encode.check(text)
            for encode in self.encodes
        )

    def get_all(self, text: str) -> str:
        values = set()
        for encode in self.encodes:
            encode_values = encode.find_all(text)
            encode_values = (value[0] for value in encode_values)
            values.update(encode_values)
        # don't use `return str(values)` because
        # it uses __repr__() function instead of __str()__
        # that's why \\u0xxx chars shows with double \\
        # https://stackoverflow.com/questions/59460305/in-python-how-do-i-have-a-single-backslash-element-in-a-list
        return '[' + ','.join(values) + ']'
