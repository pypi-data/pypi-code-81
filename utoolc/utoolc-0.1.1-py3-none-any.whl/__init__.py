__version__ = '0.1.1'
__author__ = 'LC'
__email__ = 'ahlc@sina.cn'

# 使用下面的 from * import * 导出去 才可被使用
from . import get_random
from .utils import utils
from .utils import start_to_end_time_consuming
from .utils import print_msg_to_log_model
from .easy import easy_say

# __all__
# Python __all__变量用法
# http://c.biancheng.net/view/2401.html
# Python模块__all__变量
# 除此之外，还可以借助模块提供的 __all__ 变量，该变量的值是一个列表，存储的是当前模块中一些成员（变量、函数或者类）的名称。
# 通过在模块文件中设置 __all__ 变量，当其它文件以“from 模块名 import *”的形式导入该模块时，该文件中只能使用 __all__ 列表中指定的成员。
# 也就是说，只有以“from 模块名 import *”形式导入的模块，当该模块设有 __all__ 变量时，只能导入该变量指定的成员，未指定的成员是无法导入的。
# 再次声明，__all__ 变量仅限于在其它文件中以“from 模块名 import *”的方式引入。也就是说，如果使用以下 2 种方式引入模块，则 __all__ 变量的设置是无效的。
# 1) 以“import 模块名”的形式导入模块。通过该方式导入模块后，总可以通过模块名前缀（如果为模块指定了别名，则可以使用模快的别名作为前缀）来调用模块内的所有成员（除了以下划线开头命名的成员）
# 2) 以“from 模块名 import 成员”的形式直接导入指定成员。使用此方式导入的模块，__all__ 变量即便设置，也形同虚设。
__all__ = ['easy_say', 'get_random', 'print_msg_to_log_model', 'utils', 'start_to_end_time_consuming', '__version__',
           '__author__', '__email__']
