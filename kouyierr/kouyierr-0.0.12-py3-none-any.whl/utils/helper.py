import logging


class Helper:
    _logger = logging.getLogger(__name__)

    @staticmethod
    def format_currency(value):
        ''' Allow currency format with thousand separator and float double digit'''
        return "{:,.2f}".format(float(value)).replace(',', ' ')
