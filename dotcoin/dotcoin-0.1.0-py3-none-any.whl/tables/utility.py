from collections import Counter
from itertools import groupby

from beautifultable import BeautifulTable

from dotcoin.core.types import Table


def content_padding(header, body, width):
    header = header + [''] * (width - len(header))
    body = [row + [''] * (width - len(row)) for row in body]
    return header, body


def content_chunks(items, width, parse=None):
    if parse:
        items = map(parse, items)
    items = list(items)
    return [items[i:i + width] for i in range(0, len(items), width)]


def content_fold(columns: dict):
    return [[key] + row for key, rows in columns.items() for row in rows]


class KeyTable:
    def __init__(self, header: list, items: list):
        self.header = header
        self.items = items
        self.key = None
        self.parser = None
        self.content_header = None
        self.content_body = None

    def set_key(self, key):
        self.key = key

    def set_parser(self, parser):
        self.parser = parser

    def build(self, span):
        counter = Counter(map(self.key, self.items))
        width = min(max(counter.values()), span)

        groups = groupby(self.items, self.key)
        span = {key: content_chunks(items, width, self.parser) for key, items in groups}

        body = content_fold(span)
        content_header, content_body = content_padding(self.header, body, width + 1)

        self.content_header = content_header
        self.content_body = content_body

    def get_table(self):
        header = self.content_header
        body = self.content_body
        return Table(header, body)


def print_table(table: Table) -> str:
    echo = BeautifulTable(detect_numerics=False)
    echo.columns.header = table.header
    for row in table.content:
        echo.rows.append(row)

    echo.columns.alignment = BeautifulTable.ALIGN_LEFT
    echo.set_style(BeautifulTable.STYLE_BOX)
    echo.columns.header.separator = '═'
    echo.border.header_left = '╞'
    echo.border.header_right = '╡'
    echo.columns.header.junction = '╪'
    return str(echo)
