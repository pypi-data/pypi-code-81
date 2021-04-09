import random
import string


# 从a-zA-Z0-9生成指定数量的随机字符
# 生成指定数量的随机字符
# @param counts 生成的数量
# @return 结果字符串
def get_random_str_with_counts(counts):
    return ''.join(random.sample(string.ascii_letters + string.digits, counts))
