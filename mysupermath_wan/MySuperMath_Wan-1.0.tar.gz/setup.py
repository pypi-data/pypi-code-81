from distutils.core import setup
setup(
    name='MySuperMath_Wan',   # 对外我们模块的名字
    version='1.0',      # 版本号
    description='这是第一个对外发布的模块，只有数学方法，测试哦',     #描述
    author='seele',        # 作者
    author_email='paaodo@163.com',
    py_modules=['MySuperMath_Wan.demo1', 'MySuperMath_Wan.demo2']          # 要发布的模块
)