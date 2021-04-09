import datetime
import random
import string


# get_now_time
# @return 当前日期时间
def get_now_time():
    return datetime.datetime.now()


# 获取间隔n天时间的最小时间(0点)和最大时间(23点59分59秒)-datetime.timedelta(days=1)可以处理天，datetime.timedelta(weeks=1)也可以处理周等
# @param  n,type,isFormat; n代表几天，可以正值(n天后)，可以负值(n天前),0代表今天 ;
#                          type取值有max和min,max代表输出当前时间最大时间，min代表输出当前时间最小时间;
#                          isFormat是否格式化输出，布尔值为True,格式化输出str类型时间,为False,不格式化输出，直接返回datetime类型时间。
# @return 符合要求的datetime格式日期
# 使用示例:
# print(to_n_datetime_max_min_time(2,"max", False))-2019-03-09 23:59:59.999999
# print(to_n_datetime_max_min_time(0,"min", False))-2019-03-07 00:00:00
# print(to_n_datetime_max_min_time(-1,"min", False))-2019-03-06 00:00:00
# print(to_n_datetime_max_min_time(-5, "max", True))-2019-03-02 23:59:59
def to_n_datetime_max_min_time(n, type, is_format):
    if type == "max":
        return_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=n), datetime.time.max)
    elif type == "min":
        return_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=n), datetime.time.min)
    if (is_format):
        return_time = return_time.strftime('%Y-%m-%d %H:%M:%S')
    return return_time


# 获取指定日期的时间的最小时间(0点)和最大时间(23点59分59秒)-datetime.timedelta(days=1)可以处理天，datetime.timedelta(weeks=1)也可以处理周等
# @param  diy_date,type,isFormat; diy_date代表指定的日期 ;
#                          type取值有max和min,max代表输出当前时间最大时间，min代表输出当前时间最小时间;
#                          isFormat是否格式化输出，布尔值为True,格式化输出str类型时间,为False,不格式化输出，直接返回datetime类型时间。
# @return 符合要求的datetime格式日期
# 使用示例:
# print(to_diy_date_datetime_max_min_time('20190309',"max", False))-2019-03-09 23:59:59.999999
# print(to_diy_date_datetime_max_min_time('20190307',"min", False))-2019-03-07 00:00:00
# print(to_diy_date_datetime_max_min_time('20190306',"min", False))-2019-03-06 00:00:00
# print(to_diy_date_datetime_max_min_time('20190302', "max", True))-2019-03-02 23:59:59
def to_diy_date_datetime_max_min_time(diy_date, type, is_format):
    this_datetime_date = datetime.date(year=int(diy_date[0:4]), month=int(diy_date[4:6]), day=int(diy_date[6:8]))
    if type == "max":
        return_time = datetime.datetime.combine(this_datetime_date, datetime.time.max)
    elif type == "min":
        return_time = datetime.datetime.combine(this_datetime_date, datetime.time.min)
    if (is_format):
        return_time = return_time.strftime('%Y-%m-%d %H:%M:%S')
    return return_time


# 传入一个datetime 获取其 年月日
# @param in_datetime 传入的datetime
# @return 输出格式为 2021,04,06
# 输出均是字符串
def get_year_month_day_from_datetime(in_datetime):
    this_year = in_datetime.year
    this_month = in_datetime.month
    this_day = in_datetime.day
    # 处理年
    this_year = get_real_year_month_day(this_year)
    # 处理月
    # print(len(str(this_month)))
    # 如果月份小于10 补零 让9变为09月
    this_month = get_real_year_month_day(this_month)
    # 处理日
    # print(len(this_day))
    # 如果日小于10 补零 让9变为09日
    this_day = get_real_year_month_day(this_day)
    return this_year, this_month, this_day


# 从a-zA-Z0-9生成指定数量的随机字符
# 生成指定数量的随机字符
# @param counts 生成的数量
# @return 结果字符串
def get_random_str_with_counts(counts):
    return ''.join(random.sample(string.ascii_letters + string.digits, counts))


# 返回符合要求的 年月日 格式
# @param in_ymd 进来的可能是 int 类型的 年 2021 月 4 日 6
# @return 返回出去的会是 字符串类型的 年 2021 月 04 日 06
def get_real_year_month_day(in_ymd):
    # 处理年月日
    # print(len(str(in_ymd)))
    # 如果月份小于10 补零 让9变为09月
    if len(str(in_ymd)) < 2:
        in_ymd = "0" + str(in_ymd)
    else:
        in_ymd = str(in_ymd)
    return in_ymd


# @param in_num 输入的字符或者数字或者 float
# @return 如果是浮点数 float 则直接返回其字符串格式
# 如果不是 float 则返回 None
def get_float_str(in_num):
    if is_float(in_num):
        return str(in_num)
    else:
        return None


# 判断"字符串"是否为数字
# @param s 要检测的字符串
# @return 处理结果 True是数字 False不是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# 判断字符串是否为 float
# @param num 要检测的num或者字符串num
# @return 如果包含两个（或以上）小数点，return False
# 否则（只剩一个或者没有小数点），去掉字符串中的小数点，然后判断是否全是由数字组成，是，return True，否，return False
# 返回True 代表为 float 返回False 代表不为 float
def is_float(num):
    string1 = str(num)
    if string1.count('.') > 1:  # 检测字符串小数点的个数
        # 如果小数点个数大于 1 肯定不是float
        return False
    elif string1.isdigit():  # 检测字符串是否只由数字组成，如果字符串只包含数字则返回 True 否则返回 False
        # 只是包含数字的话 就不是float
        return False
    else:
        new_string = string1.split(".")  # 按小数点分割字符
        first_num = new_string[0]  # 取分割完之后这个list的第一个元素
        # 判断负号的个数和first_num第一个元素是不是"-"，如果负号个数等于1并且firs_num第一个元素是"-"，则合法
        if first_num.count('-') == 1 and first_num[0] == '-':
            first_num = first_num.replace('-', '')
        if first_num.isdigit() and new_string[1].isdigit():
            return True
        else:
            return False


# 通过that_day_min和that_day_max 拿出所有的对应日 肯定不会跨年 跨月 所以不用理会
# @param that_day_min,that_day_max
# @return 返回 年 月 日的list集合
def get_days_list_from_day_min_to_day_max(that_day_min, that_day_max):
    min_this_year, min_this_month, min_this_day = get_year_month_day_from_datetime(that_day_min)
    max_this_year, max_this_month, max_this_day = get_year_month_day_from_datetime(that_day_max)
    days_list = []
    for i in range(int(min_this_day), int(max_this_day) + 1, 1):
        # print(i)
        days_list.append(get_real_year_month_day(i))
    return min_this_year, max_this_month, days_list


# 打印一条直线 用于分割日志 是log日志更加直观
# @param counts_tuple '-'的数量 传来的可变元组（Tuple） 如果不传或者传0 则使用默认值 95 如果传多值 则取第一个值
# @return 返回 加工好的直线
def print_a_line(*counts_tuple):
    counts = None
    # 不传
    if len(counts_tuple) == 0:
        counts = 95
    # 传1值 并且值是0
    elif len(counts_tuple) == 1 and counts_tuple[0] == 0:
        counts = 95
    # 传其他 多值的话 取第一个值
    else:
        counts = counts_tuple[0]
    a_line = '-' * counts
    print(a_line)
    return a_line
