# from ..file_utils import checkout
# 이렇게 하면 ImportError: attempted relative import with no known parent package 발생
# 이렇게 시행하면 이 모듈이 __main__ 모듈이 되어서 제대로 파일을 검색할수 없ㄱ게됨

from ktextaug.file_utils import checkout
# checkout()

import os

cur_dir = os.path.curdir
print(cur_dir)
print(os.path.abspath("stopwords-ko.txt"))
# print(os.path.abspath())
path = os.path.join(os.path.curdir, "../stopwords-ko.txt")
print("path from cur dir", os.path.exists(path))


print(__package__)