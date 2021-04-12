from typing import List
import os, inspect


class MMM():
    """Maximum Matching Model，最大匹配法 """
    def __init__(self):
        self._words = set()
        self.load_dictionary()

    def load_dictionary(self):
        file_path = os.path.dirname(
            os.path.realpath(inspect.getfile(
                inspect.currentframe()))) + '/data/'

        with open(f'{file_path}/dict.txt') as fd, open(
                f'{file_path}/oov.txt') as fo:
            for line in fd.readlines() + fo.readlines():
                line = line.replace('\t', ' ')
                self._words.add(line.split(' ')[0].rstrip())

    def forward_segment(self, text: str) -> List:
        word_list = []
        i = 0
        while i < len(text):
            longest_word = text[i]
            for j in range(i + 1, len(text)):
                word = text[i:j]
                if word in self._words:
                    if len(word) > len(longest_word):
                        longest_word = word
            word_list.append(longest_word) 
            i += len(longest_word) 
        return word_list

    def backward_segment(self, text: str) -> List:
        word_list = []
        i = len(text) - 1
        while i >= 0:  
            longest_word = text[i]
            for j in range(i): 
                word = text[j:i + 1]
                if word in self._words:
                    if len(word) > len(longest_word):
                        longest_word = word
                        break
            word_list.insert(0, longest_word) 
            i -= len(longest_word)
        return word_list

    def count_single_char(self, word_list: List) -> int:     # 统计单字成词的个数
        return sum(1 for word in word_list if len(word) == 1)

    def bidirectional_segment(self, text: str)->List[str]:
        """双向最大匹配"""
        f = self.forward_segment(text)
        b = self.backward_segment(text)
        if len(f) < len(b):     # 词数更少优先级更高
            return f
        elif len(f) > len(b):
            return b
        else:
            if self.count_single_char(f) < self.count_single_char(
                    b):     # 单字更少优先级更高
                return f
            else:
                return b


if __name__ == '__main__':
    model = MMM()
    text = '好的。凭您的手机号是微信吗？我稍稍后加一下你吧，把相关的资料发给您。'
    print(model.forward_segment(text))
    # print(model.backward_segment(text))
    print(model.bidirectional_segment(text))
