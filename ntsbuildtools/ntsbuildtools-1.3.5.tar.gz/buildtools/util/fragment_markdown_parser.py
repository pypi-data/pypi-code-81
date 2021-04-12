# Copyright 2018 Tile, Inc.  All Rights Reserved.
#
# The MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from typing import List

from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer


# TODO This should actually be calculated. I think it should be 2x the size of the smallest reasonable Markdown token.
# Thinking about markdown heading markers... And the whitespace in nested lists
MIN_FRAG_SIZE = 20


def escape_url(raw):
    """
    Escape urls to prevent code injection craziness. (Hopefully.)
    """
    from urllib.parse import quote
    return quote(raw, safe='/#:')


class MarkdownRenderer(BaseRenderer):

    def __init__(self, *extras):
        self.listTokens = []
        super(MarkdownRenderer, self).__init__(*extras)

    def render_document(self, document):
        return ''.join([self.render(token) for token in document.children])

    def render_inner(self, token):
        if isinstance(token, block_token.List):
            if token.start:
                self.listTokens.append('1.')
            else:
                self.listTokens.append('-')

        # Render child tokens
        rendered_tokens = [self.render(child) for child in token.children]

        if isinstance(token, block_token.List):
            del (self.listTokens[-1])

        return ''.join(rendered_tokens)

    def render_strong(self, token):
        return f'__{self.render_inner(token)}__'

    def render_emphasis(self, token):
        return f'*{self.render_inner(token)}*'

    def render_inline_code(self, token):
        return f'`{self.render_inner(token)}`'

    def render_strikethrough(self, token):
        return f'~~{self.render_inner(token)}~~'

    def render_image(self, token):
        alt_text = self.render_inner(token)
        if token.title:
            return f'![{alt_text}]({token.src} "{token.title}")'
        else:
            return f'![{alt_text}]({token.src})'

    def render_link(self, token):
        target = escape_url(token.target)
        return f'[{self.render_inner(token)}]({target})'

    def render_auto_link(self, token):
        return escape_url(self.render_inner(token))

    def render_escape_sequence(self, token):
        return self.render_inner(token)

    def render_heading(self, token):
        return f"{'#' * token.level} {self.render_inner(token)}\n"

    def render_quote(self, token):
        return f'> {self.render_inner(token)}\n'

    def render_paragraph(self, token):
        return f'{self.render_inner(token)}\n'

    def render_block_code(self, token):
        return f'```{token.language}\n{self.render_inner(token)}```\n'

    def render_list(self, token):
        return self.render_inner(token)

    def render_list_item(self, token):
        prefix = ''.join(self.listTokens)
        return f'{prefix} {self.render_inner(token)}\n'

    def render_table(self, token):
        if hasattr(token, 'header'):
            header = token.children[0]
            header_inner_rendered = self.render_table_row(header, True)
        else:
            header_inner_rendered = ''
        body_inner_rendered = self.render_inner(token)
        return f'{header_inner_rendered}{body_inner_rendered}\n'

    def render_table_row(self, token, is_header=False):
        inner_rendered = ''.join([
            self.render_table_cell(child, is_header) for child in token.children
        ])
        if is_header:
            return f'{inner_rendered}||\n'
        else:
            return f'{inner_rendered}|\n'

    def render_table_cell(self, token, is_header=False):
        if is_header:
            return f'||{self.render_inner(token)}'
        else:
            return f'|{self.render_inner(token)}'

    def render_raw_text(self, token):
        return token.content

    @staticmethod
    def render_thematic_break(token):
        return '---\n'

    @staticmethod
    def render_line_break(token):
        return '\n'


