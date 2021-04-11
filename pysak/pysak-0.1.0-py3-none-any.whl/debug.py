# 日志等级常量
INFO_LOG_LEVEL = "INFO"
WARNING_LOG_LEVEL = "WARNING"
ERROR_LOG_LEVEL = "ERROR"


# 输出日志 INFO级显示为绿色、WARNING级显示为黄色、ERROR级显示为红色
def showLog(msg="", title="", level=INFO_LOG_LEVEL, showEmptyLine=False):
    """
        # print("\033[1;32m 字体颜色：绿色\033[0m")
        # print("\033[1;33m 字体颜色：浅黄色\033[0m")
        # print("\033[1;31m 字体颜色：红色\033[0m")

    :param title: 标题
    :param msg: 信息
    :param level: 日志等级
    :param showEmptyLine: 是否显示空行
    :return:
    """
    # 根据日志等级更换颜色显示
    if level == INFO_LOG_LEVEL:
        prefix = "\033[1;32m"
    elif level == WARNING_LOG_LEVEL:
        prefix = "\033[1;33m"
    elif level == ERROR_LOG_LEVEL:
        prefix = "\033[1;31m"

    suffix = "\033[0m"

    if title != "":
        print(f"{prefix}[ {level} ]: {title}{suffix}")
    else:
        print(f"{prefix}[ {level} ]: {msg}{suffix}")
        return True

    if msg != "":
        print(f"{prefix}{msg}{suffix}")

    if showEmptyLine:
        print()


# 关闭 InsecureRequestWarning
def hideInsecureRequestWarning():
    """
    关闭 InsecureRequestWarning
    :return:
    """
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
