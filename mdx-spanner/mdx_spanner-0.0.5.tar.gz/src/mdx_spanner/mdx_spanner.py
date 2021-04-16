from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

import copy
import re

class MdxSpannerExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        if 'table' in md.parser.blockprocessors:
            md.treeprocessors.add(
                'mdx_spanner',
                MdxSpannerTreeProcessor(self),
                '<inline'
            )

class MdxSpannerTreeProcessor(Treeprocessor):

    ROWSPAN_MARKER_PATTERN = re.compile(r'_[_^= ]*_')
    COLSPAN_MARKER_PATTERN = re.compile(r':?~~:?')
    EMPTY_PATTERN = re.compile(r'^\s*$')
    VALIGN = {
        '^': 'top',
        '=': 'middle',
        '_': 'bottom'
    }

    def __init__(self, extension_obj):
        super(MdxSpannerTreeProcessor, self).__init__()

    def run(self, root):
        tables = root.findall('.//table')
        for table in tables:
            tbody = table.find('tbody')

            for row in tbody:
                self._merge_row_cells(row)

            for col in zip(*tbody):
                self._merge_col_cells(col)

            for tr in tbody:
                for td in copy.copy(tr):
                    if td.get('remove'):
                        tr.remove(td)

    def _merge_row_cells(self, row):
        span_count = 1
        halign = 'left'
        for cell in row[::-1]:
            text = cell.text.strip()
            if self.COLSPAN_MARKER_PATTERN.search(text):
                span_count += 1
                cell.set('remove', 'true')

                begin_is_colon = text[0] == ':'
                end_is_colon = text[-1] == ':'

                if begin_is_colon and end_is_colon:
                    halign = 'center'
                elif end_is_colon:
                    halign = 'right'
            elif span_count > 1:
                cell.set('colspan', str(span_count))
                prev_style = cell.get('style') if cell.get('style') else ''
                cell.set('style', '{}text-align:{};'.format(prev_style, halign))
                span_count = 1

    def _merge_col_cells(self, col):
        span_count = 1
        valign = 'top'
        for cell in col[::-1]:
            text = cell.text.strip()
            if self.ROWSPAN_MARKER_PATTERN.search(text):
                span_count = 2
                cell.set('remove', 'true')

                valign_marker = text[1:-1]
                for key in self.VALIGN:
                    if key in valign_marker:
                        valign = self.VALIGN[key]
            elif self.EMPTY_PATTERN.search(text) and span_count > 1:
                span_count += 1
                cell.set('remove', 'true')
            elif span_count > 1:
                cell.set('rowspan', str(span_count))
                prev_style = cell.get('style') if cell.get('style') else ''
                cell.set('style', '{}vertical-align:{};'.format(prev_style, valign))
                span_count = 1

def makeExtension(*args, **kwargs):
    return MdxSpannerExtension(*args, **kwargs)
