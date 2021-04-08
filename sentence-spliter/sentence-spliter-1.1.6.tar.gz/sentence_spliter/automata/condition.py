# -*- coding:utf-8 -*-
# CREATED BY: bohuai jiang 
# CREATED ON: 2020/8/7 3:50 PM
# LAST MODIFIED ON: 2021/3/1 3:46 PM
# AIM:
from abc import ABC
from typing import List
import re

from .abc import Criteria
from .sequence import StrSequence, EnSequence
from .symbols import SYMBOLS
from .white_list import white_list


class IsEndState(Criteria):
    def __init__(self, symbols: dict):
        super(IsEndState, self).__init__('IsEndState', symbols)

    def accept(self, state: StrSequence) -> bool:
        return state.reach_right_end()


class IsEndSymbolCN(Criteria):
    def __init__(self, symbols: dict):
        super(IsEndSymbolCN, self).__init__('IsEndSymbolZH', symbols)
        self.empty = re.compile('\s')

    def is_zh(self, char: str):
        if '\u4e00' <= char <= '\u9fa5':
            return True

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['end_symbols'].match(state.current_value) and \
                not (self.symbols['en_dot'].match(state.next_value) or self.symbols['end_symbols'].match(
                    state.next_value)):
            return True
        if self.symbols['en_dot'].match(state.current_value):
            if self.is_zh(state.next_value) or self.empty.match(state.next_value):
                return True
        return False


class IsEndSymbolEN(Criteria):
    def __init__(self, symbols: dict):
        super(IsEndSymbolEN, self).__init__('IsEndSymbolEN', symbols)
        self.empty = re.compile('\s')
        self.number = re.compile('[0-9]')

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['end_symbols'].match(state.current_value) and \
                not (self.symbols['en_dot'].match(state.next_value) or self.symbols['end_symbols'].match(
                    state.next_value)):
            return True
        if self.symbols['en_dot'].match(state.current_value):

            if self.number.match(state.next_value):
                return False
            else:
                return True
        return False


class IsComma(Criteria):
    def __init__(self, symbols: dict):
        super(IsComma, self).__init__('IsComma', symbols)

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['comma'].match(state.current_value):
            return True
        return False


class IsBracketClose(Criteria):
    def __init__(self, symbols: dict):
        super(IsBracketClose, self).__init__('IsBracketClose', symbols)

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True
        if state.bracket_left <= state.bracket_right:
            state.reset_bracket()
            return True
        else:
            return False


class IsQuoteClose(Criteria):
    def __init__(self, symbols: dict):
        super(IsQuoteClose, self).__init__('IsQuoteClose', symbols)

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True

        if state.quota_en > 0:
            if (state.quota_en + state.quota_left) % 2 == 0:
                state.reset_quota()
                return True
            else:
                return False
        elif state.quota_left > 0:
            return False
        else:
            return True


class IsBookClose(Criteria):
    def __init__(self, symbols: dict):
        super(IsBookClose, self).__init__('IsBookClose', symbols)

    def accept(self, state: StrSequence) -> bool:
        # -- avoid endless loop -- #
        if state.reach_right_end():
            return True
        if state.book_left <= state.book_right:
            # state.reset_bookmark()
            return True
        else:
            return False


class IsLongSentence(Criteria):
    def __init__(self, symbols: dict, max_len: int = 128):
        super(IsLongSentence, self).__init__('IsLongSentence', symbols)
        self.max_len = max_len

    def accept(self, state: StrSequence) -> bool:
        if state.candidate_len > self.max_len:
            return True
        return False


class IsShortSentence(Criteria):
    def __init__(self, symbols: dict, min_len: int = 17, **kwargs):
        super(IsShortSentence, self).__init__('IsShortSentence', symbols, **kwargs)
        self.min_len = min_len

    def accept(self, state: StrSequence) -> bool:
        if state.candidate_len < self.min_len:
            return True
        return False


# --- space --- #

class IsSpace(Criteria):
    def __init__(self, symbols: dict):
        super(IsSpace, self).__init__('IsSpace', symbols)
        self.pattern = re.compile('\s')

    def accept(self, state: StrSequence) -> bool:
        if self.pattern.match(state.current_value):
            return True
        else:
            return False


class IsNextWithSpace(Criteria):
    def __init__(self, symbols: dict):
        super(IsNextWithSpace, self).__init__('IsNextWithSpace', symbols)
        self.pattern = re.compile('\s')

    def accept(self, state: StrSequence) -> bool:
        if self.pattern.match(state.next_value):
            return True
        return False


class IsNextWithEndQuota(Criteria):
    def __init__(self, symbols: dict):
        super(IsNextWithEndQuota, self).__init__('IsNextWithQuota', symbols)

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['quotation_right'].match(state.next_value):
            return True
        elif self.symbols['quotation_en'].match(state.next_value):  # and (state.quota_en + state.quota_left)%2 != 0
            return True
        return False


# =========================== #
#      Special Condition      #
# =========================== #

class SpecialCondition(Criteria, ABC):
    pass


class IsRightQuotaZH(SpecialCondition):
    def __init__(self, index=0):
        super(IsRightQuotaZH, self).__init__('IsRightQuota', SYMBOLS)
        self.index = index

    def accept(self, state: StrSequence) -> bool:
        if self.index >= 0:
            index = min(state.v_pointer + self.index, state.length - 1)
        else:
            index = max(0, state.v_pointer + self.index)
        if self.symbols["quotation_right"].match(state[index]):
            state.reset_quota()
            return True
        return False


