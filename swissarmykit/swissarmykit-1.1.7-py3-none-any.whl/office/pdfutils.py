from pprint import pprint
from tika import parser


class PDFUtils:

    def __init__(self, path, xmlContent=False):
        self.raw = parser.from_file(path, xmlContent=xmlContent)

    def get_content(self):
        return self.raw['content']

    def __str__(self):
        return self.raw['content']


if __name__ == '__main__':
    # p = PDFUtils('C:/Users/Will/Desktop/code/ai_/ztest/Largest_Investment_Consultants_List.pdf', True)
    p = PDFUtils('C:/Users/Will/Desktop/code/ai_/ztest/TOP-1000-Global_2016.pdf', True)
    print(p.get_content())


