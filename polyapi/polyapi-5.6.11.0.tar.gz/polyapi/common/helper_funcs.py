#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Содержит набор вспомогательных функций, использующихся в различных классах PPL.
Это различные декораторы, обработчики ошибок, методы логирования и тд.
"""

import logging
import time
from ..exceptions import *


def timing(func):
    """
    Используется как декоратор функций класса BusinessLogic для профилирования времени работы.
    :param func: декорируемая функция.
    """
    def timing_wrap(self, *args, **kwargs):
        """
        Непосредственно функция-декоратор.
        :param self: экземпляр класса BusinessLogic.
        """
        self.func_name = func.__name__
        try:
            logging.info('Exec func "{}"'.format(self.func_name))
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            self.func_timing = 'func "{}" exec time: {:.2f} sec'.format(self.func_name, (end_time - start_time))
            logging.info(self.func_timing)
            return result
        except SystemExit:
            logging.critical('Func "{}" failure with SystemExit exception!'.format(self.func_name))
            raise
    return timing_wrap


def raise_exception(bl_instance: 'BusinessLogic'):
    """
    Обёртка над функцией-генератором исключений.
    Сделано для того, чтобы каждый раз не передавать в функцию экземпляр класса "BusinessLogic".
    :param bl_instance: экземпляр класса BusinessLogic.
    """
    def wrap(exception: Exception, message: str, extend_message: str = '', code: int = 0, with_traceback: bool = True):
        """
        Непосредственно функция, генерирующая пользовательские исключения с заданным сообщением.

        :param exception: вид исключения, которое нужно сгенерировать. Например, ValueError, PolymaticaException...
        :param message: сообщение об ошибке.
        :param extend_message: расширенное сообщение об ошибке (не обязательно).
        :param code: код ошибки (не обязательно).
        :param with_traceback: нужно ли показывать traceback ошибки (по-умолчанию True).
        :return: (str) сообщение об ошибке, если работа с API происходит через Jupyter Notebook;
            в противном случае генерируется ошибка.
        """
        bl_instance.current_exception = message

        # записываем сообщение в логи
        # logging.error(msg, exc_info=True) аналогичен вызову logging.exception() - вывод с трассировкой ошибки
        # logging.error(msg, exc_info=False) аналогичен вызову logging.error(msg) - вывод без трассировки ошибки
        logging.error(message, exc_info=with_traceback)
        logging.info("APPLICATION STOPPED")

        # если работа с API происходит через Jupyter Notebook, то выведем просто сообщение об ошибке
        if bl_instance.jupiter:
            return message

        # если текущее исключение является наследником класса PolymaticaException, то генерируем ошибку Полиматики
        if issubclass(exception, PolymaticaException):
            raise exception(message, extend_message, code)

        # прочие (стандартные) исключения, по типу ValueError, IndexError и тд
        raise exception(message)
    return wrap


def log(message: str, level: str = 'info'):
    """
    Запись сообщения в логи.
    :param message: сообщение, записываемое в логи.
    :param level: уровень логирования; возможны варианты: 'debug', 'info', 'warning', 'error', 'critical'.
        По-умолчанию 'info'.
    """
    level = level.lower()
    if level not in ['debug', 'info', 'warning', 'error', 'critical']:
        level = 'info'
    if level == 'debug':
        logging.debug(message)
    elif level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
