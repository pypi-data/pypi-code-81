class HuoYanError(Exception):
    """nothing"""


def _raise_huoyanerror_object():
    raise HuoYanError('Please use the right object')


def _raise_huoyanerror_parameter():
    raise HuoYanError('All parameters you pass in must have default values')


__version__ = '2.2.0'
__author__ = 'F.S'
__all__ = ["request", 'c', 'log_in', 'print', 'print_logo', 'python_plot',
           'spark_word']