class IsLeftQuotaZH(SpecialCondition):
    def __init__(self, index=0):
        super(IsLeftQuotaZH, self).__init__('IsLeftQuotaZH', SYMBOLS)
        self.index = index

    def accept(self, state: StrSequence) -> bool:
        if self.index >= 0:
            index = min(state.v_pointer + self.index, state.length - 1)
        else:
            index = max(0, state.v_pointer + self.index)
        if SYMBOLS["quotation_left"].match(state[index]):
            return True
        return False


class IsLeftQuotaEn(SpecialCondition):
    def __init__(self, SYMBOLS: dict):
        super(IsLeftQuotaEn, self).__init__('IsListQuota', SYMBOLS)

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['quotation_en'].match(state.current_value) and state.quota_en % 2 != 0 or self.symbols[
            'quotation_left'].match(state.current_value):
            # state.v_pointer = max(0, state.v_pointer - 1)
            return True
        return False


class IsRightQuotaEn(SpecialCondition):
    def __init__(self, SYMBOLS: dict):
        super(IsRightQuotaEn, self).__init__('SpecialCondition', SYMBOLS)

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['quotation_en'].match(state.current_value) and state.quota_en % 2 == 0 or self.symbols[
            'quotation_right'].match(state.current_value):
            return True
        return False


class DialogueIsGreaterThanEN(SpecialCondition, ABC):
    def __init__(self, SYMBOLS: dict, length: int):
        super(DialogueIsGreaterThanEN, self).__init__('DialogueIsGreaterThanEN', SYMBOLS)
        self.length = length
        self.word_pattern = re.compile('^[a-zA-Z0-9]+')

    def accept(self, state: EnSequence) -> bool:
        if state.v_pointer < self.length:
            return False
        i = state.v_pointer
        n_quota = 0
        n_word = 0
        out = True
        while i >= 0:
            if self.symbols['all_quota'].match(state[i]):
                n_quota += 1
            if n_quota >= 2:
                out = False
            if self.word_pattern.match(state[i]):
                n_word += 1
                if n_word >= self.length:
                    break
            i -= 1

        return out


class IsListQuotaEN(SpecialCondition):
    def __init__(self, index=0):
        super(IsListQuotaEN, self).__init__('IsListQuotaEN', SYMBOLS)
        self.index = index

    def accept(self, state: StrSequence) -> bool:
        if self.index >= 0:
            index = min(state.v_pointer + self.index, state.length - 1)
        else:
            index = max(0, state.v_pointer + self.index)
        if self.symbols["quotation_en"].match(state[index]):
            return True
        return False


class IsLeftQuotaGreaterThan(SpecialCondition):
    '''
    左引号 重复次数大于一定值
    '''

    def __init__(self, theta: int = 1):
        super(IsLeftQuotaGreaterThan, self).__init__('IsLeftQuotaGreaterThan', SYMBOLS)
        self.theta = theta

    def accept(self, state: StrSequence) -> bool:
        if state.quota_left > self.theta:
            state.reset_quota()
            state.v_pointer -= 1
            return True


class IsRQuotaStickWithLQuota(SpecialCondition):
    '''
    右引号紧跟着左引号
    '''

    def __init__(self):
        super(IsRQuotaStickWithLQuota, self).__init__('IsRQuotaStickWithLQuota', SYMBOLS)

    def accept(self, state: StrSequence) -> bool:
        if self.symbols['quotation_right'].match(state.current_value) and \
                self.symbols['quotation_left'].match(state.next_value):
            return True
        return False


class WithSays(SpecialCondition):
    def __init__(self):
        super(WithSays, self).__init__('WithSays', SYMBOLS)
        self.pattern = re.compile('([他她](说|说道|笑道|道))+')

    def accept(self, state: StrSequence) -> bool:
        sentence = state[state.v_pointer + 1:15]
        if self.pattern.match(sentence):
            return True
        return False


class SpecialEnds(SpecialCondition):
    def __init__(self):
        super(SpecialEnds, self).__init__('SpecialEnds', SYMBOLS)
        self.pattern_pre = re.compile('([~～])')
        self.pattern_cur = re.compile('\s')

    def accept(self, state: StrSequence) -> bool:
        if self.pattern_pre.match(state.pre_value) and self.pattern_cur.match(state.current_value):
            return True
        else:
            return False


class NotInWhitelistDotEn(SpecialCondition):
    '''
    note: 大小写敏感
    '''

    def __init__(self):
        super(NotInWhitelistDotEn, self).__init__('NotInWhitelistDotEn', SYMBOLS)
        pattern = re.compile('\s')
        self.white_list = [pattern.sub('', v.strip()) for v in white_list.splitlines()]

    def accept(self, state: EnSequence) -> bool:
        if not state.current_value in ['.', '!']:
            return True
        else:
            for word in self.white_list:
                if not word:
                    continue
                word_token = state.tokenize(word)
                dots_pos = self.find_dot(word_token)
                word_len = len(word_token)
                atcual_word = ''.join(state[state.v_pointer - dots_pos:state.v_pointer])
                if dots_pos == word_len and word == atcual_word:
                    return False
                if dots_pos != word_len:
                    # case Mac. book 走搜索
                    while dots_pos > 0:
                        i = 0
                        whole_word = atcual_word + ''.join(
                            state[state.v_pointer:state.v_pointer + i + word_len - dots_pos])
                        if word == whole_word:
                            state.v_pointer = state.v_pointer + i + word_len - dots_pos
                            return False
                        dots_pos = self.find_dot(word_token, dots_pos + 1)
                        atcual_word = ''.join(state[state.v_pointer - dots_pos:state.v_pointer])
            return True

    def find_dot(self, str_list: List[str], start=0):
        for i, v in enumerate(str_list[start::]):
            if v in ['.', '!']:
                return i + start
        return -1
