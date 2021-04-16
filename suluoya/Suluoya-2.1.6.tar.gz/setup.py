import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Suluoya",
    version="2.1.6",
    author="Suluoya",
    author_email="1931960436@qq.com",
    maintainer='Suluoya',
    maintainer_email='1931960436@qq.com',
    description="A package called Suluoya.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests',  # 爬虫
                      'pandas',  # 数据分析
                      # 'beautifulsoup4', # 爬虫解析
                      # 'translators', # 翻译
                      # 'fuzzywuzzy', # 字符串模拟匹配
                      # 'ngender', # 性别
                      # 'MyQR', # 二维码
                      # 'pyforest', # 自动导入库
                      # 'wget', # 下载
                      #'urllib3',  # 爬虫
                      # 'you-get', # 下载视频
                      # 'goose3', # 文章提取
                      #'parsel',  # 爬虫解析
                      # 'pandas_profiling == 2.9.0', # 报告
                      # 'flashtext', # 关键词查找与替换
                      # 'textblob', # 英文情感
                      # 'snownlp', # 中文情感
                      'tqdm',  # 进度条
                      # 'pyttsx3', # 语音
                      # 'textract', # 提取文档信息
                      # 'newspaper3k', # 提取新闻
                      'baostock',  # 股票数据
                      'pretty_errors',  # 打印错误
                      'termcolor',  # 彩色打印
                      # 'fake_useragent', # 伪装
                      'lunar_python',  # 日期
                      # 'pandasgui', # 可视化界面
                      # 'sweetviz', # 数据分析
                      'pyecharts',  # 图
                      #'pygal',  # 矢量图
                      # 'cutecharts',  # 超可耐的图
                      'pysimplegui',  # gui
                      # 'zhon',  # 中文
                      # 'pdfplumber',  # pdf提取
                      # 'jieba',  # 分词
                      # 'python-docx',  # word提取
                      # 'zhconv',  # 繁体简体转换
                      ]
)
