import re
import math
import locale

class NumberUtils:

    def __init__(self):
        pass


    @staticmethod
    def format_thousands(value, format='{:,}'):
        ''' 10000 => 10,000'''
        if value:
            return format.format(value)
        return ''

    @staticmethod
    def padding_zero(number, digit): # type: (int, int) -> str
        ''' https://stackoverflow.com/questions/339007/nicest-way-to-pad-zeroes-to-a-string '''
        n = number
        if isinstance(number, int) or isinstance(number, float):
            n = str(number)

        return n.zfill(digit)

    @staticmethod
    def to_dollar(number):
        locale.setlocale(locale.LC_ALL, 'en_US')
        return locale.currency(number, grouping=True)

    @staticmethod
    def format(n, precision=1, current_unit='$'):
        '''https://stackoverflow.com/questions/3154460/python-human-readable-large-numbers '''
        # millnames = ['', ' Thousand', ' Million', ' Billion', ' Trillion']
        millnames = ['', 'k', 'm', 'b', 't']
        n = float(n)
        millidx = max(0, min(len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
        format = '%s{:.%df}{}' % (current_unit, precision)
        return format.format(n / 10 ** (3 * millidx), millnames[millidx])

    @staticmethod
    def number_to_digits(number, precision=1):
        ''' 1800 => 1.8k'''
        return NumberUtils.format(number, precision=precision, current_unit='')

    @staticmethod
    def digits_to_number(digits):
        ''' 2.3K =>2300'''
        millnames = {'k':1e3, 'm':1e6, 'b':1e9, 't':1e12}

        d = re.sub('[ ,.+]', '', digits.lower())
        m = 1
        if d[-1] in millnames:
            m = millnames.get(d[-1])
            d = d[:-1]
        d = float(d) * m
        return int(d)

    @staticmethod
    def to_readable_money(number):
        return NumberUtils.format_thousands(number, format='${:,.2f}')


if __name__ == '__main__':
    n = NumberUtils()


    print(NumberUtils.format_thousands(10000))
    print(NumberUtils.padding_zero(2,10))
    print(NumberUtils.to_dollar(10000))
    print(NumberUtils.format(10000))
    print(NumberUtils.to_readable_money(10000))

    print(NumberUtils.digits_to_number('1.5k'))
    print(NumberUtils.digits_to_number('1,200'))
    print(NumberUtils.digits_to_number('500+'))
    print(NumberUtils.digits_to_number('20k'))

