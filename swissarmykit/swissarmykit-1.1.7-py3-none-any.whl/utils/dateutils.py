import re
import time
import dateparser
from datetime import date, datetime, timedelta
import dateutil.relativedelta

class DateUtils:
    '''
    Ref: https://stackoverflow.com/questions/7479777/difference-between-python-datetime-vs-time-modules

    '''
    def __init__(self):
        pass


    @staticmethod
    def get_current_time_for_file(file_name=''):
        return file_name + str(time.strftime('%Y-%m-%d-%H-%M-%S'))


    @staticmethod
    def get_unix_timestamp(): # type: () -> int
        ''' Same as datetime.utcnow().timestamp() 13 digits'''
        return int(time.time() * 1000)

    @staticmethod
    def datetime_to_timestamp(datetime_str):
        return time.mktime(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').timetuple())

    @staticmethod
    def timestamp_to_datetime(timestamp):
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def get_unix_time_diff(seconds=0): # type: (int) -> int
        return DateUtils.get_unix_timestamp() - seconds * 1000

    @staticmethod
    def convert_unix_datetime(unix_time): # type: (int) -> datetime
        return datetime.utcfromtimestamp(unix_time)

    @staticmethod
    def get_mysql_datetime(): # type: () -> str
        return time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def datetime_second_diff(seconds=0):
        return datetime.now() - timedelta(seconds=seconds)

    @staticmethod
    def get_current_time_str():
        return str(datetime.now())[11:19]

    @staticmethod
    def convert_str_datetime(str, format='%b %d, %Y', only_date=False):
        ''' str => datetime obj
            format: Feb 04, 2018  =  %b %d, %Y
                    2/4/18        =  %m/%d/%y
                    '%H:%M:%S.%f
        '''

        if only_date:
            return datetime.strptime(str, format).date()
        return  datetime.strptime(str, format)

    @staticmethod
    def timedelta_str_divided_by(str, divided_by=1):
        seconds = DateUtils.convert_timedelta_str_to_object(str).total_seconds() // divided_by
        return timedelta(seconds=seconds)

    @staticmethod
    def convert_timedelta_str_to_object(s):
        '''
        :param s: str
        :return: timedelta
        '''
        if 'day' in s:
            m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
        else:
            m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
        return timedelta(**{key: float(val) for key, val in m.groupdict().items()})


    @staticmethod
    def convert_str_date(str, format='%b %d, %Y'):
        ''' 
            format='%b %d, %Y'
                    %Y:%m:%d        
        '''
        return DateUtils.convert_str_datetime(str, format=format, only_date=True)

    @staticmethod
    def get_diff_ago(ago, now=datetime.now()):
        ''' ago: 2 days ago, 4 months ago, 1 year ago'''

        diff = None
        ago_diff = int(ago.split(' ')[0])

        if 'day' in ago:
            diff = now - dateutil.relativedelta.relativedelta(days=ago_diff)
        elif 'hour' in ago:
            diff = now - dateutil.relativedelta.relativedelta(hours=ago_diff)
        elif 'min' in ago:
            diff = now - dateutil.relativedelta.relativedelta(minutes=ago_diff)
        elif 'month' in ago:
            diff = now - dateutil.relativedelta.relativedelta(months=ago_diff)
        elif 'year' in ago:
            diff = now - dateutil.relativedelta.relativedelta(years=ago_diff)
        elif 'week' in ago:
            diff = now - dateutil.relativedelta.relativedelta(weeks=ago_diff)

        return diff

    @staticmethod
    def generic_parse(str):
        '''     https://github.com/scrapinghub/dateparser

              print(DateUtils.generic_parse('1 hour ago'))
              print(DateUtils.generic_parse('1 day ago'))
              print(DateUtils.generic_parse('2020-06-25 18:20:38.532'))
        '''
        return dateparser.parse(str)


if __name__ == '__main__':
    d = DateUtils()

    # print(d.get_unix_timestamp())
    # print(type(DateUtils.convert_unix_datetime(1588264584)))
    # print(type(DateUtils.get_mysql_datetime()))
    # print(DateUtils.convert_str_date('Feb 04, 2018'))

    # print(datetime(2009, 5, 5))

    # print(DateUtils.generic_parse('1 hour ago'))
    # print(DateUtils.generic_parse('1 day ago'))
    print(type(DateUtils.generic_parse('2020-06-25 18:20:38.532')))