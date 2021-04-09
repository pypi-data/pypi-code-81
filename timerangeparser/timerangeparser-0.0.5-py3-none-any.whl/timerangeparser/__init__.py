import datetime

from dateutil import rrule
from dateutil.parser import parse as date_parse
from dateutil.relativedelta import relativedelta

TIME_UNIT_MAPPER = {
    'Y': 'years',
    'M': 'months',
    'D': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds',
}


def date2datetime(x):
    return datetime.datetime.combine(x, datetime.datetime.min.time())


def delta2datetime(s):
    unit = s[-1]
    value = int(s[:-1])

    assert unit in TIME_UNIT_MAPPER, f'`{unit}`은 알 수 없는 시간 단위입니다.'

    delta_key = TIME_UNIT_MAPPER[unit]

    x = datetime.datetime.now() + relativedelta(**{delta_key: value})

    return x


def str2datetime(string):
    if string == 'now':
        string = '0s'
    elif string == 'today':
        string = '0D'
    elif string == 'tomorrow':
        string = '+1D'
    elif string == 'yesterday':
        string = '-1D'

    if string[-1] in TIME_UNIT_MAPPER:
        return delta2datetime(string)
    else:
        return date_parse(string)


def parse(string):
    begin, until, interval = string.split(':')

    begin = str2datetime(begin)
    until = str2datetime(until)

    freq_key = interval[-1]
    freq_val = interval[:-1]

    freq_val = int(freq_val)

    assert freq_val > 0, f'`interval`은 0보다 커야합니다. `{string}`으로 부터 추출한 `interval`은 {freq_val}입니다.'

    freq = {
        'Y': rrule.YEARLY,
        'M': rrule.MONTHLY,
        'D': rrule.DAILY,
        'h': rrule.HOURLY,
        'm': rrule.MINUTELY,
        's': rrule.SECONDLY,
    }[freq_key]

    time_list = rrule.rrule(freq, begin, until=until, interval=freq_val)

    if freq in {rrule.YEARLY, rrule.MONTHLY, rrule.DAILY}:
        time_list = [x.date() for x in time_list]
    else:
        time_list = list(time_list)

    return time_list