class FragmentRenderer(MarkdownRenderer):
    def __init__(self, *extras, **kwargs):
        """
        Args:
            extras (list): allows subclasses to add even more custom tokens.
            kwargs (dict):
              * fragment_size: The size that fragments should be that are generated by this renderer. If unset, this
              will essentially re-render the Markdown as-is (without any fragmentation).
              * min_fragment_size: The minimum fragment size, which will effect the efficiency of the fragmentation as
              well as the readability. For maximum readability, leave the (default) minimum value. On the opposite
              side of things, to ensure that every fragment is as full as possible, set min_fragment_size =
              fragment_size.
        """
        self.listTokens = []
        super(FragmentRenderer, self).__init__(*extras)

        # Attributes that help with fragmentation logic.
        self.ideal_fragment_size = None
        self.min_fragment_size = None
        if 'fragment_size' in kwargs:
            self.set_fragment_size(kwargs['fragment_size'])
        if 'min_fragment_size' in kwargs:
            self.set_min_fragment_size(kwargs['min_fragment_size'])

        self.split_token_map = {
            # NOTE: The algorithm only splits on BlockTokens at this time
            'Heading':        self.split_token_inner,
            'CodeFence':      self.split_token_code_fence,
            'BlockCode':      self.split_token_code_fence,
            'SetextHeading':  self.split_token_simple,
            'Quote':          self.split_token_simple,
            'Paragraph':      self.split_token_paragraph,
            'List':           self.split_token_simple,
            'ListItem':       self.split_token_simple,
            'Table':          self.split_token_simple,
            'TableRow':       self.split_token_simple,
            'TableCell':      self.split_token_simple,
            'ThematicBreak':  self.split_token_simple,
            }

    def split_token(self, token, space_available):
        """Split a token into 'chunks'. Subsequent calls to the render_chunk(token) will return the chunks in
        sequential order. The subsequent chunks are split based on the `fragment_size` that we are targeting in this
        FragmentRenderer.

        :param token: The token being rendered (which will be split into 'chunks').
        :type token: Token
        :param space_available: The amount of space that is available to be rendered in this first fragment.
        :type space_available: int
        :return: The first 'chunk' of the token (other chunks are provided by invoking the render_next_chunk() method).
        :returns: str
        """
        return self.split_token_map[token.__class__.__name__](token, space_available)

    def _smallest_possible_token_of_type(self, token) -> int:
        copy = token.copy()
        copy.children = tuple()
        return len(self.render(copy))

    def _calc_split_token_inner_index(self, token, space_available) -> int:
        base_size = self._smallest_possible_token_of_type(token)
        return space_available - base_size

    def split_token_simple(self, token, space_available):
        content = self.render_inner(token)
        # 1. Get the first chunk based on space available.
        first_chunk = content[:space_available]
        token.chunks = [first_chunk]

        # 2. Any additional chunks will be split based on fragment_size.
        for start_index in range(space_available, len(content), self.ideal_fragment_size):
            next_chunk = content[start_index: start_index + self.ideal_fragment_size]
            token.chunks.append(next_chunk)

    def split_token_code_fence(self, token, space_available):
        # This is an easy example since it just has a single 'raw text' inside of it
        return self.split_token_inner(token, space_available)

    def split_token_paragraph(self, token, space_available):
        # The implication is that this paragraph needs to be split at 'space avialable'. This is another trivial example
        # since it can just do split_token_dumb
        return self.split_token_simple(token, space_available)

    def split_token_inner(self, token, space_available):
        # Render the token's children -- this is what we will be chunking/fragmenting.
        content = self.render_inner(token)

        # 1. Handle the first chunk based on space_available variable
        raw_first_chunk_size = self._calc_split_token_inner_index(token, space_available)
        raw_first_chunk_size -= 1  # Make space for an extra '\n' newline that is added in '_get_token_chunk'
        first_chunk_size = content.rfind('\n', 0, raw_first_chunk_size)
        if first_chunk_size < 1:
            # The token will not fit if split on a newline, so split arbitrarily instead...
            first_chunk_size = raw_first_chunk_size
        first_chunk = self._get_token_chunk(token, content, 0, first_chunk_size)
        token.chunks = [self.render(first_chunk)]

        # 2. Any additional chunks will be split based on fragment_size
        max_chunk_size = self._calc_split_token_inner_index(token, self.ideal_fragment_size)
        max_chunk_size -= 1  # Make space for an extra '\n' newline that is added in '_get_token_chunk'
        rendered_so_far = first_chunk_size
        while rendered_so_far < len(content):
            next_chunk_end_index = content.rfind('\n', 0, rendered_so_far + max_chunk_size)
            if next_chunk_end_index < 1:
                # The token will not fit if split on a newline, so split arbitrarily instead...
                next_chunk_end_index = rendered_so_far + max_chunk_size
            next_chunk = self._get_token_chunk(token, content, rendered_so_far, next_chunk_end_index)
            token.chunks.append(self.render(next_chunk))
            rendered_so_far = sum([len(_) for _ in token.chunks])

    @staticmethod
    def _get_token_chunk(token, token_rendered, start_index, end_index):
        ret = token.copy()
        ret.children = (span_token.RawText(token_rendered[start_index:end_index] + '\n'),)
        return ret

    def split(self, document):
        fragments = []
        while True:
            fragment = self.render_document_fragment(document)
            if fragment == '':  # render returns an empty string only when all tokens are rendered!
                break
            fragments.append(fragment)
        return fragments

    def render_document_fragment(self, document) -> str:
        """Render a fragment of the document. The fragment returned will be smaller than the user-specified
        fragment_size (if specified -- otherwise this will render the entire document).

        Essentially, the first call will return the 1st fragment, and subsequent calls will return the 2nd, 3rd, and so
        on.

        > NOTE: This code focuses on fragmenting 'BlockTokens' and does not focus on fragmenting 'SpanTokens'.

        :param document: The Document token to be rendered.
        :type document: mistletoe.Document
        :return: The rendered string that is the next fragment of the document.
        :rtype: str
        """
        rendered_tokens = []
        for token in document.children:
            '''
            Basically, this for loop has 2 possible paths: 
             1. handle a prior-partially rendered token.
             2. handle a new token.
            In the latter case, when handling a new token, there is a follow up step: 
             3. When the token won't fit in the current fragment empty partially render the token
            '''
            # If the child token has been chunked, just render the next chunk and continue.
            if self.has_been_partially_rendered(token):
                rendered_chunk = self.render_chunk(token)
                if self.has_more_chunks(token):
                    # When there is more than 1 chunk left in a child_token that has already been partially rendered,
                    # that implies that the chunk that was just rendered must have entirely filled the fragment buffer.
                    return rendered_chunk
                else:
                    # Else, there are no more chunks, so continue on to the next child_token in the document!
                    rendered_tokens.append(rendered_chunk)
                    continue

            # 2. Render the token!
            rendered_tokens.append(self.render(token))

            # 3. If the token fits, mark it as rendered and continue to the next child_token in the document.
            if self.fits_in_fragment(rendered_tokens):
                self.has_been_rendered(token, True)
                continue
            else:  # Stop rendering child tokens if we've "overfilled the fragment"
                # IMPORTANT: Make sure to 'pop' the token that doesn't fit!!
                rendered_tokens.pop()
                if not self.meets_min_frag_size(rendered_tokens):
                    available_space = self.ideal_fragment_size - sum([len(t) for t in rendered_tokens])
                    # Split the token into chunks, then call 'render_chunk' for the 1st chunk.
                    self.split_token(token, available_space)
                    rendered_tokens.append(self.render_chunk(token))
                break  # Stop rendering 'child tokens'!
        return ''.join(rendered_tokens)

    @staticmethod
    def render_chunk(token):
        if len(token.chunks) == 0:
            return ''
        return token.chunks.pop(0)  # pop method will update token.chunks list.

    def render(self, token) -> str:
        # Never do any rendering if the token 'has_been_rendered' already
        if self.has_been_rendered(token):
            return ''
        return super().render(token)

    def meets_min_frag_size(self, tokenz):
        if not self.min_fragment_size:
            return True
        return self._tokenz_len(tokenz) >= self.min_fragment_size

    def fits_in_fragment(self, tokenz):
        if not self.ideal_fragment_size:
            return True
        return self._tokenz_len(tokenz) <= self.ideal_fragment_size

    def set_min_fragment_size(self, min_fragment_size: int):
        """Set the minimum fragment size, which will effect the efficiency of the fragmentation as well as the
        readability. For maximum readability, leave the (default) minimum value. On the opposite side of things, to
        ensure that every fragment is as full as possible, set min_fragment_size = fragment_size.

        :param min_fragment_size: The minimum fragment size.
        :type min_fragment_size: int
        """
        if min_fragment_size < MIN_FRAG_SIZE:
            raise ValueError(f'Must have min_fragment_size larger than {MIN_FRAG_SIZE}.')
        self.min_fragment_size = min_fragment_size

    def set_fragment_size(self, fragment_size: int, min_fragment_size: int = None):
        if fragment_size < MIN_FRAG_SIZE:
            raise ValueError(f'Must have fragment_size larger than or equal to {MIN_FRAG_SIZE}.')
        self.ideal_fragment_size = fragment_size
        if min_fragment_size:
            self.set_min_fragment_size(min_fragment_size)
        else:
            half_fragment_size = fragment_size // 2 + 1
            self.set_min_fragment_size(half_fragment_size if half_fragment_size > MIN_FRAG_SIZE else MIN_FRAG_SIZE)

    @staticmethod
    def has_been_rendered(token, set_to: bool = None):
        if set_to is not None:
            token._is_rendered = set_to
        return getattr(token, '_is_rendered', False)

    @staticmethod
    def has_more_chunks(token):
        if FragmentRenderer.has_been_partially_rendered(token):
            return len(token.chunks) > 0

    @staticmethod
    def has_been_partially_rendered(token):
        return hasattr(token, 'chunks')

    @staticmethod
    def _tokenz_len(tokenz) -> int:
        """
        Take a token or a list of tokens and return the length.
        :param tokenz: A token or list of tokens.
        :type tokenz: List[Token] or Token
        :return: int
        :rtype:
        """
        if isinstance(tokenz, int):
            return tokenz
        elif isinstance(tokenz, str):
            return len(tokenz)
        elif isinstance(tokenz, List) and all([isinstance(token, str) for token in tokenz]):
            return sum([len(token) for token in tokenz])
        else:
            raise TypeError("Expected tokens argument to be one of int, str, or List[str]")
