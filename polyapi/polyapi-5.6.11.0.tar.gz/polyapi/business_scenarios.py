#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Модуль работы с бизнес-сценариями Полиматики. Все реализованные в модуле методы заточены под Полиматику версии 5.6.
"""

# default lib
import os
import re
import time
import ast
import datetime
import requests
import pandas as pd
import json
import logging
from logging import NullHandler
from itertools import count
from typing import List, Dict, Tuple, Any, Union

# Polymatica imports

from . import error_handler
from .helper import Helper
from .authorization import Authorization
from .exceptions import *
from .executor import Executor
from .versions import VersionRedirect
from .common import timing, raise_exception, MULTISPHERE_ID, GRAPH_ID, CODE_NAME_MAP
from .commands import ManagerCommands, OlapCommands, GraphCommands
from .graph import Graph

# ----------------------------------------------------------------------------------------------------------------------

# настройка логирования
logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())

# ----------------------------------------------------------------------------------------------------------------------

# описание констант
OPERANDS = ["=", "+", "-", "*", "/", "<", ">", "!=", "<=", ">="]
ALL_PERMISSIONS = 31
MONTHS = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
          "Ноябрь", "Декабрь"]
WEEK_DAYS = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
PERIOD = {"Ежедневно": 1, "Еженедельно": 2, "Ежемесячно": 3}
WEEK = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3, "пятница": 4, "суббота": 5, "воскресенье": 6}
UPDATES = ["ручное", "по расписанию", "интервальное", "инкрементальное"]
ISO_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_POLYMATICA_VERSION = '5.6'

# ----------------------------------------------------------------------------------------------------------------------

class BusinessLogic:
    """
    Базовый класс, описывающий бизнес-сценарии использования Полиматики.
    Используемые переменные класса:

    # Версия сервера Полиматики; например, '5.6'
    self.polymatica_version

    # Полная версия сервера Полиматики; например, '5.6.14-ab9def0-7799123f-x86_64-centos'
    self.full_polymatica_version

    # Язык интерфейса. Задается во время авторизации. Возможно задать значения: "ru", "en", "de" или "fr".
    # По-умолчанию "ru"
    self.language

    # URL стенда Полиматики
    self.url

    # Флаг работы в Jupiter Notebook
    self.jupiter

    # Таймаут выполнения запросов
    self.timeout

    # Текст ошибки присвается в случае аварийного завершения работы; может быть удобно при работе в Jupiter Notebook
    self.current_exception

    # Логин пользователя Полиматики
    self.login

    # Для измерения времени работы функций бизнес-логики
    self.func_timing

    # Таблица команд и состояний
    self.server_codes

    # Идентификатор активного OLAP-модуля (мультисферы)
    self.multisphere_module_id

    # Идентификатор куба, соответствующего активному OLAP-модулю
    self.cube_id

    # Название куба, соответствующего активному OLAP-модулю
    self.cube_name

    # Список идентификаторов всех слоёв
    self.layers_list

    # Идентификатор активного слоя
    self.active_layer_id

    # Данные мультисферы в формате {"dimensions": "", "facts": "", "data": ""}
    self.multisphere_data

    # Общее число строк текущего (активного) OLAP-модуля
    self.total_row

    # Идентификатор активного модуля графиков
    self.graph_module_id

    # Идентификатор сессии
    self.session_id

    # Идентификатор (uuid) авторизации
    self.authorization_uuid

    # Класс, выполняющий HTTP-запросы
    self.exec_request

    # Объект выполнения команд модуля Manager
    self.manager_command

    # Объект выполнения команд модуля OLAP
    self.olap_command

    # Объект выполнения команд модуля Graph
    self.graph_command

    # Helper class
    self.h

    # Сохранённое имя функции для избежания конфликтов с декоратором
    self.func_name

    # Содержимое DataFrame
    self.df

    # Колонки DataFrame
    self.df_cols

    # Вспомогательный класс, перенаправляющий вызовы методы на нужные реализации (в зависимости от версии)
    self.version_redirect
    """
    def __init__(self, login: str, url: str, password: str = None, session_id: str = None,
                 authorization_id: str = None, timeout: float = 60.0, jupiter: bool = False, language: str = "ru"):
        """
        Инициализация класса BusinessLogic.
        :param login: логин пользователя Полиматика.
        :param url: URL стенда Полиматика.
        :param password: (необязательный) пароль пользователя Полиматика.
        :param session_id: (необязательный) идентификатор сессии.
        :param authorization_id: (необязательный) идентификатор авторизации.
        :param timeout: (необязательный) таймаут выполнения запросов, по умолчанию 60 секунд.
        :param jupiter: (необязательный) запускается ли скрипт из Jupiter Notebook, по-умолчанию False.
        """
        logger.info("BusinessLogic init")

        # версия сервера Полиматики; необходима для инвариантности методов
        # (т.е. в зависимости от этого параметра будет вызвана та или иная реализация метода в зависимости от версии)
        # по-умолчанию - версия Полиматики, с которой PPL имеет 100%-ную совместимость
        self.polymatica_version = DEFAULT_POLYMATICA_VERSION

        # полная версия сервера Полиматики; по-умолчанию мы её не заполняем, а потом подтягиваем во время авторизации
        # необходим для нужд внешних пользователей
        self.full_polymatica_version = str()

        # язык, возможны варианты: "ru", "en", "de" или "fr"
        self.language = language

        # URL стенда Полиматики
        self.url = url

        # флаг работы в Jupiter Notebook
        self.jupiter = jupiter

        # таймаут выполнения запросов
        self.timeout = timeout

        # текст ошибки присвается в случае аварийного завершения работы; может быть удобно при работе в Jupiter Notebook
        self.current_exception = None

        # логин пользователя Полиматики
        self.login = login

        # для измерения времени работы функций бизнес-логики
        self.func_timing = str()

        # таблица команд и состояний
        self.server_codes = Executor.get_server_codes(url)

        # хранит функцию-генератор исключений
        self._raise_exception = raise_exception(self)

        # переменные, хранящие текущую конфигурацию
        self.multisphere_module_id = str()   # идентификатор активного OLAP-модуля (мультисферы)
        self.cube_id = str()                 # идентификатор куба, соответствующего активному OLAP-модулю
        self.cube_name = str()               # название куба, соответствующего активному OLAP-модулю
        self.layers_list = list()            # список идентификаторов всех слоёв
        self.active_layer_id = str()         # идентификатор активного слоя
        self.multisphere_data = dict()       # данные мультисферы в формате {"dimensions": "", "facts": "", "data": ""}
        self.total_row = 0                   # общее число строк текущего (активного) OLAP-модуля
        self.graph_module_id = str()         # идентификатор активного модуля графиков

        # авторизация и получение идентификатора сессии и uuid авторизации
        if not session_id:
            # идентификатор сессии не задан; вызываем метод авторизации в любом случае,
            # независимо от наличия идентификатора авторизации
            self._login(login, password, url)
        else:
            # идентификатор сессии задан пользователем;
            # если идентификатор авторизации тоже задан пользователем - никаких лишних действий не делаем;
            # если же идентификатор авторизации не задан - получаем его
            if authorization_id:
                self.authorization_uuid = authorization_id
            else:
                self._login(login, password, url)
            self.session_id = session_id
            self._check_connection()

        # класс, выполняющий HTTP-запросы
        self.exec_request = Executor(self.session_id, self.authorization_uuid, url, timeout)

        # инициализация модуля Manager
        self.manager_command = ManagerCommands(
            self.session_id, self.authorization_uuid, url, self.server_codes, self.jupiter)

        # инициализация модуля Olap
        # ВАЖНО! OLAP модуль базируется на конкретной (активной) мультисфере, поэтому после переключения фокуса
        # на другую мультисферу (т.е. после того, как стала активна другая мультисфера)
        # необходимо заново инициализировать OLAP-модуль
        self._set_multisphere_module_id(self.multisphere_module_id)

        # инициализация модуля графиков
        # ВАЖНО! модуль графиков базируется на конкретном (активном) графике, поэтому после переключения фокуса
        # на другой график (т.е. после того, как стал активен другой график)
        # необходимо заново инициализировать этот модуль
        self._set_graph_module_id(self.graph_module_id)

        # инициализация модуля Graph
        self.graph_command = GraphCommands(
            self.session_id, self.authorization_uuid, url, self.server_codes, self.jupiter)

        # helper
        self.h = Helper(self)

        # сохранённое имя функции для избежания конфликтов с декоратором
        self.func_name = str()

        # если пользователь задан свой идентификатор сессии - получаем начальные данные
        if session_id:
            self._get_initial_config()

        # DataFrame content, DataFrame columns
        self.df, self.df_cols = str(), str()

        # вспомогательный класс, перенаправляющий вызовы методы на нужные реализации (в зависимости от версии)
        self.version_redirect = VersionRedirect(self)

    def __str__(self):
        # вернём ссылку на просмор сессии в интерфейсе
        url = self.url if self.url[-1] == '/' else '{}/'.format(self.url)
        return '{}login?login={}&session_id={}'.format(url, self.login, self.session_id)

    def _get_session_bl(self, sid: str) -> 'BusinessLogic':
        """
        Подключение к БЛ по заданному идентификатору сессии. Если идентификатор сессии пуст или он совпадает с
        текущей сессией, вернётся текущий экземпляр класса БЛ. В противном случае вернётся новый экземпляр класса.
        :param sid: 16-ричный идентификатор сессии.
        :return: (BusinessLogic) экземпляр класса BusinessLogic.
        """
        if not sid or sid == self.session_id:
            return self
        # пароль подключения передавать не нужно - он не будет использован при передаче идентификатора сессии
        return BusinessLogic(
            login=self.login,
            url=self.url,
            session_id=sid,
            authorization_id=self.authorization_uuid,
            timeout=self.timeout,
            jupiter=self.jupiter,
            language=self.language
        )

    def _set_multisphere_module_id(self, module_id: str):
        """
        Установка идентификатора новой активной мультисферы. После смены активной мультисферы происходит
        переинициализация объекта, исполняющего OLAP команды.
        :param module_id: идентификатор мультисферы.
        """
        self.multisphere_module_id = module_id
        self.olap_command = OlapCommands(
            self.session_id, self.multisphere_module_id, self.url, self.server_codes, self.jupiter)

    def _set_graph_module_id(self, module_id: str):
        """
        Установка идентификатора нового активного графика. После смены активного графика происходит
        переинициализация объекта, исполняющего команды модуля Graph.
        :param module_id: идентификатор активного модуля графиков.
        """
        self.graph_module_id = module_id
        self.graph_command = GraphCommands(
            self.session_id, self.graph_module_id, self.url, self.server_codes, self.jupiter)

    @timing
    def _login(self, login: str, password: str, url: str):
        """
        Авторизация на сервере Полиматики.
        :param login: (str) логин авторизации.
        :param password: (str) пароль авторизации.
        :param url: (str) URL-адрес стенда Полиматики.
        """
        try:
            self.session_id, self.authorization_uuid, polymatica_version = Authorization().login(
                user_name=login,
                password=password,
                url=url,
                server_codes=self.server_codes,
                language=self.language
            )
            self.full_polymatica_version = polymatica_version
            self.polymatica_version = self._get_polymatica_version(polymatica_version or str())
            logger.info('Login success')
        except AssertionError as ex:
            error_info = ex.args[0]
            if isinstance(error_info, dict):
                error_msg = "Auth failure: {}".format(error_info.get('message', str(ex)))
                return self._raise_exception(AuthError, message=error_msg, code=error_info.get('code', 0))
            else:
                return self._raise_exception(AuthError, "Auth failure: {}".format(error_info))
        except Exception as ex:
            return self._raise_exception(AuthError, "Auth failure: {}".format(ex))

    def _get_polymatica_version(self, polymatica_version: str) -> str:
        """
        Формирование мажорной версии Полиматики.
        """
        return '.'.join(polymatica_version.split('.')[0:2]) or DEFAULT_POLYMATICA_VERSION

    @timing
    def _check_connection(self, command_name: str = 'user_layer', state: str = 'get_session_layers'):
        """
        Проверка подключения посредством вызова заданной команды, показывающая, валиден ли пользовательский
        идентификатор сессии. Актуально только если пользователем был передан идентификатор сессии.
        Ничего не возвращает, но может сгенерировать исключение AuthError, если идентификатор невалиден.
        :param command_name: название команды.
        :param state: состояние команды.
        """
        # подготовка данных для отправки запроса
        headers = {'Accept': 'text/plain', 'Content-Type': 'application/json'}
        manager_commands = self.server_codes.get('manager', {}).get('command', {})
        if not manager_commands:
            return self._raise_exception(PolymaticaException, 'Manager commands not found!')
        data = {
            'state': 0,
            'session': self.session_id,
            'queries': [
                {
                    'uuid': self.authorization_uuid,
                    'command': {
                        'plm_type_code': manager_commands.get(command_name, {}).get('id'),
                        'state': manager_commands.get(command_name, {}).get('state', {}).get(state),
                    }
                }
            ]
        }
        # отправка запроса
        responce = requests.request(
            method='POST', url=self.url, headers=headers, data=json.dumps(data), timeout=self.timeout)
        responce_json = responce.json()
        # анализ ответа
        command_result = next(iter(responce_json.get('queries'))).get('command', {})
        if 'error' in command_result:
            error_data = command_result.get('error', {})
            error_code, error_msg = error_data.get('code', 0), error_data.get('message', '')
            if error_code == 270:
                # неверная сессия
                return self._raise_exception(AuthError, 'Session does not exist', code=error_code, with_traceback=False)
            # любая другая ошибка
            return self._raise_exception(PolymaticaException, error_msg, code=error_code, with_traceback=False)

    @timing
    def _get_initial_config(self):
        """
        Получение начальных данных (см. блок переменных, хранящих текущую конфигурацию в методе __init__).
        Актуально только если пользователем был передан идентификатор сессии.
        """
        # получаем список слоёв
        layers = self.get_layer_list()
        self.layers_list = [layer[0] for layer in layers]

        # получаем идентификатор активного слоя
        self.active_layer_id = self.get_active_layer_id()

        # получаем все модули на текущем слое (это и OLAP-модули, и модули графиков и тд)
        layer_settings = self.execute_manager_command(
            command_name="user_layer", state="get_layer", layer_id=self.active_layer_id)
        layer_modules = self.h.parse_result(result=layer_settings, key="layer", nested_key="module_descs") or list()

        # на текущем слое может быть несколько открытых модулей одного типа (несколько OLAP, несколько графиков и тд);
        # активным будем считать последний из них - поэтому проходим по реверсированному списку
        search_map = {'olap': True, 'graph': True}
        for module in reversed(layer_modules):
            module_type, module_uuid = module.get('type_id'), module.get('uuid')
            # получаем идентификатор активного OLAP-модуля и соответствующий ему идентификатор куба
            if search_map.get('olap') and module_type == MULTISPHERE_ID:
                self._set_multisphere_module_id(module_uuid)
                self.cube_id = module.get('cube_id')
                search_map['olap'] = False
            # получаем идентификатор модуля графиков
            if search_map.get('graph') and module_type == GRAPH_ID:
                self._set_graph_module_id(module_uuid)
                search_map['graph'] = False

        # получаем имя куба
        if self.cube_id:
            cubes_data = self.execute_manager_command(command_name="user_cube", state="list_request")
            cubes_list = self.h.parse_result(result=cubes_data, key="cubes") or list()
            for cube in cubes_list:
                if cube.get('uuid') == self.cube_id:
                    self.cube_name = cube.get('name')
                    break

        # обновляем общее количество строк, если открыт OLAP-модуль
        if self.multisphere_module_id:
            self.update_total_row()

    def execute_manager_command(self, command_name: str, state: str, **kwargs) -> Dict:
        """
        Выполнить любую команду модуля Manager.
        :param command_name: (str) название выполняемой команды.
        :param state: (str) название состояния команды.
        :param kwargs: дополнительные параметры, передаваемые в команду.
        :return: (Dict) ответ на запрашиваемую команду;
            если же передана неверная (несуществующая) команда, будет сгенерировано исключение ManagerCommandError.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Выполняем команду модуля Manager:
                bl_test.execute_manager_command(command_name="command_name", state="state")
                Например: bl_test.execute_manager_command(command_name="user_layer", state="get_session_layers").
        """
        try:
            # вызов команды
            logger.info("Starting manager command: command_name='{}' state='{}'".format(command_name, state))
            command = self.manager_command.collect_command("manager", command_name, state, **kwargs)
            query = self.manager_command.collect_request(command)

            # executing query and profiling
            start = time.time()
            result = self.exec_request.execute_request(query)
            end = time.time()
            return str(result).encode("utf-8") if command_name == "admin" and state == "get_user_list" else result
        except Exception as e:
            return self._raise_exception(ManagerCommandError, str(e))

    def execute_olap_command(self, command_name: str, state: str, **kwargs) -> Dict:
        """
        Выполнить любую команду модуля OLAP.
        :param command_name: (str) название выполняемой команды.
        :param state: (str) название состояния команды.
        :param kwargs: дополнительные параметры, передаваемые в команду.
        :return: (Dict) ответ на запрашиваемую команду;
            если же передана неверная (несуществующая) команда, будет сгенерировано исключение OLAPCommandError.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Выполняем команду модуля Manager:
                bl_test.execute_olap_command(command_name="command_name", state="state")
                Например: bl_test.execute_olap_command(command_name="fact", state="list_rq").
        """
        try:
            # проверки
            error_handler.checks(self, self.execute_olap_command.__name__)

            # вызов команды
            logger.info("Starting OLAP command: command_name='{}' state='{}'".format(command_name, state))
            command = self.olap_command.collect_command("olap", command_name, state, **kwargs)
            query = self.olap_command.collect_request(command)

            # executing query and profiling
            start = time.time()
            result = self.exec_request.execute_request(query)
            end = time.time()
            return result
        except Exception as e:
            return self._raise_exception(OLAPCommandError, str(e))

    def execute_graph_command(self, command_name: str, state: str, **kwargs) -> Dict:
        """
        Выполнить любую команду модуля Graph.
        :param command_name: (str) название выполняемой команды.
        :param state: (str) название состояния команды.
        :param kwargs: дополнительные параметры, передаваемые в команду.
        :return: (Dict) ответ на запрашиваемую команду;
            если же передана неверная (несуществующая) команда, будет сгенерировано исключение ManagerCommandError.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Выполняем команду модуля Graph:
                bl_test.execute_manager_command(command_name="command_name", state="state")
                Например: bl_test.execute_manager_command(command_name="user_layer", state="get_session_layers").
        """
        try:
            # вызов команды
            logger.info("Starting graph command: command_name='{}' state='{}'".format(command_name, state))
            command = self.graph_command.collect_command("graph", command_name, state, **kwargs)
            query = self.graph_command.collect_request(command)

            # executing query and profiling
            start = time.time()
            result = self.exec_request.execute_request(query)
            end = time.time()
            return result
        except Exception as e:
            return self._raise_exception(GraphCommandError, str(e))

    def update_total_row(self):
        """
        Обновить количество строк мультисферы. Ничего не возвращает.
        """
        result = self.execute_olap_command(
            command_name="view", state="get_2", from_row=0, from_col=0, num_row=1, num_col=1)
        self.total_row = self.h.parse_result(result, "total_row")

    @timing
    def get_cube(self, cube_name: str, num_row: int = 100, num_col: int = 100) -> str:
        """
        Получить идентификатор куба по его имени и открыть соответствующий OLAP-модуль.
        :param cube_name: (str) имя куба (мультисферы).
        :param num_row: (int) количество строк, которые будут выведены; по-умолчанию 100.
        :param num_col: (int) количество колонок, которые будут выведены; по-умолчанию 100.
        :return: идентификатор куба;
            если передано неверное имя куба, будет сгенерировано исключение CubeNotFoundError.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода:
                cube_id = bl_test.get_cube(cube_name="cube_name", num_row="num_row", num_col="num_col")
        """
        self.cube_name = cube_name

        # получение списка описаний мультисфер
        result = self.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_list = self.h.parse_result(result=result, key="cubes")

        # получить cube_id из списка мультисфер
        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except Exception as e:
            return self._raise_exception(CubeNotFoundError, str(e))

        # обновляем данные мультисферы
        self.multisphere_data = self._create_multisphere_module(num_row=num_row, num_col=num_col)
        self.update_total_row()

        return self.cube_id

    def get_multisphere_data(self, num_row: int = 100, num_col: int = 100) -> [Dict, str]:
        """
        Получить данные мультисферы
        :param self: экземпляр класса BusinessLogic
        :param num_row: количество отображаемых строк
        :param num_col: количество отображаемых столбцов
        :return: (Dict) multisphere data, format: {"dimensions": "", "facts": "", "data": ""}
        """
        # Получить список слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        # список слоев
        layers_list = self.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(layers_list):
                return layers_list
        try:
            # получить layer id
            self.layer_id = layers_list[0]["uuid"]
        except KeyError as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise
        except IndexError as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # инициализация модуля Olap
        self._set_multisphere_module_id(self.multisphere_module_id)

        # рабочая область прямоугольника
        view_params = {
            "from_row": 0,
            "from_col": 0,
            "num_row": num_row,
            "num_col": num_col
        }

        # получить список размерностей и фактов, а также текущее состояние таблицы со значениями
        # (рабочая область модуля мультисферы)
        query = self.olap_command.multisphere_data_query(self.multisphere_module_id, view_params)
        if self.jupiter:
            if "EXCEPTION" in str(query):
                return query
        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # multisphere data
        self.multisphere_data = {"dimensions": "", "facts": "", "data": ""}
        for item, index in [("dimensions", 0), ("facts", 1), ("data", 2)]:
            self.multisphere_data[item] = result["queries"][index]["command"][item]
        return self.multisphere_data

    def get_cube_without_creating_module(self, cube_name: str) -> str:
        """
        Получить id куба по его имени, без создания модуля мультисферы
        :param cube_name: (str) имя куба (мультисферы)
        :return: id куба
        """
        self.cube_name = cube_name
        result = self.execute_manager_command(command_name="user_cube", state="list_request")

        # получение списка описаний мультисфер
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if self.jupiter:
            if "ERROR" in str(cubes_list):
                return cubes_list

        # получить cube_id из списка мультисфер
        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError:
            return "Cube '%s' not found" % cube_name
        return self.cube_id

    @timing
    def move_dimension(self, dim_name: str, position: str, level: int = None) -> Dict:
        """
        Вынести размерность влево/вверх, либо убрать размерность из таблицы мультисферы.
        При передаче неверных параметров генерируется исключение ValueError.
        :param dim_name: (str) название размерности.
        :param position: (str) "left" (вынети влево) / "up" (вынести вверх) / "out" (вынести из таблицы).
        :param level: (int) 0, 1, ... (считается слева-направо для левой позиции, сверху-вниз для верхней размерности);
            обязательно должно быть задано при значении параметра position = "left" или position = "up";
            при значении параметра position = "out" параметр level игнорируется (даже если передано какое-то значение).
        :return: (Dict) результат OLAP-команды ("dimension", "move").
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Примеры вызова метода:
                bl_test.move_dimension(dim_name="dim_name", position="left", level=1)
                bl_test.move_dimension(dim_name="dim_name", position="up", level=1)
                bl_test.move_dimension(dim_name="dim_name", position="out")
        """
        # проверки
        try:
            position = error_handler.checks(self, self.func_name, position)
            # при выносе размерности влево/вверх уровень должен быть явно задан
            if position in [1, 2] and level is None:
                raise ValueError('При выносе размерности влево/вверх должен быть явно задан параметр "level"!')
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # получение id размерности
        self.multisphere_data = self.get_multisphere_data()
        dim_id = self.h.get_dim_id(self.multisphere_data, dim_name, self.cube_name)
        if self.jupiter and "ERROR" in str(dim_id):
            return dim_id

        self.update_total_row()
        # position: 0 - вынос размерности из таблицы, 1 - вынос размерности влево, 2 - вынос размерности вверх
        return self.execute_olap_command(
            command_name="dimension", state="move", position=position, id=dim_id, level=level if position != 0 else 0)

    @timing
    def get_measure_id(self, measure_name: str, need_get_data: bool = True) -> str:
        """
        Получить идентификатор факта по его названию.
        :param measure_name: название факта.
        :param need_get_data: нужно ли перед поиском нужного факта получать данные мультисферы.
            По-умолчанию нужно. Крайне не рекомендуется менять этот параметр без необходимости.
        :return: (str) идентификатор факта.
        """
        # получить словарь с размерностями, фактами и данными, если нужно;
        # если не нужно - подразумевается, что данные уже есть
        if need_get_data:
            self.get_multisphere_data()
        return self.h.get_measure_id(self.multisphere_data, measure_name, self.cube_name)

    @timing
    def get_dim_id(self, dim_name: str) -> str:
        """
        Получить идентификатор размерности по его названию.
        :param dim_name: (str) название размерности.
        :return: (str) идентификатор размерности.
        """
        # получить словарь с размерностями, фактами и данными
        self.get_multisphere_data()
        return self.h.get_dim_id(self.multisphere_data, dim_name, self.cube_name)

    @timing
    def get_measure_name(self, measure_id: str) -> str:
        """
        Получить название факта по его идентификатору.
        :param measure_id: (str) идентификатор факта.
        :return: (str) название факта.
        """
        try:
            result = self.h.get_measure_or_dim_name_by_id(measure_id, 'facts')
        except Exception as ex:
            return self._raise_exception(PolymaticaException, str(ex))
        return result

    @timing
    def get_dim_name(self, dim_id: str) -> str:
        """
        Получить название размерности по его идентификатору.
        :param dim_id: (str) идентификатор размерности.
        :return: (str) название размерности.
        """
        try:
            result = self.h.get_measure_or_dim_name_by_id(dim_id, 'dimensions')
        except Exception as ex:
            return self._raise_exception(PolymaticaException, str(ex))
        return result

    @timing
    def delete_dim_filter(self, dim_name: str, filter_name: str, num_row: int = 100) -> Dict:
        """
        Убрать выбранный фильтр размерности.
        Позволяет работать с любыми типами размерностей: верхними, левыми, не вынесенными в мультисферу.
        :param dim_name: (str) Название размерности.
        :param filter_name: (str) Название метки/фильтра.
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере.
        :return: (Dict) команда ("filter", "apply_data").
        """
        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # id размерности по её названию
        dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", dim_name)
        if self.jupiter and "ERROR" in str(dim_id):
            return dim_id

        result = self.execute_olap_command(
            command_name="filter", state="pattern_change", dimension=dim_id, pattern="", num=num_row)
        # получаем данные размерности (обрезаем все ненужные пробелы)
        filters_list = self.h.parse_result(result=result, key="data")
        filters_list = list(map(lambda item: (item or '').strip(), filters_list))
        # получаем индексы данных (0 - не отмечено, 1 - отмечено)
        filters_values = self.h.parse_result(result=result, key="marks")

        # проверяем, есть ли заданный пользователем фильтр в списке данных
        if filter_name not in filters_list:
            error_msg = 'Element "{}" is missing in the filter of specified dimension'.format(filter_name)
            return self._raise_exception(ValueError, error_msg, with_traceback=False)

        # если же заданный пользователем фильтр есть, то снимаем с него метку
        filters_values[filters_list.index(filter_name)] = 0

        # применяем
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        cmds = [command1, command2]
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(*cmds)

        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        self.update_total_row()
        return result

    @timing
    def clear_all_dim_filters(self, dim_name: str, num_row: int = 100) -> [Dict, bool]:
        """
        Очистить все фильтры размерности
        :param dim_name: (str) Название размерности
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере
        :return: (Dict) команда Olap "filter", state: "apply_data"
        """
        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data(num_row=num_row)

        # получение id размерности
        dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", dim_name)
        if self.jupiter:
            if "ERROR" in str(dim_id):
                return dim_id

        # Наложить фильтр на размерность (в неактивной области)
        # получение списка активных и неактивных фильтров
        result = self.execute_olap_command(command_name="filter",
                                           state="pattern_change",
                                           dimension=dim_id,
                                           pattern="",
                                           # кол-во значений отображается на экране, после скролла их становится больше:
                                           # num=30
                                           num=num_row)

        filters_values = self.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        if self.jupiter:
            if "ERROR" in str(filters_values):
                return filters_values

        # подготовить список для снятия меток: [0,0,..,0]
        length = len(filters_values)
        for i in range(length):
            filters_values[i] = 0

        # 1. сначала снять все отметки
        self.execute_olap_command(command_name="filter", state="filter_all_flag", dimension=dim_id)

        # 2. нажать применить
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def put_dim_filter(self, dim_name: str, filter_name: Union[str, List] = None, start_date: Union[int, str] = None,
                       end_date: Union[int, str] = None) -> [Dict, str]:
        """
        Сделать выбранный фильтр активным.
        Если в фильтрах используются месяцы, то использовать значения (регистр важен!):
            ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
            "Ноябрь", "Декабрь"]
        Если в фильтрах используются дни недели, то использовать значения (регистр важен!):
            ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        :param dim_name: (str) Название размерности
        :param filter_name: (str) Название фильтра. None - если нужно указать интервал дат.
        :param start_date: (int, datetime.datetime) Начальная дата
        :param end_date: (int, datetime.datetime) Конечная дата
        :return: (Dict) команда Olap "filter", state: "apply_data"
        """
        # много проверок...
        # Заполнение списка dates_list в зависимости от содержания параметров filter_name, start_date, end_date
        try:
            dates_list = error_handler.checks(self,
                                              self.func_name,
                                              filter_name,
                                              start_date,
                                              end_date,
                                              MONTHS,
                                              WEEK_DAYS)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получение id размерности
        dim_id = self.get_dim_id(dim_name)

        # Наложить фильтр на размерность (в неактивной области)
        # получение списка активных и неактивных фильтров
        result = self.h.get_filter_rows(dim_id)

        filters_list = self.h.parse_result(result=result, key="data")  # получить названия фильтров
        if self.jupiter:
            if "ERROR" in str(filters_list):
                return filters_list
        filters_values = self.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        if self.jupiter:
            if "ERROR" in str(filters_values):
                return filters_values

        try:
            if (filter_name is not None) and (filter_name not in filters_list):
                if isinstance(filter_name, List):
                    for elem in filter_name:
                        if elem not in filters_list:
                            raise ValueError("No filter '%s' in dimension '%s'" % (elem, dim_name))
                else:
                    raise ValueError("No filter '%s' in dimension '%s'" % (filter_name, dim_name))
        except ValueError as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # подготовить список для снятия меток: [0,0,..,0]
        length = len(filters_values)
        for i in range(length):
            filters_values[i] = 0

        # сначала снять все отметки
        self.execute_olap_command(command_name="filter",
                                  state="filter_all_flag",
                                  dimension=dim_id)

        # ******************************************************************************************************

        # подготовить список фильтров с выбранными отмеченной меткой
        for idx, elem in enumerate(filters_list):
            if isinstance(filter_name, List):
                if elem in filter_name:
                    filters_values[idx] = 1
            # если фильтр по интервалу дат:
            elif filter_name is None:
                if elem in dates_list:
                    filters_values[idx] = 1
            # если фильтр выставлен по одному значению:
            elif elem == filter_name:
                ind = filters_list.index(filter_name)
                filters_values[ind] = 1
                break

        # 2. нажать применить
        command1 = self.olap_command.collect_command("olap", "filter", "apply_data", dimension=dim_id,
                                                     marks=filters_values)
        command2 = self.olap_command.collect_command("olap", "filter", "set", dimension=dim_id)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        self.update_total_row()

        return result

    @timing
    def create_consistent_dim(self, formula: str, separator: str, dimension_list: List) -> [Dict, str]:
        """
        Создать составную размерность
        :param formula: (str) формат [Размерность1]*[Размерность2]
        :param separator: (str) "*" / "_" / "-", ","
        :param dimension_list: (List) ["Размерность1", "Размерность2"]
        :return: (Dict) команда модуля Olap "dimension", состояние: "create_union",
        """
        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # подготовка списка с id размерностей
        dim_ids = []
        for i in dimension_list:
            dim_id = self.h.get_measure_or_dim_id(self.multisphere_data, "dimensions", i)
            if self.jupiter:
                if "ERROR" in str(dim_id):
                    return dim_id
            dim_ids.append(dim_id)

        # заполнение списка параметров единицами (1)
        visibillity_list = [1] * len(dim_ids)

        return self.execute_olap_command(command_name="dimension",
                                         state="create_union",
                                         name=formula,
                                         separator=separator,
                                         dim_ids=dim_ids,
                                         union_dims_visibility=visibillity_list)

    @timing
    def switch_unactive_dims_filter(self) -> [Dict, str]:
        """
        Переключить фильтр по неактивным размерностям
        :return: (Dict) команда модуля Olap "dimension", состояние "set_filter_mode"
        """
        result = self.execute_olap_command(command_name="dimension", state="set_filter_mode")
        self.update_total_row()
        return result

    @timing
    def copy_measure(self, measure_name: str) -> str:
        """
        Копировать факт
        :param measure_name: (str) имя факта
        :return: id копии факта
        """
        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # Получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter:
            if "ERROR" in str(measure_id):
                return measure_id

        result = self.execute_olap_command(command_name="fact", state="create_copy", fact=measure_id)

        new_measure_id = self.h.parse_result(result=result, key="create_id")

        return new_measure_id

    @timing
    def rename_measure(self, measure_name: str, new_measure_name: str) -> Dict:
        """
        Переименовать факт.
        :param measure_name: (str) имя факта
        :param new_measure_name: (str) новое имя факта
        :return: (Dict) ответ после выполнения команды модуля Olap "fact", состояние: "rename"
        """
        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter:
            if "ERROR" in str(measure_id):
                return measure_id

        return self.execute_olap_command(command_name="fact", state="rename", fact=measure_id, name=new_measure_name)

    @timing
    def measure_rename_group(self, group: str, new_name: str, module: str = None, sid: str = None) -> Dict:
        """
        [ID-2992] Переименование группы фактов.
        :param group: (str) название/идентификатор группы фактов, которую нужно переименовать.
        :param new_name: (str) новое название группы фактов; не может быть пустым.
        :param module: (str) название/идентификатор OLAP-модуля, в котором нужно переименовать группу фактов;
            если модуль указан, но такого нет - сгенерируется исключение;
            если модуль не указан, то берётся текущий (активный) модуль (если его нет - сгенерируется исключение).
        :param sid: (str) 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущая сессия.
        :return: (Dict) command_name="fact" state="rename".
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                group, new_name = "group_id_or_group_name", "new_name"
                bl_test.measure_rename_group(group=group, new_name=new_name)
            3. Вызов метода с передачей валидного sid:
                group, new_name, session_id = "group_id_or_group_name", "new_name", "valid_sid"
                bl_test.measure_rename_group(group=group, new_name=new_name, sid=session_id)
            4. Вызов метода с передачей невалидного sid:
                group, new_name, session_id = "group_id_or_group_name", "new_name", "invalid_sid"
                bl_test.measure_rename_group(group=group, new_name=new_name, sid=session_id)
                output: exception "Session does not exist".
            5. Вызов метода с передачей валидного идентификатора/названия модуля:
                group, new_name, module = "group_id_or_group_name", "new_name", "valid_module_id_or_valid_module_name"
                bl_test.measure_rename_group(group=group, new_name=new_name, module=module)
            6. Вызов метода с передачей невалидного идентификатора/названия модуля:
                group, new_name = "group_id_or_group_name", "new_name"
                module = "invalid_module_id_or_invalid_module_name"
                bl_test.measure_rename_group(group=group, new_name=new_name, module=module)
                output: exception "Module cannot be found by ID or name".
        """
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.measure_rename_group(group=group, new_name=new_name, module=module)

        # проверка нового имени на пустоту
        if not new_name:
            return self._raise_exception(
                ValueError, 'New name of measure group cannot be empty!', with_traceback=False)

        # получаем идентификатор указанного OLAP-модуля и получаем список его фактов
        module_id = self._get_olap_module_id(module)
        self._set_multisphere_module_id(module_id)
        measures_list = self._get_measures_list()

        # переименовать группу, если в мультисфере есть такая такая группа фактов
        query = str()
        for item in measures_list:
            item_id = item.get("id")
            if group == item.get("name") or group == item_id:
                query = self.execute_olap_command(command_name="fact", state="rename", fact=item_id, name=new_name)
                break

        # если же в мультисфере нет указанной группы фактов - выбрасываем исключение
        if not query:
            self._raise_measure_group_error(group)

        # снять выделение фактов
        self.execute_olap_command(command_name="fact", state="unselect_all")
        return query

    @timing
    def measure_remove_group(self, group: str, module: str = None, sid: str = None) -> Dict:
        """
        [ID-2992] Удаление группы фактов.
        :param group: (str) название/идентификатор группы фактов, которую нужно удалить.
        :param module: (str) название/идентификатор OLAP-модуля, в котором нужно удалить группу фактов;
            если модуль указан, но такого нет - сгенерируется исключение;
            если модуль не указан, то берётся текущий (активный) модуль (если его нет - сгенерируется исключение).
        :param sid: (str) 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущая сессия.
        :return: (Dict) command_name="fact", state="del".
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                group = "group_id_or_group_name"
                bl_test.measure_remove_group(group=group)
            3. Вызов метода с передачей валидного sid:
                group, session_id = "group_id_or_group_name", "valid_sid"
                bl_test.measure_remove_group(group=group, sid=session_id)
            4. Вызов метода с передачей невалидного sid:
                group, session_id = "group_id_or_group_name", "invalid_sid"
                bl_test.measure_remove_group(group=group, sid=session_id)
                output: exception "Session does not exist".
            5. Вызов метода с передачей валидного идентификатора/названия модуля:
                group, module = "group_id_or_group_name", "valid_module_id_or_valid_module_name"
                bl_test.measure_remove_group(group=group, module=module)
            6. Вызов метода с передачей невалидного идентификатора/названия модуля:
                group, module = "group_id_or_group_name", "invalid_module_id_or_invalid_module_name"
                bl_test.measure_remove_group(group=group, module=module)
                output: exception "Module cannot be found by ID or name".
        """
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.measure_remove_group(group=group, module=module)

        # получаем идентификатор указанного OLAP-модуля и получаем список его фактов
        module_id = self._get_olap_module_id(module)
        self._set_multisphere_module_id(module_id)
        measures_list = self._get_measures_list()

        # удалить группу, если в мультисфере есть такая такая группа фактов
        query = str()
        for item in measures_list:
            item_id = item.get("id")
            if group == item.get("name") or group == item_id:
                query = self.execute_olap_command(command_name="fact", state="del", fact=item_id)
                break

        # если же в мультисфере нет указанной группы фактов - выбрасываем исключение
        if not query:
            self._raise_measure_group_error(group)

        # снять выделение фактов
        self.execute_olap_command(command_name="fact", state="unselect_all")
        return query

    def _raise_measure_group_error(self, group_name: str):
        """
        Генерация исключения в случае, когда в мультисфере отсутствует заданная группа фактов.
        """
        msg_error = "Group <{}> not found".format(group_name)
        logger.exception("ERROR!!! {}".format(msg_error))
        logger.info("APPLICATION STOPPED")
        self.current_exception = msg_error
        if self.jupiter:
            return msg_error
        raise ValueError(msg_error)

    def _get_measures_list(self) -> List:
        """
            Получить список фактов мультисферы.
        """
        result = self.execute_olap_command(command_name="fact", state="list_rq")
        return self.h.parse_result(result, "facts")

    @timing
    def rename_dimension(self, dim_name: str, new_name: str) -> Dict:
        """
        Переименовать размерность, не копируя её.
        Переименовывать можно как вынесенную (влево/вверх), так и невынесенную размерность.
        :param dim_name: (str) название размерности, которую требуется переименовать.
        :param new_name: (str) новое название размерности.
        :return: (Dict) результат выполнения команды ("dimension", "rename").
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода: bl_test.rename_dimension(dim_name="dim_name", new_name="new_name")
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, new_name)
        except Exception as ex:
            return self._raise_exception(ValueError, str(ex))

        # получить id размерности и переименовать её
        dim_id = self.get_dim_id(dim_name)
        return self.execute_olap_command(command_name="dimension", state="rename", id=dim_id, name=new_name)

    @timing
    def change_measure_type(self, measure_name: str, type_name: str) -> Dict:
        """
        Поменять вид факта.
        :param measure_name: (str) название факта
        :param type_name: (str) название вида факта; принимает значения, как на интерфейсе:
            "Значение"
            "Процент"
            "Ранг"
            "Изменение"
            "Изменение в %"
            "Нарастающее"
            "ABC"
            "Среднее"
            "Количество уникальных"
            "Количество"
            "Медиана"
            "Отклонение"
            "Минимум"
            "Максимум"
            "UNKNOWN"
        :return: (Dict) результат OLAP-команды ("fact", "set_type")
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода: bl_test.change_measure_type(measure_name="measure_name", type_name="type_name")
                В случае, если были переданы некорректные данные, сгенерируется ошибка.
        """
        # Получить вид факта (id)
        measure_type = self.h.get_measure_type(type_name)
        if self.jupiter:
            if "ERROR" in str(measure_type):
                return measure_type

        # по имени факта получаем его идентификатор
        measure_id = self.get_measure_id(measure_name)

        # выбрать вид факта
        return self.execute_olap_command(command_name="fact", state="set_type", fact=measure_id, type=measure_type)

    @timing
    def export(self, path: str, file_format: str) -> [Tuple, str]:
        """
        Экспортировать загруженную мультисферу в файл.
        :param path: (str) путь, по которому файл будет сохранен
        :param file_format: (str) формат сохраненного файла: "csv", "xls", "json"
        :return (Tuple): file_name, path
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, file_format, path)
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # Экспортировать полученный результат
        self.execute_olap_command(
            command_name="xls_export",
            state="start",
            export_format=file_format,
            export_destination_type="local"
        )

        time.sleep(10)
        result = self.execute_olap_command(command_name="xls_export", state="check")
        file_name = self.h.parse_result(result=result, key="file_name")
        if self.jupiter and "ERROR" in str(file_name):
            return file_name

        # URL, по которому лежит файл экспортируемый файл: базовый URL/resources/файл
        file_url = self.url + "/" + "resources" + "/" + file_name

        # выполнить запрос
        try:
            r = self.exec_request.execute_request(params=file_url, method="GET")
        except Exception as e:
            return self._raise_exception(ExportError, str(e))

        # сохранить файл по указанному пути
        file_name = file_name[:-8].replace(":", "-")
        filePath = path + "//" + file_name

        # запись файла в указанную директорию
        try:
            with open(filePath, 'wb') as f:
                f.write(r.content)
        except IOError as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.exception("Creating path recursively...")
            os.makedirs(path, exist_ok=True)
            with open(filePath, 'wb') as f:
                f.write(r.content)

        # проверка что файл скачался после экспорта
        filesList = os.listdir(path)
        assert file_name in filesList, "File %s not in path %s" % (file_name, path)
        return file_name, path

    def _is_numeric(self, value: str) -> bool:
        """
        Проверка, является ли заданная строка числом.
        :param value: (str) строка для проверки.
        :return: (bool) True - строка является числом, False - в противном случае.
        """
        is_float = True
        try:
            float(value.replace(',', '.'))
        except ValueError:
           is_float = False
        return value.isnumeric() or is_float

    @timing
    def create_calculated_measure(self, new_name: str, formula: str) -> Dict:
        """
        Создать вычислимый факт. Элементы формулы должный быть разделеный ПРОБЕЛОМ!
        Список используемых операндов: ["=", "+", "-", "*", "/", "<", ">", "!=", "<=", ">="]

        Примеры формул:
        top([Сумма долга];1000)
        100 + [Больницы] / [Количество вызовов врача] * 2 + corr([Количество вызовов врача];[Больницы])

        :param new_name: (str) Имя нового факта
        :param formula: (str) формула. Элементы формулы должный быть разделеный ПРОБЕЛОМ!
        :return: (Dict) команда модуля Olap "fact", состояние: "create_calc"
        """
        # получить данные мультисферы
        self.get_multisphere_data()

        # преобразовать строковую формулу в список
        formula_lst = formula.split()
        # количество фактов == кол-во итераций
        join_iterations = formula.count("[")
        # если в названии фактов есть пробелы, склеивает их обратно
        formula_lst = self.h.join_splited_measures(formula_lst, join_iterations)

        # параметра formula
        output = ""
        opening_brackets = 0
        closing_brackets = 0
        try:
            for i in formula_lst:
                if i in ["(", ")", "not", "and", "or"]:
                    output += i
                    if i == "(":
                        opening_brackets += 1
                    if i == ")":
                        closing_brackets += 1
                    continue
                elif "total(" in i:
                    m = re.search(r'\[(.*?)\]', i)
                    total_content = m.group(0)
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", total_content[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure_id:
                            return measure_id
                    output += "total(%s)" % measure_id
                    continue
                elif "top(" in i:
                    # top([из чего];сколько)
                    m = re.search(r'\[(.*?)\]', i)
                    measure_name = m.group(0)[1:-1]
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                    if self.jupiter:
                        if "ERROR" in measure_id:
                            return measure_id

                    m = re.search(r'\d+', i)
                    int_value = m.group(0)

                    output += "top( fact(%s) ;%s)" % (measure_id, int_value)
                    continue
                elif "if(" in i:
                    message = "if(;;) не реализовано!"
                    logger.exception(message)
                    logger.info("APPLICATION STOPPED")
                    self.current_exception = message
                    if self.jupiter:
                        return self.current_exception
                    raise ValueError(message)
                elif "corr(" in i:
                    m = re.search(r'\((.*?)\)', i)
                    measures = m.group(1).split(";")
                    measure1 = measures[0]
                    measure2 = measures[1]
                    measure1 = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure1[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure1:
                            return measure1
                    measure2 = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure2[1:-1])
                    if self.jupiter:
                        if "ERROR" in measure2:
                            return measure2
                    output += "corr( fact(%s) ; fact(%s) )" % (measure1, measure2)
                    continue
                elif i[0] == "[":
                    # если пользователь ввел факт в формате [2019,Больница]
                    # где 2019 - элемент самой верхней размерности, Больница - название факта
                    if "," in i:
                        measure_content = i[1:-1].split(",")
                        elem = measure_content[0]
                        measure_name = measure_content[1]

                        # сформировать словарь {"элемент верхней размерности": индекс_элемнета}
                        result = self.execute_olap_command(command_name="view",
                                                           state="get_2",
                                                           from_row=0,
                                                           from_col=0,
                                                           num_row=1,
                                                           num_col=1)

                        top_dims = self.h.parse_result(result=result, key="top_dims")
                        if self.jupiter:
                            if "ERROR" in str(top_dims):
                                return top_dims
                        result = self.execute_olap_command(command_name="dim_element_list_data", state="pattern_change",
                                                           dimension=top_dims[0], pattern="", num=30)

                        top_dim_values = self.h.parse_result(result=result, key="data")
                        if self.jupiter:
                            if "ERROR" in str(top_dim_values):
                                return top_dim_values
                        top_dim_indexes = self.h.parse_result(result=result, key="indexes")
                        if self.jupiter:
                            if "ERROR" in str(top_dim_indexes):
                                return top_dim_indexes
                        top_dim_dict = dict(zip(top_dim_values, top_dim_indexes))

                        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                        if self.jupiter:
                            if "ERROR" in str(measure_id):
                                return measure_id

                        output += " fact(%s; %s) " % (measure_id, top_dim_dict[elem])
                        continue
                    measure_name = i[1:-1]
                    measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
                    if self.jupiter:
                        if "ERROR" in str(measure_id):
                            return measure_id
                    output += " fact(%s) " % measure_id
                    continue
                elif i in OPERANDS:
                    output += i
                    continue
                elif self._is_numeric(i):
                    output += i
                    continue
                else:
                    raise ValueError("Unknown element in formula: %s " % i)

            if opening_brackets != closing_brackets:
                raise ValueError("Неправильный баланс скобочек в формуле!\nОткрывающих скобочек: %s \n"
                                 "Закрывающих скобочек: %s" % (opening_brackets, closing_brackets))
        except Exception as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        result = self.execute_olap_command(command_name="fact",
                                           state="create_calc",
                                           name=new_name,
                                           formula=output,
                                           uformula=formula)

        return result

    def _get_scripts_description_list(self) -> 'json':
        """
        Получить описание всех сценариев.
        :return: (json) информация по каждому сценарию в формате JSON (список словарей).
        """
        script_data = self.execute_manager_command(command_name="script", state="list")
        return self.h.parse_result(script_data, "script_descs")

    @timing
    def get_scripts_list(self) -> 'json':
        """
        Возвращает список сценариев с их описанием.
        :return: (json) информация по каждому сценарию в формате JSON (список словарей).
        """
        return self.version_redirect.invoke_method('_get_scripts_description_list') or list()

    def _get_scenario_cube_ids(self, scenario_id: str) -> set:
        """
        Возвращает идентификаторы всех мультисфер, входящих в заданный сценарий.
        :param scenario_id: (str) идентификатор сценария.
        :return: (set) идентфикаторы мультисфер, входящих в заданный сценарий.
        """
        result = self.execute_manager_command(command_name="script", state="list_cubes_request", script_id=scenario_id)
        return set(self.h.parse_result(result, "cube_ids"))

    def _check_scenario_cubes_permission(self, scenario_id: str):
        """
        Проверка, обладает ли текущий пользователь админскими правами на все мультисферы, входящие в заданный сценарий.
        Если не обладает, то генерируется ошибка.
        :param scenario_id: (str) идентификатор сценария.
        """
        # получаем идентификаторы всех мультисфер, входящих в заданный сценарий
        script_cube_ids = self.version_redirect.invoke_method('_get_scenario_cube_ids', scenario_id=scenario_id)

        # получаем идентификаторы мультисфер, на которые текущий пользователь имеет админские права
        ms_permission_data = self.get_cube_permissions()
        ms_permission_ids = {item.get('cube_id') for item in ms_permission_data if item.get('accessible')}

        # собственно, сама проверка
        if script_cube_ids <= ms_permission_ids:
            return
        return self._raise_exception(
            RightsError, 'Not all multisphere used in a scenario are available', with_traceback=False)

    def _check_scenario_data(self, scenario_id: str, scenario_name: str) -> [str, str]:
        """
        Проверка данных сценария:
        1. Если задан идентификатор, но не задано имя - проверяем, что такой идентификатор реально есть и находим имя.
        2. Если задано имя, но не задан идентификатор - находим идентификатор.
        3. Если задано и имя, и идентификатор - проверяем соответствие имени и идентификатора сценария.
        Если какая-то проверка не пройдёт - сгенерируется ошибка ScenarioError.
        :return: (str) идентификатор сценария.
        :return: (str) название сценария.
        """
        # получаем данные по всем сценариям
        script_desc = self.get_scripts_list()

        # eсли задан идентификатор, но не задано имя - проверяем, что такой реально действительно есть и находим имя
        if (scenario_id is not None) and (scenario_name is None):
            scenario_name = self.h.get_scenario_name_by_id(script_desc, scenario_id)

        # eсли задано имя, но не задан идентификатор - находим идентификатор
        elif (scenario_id is None) and (scenario_name is not None):
            scenario_id = self.h.get_scenario_id_by_name(script_desc, scenario_name)

        # eсли задано и имя, и идентификатор - проверяем соответствие имени и идентификатора сценария
        elif (scenario_id is not None) and (scenario_name is not None):
            find_scenario_id = self.h.get_scenario_id_by_name(script_desc, scenario_name)
            if find_scenario_id != scenario_id:
                return self._raise_exception(ScenarioError, "ID или имя сценария некорректно!", with_traceback=False)

        return scenario_id, scenario_name

    def _get_session_layers(self) -> list:
        """
        Возвращает список слоёв сессии.
        :return: (list) список идентификаторо слоёв.
        """
        layers_result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        return self.h.parse_result(result=layers_result, key="layers")

    def _run_scenario_impl(self, **kwargs) -> Dict:
        """
        Запуск сценария.
        :return: (Dict) результат выполнения команды ("user_iface", "save_settings").
        """
        scenario_id = kwargs.get('scenario_id')

        # получить список идентификаторов слоев сессии до запуска сценария
        layers = self._get_session_layers()
        layers_ids = [layer.get('uuid') for layer in layers]

        # запустить сценарий
        self.execute_manager_command(command_name="script", state="run", script_id=scenario_id)

        # сценарий должен создать новый слой и запуститься на нем;
        # получаем список идентификаторов слоёв после запуска сценария
        new_layers = self._get_session_layers()
        new_layers_ids = [layer.get('uuid') for layer in new_layers]

        # сохраняем новый список слоёв
        self.layers_list = new_layers_ids

        # получить id слоя, на котором запущен наш сценарий
        target_layer = set(new_layers_ids) - set(layers_ids)
        sc_layer = next(iter(target_layer))

        # ожидание загрузки сценария на слое
        self.h.wait_scenario_layer_loaded(sc_layer)

        # обновить слои
        user_layers = self._get_session_layers()

        for layer in user_layers:
            layer_uuid = layer.get("uuid")

            # интересует только слой, на котором запущем сценарий
            if layer_uuid != sc_layer:
                continue

            # для случаев, когда "module_descs" - пустой список (пустой сценарий) - вернуть False
            if not layer.get("module_descs"):
                return False

            # извлекаем uuid первой мультисферы, сохраняем его и инициализируем модуль OLAP
            try:
                multisphere_module_id = layer["module_descs"][0]["uuid"]
            except IndexError:
                error_msg = "No module_descs for layer with id {}; layer data: {}".format(sc_layer, layer)
                return self._raise_exception(ScenarioError, error_msg)
            self._set_multisphere_module_id(multisphere_module_id)

            # сохраняем текущий слой как активный
            self.active_layer_id = layer_uuid

            # выбрать слой с запущенным скриптом
            self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=layer_uuid)
            self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=layer_uuid)

            # сохраняем интерфейсные настройки и обновляем общее количество строк
            settings = {"wm_layers2": {"lids": new_layers_ids, "active": sc_layer}}
            result = self.execute_manager_command(
                command_name="user_iface", state="save_settings", module_id=self.authorization_uuid, settings=settings)
            self.update_total_row()
            return True

    @timing
    def run_scenario(self, scenario_id: str = None, scenario_name: str = None, timeout: int = None) -> Dict:
        """
        Запустить сценарий и дождаться его загрузки. В параметрах метода обязательно нужно указать либо идентификатор
        сценария, либо его название. И то и то указывать не обязательно.
        Если по каким-то причинам невозможно дождаться загрузки выбранного сценария (не отвечает сервер Полиматики или
        сервер вернул невалидный статус), генерируется ошибка.
        :param scenario_id: (str) идентификатор (uuid) сценария (необязательное значение).
        :param scenario_name: (str) название сценария (необязательное значение).
        :return: (Dict) результат выполнения команды ("user_iface", "save_settings").
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода:
                scenario_id, scenario_name = "scenario_id or None", "scenario_name or None"
                result = bl_test.run_scenario(scenario_id=scenario_id, scenario_name=scenario_name)
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, scenario_id, scenario_name)
        except Exception as e:
            return self._raise_exception(ScenarioError, str(e))

        # если пользователь прокинул тайм-аут - отобразим это в логах в виде warning
        if timeout is not None:
            logger.warning('Using deprecated param "timeout" in "run_scenario" method!')

        # проверка данных сценария
        scenario_id, scenario_name = self._check_scenario_data(scenario_id, scenario_name)

        # проверка прав на сценарий (на все ли мультисферы, участвующие в сценарии, пользователь имеет права)
        self._check_scenario_cubes_permission(scenario_id)

        # запуск сценария в зависимости от версии Полиматики
        return self.version_redirect.invoke_method(
            '_run_scenario_impl', scenario_id=scenario_id, scenario_name=scenario_name)

    @timing
    def run_scenario_by_id(self, sc_id: str) -> Dict:
        """
        Запустить сценарий по по его идентификатору.
        :param sc_id: (str) идентификатор запускаемого сценария.
        :return: (Dict) Результат команды ("script", "run").
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода: result = bl_test.run_scenario_by_id(sc_id="scenario_id")
        """
        return self.execute_manager_command(command_name="script", state="run", script_id=sc_id)

    def _check_user_exists(self, user_name: str, users_data: list = None):
        """
        Проверка на существование пользователя с заданным именем (логином).
        Если пользователь не найден - генерируется ошибка.
        :param user_name: (str) имя (логин) пользователя.
        :param users_data: (list) список пользователей Полиматики; может быть не задан.
        """
        # получаем список пользователей
        if not users_data:
            users = self.execute_manager_command(command_name="user", state="list_request")
            users_data = self.h.parse_result(result=users, key="users")
        # поиск соответствия заданному логину
        users_data = users_data or []
        for user in users_data:
            if user.get('login') == user_name:
                return
        # если такого пользователя нет - генерируем ошибку
        return self._raise_exception(UserNotFoundError, 'User with login "{}" not found!'.format(user_name))

    @timing
    def run_scenario_by_user(self, scenario_name: str, user_name: str, units: int = 500, timeout: int = None) -> [str, str]:
        """
        Запустить сценарий от имени заданного пользователя и дождаться его загрузки. Внутри метода будет создана
        новая сессия для указанного пользователя, а после выполнения сценария эта сессия будет закрыта.
        В метод необходимо обязательно передать название сценария и имя пользователя.
        Если по каким-то причинам невозможно дождаться загрузки выбранного сценария (не отвечает сервер Полиматики или
        сервер вернул невалидный статус), генерируется ошибка.
        :param scenario_name: (str) название сценария.
        :param user_name: (str) имя пользователя, под которым запускается сценарий.
        :param units: (int) число выгружаемых строк мультисферы.
        :return: (Tuple) данные мультисферы (df) и данные о колонках мультсферы (df_cols).
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода:
                df, df_cols = bl_test.run_scenario_by_user(scenario_name="scenario_name", user_name="user_name")
        """
        # создаём новую сессию под указанным пользователем
        self._check_user_exists(user_name)
        sc = BusinessLogic(login=user_name, url=self.url)

        # если пользователь прокинул тайм-аут - отобразим это в логах в виде warning
        if timeout is not None:
            logger.warning('Using deprecated param "timeout" in "run_scenario_by_user" method!')

        # Получить список слоев сессии
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers = set()

        session_layers_lst = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(session_layers_lst):
                return session_layers_lst

        for i in session_layers_lst:
            layers.add(i["uuid"])

        # Получить данные по всем сценариям
        script_desc = self.get_scripts_list()

        # Получить id сценария
        script_id = sc.h.get_scenario_id_by_name(script_desc, scenario_name)
        if self.jupiter:
            if "ERROR" in script_id:
                return script_id

        # Запустить сценарий
        sc.execute_manager_command(command_name="script", state="run", script_id=script_id)

        # Сценарий должен создать новый слой и запуститься на нем
        # Получить список слоев сессии
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        # Получить новый список слоев сессии
        new_layers = set()

        session_layers_lst = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in session_layers_lst:
                return session_layers_lst

        for i in session_layers_lst:
            new_layers.add(i["uuid"])
        sc.layers_list = list(new_layers)

        # получить id слоя, на котором запущен наш сценарий
        target_layer = new_layers - layers
        sc_layer = next(iter(target_layer))

        # ожидание загрузки сценария на слое
        sc.h.wait_scenario_layer_loaded(sc_layer)

        # параметр settings, для запроса, который делает слой активным
        settings = {"Profile": {
            "geometry": {"height": None, "width": 300, "x": 540.3125,
                         "y": "center", "z": 780}}, "cubes": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 813}}, "users": {
            "geometry": {"height": 450, "width": 700, "x": "center",
                         "y": "center", "z": 788}},
            "wm_layers2": {"lids": list(new_layers),
                           "active": sc_layer}}

        session_layers = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layer_progress = sc.h.parse_result(result=session_layers, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layer_progress):
                return user_layer_progress

        # проверка, что слой не в статусе Running
        # список module_descs должен заполнится, только если слой находится в статусе Stopped
        for _ in count(0):
            start = time.time()
            for i in user_layer_progress:
                if (i["uuid"] == sc_layer) and (i["script_run_status"]["message"] == "Running"):
                    session_layers = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
                    user_layer_progress = sc.h.parse_result(result=session_layers, key="layers")
                    if self.jupiter:
                        if "ERROR" in str(user_layer_progress):
                            return user_layer_progress
                    time.sleep(5)
                end = time.time()
                exec_time = end - start
                if exec_time > 60.0:
                    error_msg = "ERROR!!! Waiting script_run_status is too long! Layer info: {}".format(i)
                    logger.exception(error_msg)
                    logger.info("APPLICATION STOPPED")
                    self.current_exception = error_msg
                    if self.jupiter:
                        return self.current_exception
                    raise ValueError(error_msg)
            break

        # обновить get_session_layers
        result = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")

        user_layers = sc.h.parse_result(result=result, key="layers")
        if self.jupiter:
            if "ERROR" in str(user_layers):
                return user_layers

        for i in user_layers:
            if i["uuid"] == sc_layer:
                # для случаев, когда "module_descs" - пустой список (пустой сценарий) - вернуть False
                if not i["module_descs"]:
                    return False
                try:
                    sc.multisphere_module_id = i["module_descs"][0]["uuid"]
                except IndexError:
                    logger.exception("No module_descs for layer id %s\nlayer data: %s", sc_layer, i)
                    logger.info("APPLICATION STOPPED")
                    self.current_exception = "No module_descs for layer id %s\nlayer data: %s" % (sc_layer, i)
                    if self.jupiter:
                        return self.current_exception
                    raise

                sc.active_layer_id = i["uuid"]
                # инициализация модуля Olap (на случай, если нужно будет выполнять команды для работы с мультисферой)
                sc.olap_command = OlapCommands(sc.session_id, sc.multisphere_module_id,
                                                             sc.url, sc.server_codes, sc.jupiter)

                # Выбрать слой с запущенным скриптом
                sc.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=i["uuid"])

                sc.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=i["uuid"])

                sc.execute_manager_command(command_name="user_iface", state="save_settings",
                                           module_id=self.authorization_uuid, settings=settings)

                sc.update_total_row()
                gen = sc.get_data_frame(units=units)
                self.df, self.df_cols = next(gen)
                sc.logout()

                return self.df, self.df_cols

    def _get_active_measure_ids(self, total_column: int = 1000) -> set:
        """
        Получение идентификаторов активных фактов (т.е. фактов, отображаемых в таблице мультисферы).
        :param total_column: общее количество колонок в мультисфере.
        :return: (set) идентификаторы активных фактов.
        """
        data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=total_column)
        top, measure_data = self.h.parse_result(data, "top"), dict()
        for item in top:
            if "fact_id" in str(item):
                measure_data = item
                break
        return {measure.get("fact_id") for measure in measure_data}

    def _prepare_data(self) -> Union[List, int, int, int, int]:
        """
        Подготовка данных для дальнейшего получения датафрейма:
        1. Формирование колонок мультисферы с учётом вынесенных верхних размерностей.
        2. Подготовка дополнительных данных (общее число колонок, число левых/верхних размерностей, число фактов).
        :return: (List) список, содержащий список колонок: [[column_1, ..., column_N], [column_1, ..., column_N], ... ];
            количество вложенных списов зависит от наличия верхних размерностей:
            1. Если верхних размерностей нет, то будет один вложенный список: [[column_1, ..., column_N]].
            2. Если вынесено K верхних размерностей, то будет (K + 1) вложенных списков.
        :return: (int) общее количество колонок (размерностей + фактов).
        :return: (int) количество верхних размерностей.
        :return: (int) количество левых размерностей.
        :return: (int) количество фактов.
        """
        # получаем общее количество колонок
        total_cols_result = self.execute_olap_command(
            command_name="view", state="get_2", from_row=0, from_col=0, num_row=1, num_col=1)
        total_cols = self.h.parse_result(total_cols_result, "total_col")

        # получаем количество левых и верхних размерностей
        dims_data_result = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        left_dims_count = len(self.h.parse_result(dims_data_result, 'left_dims') or [])
        top_dims_count = len(self.h.parse_result(dims_data_result, 'top_dims') or [])

        # получаем названия колонок
        columns_data_result = self.execute_olap_command(
            command_name="view", state="get_2", from_row=0, from_col=0, num_row=1, num_col=total_cols)
        columns_data = self.h.parse_result(columns_data_result, "data")

        # получаем число активных фактов
        measures = self._get_active_measure_ids(total_cols)
        measures_count = len(measures)

        # если нет верхних размерностей - дальше делать нечего, возвращаем все данные
        if top_dims_count == 0:
            return [columns_data[0]], total_cols, top_dims_count, left_dims_count, measures_count

        # если есть верхние размерности, но не левых - чутка корректируем данные:
        # 1. В последней записи в columns_data содержатся названия левых размерностей и фактов;
        #    Если нет левых размерностей, то данные содержат только названия фактов, что в данном случае неверно -
        #    теряется очерёдность данных; поэтому добавим пустое поле (фактически это означает, что нет размерности)
        # 2. Т.к. добавили пустой элемент - увеличиваем число колонок
        if top_dims_count and not left_dims_count:
            columns_data[-1].insert(0, '')
            total_cols += 1

        # функция-слайсер, обрезающая элементы, относящиеся к колонке "Всего"
        total_f = lambda item, t_cols=total_cols, m_count=measures_count: item[0: t_cols - m_count]

        # в противном случае преобразовываем колонки к нужному виду
        columns_result = [total_f(columns_data.pop())]
        for top_columns in reversed(columns_data):
            # срез нужен для обрезания колонки "Всего"
            current_data = total_f(top_columns)
            for i, column in enumerate(current_data):
                if not column:
                    current_data[i] = current_data[i - 1]
            columns_result.insert(0, current_data)
        return columns_result, total_cols, top_dims_count, left_dims_count, measures_count

    @timing
    def get_data_frame(self, units: int = 100, show_all_columns: bool = False, show_all_rows: bool = False):
        """
        Генератор, подгружающий мультисферу постранично (порциями строк). Подразумевается,
        что перед вызовом метода вся иерархия данных в мультисфере раскрыта (иначе будут возвращаться неполные данные).
        Важно: генерация строк не учитывает ни промежуточные итоги по выборкам (строка "Всего" на уровне иерархии),
        ни общие итоги (строка "Всего" в конце мультисферы, а также колонка "Всего" по фактам).
        :param units: (int) количество подгружаемых строк; по-умолчанию 100.
        :param show_all_columns: (bool) установка показа всех колонок датафрейма.
        :param show_all_rows: (bool) установка показа всех строк датафрейма.
        :return: (DataFrame, DataFrame) данные мультисферы, колонки мультисферы.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url", **args)
            2. Этап подготовки: открываем мультисферу, выносим размерности и др. операции
            3. Раскрываем всю иерархию данных: bl_test.expand_all_dims()
            4. Собственно, сам вызов метода:
                I вариант:
                    gen = bl_test.get_data_frame(units="units")
                    df, df_cols = next(gen)
                II вариант:
                    gen = bl_test.get_data_frame(units="units")
                    for df, df_cols in gen:
                        # do something
        """
        # формируем колонки мультисферы, получаем вспомогательные данные
        columns, total_cols, top_dims_count, left_dims_count, measures_count = self._prepare_data()
        df_cols = pd.DataFrame(columns)

        # вычисляем число запрашиваемых колонок
        # вычитание числа фактов в случае наличия верхних размерностей нужно для соответствия количества
        # данных и колонок (количество колонок меньше, т.к. обрезается итоговая колонка "Всего")
        num_col = total_cols - left_dims_count - measures_count if top_dims_count else total_cols - left_dims_count

        # настройки датафрейма
        if show_all_columns:
            pd.set_option('display.max_columns', None)
        if show_all_rows:
            pd.set_option('display.max_rows', None)

        # пока не обойдём всю мультисферу - генерируем данные
        start, total_row = 0, self.total_row
        while total_row > 0:
            total_row = total_row - units

            # получаем данные мультисферы (туда также будут включены колонки)
            result = self.execute_olap_command(
                command_name="view", state="get_2", from_row=start, from_col=0, num_row=units + 1, num_col=num_col)
            data = self.h.parse_result(result=result, key="data")

            # реально данные (без колонок) начинаются с индекса, который учитывает наличие верхних размерностей
            df = pd.DataFrame(data[top_dims_count + 1:], columns=columns)
            yield df, df_cols
            start += units
        return

    @timing
    def set_measure_level(self, measure_name: str, level: int) -> Dict:
        """
        Установить уровень расчета сложного факта (т.е. факта, имеющего вид, отличного от "Значение"). Актуально при
        наличии трех и более левых размерностей, т.е. когда для основной размерности есть как минимум две вложенных.
        По-умолчанию расчёт осуществляется по первому уровню вложенности.
        :param measure_name: (str) имя факта.
        :param level: (int) уровень расчета факта (1 - по-умолчанию, 2, 3, ...).
        :return: (Dict) результат выполнения команды ("fact", "set_level").
        """
        # провека значения уровня
        left_dims_count, _ = self._get_left_and_top_dims_count()
        try:
            error_handler.checks(self, self.func_name, level, left_dims_count)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # получить id факта
        measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
        if self.jupiter and "ERROR" in measure_id:
            return measure_id

        # выполнить команду: fact, state: set_level
        command1 = self.olap_command.collect_command(
            module="olap", command_name="fact", state="set_level", fact=measure_id, level=level)
        command2 = self.olap_command.collect_command("olap", "fact", "list_rq")
        query = self.olap_command.collect_request(command1, command2)

        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))
        return result

    @timing
    def set_measure_precision(self, measure_names: List, precision: List) -> [Dict, str]:
        """
        Установить Уровень расчета факта
        :param measure_names: (List) список с именами фактов
        :param precision: (List) список с точностями фактов
                                (значения должны соответствовать значениям списка measure_names)
        :return: (Dict) результат выполнения команды: user_iface, state: save_settings
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, measure_names, precision)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить словать с размерностями, фактами и данными
        self.get_multisphere_data()

        # получить id фактов
        measure_ids = []
        for measure_name in measure_names:
            measure_id = self.h.get_measure_or_dim_id(self.multisphere_data, "facts", measure_name)
            if self.jupiter:
                if "ERROR" in measure_id:
                    return measure_id
            measure_ids.append(measure_id)

        # settings with precision for fact id
        settings = {"factsPrecision": {}}
        for idx, f_id in enumerate(measure_ids):
            settings["factsPrecision"].update({f_id: str(precision[idx])})

        # выполнить команду: user_iface, state: save_settings
        return self.execute_manager_command(command_name="user_iface",
                                            state="save_settings",
                                            module_id=self.multisphere_module_id,
                                            settings=settings)

    @timing
    def _get_olap_module_id(self, module: str=str(), set_active_layer: bool=True) -> str:
        """
        Возвращает идентификатор OLAP-модуля.
        Если идентификатор модуля задан пользователем, то пытаемся найти его;
            в случае, если не найден - бросаем исключение.
        Если пользователем не задан идентификатор модуля, то возвращаем идентификатор текущего (активного) модуля;
            в случае, если его нет - бросаем исключение.
        :param module: название/идентификатор искомого модуля; если не задан пользователем, то None.
        :param set_active_layer: нужно ли обновлять идентификатор активного слоя (по-умолчанию нужно).
        :return: (str) uuid найденного OLAP-модуля.
        """
        if module:
            # ищем указанный пользователем модуль и сохраняем его идентификатор
            layer_id, module_id = self._find_olap_module(module)
            if not module_id:
                error_msg = 'Module "{}" not found!'.format(module)
                return self._raise_exception(OLAPModuleNotFoundError, error_msg, with_traceback=False)
            result_module_id = module_id
        else:
            # пользователем не задан конкретный модуль - возвращаем текущий активный идентификатор OLAP-модуля
            if not self.multisphere_module_id:
                error_msg = 'No active OLAP-modules!'
                return self._raise_exception(OLAPModuleNotFoundError, error_msg, with_traceback=False)
            result_module_id, set_active_layer, layer_id = self.multisphere_module_id, False, str()

        # обновляем идентификатор активного слоя
        if layer_id and set_active_layer:
            self.active_layer_id = layer_id

        return result_module_id

    @timing
    def clone_olap_module(self, module: str = None, sid: str = None) -> Union[str, str]:
        """
        [ID-2994] Создать копию указанного OLAP-модуля. Если модуль не указан, то копируется текущий OLAP-модуль.
        :param module: название/идентификатор клонируемого OLAP-модуля;
            если модуль указан, но такого нет - сгенерируется исключение;
            если модуль не указан, то берётся текущий (активный) модуль (если его нет - сгенерируется исключение).
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :return: (str) uuid нового модуля
        :return: (str) название нового модуля
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Открываем произвольный куб: bl_test.get_cube("cube_name").
                Этот шаг обязательно нужен, т.к. без открытого OLAP-модуля копировать будет нечего.
            3. Вызов метода без передачи sid:
                new_module_uuid, new_module_name = bl_test.clone_olap_module()
            4. Вызов метода с передачей валидного sid:
                sid = "valid_sid"
                new_module_uuid, new_module_name = bl_test.clone_olap_module(sid=sid)
            5. Вызов метода с передачей невалидного sid:
                sid = "invalid_sid"
                new_module_uuid, new_module_name = bl_test.clone_olap_module(sid=sid)
                output: exception "Session does not exist"
            6. Вызов метода с передачей идентификатора/названия модуля:
                module = "module_id_or_name"
                new_module_uuid, new_module_name = bl_test.clone_olap_module(module=module).
            7. Вызов метода с передачей идентификатора/названия модуля и сессии:
                module = "module_id_or_name"
                sid = "valid_sid"
                new_module_uuid, new_module_name = bl_test.clone_olap_module(module=module, sid=sid).
        """
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.clone_olap_module(module=module)

        # клонирование OLAP-модуля
        cloned_module_id = self._get_olap_module_id(module)
        result = self.execute_manager_command(command_name="user_iface",
                                              state="clone_module",
                                              module_id=cloned_module_id,
                                              layer_id=self.active_layer_id)

        # переключиться на созданную копию OLAP-модуля
        new_module_id = self.h.parse_result(result=result, key="module_desc", nested_key="uuid")
        self._set_multisphere_module_id(new_module_id)
        # self.update_total_row()

        # возвращаем идентификатор нового модуля и его название (название совпадает с исходным OLAP-модулем)
        return self.multisphere_module_id, self.cube_name

    @timing
    def set_measure_visibility(self, measure_names: Union[str, List], is_visible: bool = False) -> [List, str]:
        """
        Изменение видимости факта (скрыть / показать факт).
        Можно изменять видимость одного факта или списка фактов.
        :param measure_names: (str, List) название факта/фактов
        :param is_visible: (bool) скрыть (False) / показать (True) факт. По-умолчанию факт скрывается.
        :return: (List) список id фактов с изменной видимостью
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, is_visible)
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # список фактов с измененной видимостью
        m_ids = []

        # если передан один факт (строка)
        if isinstance(measure_names, str):
            m_id = self.get_measure_id(measure_name=measure_names)

            self.execute_olap_command(command_name="fact", state="set_visible", fact=m_id, is_visible=is_visible)
            m_ids.append(m_id)
            return m_ids

        # если передан список фактов
        for measure in measure_names:
            m_id = self.get_measure_id(measure_name=measure)
            if not m_id:
                logger.exception("No such measure name: %s", measure)
                continue
            self.execute_olap_command(command_name="fact", state="set_visible", fact=m_id, is_visible=is_visible)
            m_ids.append(m_id)
        return m_ids

    @timing
    def set_all_measure_visibility(self, is_visible: bool = True, multisphere_module_id: str = str()) -> List:
        """
        Показать/скрыть все факты мультисферы.
        ВАЖНО: скрыть вообще все факты мультисферы нельзя, поэтому, если пользователем была передана команда
        скрыть все факты мультисферы, то будут скрыты все факты, кроме самого первого.
        :param is_visible: скрыть (False) либо показать (True) факты. По-умолчанию факты показываются.
        :param multisphere_module_id: идентификатор OLAP-модуля;
            если модуль указан, но такого нет - сгенерируется исключение;
            если модуль не указан, то берётся текущий (активный) модуль (если его нет - сгенерируется исключение).
        :return: идентификаторы показанных/скрытых фактов (в зависимости от команды).
        """
        # проверка
        try:
            error_handler.checks(self, self.func_name, is_visible)
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # получаем идентификатор OLAP-модуля
        module_id = self._get_olap_module_id(multisphere_module_id)
        self._set_multisphere_module_id(module_id)

        # получаем данные мультисферы (в т.ч. список фактов)
        m_data = self.get_multisphere_data()
        ids = list()
        for i, measure in enumerate(m_data.get('facts', list())):
            # если выполняется скрытие фактов, то самый первый факт не трогаем,
            # т.к. в мультисфере должен остаться хотя бы один нескрытый факт
            if not is_visible and i == 0:
                continue
            m_id = measure.get('id')
            res = self.execute_olap_command(command_name="fact", state="set_visible", fact=m_id, is_visible=is_visible)
            ids.append(m_id)
        return ids

    @timing
    def sort_measure(self, measure_name: str, sort_type: str) -> [Dict, str]:
        """
        Сортировка значений факта.
        :param measure_name: (str) Название факта.
        :param sort_type: (int) "ascending"/"descending"/"off" (по возрастанию/по убыванию/выключить сортировку)
        :return: (Dict) результат команды ("view", "set_sort").
        """
        # проверки
        try:
            error_handler.checks(self, self.func_name, sort_type)
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # определяем тип сортировки
        sort_values = {"off": 0, "ascending": 1, "descending": 2}
        sort_type = sort_values[sort_type]

        # получить данные активных (вынесенных в колонки) фактов
        result = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=20, num_col=20)
        measures_data = self.h.parse_result(result=result, key="top")
        if self.jupiter and "ERROR" in str(measures_data):
            return measures_data

        # получить список всех фактов
        measures_list = []
        for i in measures_data:
            for elem in i:
                if "fact_id" in elem:
                    measure_id = elem["fact_id"].rstrip()
                    measures_list.append(self.get_measure_name(measure_id))

        # индекс нужного факта
        measure_index = measures_list.index(measure_name)
        return self.execute_olap_command(command_name="view", state="set_sort", line=measure_index, sort_type=sort_type)

    def _get_left_and_top_dims_count(self, level: int = None, position: int = None) -> [int, int]:
        """
        Возвращает количество левых и верхних размерностей мультисферы.
        Если передан параметр level, то также осуществляется проверка уровня левых/верхних размерностей:
        если level больше, чем количество раскрываемых (т.е. иерархических) размерностей - сгенерируется ошибка.
        Если передан параметр level, то должен быть передан и параметр position, и наоборот.
        :param level: (int) уровень размерности.
        :param position: (int) 1 - левые размерности, 2 - верхние размерности.
        :return: (int) число левых размерностей.
        :return: (int) число верхних размерностей.
        """
        # получаем данные
        dims_data_result = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        left_dims_count = len(self.h.parse_result(dims_data_result, 'left_dims') or [])
        top_dims_count = len(self.h.parse_result(dims_data_result, 'top_dims') or [])

        # проверки
        if level is not None and position is not None:
            # проверка на то, что есть хотя бы одна вынесенная размерность
            if left_dims_count == 0 and top_dims_count == 0:
                raise ValueError('No left/up dims!')

            # проверка на уровень
            checked_level = left_dims_count if position == 1 else top_dims_count
            # т.к. последняя размерность мультисферы не имеет возможности расширяться
            checked_level -= 1
            # а в проверке указано (checked_level - 1) т.к. индексацию ведём с нуля
            if level > checked_level - 1:
                if checked_level == 0:
                    error_msg = 'No dimensions available for expand!'
                else:
                    error_msg = '{} dimensions available for expand!'.format(checked_level)
                raise ValueError('Invalid level! {}'.format(error_msg))

        # вернём число левых и верхних размерностей
        return left_dims_count, top_dims_count

    @timing
    def unfold_all_dims(self, position: str, level: int, **kwargs) -> Dict:
        """
        Развернуть все элементы размерности до заданного уровня иерархии.
        :param position: (str) "left" / "up" (левые / верхние размерности).
        :param level: (int) 0, 1, 2, ... (считается слева-направо для левой размерности, сверху - вниз для верхней).
        :param num_row: (int) Количество строк, которые будут отображаться в мультисфере.
        :param num_col: (int) Количество колонок, которые будут отображаться в мультисфере.
        :return: (Dict) after request view get_hints
        """
        # проверки
        try:
            position = error_handler.checks(self, self.func_name, position, level)
            left_dims_count, top_dims_count = self._get_left_and_top_dims_count(level, position)
        except Exception as e:
            return self._raise_exception(ValueError, str(e))

        # формируем запрос на раскрытие узлов ...
        arrays_dict = []
        # для того, чтобы развернуть все узлы заданного уровня, нужно развернуть все узлы до заданного уровня
        # для этого цикл и нужен
        for i in range(0, level + 1):
            arrays_dict.append(self.olap_command.collect_command(
                module="olap", command_name="view", state="fold_all_at_level", position=position, level=i))
        query = self.olap_command.collect_request(*arrays_dict)

        # ... и исполняем его
        try:
            self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        # формируем запрос на показ хинтов ...
        hints_command = []
        if left_dims_count:
            hints_command.append(self.olap_command.collect_command(
                module="olap", command_name="view", state="get_hints", position=1, hints_num=100))
        if top_dims_count:
            hints_command.append(self.olap_command.collect_command(
                module="olap", command_name="view", state="get_hints", position=2, hints_num=100))
        query = self.olap_command.collect_request(*hints_command)

        # ... и исполняем его
        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        self.update_total_row()
        return result

    @timing
    def move_measures(self, new_order: List) -> [str, Any]:
        """
        Функция, упорядочивающая факты в заданной последовательности

        Пример: self.move_measures(new_order=["факт1", "факт2", "факт3", "факт4"])

        :param new_order: (List) список упорядоченных фактов
        :return: (str) сообщение об ошибке или об успехе
        """
        c = 0
        for idx, new_elem in enumerate(new_order):
            # get ordered measures list
            result = self.execute_olap_command(command_name="fact", state="list_rq")
            measures_data = self.h.parse_result(result=result, key="facts")
            if self.jupiter:
                if "ERROR" in str(measures_data):
                    return measures_data
            measures_list = [i["name"].rstrip() for i in measures_data]  # measures list in polymatica

            # check if measures are already ordered
            if (measures_list == new_order) and (c == 0):
                logger.warning("WARNING!!! Facts are already ordered!")
                return

            measure_index = measures_list.index(new_elem)
            # если индекс элемента совпал, то перейти к следующей итерации
            if measures_list.index(new_elem) == idx:
                continue

            # id факта
            measure_id = self.get_measure_id(new_elem)

            # offset
            measure_index -= c

            self.execute_olap_command(command_name="fact", state="move", fact=measure_id, offset=-measure_index)
            c += 1
        self.update_total_row()
        return "Fact successfully ordered!"

    @timing
    def set_width_columns(self, measures: List, left_dims: List, width: int = 890, height: int = 540) -> [Dict, str]:
        """
        Установить ширину колонок в текущем (активном) модуле. Под колонками подразумеваются как левые размерности,
        так и факты.
        :param measures: (List) список новых значений ширины фактов.
            ВАЖНО! Длина списка должна совпадать с количеством нескрытых фактов в мультисфере без учёта верхних
            размерностей. То есть:
                1. Если в мультисфере нет вынесенных вверх размерностей, то длина списка должна совпадать с
                количеством нескрытых фактов в мультисфере.
                2. Если в мультисфере есть вынесенные вверх размерности, то длина списка должна совпадать с
                количеством уникальных (не дублирующихся из-за верхних размерностей) нескрытых фактов в мультисфере.
        :param left_dims: (List) список новых значений ширины вынесенных влево размерностей.
            ВАЖНО! Длина списка должна совпадать с количеством реально вынесенных влево размерностей мультисферы!
        :param width: (int) ширина мультисферы.
        :param height: (int) высота мультисферы.
        :return: Команда ("user_iface", "save_settings").
        """
        result = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=20, num_col=20)

        # получить список левых размерностей
        left_dims_data = self.h.parse_result(result=result, key="left_dims")

        # получить список нескрытых фактов (без учёта верхних размерностей)
        measures_data = self.h.parse_result(result=result, key="top")
        measures_ids = set()
        for i in measures_data:
            for elem in i:
                if "fact_id" in elem:
                    measures_ids.add(elem["fact_id"].rstrip())

        # проверки
        try:
            error_handler.checks(self, self.func_name, measures, measures_ids, left_dims, left_dims_data)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        # сохраняем новые настройки
        settings = {
            "dimAndFactShow": True,
            "itemWidth": measures,
            "geometry": {"width": width, "height": height},
            "workWidths": left_dims
        }
        return self.execute_manager_command(
            command_name="user_iface", state="save_settings", module_id=self.multisphere_module_id, settings=settings)

    def _get_layers(self) -> Union[dict, str]:
        """
        Получает список слоёв в текущей сессии.
        Возвращает два параметра: список слоёв, сообщение об ошибке (если есть).
        """
        layers_data = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers = self.h.parse_result(result=layers_data, key="layers")
        if "ERROR" in str(layers):
            return set(), str(layers)
        return layers, str()

    def _get_profiles(self) -> Union[dict, str]:
        """
        Получение профилей.
        Возвращает два параметра: список профилей, сообщение об ошибке (если есть).
        """
        profiles_data = self.execute_manager_command(command_name="user_layer", state="get_saved_layers")
        layers_descriptions = self.h.parse_result(result=profiles_data, key="layers_descriptions")
        if "ERROR" in str(layers_descriptions):
            return dict(), str(layers_descriptions)
        return layers_descriptions, str()

    @timing
    def load_profile(self, name: str) -> Dict:
        """
        Загрузить профиль по его названию.
        :param name: (str) название нужного профиля
        :return: (Dict) user_iface, save_settings
        """
        # получаем начальные слои (т.е. те, которые уже были до загрузки профиля)
        layers_data, error = self._get_layers()
        if error and self.jupiter:
            return error
        layers = {layer.get('uuid') for layer in layers_data}

        # получаем сохранённые профили
        layers_descriptions, error = self._get_profiles()
        if error and self.jupiter:
            return error

        # получаем uuid профиля по интерфейсному названию; если такого нет - генерируем ошибку
        profile_layer_id = str()
        for item in layers_descriptions:
            if item.get("name") == name:
                profile_layer_id = item.get("uuid")
                break
        if profile_layer_id == "":
            return self._raise_exception(PolymaticaException, 'No such profile: {}'.format(name), with_traceback=False)

        # загружаем сохраненный профиль
        self.execute_manager_command(command_name="user_layer", state="load_saved_layer", layer_id=profile_layer_id)

        # получаем новое множество слоев сессии
        session_layers, error = self._get_layers()
        if error and self.jupiter:
            return error
        new_layers = {layer.get('uuid') for layer in session_layers}

        # получить id слоя, на котором запущен загруженный сценарий; такой слой всегда будет один
        target_layer = new_layers - layers
        profile_layer_id = next(iter(target_layer))

        # дождаться загрузки новог слоя, инициализировать его, сделать активным и сохранить все настройки
        for layer in session_layers:
            current_uuid = layer.get('uuid')
            if current_uuid != profile_layer_id:
                continue

            # поиск OLAP-модуля на этом слое; если их несколько, то возьмём первый из них
            try:
                layer_module_descs = layer["module_descs"]
            except IndexError:
                error_msg = 'No module_descs for layer with id "{}"! Layer data: "{}"'.format(current_uuid, layer)
                return self._raise_exception(PolymaticaException, error_msg)
            multisphere_module_id = ""
            for module in layer_module_descs:
                if module.get('type_id') == MULTISPHERE_ID:
                    multisphere_module_id = module.get('uuid')
                    break

            # выбрать слой с запущенным профилем
            self.active_layer_id = current_uuid
            self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=current_uuid)
            self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=current_uuid)

            # ожидание загрузки слоя
            progress = 0
            while progress < 100:
                time.sleep(0.5)
                result = self.execute_manager_command(
                    command_name="user_layer", state="get_load_progress", layer_id=current_uuid)
                progress = self.h.parse_result(result, "progress")

            # сохраняем настройки
            settings = {"wm_layers2": {"lids": list(new_layers), "active": current_uuid}}
            result = self.execute_manager_command(
                command_name="user_iface", state="save_settings", module_id=self.authorization_uuid, settings=settings)

            # обновляем общее число строк мультисферы
            if multisphere_module_id:
                self._set_multisphere_module_id(multisphere_module_id)
                self.update_total_row()
            return result

    @timing
    def create_sphere(self, cube_name: str, source_name: str, file_type: str, update_params: Dict,
                      sql_params: Dict = None, user_interval: str = "с текущего дня", filepath: str = "", separator="",
                      increment_dim=None, encoding: str = False, delayed: bool = False) -> [str, Dict]:
        """
        Создать мультисферу через импорт из источника
        :param cube_name: (str) название мультисферы, которую будем создавать
        :param filepath: (str) путь к файлу, либо (если файл лежит в той же директории) название файла.
            Не обязательно для бд
        :param separator: (str) разделитель для csv-источника. По умолчанию разделитель не выставлен
        :param increment_dim: (str) название размерности, необходимое для инкрементального обновления.
                            На уровне API параметр называется increment_field
        :param sql_params: (Dict) параметры для источника данных SQL.
            Параметры, которые нужно передать в словарь: server, login, passwd, sql_query
            Пример: {"server": "10.8.0.115",
                     "login": "your_user",
                     "passwd": "your_password",
                     "sql_query": "SELECT * FROM DIFF_data.dbo.TableForTest"}
        :param update_params: (Dict) параметры обновления мультисферы.
            Типы обновления:
              - "ручное"
              - "по расписанию"
              - "интервальное"
              - "инкрементальное" (доступно ТОЛЬКО для источника SQL!)
            Для всех типов обновления, кроме ручного, нужно обязательно добавить параметр schedule.
            Его значение - словарь.
               В параметре schedule параметр type:
               {"Ежедневно": 1,
                "Еженедельно": 2,
                "Ежемесячно": 3}
            В параметре schedule параметр time записывается в формате "18:30" (в запрос передается UNIX-time).
            В параметре schedule параметр time_zone записывается как в server-codes: "UTC+3:00"
            В параметре schedule параметр week_day записывается как в списке:
               - "понедельник"
               - "вторник"
               - "среда"
               - "четверг"
               - "пятница"
               - "суббота"
               - "воскресенье"
            Пример: {"type": "по расписанию",
                     "schedule": {"type": "Ежедневно", "time": "18:30", "time_zone": "UTC+3:00"}}
        :param user_interval: (str) интервал обновлений. Указать значение:
               {"с текущего дня": 0,
                "с предыдущего дня": 1,
                "с текущей недели": 2,
                "с предыдущей недели
                "с и по указанную дату": 11}": 3,
                "с текущего месяца": 4,
                "с предыдущего месяца": 5,
                "с текущего квартала": 6,
                "с предыдущего квартала": 7,
                "с текущего года": 8,
                "с предыдущего года": 9,
                "с указанной даты": 10,
                "с и по указанную дату": 11}
        :param source_name: (str) поле Имя источника. Не должно быть пробелов, и длина должна быть больше 5 символов!
        :param file_type: (str) формат файла. См. значения в server-codes.json
        :param encoding: (str) кодировка, например, UTF-8 (обязательно для csv!)
        :param delayed: (bool) отметить чекбокс "Создать мультисферу при первом обновлении."
        :return: (Dict) command_name="user_cube", state="save_ext_info_several_sources_request"
        """

        encoded_file_name = ""  # response.headers["File-Name"] will be stored here after PUT upload of csv/excel

        interval = {"с текущего дня": 0,
                    "с предыдущего дня": 1,
                    "с текущей недели": 2,
                    "с предыдущей недели": 3,
                    "с текущего месяца": 4,
                    "с предыдущего месяца": 5,
                    "с текущего квартала": 6,
                    "с предыдущего квартала": 7,
                    "с текущего года": 8,
                    "с предыдущего года": 9,
                    "с указанной даты": 10,
                    "с и по указанную дату": 11}

        # часовые зоны
        time_zones = self.server_codes["manager"]["timezone"]
        # проверки
        try:
            error_handler.checks(self, self.func_name, update_params, UPDATES, file_type, sql_params,
                                 user_interval, interval, PERIOD, WEEK, time_zones, source_name, cube_name)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        interval = interval[user_interval]

        if update_params["type"] != "ручное":
            # установить значение периода для запроса
            user_period = update_params["schedule"]["type"]
            update_params["schedule"]["type"] = PERIOD[user_period]

            # установить значение часовой зоны для запроса
            h_timezone = update_params["schedule"]["time_zone"]
            update_params["schedule"]["time_zone"] = time_zones[h_timezone]

            # преобразование времение в UNIX time
            user_time = update_params["schedule"]["time"]
            h_m = user_time.split(":")
            d = datetime.datetime(1970, 1, 1, int(h_m[0]) + 3, int(h_m[1]), 0)
            unixtime = time.mktime(d.timetuple())
            unixtime = int(unixtime)
            update_params["schedule"]["time"] = unixtime

        # пармаметр server_types для различных форматов данных
        server_types = self.server_codes["manager"]["data_source_type"]
        server_type = server_types[file_type]

        # создать мультисферу, получить id куба
        result = self.execute_manager_command(command_name="user_cube", state="create_cube_request",
                                              cube_name=cube_name)
        self.cube_id = self.h.parse_result(result=result, key="cube_id")
        if self.jupiter:
            if "ERROR" in self.cube_id:
                return self.cube_id

        # upload csv file
        if (file_type == "excel") or (file_type == "csv"):
            try:
                response = self.exec_request.execute_request(params=filepath, method="PUT")
            except Exception as e:
                logger.exception(e)
                logger.info("APPLICATION STOPPED")
                self.current_exception = str(e)
                if self.jupiter:
                    return self.current_exception
                raise

            encoded_file_name = response.headers["File-Name"]

        # data preview request, выставить кодировку UTF-8
        preview_data = {"name": source_name,
                        "server": "",
                        "server_type": server_type,
                        "login": "",
                        "passwd": "",
                        "database": "",
                        "sql_query": separator,
                        "skip": -1}
        # для бд выставить параметры server, login, passwd:
        if (file_type != "csv") and (file_type != "excel"):
            preview_data.update({"server": sql_params["server"]})
            preview_data.update({"login": sql_params["login"]})
            preview_data.update({"passwd": sql_params["passwd"]})
            preview_data.update({"sql_query": ""})
            # для бд psql прописать параметр database=postgres
            if file_type == "psql":
                preview_data.update({"database": "postgres"})
            # соединиться с бд
            result = self.execute_manager_command(command_name="user_cube",
                                                  state="test_source_connection_request",
                                                  datasource=preview_data)

        # для формата данных csv выставить кодировку
        if file_type == "csv":
            preview_data.update({"encoding": encoding})
        # для файлов заполнить параметр server:
        if (file_type == "csv") or (file_type == "excel"):
            preview_data.update({"server": encoded_file_name})

        # для бд заполнить параметр sql_query
        if (file_type != "csv") and (file_type != "excel"):
            preview_data.update({"sql_query": sql_params["sql_query"]})
        # для бд psql прописать параметр database=postgres
        if file_type == "psql":
            preview_data.update({"database": "postgres"})

        self.execute_manager_command(command_name="user_cube",
                                     state="data_preview_request",
                                     datasource=preview_data)

        # для формата данных csv сделать связь данных
        if file_type == "csv":
            self.execute_manager_command(command_name="user_cube",
                                         state="structure_preview_request",
                                         cube_id=self.cube_id,
                                         links=[])

        # добавить источник данных
        preview_data = [{"name": source_name,
                         "server": "",
                         "server_type": server_type,
                         "login": "",
                         "passwd": "",
                         "database": "",
                         "sql_query": separator,
                         "skip": -1}]
        # для формата данных csv выставить кодировку
        if file_type == "csv":
            preview_data[0].update({"encoding": encoding})
        # для файлов заполнить параметр server:
        if (file_type == "csv") or (file_type == "excel"):
            preview_data[0].update({"server": encoded_file_name})
        # для бд
        if (file_type != "csv") and (file_type != "excel"):
            preview_data[0].update({"server": sql_params["server"]})
            preview_data[0].update({"login": sql_params["login"]})
            preview_data[0].update({"passwd": sql_params["passwd"]})
            preview_data[0].update({"sql_query": sql_params["sql_query"]})
        # для бд psql прописать параметр database=postgres
        if file_type == "psql":
            preview_data[0].update({"database": "postgres"})
        self.execute_manager_command(command_name="user_cube",
                                     state="get_fields_request",
                                     cube_id=self.cube_id,
                                     datasources=preview_data)

        # структура данных
        result = self.execute_manager_command(command_name="user_cube", state="structure_preview_request",
                                              cube_id=self.cube_id, links=[])

        # словари с данными о размерностях
        dims = self.h.parse_result(result=result, key="dims")
        if self.jupiter:
            if "ERROR" in str(dims):
                return dims
        # словари с данными о фактах
        measures = self.h.parse_result(result=result, key="facts")
        if self.jupiter:
            if "ERROR" in str(measures):
                return measures

        try:
            # циклично добавить для каждой размерности {"field_type": "field"}
            for i in dims:
                i.update({"field_type": "field"})
                if file_type == "csv":
                    error_handler.checks(self, self.func_name, i)
            # циклично добавить для каждого факта {"field_type": "field"}
            for i in measures:
                i.update({"field_type": "field"})
                if file_type == "csv":
                    error_handler.checks(self, self.func_name, i)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # параметры для ручного обновления
        if update_params["type"] == "ручное":
            schedule = {"delayed": delayed, "items": []}
        elif update_params["type"] == "инкрементальное":
            # параметры для инкрементального обновления
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": "00000000"}
            # для сохранения id размерности инкремента
            increment_field = ""
            for dim in dims:
                if dim["name"] == increment_dim:
                    increment_field = dim["field_id"]
            if increment_dim is None:
                message = "Please fill in param increment_dim!"
                logger.exception(message)
                logger.info("APPLICATION STOPPED")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise ValueError(message)
            if increment_field == "":
                message = "No such increment field in importing sphere: {}".format(increment_dim)
                logger.exception(message)
                logger.info("APPLICATION STOPPED")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise ValueError(message)
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval, increment_field=increment_field)
        elif update_params["type"] == "по расписанию":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
        elif update_params["type"] == "интервальное":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": None}
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval)
        else:
            message = "Unknown update type: {}".format(update_params["type"])
            logger.exception(message)
            logger.info("APPLICATION STOPPED")
            self.current_exception = message
            if self.jupiter:
                return self.current_exception
            raise ValueError(message)
        interval = {"type": interval, "left_border": "", "right_border": "",
                    "dimension_id": "00000000"}
        # финальный запрос для создания мультисферы, обновление мультисферы
        return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                            cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                            schedule=schedule, interval=interval)

    @timing
    def update_cube(self, cube_name: str, update_params: Dict, user_interval: str = "с текущего дня",
                    delayed: bool = False, increment_dim=None) -> [Dict, str]:
        """
        Обновить существующий куб
        :param cube_name: (str) название мультисферы
        :param update_params: (Dict) параметры обновления мультисферы.
           Типы обновления:
              - "ручное"
              - "по расписанию"
              - "интервальное"
              - "инкрементальное" (доступно ТОЛЬКО для источника SQL!)
           Для всех типов обновления, кроме ручного, нужно обязательно добавить параметр schedule.
           Его значение - словарь.
               В параметре schedule параметр type:
               {"Ежедневно": 1,
                "Еженедельно": 2,
                "Ежемесячно": 3}
           В параметре schedule параметр time записывается в формате "18:30" (в запрос передается UNIX-time).
           В параметре schedule параметр time_zone записывается как в server-codes: "UTC+3:00"
           В параметре schedule параметр week_day записывается как в списке:
               - "понедельник"
               - "вторник"
               - "среда"
               - "четверг"
               - "пятница"
               - "суббота"
               - "воскресенье"
        :param user_interval: (str) интервал обновлений. Указать значение:
               {"с текущего дня": 0,
                "с предыдущего дня": 1,
                "с текущей недели": 2,
                "с предыдущей недели
                "с и по указанную дату": 11}": 3,
                "с текущего месяца": 4,
                "с предыдущего месяца": 5,
                "с текущего квартала": 6,
                "с предыдущего квартала": 7,
                "с текущего года": 8,
                "с предыдущего года": 9,
                "с указанной даты": 10,
                "с и по указанную дату": 11}
        :param increment_dim: (str) increment_dim_id, параметр необходимый для инкрементального обновления
        :param delayed: (bool) отметить чекбокс "Создать мультисферу при первом обновлении."
        :return: (Dict)user_cube save_ext_info_several_sources_request
        """
        interval = {"с текущего дня": 0,
                    "с предыдущего дня": 1,
                    "с текущей недели": 2,
                    "с предыдущей недели": 3,
                    "с текущего месяца": 4,
                    "с предыдущего месяца": 5,
                    "с текущего квартала": 6,
                    "с предыдущего квартала": 7,
                    "с текущего года": 8,
                    "с предыдущего года": 9,
                    "с указанной даты": 10,
                    "с и по указанную дату": 11}

        # часовые зоны
        time_zones = self.server_codes["manager"]["timezone"]

        # get cube id
        self.cube_name = cube_name
        result = self.execute_manager_command(command_name="user_cube", state="list_request")

        # получение списка описаний мультисфер
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if self.jupiter:
            if "ERROR" in str(cubes_list):
                return cubes_list

        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        # получить информацию о фактах и размерностях куба
        result = self.execute_manager_command(command_name="user_cube", state="ext_info_several_sources_request",
                                              cube_id=self.cube_id)

        # словари с данными о размерностях
        dims = self.h.parse_result(result=result, key="dims")
        if self.jupiter:
            if "ERROR" in str(dims):
                return dims
        # словари с данными о фактах
        measures = self.h.parse_result(result=result, key="facts")
        if self.jupiter:
            if "ERROR" in str(measures):
                return measures

        # циклично добавить для каждой размерности {"field_type": "field"}
        for i in dims:
            i.update({"field_type": "field"})
            # циклично добавить для каждого факта {"field_type": "field"}
        for i in measures:
            i.update({"field_type": "field"})

        if user_interval not in interval:
            message = "ERROR!!! No such interval: {}".format(user_interval)
            logger.exception(message)
            logger.info("APPLICATION STOPPED")
            self.current_exception = message
            if self.jupiter:
                return self.current_exception
            raise ValueError(message)
        interval = interval[user_interval]

        if update_params["type"] != "ручное":
            # установить значение периода для запроса
            user_period = update_params["schedule"]["type"]
            update_params["schedule"]["type"] = PERIOD[user_period]

            # установить значение часовой зоны для запроса
            h_timezone = update_params["schedule"]["time_zone"]
            update_params["schedule"]["time_zone"] = time_zones[h_timezone]

            # преобразование времение в UNIX time
            user_time = update_params["schedule"]["time"]
            h_m = user_time.split(":")
            d = datetime.datetime(1970, 1, 1, int(h_m[0]) + 3, int(h_m[1]), 0)
            unixtime = time.mktime(d.timetuple())
            unixtime = int(unixtime)
            update_params["schedule"]["time"] = unixtime

        # параметры для ручного обновления
        if update_params["type"] == "ручное":
            schedule = {"delayed": delayed, "items": []}
        elif update_params["type"] == "инкрементальное":
            # параметры для инкрементального обновления
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": "00000000"}
            # для сохранения id размерности инкремента
            increment_field = ""
            for dim in dims:
                if dim["name"] == increment_dim:
                    increment_field = dim["field_id"]
            if increment_dim is None:
                message = "ERROR!!! Please fill in param increment_dim!"
                logger.exception(message)
                logger.info("APPLICATION STOPPED")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise ValueError(message)
            if increment_field == "":
                message = "ERROR!!! No such increment field in importing sphere: {}".format(increment_dim)
                logger.exception(message)
                logger.info("APPLICATION STOPPED")
                self.current_exception = message
                if self.jupiter:
                    return self.current_exception
                raise ValueError(message)
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval, increment_field=increment_field)
        elif update_params["type"] == "по расписанию":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
        elif update_params["type"] == "интервальное":
            # параметры для оставшихся видов обновлений
            schedule = {"delayed": delayed, "items": [update_params["schedule"]]}
            interval = {"type": interval, "left_border": "", "right_border": "",
                        "dimension_id": None}
            return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                                cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                                schedule=schedule, interval=interval)
        else:
            message = "ERROR!!! Unknown update type: {}".format(update_params["type"])
            logger.exception(message)
            logger.info("APPLICATION STOPPED")
            self.current_exception = message
            if self.jupiter:
                return self.current_exception
            raise ValueError(message)
        interval = {"type": interval, "left_border": "", "right_border": "",
                    "dimension_id": "00000000"}
        # финальный запрос для создания мультисферы, обновление мультисферы
        return self.execute_manager_command(command_name="user_cube", state="save_ext_info_several_sources_request",
                                            cube_id=self.cube_id, cube_name=cube_name, dims=dims, facts=measures,
                                            schedule=schedule, interval=interval)

    def wait_cube_loading(self, cube_name: str) -> str:
        """
        Ожидание загрузки мультисферы
        :param cube_name: (str) название мультисферы
        :return: информация из лога о создании мультисферы
        """
        # id куба
        self.cube_id = self.get_cube_without_creating_module(cube_name)

        # время старта загрузки мультисферы
        start = time.time()

        # Скачать лог мультисферы
        file_url = self.url + "/" + "resources/log?cube_id=" + self.cube_id
        # имя cookies: session (для скачивания файла)
        cookies = {'session': self.session_id}
        # выкачать файл GET-запросом
        r = requests.get(file_url, cookies=cookies)
        # override encoding by real educated guess as provided by chardet
        r.encoding = r.apparent_encoding
        # вывести лог мультисферы
        log_content = r.text

        while "Cube creation completed" not in log_content:
            time.sleep(5)
            # выкачать файл GET-запросом
            r = requests.get(file_url, cookies=cookies)
            # override encoding by real educated guess as provided by chardet
            r.encoding = r.apparent_encoding
            # вывести лог мультисферы
            log_content = r.text
        # Сообщение об окончании загрузки файла
        output = log_content.split("\n")

        # Информация о времени создания сферы
        end = time.time()
        exec_time = end - start
        min = int(exec_time // 60)
        sec = int(exec_time % 60)
        return output

    @timing
    def group_dimensions(self, selected_dims: List) -> Dict:
        """
        Сгруппировать выбранные элементы самой левой размерности (работает, когда все размерности свернуты)
        :param selected_dims: (List) список выбранных значений
        :return: (Dict) view group
        """
        # подготовка данных
        result = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                           num_row=500, num_col=100)
        top_dims = self.h.parse_result(result, "top_dims")
        top_dims_qty = len(top_dims)
        result = self.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                           num_row=1000, num_col=100)
        data = self.h.parse_result(result, "data")

        data = data[1 + top_dims_qty:]  # исключает ячейки с названиями столбцов
        left_dim_values = [lst[0] for lst in data]  # получение самых левых размерностей элементов
        selected_indexes = set()
        for elem in left_dim_values:
            if elem in selected_dims:
                left_dim_values.index(elem)
                selected_indexes.add(left_dim_values.index(elem))  # только первые вхождения левых размерностей

        # отметить размерности из списка selected_dims
        sorted_indexes = sorted(selected_indexes)  # отстортировать первые вхождения левых размерностей
        for i in sorted_indexes:
            self.execute_olap_command(command_name="view", state="select", position=1, line=i, level=0)

        # сгруппировать выбранные размерности
        view_line = sorted_indexes[0]
        result = self.execute_olap_command(command_name="view", state="group", position=1, line=view_line, level=0)
        # обновить total_row
        self.update_total_row()
        return result

    @timing
    def group_measures(self, measures_list: List, group_name: str) -> Dict:
        """
        Группировка фактов в (левой) панели фактов
        :param measures_list: (List) список выбранных значений
        :param group_name: (str) новое название созданной группы
        :return: (Dict) command_name="fact", state="unselect_all"
        """
        for measure in measures_list:
            # выделить факты
            measure_id = self.get_measure_id(measure)
            self.execute_olap_command(command_name="fact", state="set_selection", fact=measure_id, is_seleceted=True)

        # сгруппировать выбранные факты
        self.execute_olap_command(command_name="fact", state="create_group", name=group_name)

        # снять выделение
        return self.execute_olap_command(command_name="fact", state="unselect_all")

    @timing
    def close_layer(self, layer_id: str) -> Dict:
        """
        Закрыть слой
        :param layer_id: ID активного слоя (self.active_layer_id)
        :return: (Dict) command="user_layer", state="close_layer
        """
        # cформировать список из всех неактивных слоев
        active_layer_set = set()
        active_layer_set.add(layer_id)
        unactive_layers_list = set(self.layers_list) - active_layer_set

        # если активный слой - единственный в списке слоев
        # создать и активировать новый слой
        if len(unactive_layers_list) == 0:
            result = self.execute_manager_command(command_name="user_layer", state="create_layer")
            other_layer = self.h.parse_result(result=result, key="layer", nested_key="uuid")
            if self.jupiter:
                if "ERROR" in str(other_layer):
                    return other_layer
            self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=other_layer)
            unactive_layers_list.add(other_layer)

        # активировать первый неактивный слой
        other_layer = next(iter(unactive_layers_list))
        self.execute_manager_command(command_name="user_layer", state="set_active_layer", layer_id=other_layer)

        # закрыть слой
        result = self.execute_manager_command(command_name="user_layer", state="close_layer", layer_id=layer_id)

        # удалить из переменных класса закрытый слой
        self.active_layer_id = ""
        self.layers_list.remove(layer_id)

        return result

    def _expand_dims(self, dims: list, position: int):
        """
        Развернуть все размерности OLAP-модуля (верхние или левые).
        :param dims: (list) список размерностей (верхних или левых).
        :param position: (int) позиция: 1 - левые размерности, 2 - верхние размерности.
        """
        if position not in [1, 2]:
            return self._raise_exception(ValueError, 'Param "position" must be 1 or 2!')

        # если нет размерностей или вынесена только одна размерность, то нечего разворачивать (иначе упадёт ошибка)
        dims = dims or []
        if len(dims) < 2:
            return

        # сбор команд на разворот размерностей
        commands = []
        for i in range(0, len(dims)):
            command = self.olap_command.collect_command("olap", "view", "fold_all_at_level", position=position, level=i)
            if self.jupiter and "EXCEPTION" in str(command):
                return command
            commands.append(command)

        # выполняем собранные команды
        if commands:
            query = self.olap_command.collect_request(*commands)
            try:
                self.exec_request.execute_request(query)
            except Exception as e:
                return self._raise_exception(ValueError, str(e))

    def _collap_dims(self, dims: list, position: int):
        """
        Свернуть все размерности OLAP-модуля (верхние или левые).
        :param dims: (list) список размерностей (верхних или левых).
        :param position: (int) позиция: 1 - левые размерности, 2 - верхние размерности.
        """
        if position not in [1, 2]:
            return self._raise_exception(ValueError, 'Param "position" must be 1 or 2!')

        # если нет размерностей или вынесена только одна размерность, то нечего сворачивать (иначе упадёт ошибка)
        dims = dims or []
        if len(dims) < 2:
            return

        self.execute_olap_command(command_name="view", state="unfold_all_at_level", position=position, level=0)

    @timing
    def expand_all_left_dims(self):
        """
        Развернуть все левые размерности OLAP-модуля. Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб и выносим все необходимые размерности влево
            2. Вызываем непосредственно метод:
                bl_test.expand_all_left_dims()
        """
        # получаем все левые размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        left_dims = self.h.parse_result(result=view_data, key="left_dims")
        # разворачиваем их
        self._expand_dims(left_dims, 1)

    @timing
    def expand_all_up_dims(self):
        """
        Развернуть все верхние размерности OLAP-модуля. Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб и выносим все необходимые размерности вверх
            2. Вызываем непосредственно метод:
                bl_test.expand_all_up_dims()
        """
        # получаем все верхние размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        top_dims = self.h.parse_result(result=view_data, key="top_dims")
        # разворачиваем их
        self._expand_dims(top_dims, 2)

    @timing
    def collap_all_left_dims(self):
        """
        Свернуть все левые размерности OLAP-модуля. Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб, выносим все необходимые размерности влево и раскрываем их
            2. Вызываем непосредственно метод:
                bl_test.collap_all_left_dims()
        """
        # получаем все левые размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        left_dims = self.h.parse_result(result=view_data, key="left_dims")
        # сворачиваем их
        self._collap_dims(left_dims, 1)

    @timing
    def collap_all_up_dims(self):
        """
        Свернуть все верхние размерности OLAP-модуля. Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб, выносим все необходимые размерности вверх и раскрываем их
            2. Вызываем непосредственно метод:
                bl_test.collap_all_up_dims()
        """
        # получаем все верхние размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        top_dims = self.h.parse_result(result=view_data, key="top_dims")
        # сворачиваем их
        self._collap_dims(top_dims, 2)

    @timing
    def expand_all_dims(self):
        """
        Развернуть все размерности OLAP-модуля (и верхние, и левые). Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб и выносим все необходимые размерности вверх/влево
            2. Вызываем непосредственно метод:
                bl_test.expand_all_dims()
        """
        # получаем все размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        # разворачиваем левые размерности
        left_dims = self.h.parse_result(result=view_data, key="left_dims")
        self._expand_dims(left_dims, 1)
        # разворачиваем верхние размерности
        top_dims = self.h.parse_result(result=view_data, key="top_dims")
        self._expand_dims(top_dims, 2)

    @timing
    def collap_all_dims(self):
        """
        Свернуть все размерности OLAP-модуля (и верхние, и левые). Метод ничего не принимает и ничего не возвращает.
        :call_example:
            1. Инициализируем класс и OLAP-модуль:
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                # открываем куб, выносим все необходимые размерности вверх/влево и раскрываем их
            2. Вызываем непосредственно метод:
                bl_test.collap_all_dims()
        """
        # получаем все размерности
        view_data = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        # сворачиваем левые размерности
        left_dims = self.h.parse_result(result=view_data, key="left_dims")
        self._collap_dims(left_dims, 1)
        # сворачиваем верхние размерности
        top_dims = self.h.parse_result(result=view_data, key="top_dims")
        self._collap_dims(top_dims, 2)

    @timing
    def move_up_dims_to_left(self) -> [List, str]:
        """
        Переместить верхние размерности влево. После чего развернуть их
        :return: (List) преобразованный список id левых размерностей
        """
        self.get_multisphere_data()

        # выгрузить данные только из первой строчки мультисферы
        result = self.execute_olap_command(command_name="view",
                                           state="get",
                                           from_row=0,
                                           from_col=0,
                                           num_row=1,
                                           num_col=1)

        left_dims = self.h.parse_result(result=result, key="left_dims")
        if self.jupiter:
            if "ERROR" in str(left_dims):
                return left_dims
        top_dims = self.h.parse_result(result=result, key="top_dims")
        if self.jupiter:
            if "ERROR" in str(top_dims):
                return top_dims

        # если в мультисфере есть хотя бы одна верхняя размерность
        if len(top_dims) > 0:
            # вынести размерности влево, начиная с последней размерности списка
            for i in top_dims[::-1]:
                dim_name = self.get_dim_name(dim_id=i)
                self.move_dimension(dim_name=dim_name, position="left", level=0)

            commands = []
            for i in range(0, len(top_dims)):
                command = self.olap_command.collect_command(module="olap",
                                                            command_name="view",
                                                            state="fold_all_at_level",
                                                            level=i)
                if self.jupiter:
                    if "EXCEPTION" in str(command):
                        return command
                commands.append(command)
            # если в мультисфере нет ни одной левой размерности
            # удалить последнюю команду fold_all_at_level, т.к. ее нельзя развернуть
            if len(left_dims) == 0:
                del commands[-1]
            # если список команд fold_all_at_level не пуст
            # выполнить запрос command_name="view" state="fold_all_at_level",
            if len(commands) > 0:
                query = self.olap_command.collect_request(*commands)
                try:
                    self.exec_request.execute_request(query)
                except Exception as e:
                    logger.exception(e)
                    logger.info("APPLICATION STOPPED")
                    self.current_exception = str(e)
                    if self.jupiter:
                        return self.current_exception
                    raise
            output = top_dims[::-1] + left_dims
            self.update_total_row()
            return output
        return "No dimensions to move left"

    @timing
    def grant_permissions(self, user_name: str, clone_user: Union[str, bool] = False) -> [Dict, str]:
        """
        Предоставить пользователю Роли и Права доступа.
        :param user_name: (str) имя пользователя.
        :param clone_user: (str) имя пользователя, у которого будут скопированы Роли и Права доступа;
            если не указывать этот параметр, то пользователю будут выставлены ВСЕ роли и права.
        :return: (Dict) commands ("user", "info") и ("user_cube", "change_user_permissions").
        """
        # получаем список пользователей
        result = self.execute_manager_command(command_name="user", state="list_request")
        users_data = self.h.parse_result(result=result, key="users")
        if self.jupiter and "ERROR" in str(users_data):
            return users_data

        # проверяем, существуют ли указанные пользователи
        self._check_user_exists(user_name, users_data)
        if clone_user:
            self._check_user_exists(clone_user, users_data)

        # склонировать права пользователя
        if clone_user:
            clone_user_permissions = {k: v for data in users_data for k, v in data.items() if
                                      data["login"] == clone_user}
            user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == user_name}
            requested_uuid = clone_user_permissions["uuid"]
            clone_user_permissions["login"], clone_user_permissions["uuid"] = user_permissions["login"], \
                                                                              user_permissions["uuid"]
            user_permissions = clone_user_permissions
        # или предоставить все права
        else:
            user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == user_name}
            user_permissions["roles"] = ALL_PERMISSIONS
            requested_uuid = user_permissions["uuid"]
        # cubes permissions for user
        result = self.execute_manager_command(command_name="user_cube", state="user_permissions_request",
                                              user_id=requested_uuid)

        cube_permissions = self.h.parse_result(result=result, key="permissions")
        if self.jupiter:
            if "ERROR" in str(cube_permissions):
                return cube_permissions

        # для всех кубов проставить "accessible": True (если проставляете все права),
        # 'dimensions_denied': [], 'facts_denied': []
        if clone_user:
            cube_permissions = [dict(item, **{'dimensions_denied': [], 'facts_denied': []}) for item
                                in cube_permissions]
        else:
            cube_permissions = [dict(item, **{'dimensions_denied': [], 'facts_denied': [], "accessible": True}) for item
                                in cube_permissions]
        # для всех кубов удалить cube_name
        for cube in cube_permissions:
            del cube["cube_name"]

        # предоставить пользователю Роли и Права доступа
        command1 = self.manager_command.collect_command("manager", command_name="user", state="info",
                                                        user=user_permissions)
        command2 = self.manager_command.collect_command("manager", command_name="user_cube",
                                                        state="change_user_permissions",
                                                        user_id=user_permissions["uuid"],
                                                        permissions_set=cube_permissions)
        if self.jupiter:
            if "EXCEPTION" in str(command1):
                return command1
            if "EXCEPTION" in str(command2):
                return command2
        query = self.manager_command.collect_request(command1, command2)
        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(RightsError, str(e))
        return result

    def _set_measure_select(self, is_seleceted: bool, measure_name: str = str(), measure_id: str = str()) -> Dict:
        """
        Выделить факт/отменить выделение факта с заданным названием или идентификатором.
        При вызове нужно обязательно указать либо название факта, либо его идентификатор.
        И то, и другое указывать не нужно: в таком случае название факта будет проигнорировано.
        :param is_seleceted: показывает, какая операция выполняется: выделение факта (True) или снятие отметки (False).
        :param measure_name: название факта.
        :param measure_id: идентификатор факта.
        :return: результат работы команды ("fact", "set_selection").
        """
        # проверка на заданность имени/идентификатора
        try:
            error_handler.checks(self, 'set_measure_select', measure_name, measure_id)
        except Exception as ex:
            return self._raise_exception(ValueError, str(ex))

        # если идентификатор не задан - получаем его по имени, а если задан - проверяем, что такой действительно есть
        self.get_multisphere_data()
        if not measure_id:
            measure_id = self.get_measure_id(measure_name, False)
        else:
            measure_id = measure_id.strip()
            measure_exists = False
            for item in self.multisphere_data.get("facts"):
                if item.get("id").strip() == measure_id:
                    measure_exists = True
                    break
            if not measure_exists:
                error_msg = 'Measure with id "{}" is not valid for Multisphere "{}"'.format(measure_id, self.cube_name)
                return self._raise_exception(ValueError, error_msg, with_traceback=False)

        # а теперь, зная идентификатор, выделяем факт (либо снимаем с него выделение - смотря что передано)
        return self.execute_olap_command(
            command_name='fact', state='set_selection', fact=measure_id, is_seleceted=is_seleceted)

    @timing
    def select_measure(self, measure_name: str = str(), measure_id: str = str()) -> Dict:
        """
        Выделить факт с заданным названием или идентификатором.
        При вызове нужно обязательно указать либо название факта, либо его идентификатор.
        И то, и другое указывать не нужно: в таком случае название факта будет проигнорировано.
        :param measure_name: название факта.
        :param measure_id: идентификатор факта.
        :return: результат работы команды ("fact", "set_selection").
        """
        return self._set_measure_select(True, measure_name, measure_id)

    @timing
    def unselect_measure(self, measure_name: str = str(), measure_id: str = str()) -> Dict:
        """
        Отменить выделение факта с заданным названием или идентификатором.
        При вызове нужно обязательно указать либо название факта, либо его идентификатор.
        И то, и другое указывать не нужно: в таком случае название факта будет проигнорировано.
        :param measure_name: название факта.
        :param measure_id: идентификатор факта.
        :return: результат работы команды ("fact", "set_selection").
        """
        return self._set_measure_select(False, measure_name, measure_id)

    @timing
    def select_all_dims(self) -> Dict:
        """
        Выделение всех элементов крайней левой размерности.
        :return: (Dict) command_name="view", state="sel_all".
        :call_example:
            1. Инициализируем класс и предварительно выносим размерности влево (чтобы было, что выделять):
                bl_test = sc.BusinessLogic(login="login", password="password", url="url")
                bl_test.move_dimension(dim_name="dimension_name", position="left", level=0)
            2. Вызываем непосредственно метод:
                bl_test.select_all_dims()
        """
        # получение списка элементов левой размерности (чтобы проверить, что список не пуст)
        result = self.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        left_dims = self.h.parse_result(result, "left_dims")
        if self.jupiter and "ERROR" in str(left_dims):
            return left_dims

        # проверки
        try:
            error_handler.checks(self, self.func_name, left_dims)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        # выделить все элементы крайней левой размерности
        return self.execute_olap_command(command_name="view", state="sel_all", position=1, line=1, level=0)

    @timing
    def load_sphere_chunk(self, units: int = 100) -> Dict:
        """
        [DEPRECATED] Использовать соответствующий метод в классе "GetDataChunc".
        Генератор, подгружающий мультисферу постранично, порциями строк.
        :param units: (int) количество подгружаемых строк; по-умолчанию 100.
        :return: (Dict) словарь вида {имя колонки: значение колонки}.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода:
                gen = bl_test.load_sphere_chunk(units="units")
                row_info = next(gen)
        """
        warn_msg = 'Метод "load_sphere_chunk" класса "BusinessLogic" помечен как DEPRECATED. ' \
            'Необходимо перейти на аналогичный метод класса "GetDataChunc"!'
        logger.warning(warn_msg)
        return GetDataChunk(self).load_sphere_chunk(units)

    @timing
    def logout(self) -> Dict:
        """
        Выйти из системы
        :return: command_name="user", state="logout"
        """
        logger.info('BusinessLogic session out')
        return self.execute_manager_command(command_name="user", state="logout")

    @timing
    def close_current_cube(self) -> Dict:
        """
        Закрыть текущую мультисферу.
        :return: (Dict) command ("user_iface", "close_module")
        """
        close_module_id = self.multisphere_module_id
        self._set_multisphere_module_id(str())
        return self.execute_manager_command(command_name="user_iface", state="close_module", module_id=close_module_id)

    @timing
    def rename_group(self, group_name: str, new_name: str) -> Dict:
        """
        Переименовать группу пользователей.
        :param group_name: (str) Название группы пользователей.
        :param new_name: (str) Новое название группы пользователей.
        :return: (Dict) Команда ("group", "edit_group").
        """
        # all groups data
        result = self.execute_manager_command(command_name="group", state="list_request")
        groups = self.h.parse_result(result, "groups")

        # empty group_data
        roles, group_uuid, group_members, description = str(), str(), str(), str()

        # search for group_name
        for group in groups:
            # if group exists: saving group_data
            if group.get("name") == group_name:
                roles = group.get("roles")
                group_uuid = group.get("uuid")
                group_members = group.get("members")
                description = group.get("description")
                break

        # check is group exist
        try:
            error_handler.checks(self, self.func_name, group_uuid, group_name, new_name)
        except Exception as e:
            self._raise_exception(PolymaticaException, str(e))

        # group_data for request
        group_data = {
            "uuid": group_uuid, "name": new_name, "description": description, "members": group_members, "roles": roles}
        return self.execute_manager_command(command_name="group", state="edit_group", group=group_data)

    def _create_multisphere_module(self, num_row: int = 10000, num_col: int = 100) -> [Dict, str]:
        """
        Создать модуль мультисферы
        :param self: экземпляр класса BusinessLogic
        :param num_row: количество отображаемых строк
        :param num_col: количество отображаемых колонок
        :return: self.multisphere_data
        """
        # Получить список слоев сессии
        result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        session_layers_lst = self.h.parse_result(result=result, key="layers")
        self.layers_list = [layer.get('uuid') for layer in session_layers_lst]

        # получить идентификатор текущего слоя
        try:
            self.active_layer_id = session_layers_lst[0]["uuid"]
        except Exception as e:
            error_msg = "Error while parsing response: {}".format(e)
            return self._raise_exception(PolymaticaException, error_msg)

        # Инициализировать слой и дождаться его загрузки
        self.execute_manager_command(command_name="user_layer", state="init_layer", layer_id=self.active_layer_id)
        progress = 0
        while progress < 100:
            result = self.execute_manager_command(
                command_name="user_layer", state="get_load_progress", layer_id=self.active_layer_id)
            progress = self.h.parse_result(result=result, key="progress")

        # cоздать модуль мультисферы из <cube_id> на слое <layer_id>:
        initial_module_id = "00000000-00000000-00000000-00000000"
        result = self.version_redirect.invoke_method(
            'create_multisphere_from_cube',
            module_id=initial_module_id,
            after_module_id=initial_module_id,
            module_type=MULTISPHERE_ID
        )

        # получение идентификатора модуля мультисферы и инициализация OLAP модуля
        created_module_id = self.h.parse_result(result=result, key="module_desc", nested_key="uuid")
        self._set_multisphere_module_id(created_module_id)

        # рабочая область прямоугольника
        view_params = {"from_row": 0, "from_col": 0, "num_row": num_row, "num_col": num_col}

        # получить список размерностей и фактов, а также текущее состояние таблицы со значениями
        # (рабочая область модуля мультисферы)
        query = self.olap_command.multisphere_data_query(self.multisphere_module_id, view_params)
        try:
            result = self.exec_request.execute_request(query)
        except Exception as e:
            return self._raise_exception(PolymaticaException, str(e))

        # multisphere data
        self.multisphere_data = {"dimensions": "", "facts": "", "data": ""}
        for item, index in [("dimensions", 0), ("facts", 1), ("data", 2)]:
            self.multisphere_data[item] = result["queries"][index]["command"][item]
        return self.multisphere_data

    def create_multisphere_from_cube(self, **kwargs):
        """
        Создать мультисферу из куба.
        """
        result = self.execute_manager_command(
            command_name="user_cube",
            state="open_request",
            layer_id=self.active_layer_id,
            cube_id=self.cube_id,
            module_id=kwargs.get('module_id')
        )
        return result

    @timing
    def rename_grouped_elems(self, name: str, new_name: str) -> Dict:
        """
        Переименовать сгруппированные элементы левой размерности.
        :param name: название группы элементов.
        :param new_name: новое название группы элементов.
        :return: (Dict) command_name="group", state="set_name"
        """
        group_id = ""

        res = self.execute_olap_command(command_name="view", state="get", from_row=0, from_col=0,
                                        num_row=1000, num_col=1000)

        # взять id самой левой размерности
        left_dims = self.h.parse_result(res, "left_dims")
        if not len(left_dims):
            return self._raise_exception(PolymaticaException, "No left dims!", with_traceback=False)
        left_dim_id = left_dims[0]

        # элементы левой размерности
        left_dim_elems = self.h.parse_result(res, "left")

        # вытащить идентификатор группировки размерности (если он есть у этого элемента)
        try:
            for elem in left_dim_elems:
                if "value" in elem[0]:
                    if elem[0]["value"] == name:
                        group_id = elem[0]["group_id"]
        except KeyError:
            msg = 'No grouped dimensions with name "{}"!'.format(name)
            return self._raise_exception(ValueError, msg)

        if not group_id:
            message = "For the left dim no such elem: {}".format(name)
            return self._raise_exception(ValueError, message, with_traceback=False)
        return self.execute_olap_command(
            command_name="group", state="set_name", dim_id=left_dim_id, group_id=group_id, name=new_name)

    @timing
    def get_cubes_for_scenarios_by_userid(self, user_name: str) -> List:
        """
        Для заданного пользователя получить список с данными о сценариях и используемых в этих сценариях мультисферах:

        [{"uuid": "b8ffd729",
          "name": "savinov_test",
          "description": "",
          "cube_ids": ["79ca1aa5", "9ce3ba59"],
          "cube_names": ["nvdia", "Роструд_БФТ_F_Measures_"]},
         ...
         ]
        :param user_name: имя пользователя, под которым запускается command_name="script", state="list_cubes_request"
        :return: (List) scripts_data
        """
        # создаём новую сессию под указанным пользователем
        self._check_user_exists(user_name)
        sc = BusinessLogic(login=user_name, url=self.url)

        scripts_data = []

        # script_descs
        script_lst = sc.execute_manager_command(command_name="script", state="list")
        script_descs = sc.h.parse_result(script_lst, "script_descs")

        # cubes data
        cubes = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_data = sc.h.parse_result(cubes, "cubes")

        for script in script_descs:
            # getting list of cube_ids for this scenario id
            res = sc.execute_manager_command(command_name="script", state="list_cubes_request",
                                             script_id=script["uuid"])
            cube_ids = sc.h.parse_result(res, "cube_ids")

            # saving cubes names in list
            cube_names = []
            for cube in cubes_data:
                for cube_id in cube_ids:
                    if cube_id == cube["uuid"]:
                        cube_name = cube["name"].rstrip()
                        cube_names.append(cube_name)

            # saving data for this scenario
            script_data = {
                "uuid": script["uuid"],
                "name": script["name"],
                "description": script["description"],
                "cube_ids": cube_ids,
                "cube_names": cube_names
            }
            scripts_data.append(script_data)

        # убить сессию пользователя user_name
        sc.logout()

        return scripts_data

    @timing
    def get_cubes_for_scenarios(self) -> List:
        """
        Получить список с данными о сценариях и используемых в этих сценариях мультисферах:

        [{"uuid": "b8ffd729",
          "name": "savinov_test",
          "description": "",
          "cube_ids": ["79ca1aa5", "9ce3ba59"],
          "cube_names": ["nvdia", "Роструд_БФТ_F_Measures_"]},
         ...
         ]
        :return: (List) scripts_data
        """
        scripts_data = []

        # script_descs
        script_lst = self.execute_manager_command(command_name="script", state="list")
        script_descs = self.h.parse_result(script_lst, "script_descs")

        # cubes data
        cubes = self.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_data = self.h.parse_result(cubes, "cubes")

        for script in script_descs:
            # getting list of cube_ids for this scenario id
            res = self.execute_manager_command(command_name="script", state="list_cubes_request",
                                               script_id=script["uuid"])
            cube_ids = self.h.parse_result(res, "cube_ids")

            # saving cubes names in list
            cube_names = []
            for cube in cubes_data:
                for cube_id in cube_ids:
                    if cube_id == cube["uuid"]:
                        cube_name = cube["name"].rstrip()
                        cube_names.append(cube_name)

            # saving data for this scenario
            script_data = {
                "uuid": script["uuid"],
                "name": script["name"],
                "description": script["description"],
                "cube_ids": cube_ids,
                "cube_names": cube_names
            }
            scripts_data.append(script_data)

        return scripts_data

    @timing
    def polymatica_health_check_user_sessions(self) -> int:
        """
        Подсчет активных пользовательских сессий [ID-3040]
        :return: (int) user_sessions
        """
        res = self.execute_manager_command(command_name="admin", state="get_user_list")

        # преобразовать полученную строку к utf-8
        res = res.decode("utf-8")

        # преобразовать строку к словарю
        res = ast.literal_eval(res)

        users_info = self.h.parse_result(res, "users")

        user_sessions = 0
        for user in users_info:
            if user["is_online"]:
                user_sessions += 1

        return user_sessions

    @timing
    def polymatica_health_check_all_multisphere_updates(self) -> Dict:
        """
        [ID-3010] Проверка ошибок обновления мультисфер (для целей мониторинга):
        0, если ошибок обновления данных указанной мультисферы не обнаружено
        1, если последнее обновление указанной мультисферы завершилось с ошибкой, но мультисфера доступна пользователям для работы
        2, если последнее обновление указанной мультисферы завершилось с ошибкой и она не доступна пользователям для работы
        OTHER - другие значения update_error и available
        :return: (Dict) multisphere_upds
        """

        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # словарь со статусами обновлений мультисфер
        multisphere_upds = {}

        for cube in cubes_list:
            if cube["update_error"] and not cube["available"]:
                multisphere_upds.update({cube["name"]: 2})
                continue
            elif cube["update_error"] and cube["available"]:
                multisphere_upds.update({cube["name"]: 1})
                continue
            elif not cube["update_error"] and cube["available"]:
                multisphere_upds.update({cube["name"]: 0})
                continue
            else:
                multisphere_upds.update({cube["name"]: "OTHER"})

        return multisphere_upds

    @timing
    def polymatica_health_check_multisphere_updates(self, ms_name: str) -> [int, str]:
        """
        [ID-3010] Проверка ошибок обновления мультисферы (для целей мониторинга):
        0, не обнаружено ошибок обновления данных указанной мультисферы и мультисфера доступна.
            (Проверка, что "update_error"=False и "available"=True)
        1, ошибок обновления данных указанной мультисферы
            (Проверка, что "update_error"=True или "available"=False)
        :param ms_name: (str) Название мультисферы
        :return: (int) 0 или 1
        """
        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # Проверка названия мультисферы
        try:
            error_handler.checks(self, self.func_name, cubes_list, ms_name)
        except Exception as e:
            logger.exception(e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise

        for cube in cubes_list:
            if cube["name"] == ms_name:
                if cube["update_error"] or not cube["available"]:
                    return 1
                break

        return 0

    @timing
    def polymatica_health_check_data_updates(self) -> [List, int]:
        """
        Назначение: Метод проверки обновления мультисфер (для целей мониторинга)
        Синтаксис: polymatica_health_check_data_updates (<имя мультисферы>)
        Пример вызова: TODO
        Возвращаемые значения или результат:
        0 - если ошибок обновления данных не обнаружено (последнее обновление для всех мультисфер выполнено успешно, без ошибок)
        Перечень мультисфер - последнее обновление которых завершилось с ошибкой
        Ошибки: TODO
        """
        res = self.execute_manager_command(command_name="user_cube", state="list_request")

        cubes_list = self.h.parse_result(res, "cubes")

        # словарь со статусами обновлений мультисфер
        multisphere_upds = []

        for cube in cubes_list:
            if cube["update_error"]:
                multisphere_upds.append(cube["name"])

        if not multisphere_upds:
            return 0

        return multisphere_upds

    @timing
    def get_layer_list(self, sid: str = None) -> List:
        """
        [ID-3120] Загрузка данных о слоях.
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :return: (list) список вида [[layer_id, layer_name], [...], ...], содержащий слои в том порядке,
            в котором они отображаются на интерфейсе.
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                layer_list = bl_test.get_layer_list()
                output: [["id", "name"], ["id", "name"], ...] - список слоёв для текущей сессии.
            3. Вызов метода с передачей валидного sid:
                sid = "valid_sid"
                layer_list = bl_test.get_layer_list(sid)
                output: [["id", "name"], ["id", "name"], ...] - список слоёв для заданной сессии.
            4. Вызов метода с передачей невалидного sid:
                sid = "invalid_sid"
                layer_list = bl_test.get_layer_list(sid)
                output: exception "Session does not exist".
        """
        # если указан идентификатор сессии, то обращаемся к нему
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.get_layer_list()

        # получаем список слоёв
        layers_result = self.execute_manager_command(command_name="user_layer", state="get_session_layers")
        layers_list = self.h.parse_result(result=layers_result, key="layers")

        # сортируем список слоёв по времени создания,
        # т.к. необходимо вернуть слои в том порядке, в котором они отображаются на интерфейсе
        layers_list.sort(key=lambda item: item.get('create_timestamp', 0))

        # проходим по списку слоёв и сохраняем их идентификаторы и названия
        layers = [[layer.get('uuid', str()), layer.get('name', str())] for layer in layers_list]
        return layers

    @timing
    def set_layer_focus(self, layer: str, sid: str = None) -> str:
        """
        [ID-3121] Установка активности заданного слоя.
        :param layer: идентификатор/название слоя
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :return: (str) идентификатор установленного активного слоя.
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                layer = "layer_id_or_layer_name"
                layer_list = bl_test.set_layer_focus(layer=layer)
                output: layer_id - идентификатор установленного активного слоя.
            3. Вызов метода с передачей валидного sid:
                layer, sid = "layer_id_or_layer_name", "valid_sid"
                layer_list = bl_test.set_layer_focus(layer=layer, sid=sid)
                output: layer_id - идентификатор установленного активного слоя (для заданной сессии).
            4. Вызов метода с передачей невалидного sid:
                layer, sid = "layer_id_or_layer_name", "invalid_sid"
                layer_list = bl_test.set_layer_focus(layer=layer, sid=sid)
                output: exception "Session does not exist".
            5. Вызов метода с передачей неверного идентификатора/названия слоя:
                layer = "invalid_layer_id or invalid_layer_name"
                layer_list = bl_test.set_layer_focus(layer=layer)
                output: exception "Layer cannot be found by name or ID".
        """
        # если указан идентификатор сессии, то обращаемся к нему
        if sid:
            session_bl = self._get_session_bl(sid)
            layer_id = session_bl.set_layer_focus(layer)
            self.active_layer_id = layer_id
            return layer_id

        # получаем все слои мультисферы
        # layers имеет вид [[layer_id, layer_name], [...], ...]
        layers = self.get_layer_list(sid)

        # проходя по каждому слою, ищем соответствие среди имени/идентификатора
        for current_layer_params in layers:
            if layer in current_layer_params:
                layer_id = current_layer_params[0]
                s = {"wm_layers2": {"lids": [item[0] for item in layers], "active": layer_id}}
                self.execute_manager_command(
                    command_name="user_layer", state="set_active_layer", layer_id=layer_id)
                self.execute_manager_command(
                    command_name="user_iface", state="save_settings", module_id=self.authorization_uuid, settings=s)
                self.active_layer_id = layer_id
                return layer_id

        # если дошло сюда - слой с таким именем/идентификатором не найден, бросаем ошибку
        self.current_exception = "Layer cannot be found by name or ID"
        if self.jupiter:
            return self.current_exception
        raise Exception(self.current_exception)

    @timing
    def get_active_layer_id(self) -> str:
        """
        Возвращает идентификатор активного слоя в текущей сессии.
        :return: (str) идентификатор активного слоя.
        """
        settings = self.execute_manager_command(
            command_name="user_iface", state="load_settings", module_id=self.authorization_uuid)
        return self.h.parse_result(result=settings, key="settings").get('wm_layers2', dict()).get('active')

    @timing
    def _get_modules_in_layer(self, layer_id: str, is_int_type: bool = True) -> List:
        """
        Возвращает список модулей на заданном слое.
        :param layer_id: идентификатор слоя, модули которого необходимо получить.
        :param is_int_type: флаг, показывающий, в каком виде выводить тип модуля:
            в числовом (500) или строковом ('Мультисфера'). Соответствующая мапа переводов хранится в CODE_NAME_MAP.
        :return: (list) список вида [[module_id, module_name, module_type], [...], ...],
            содержащий информацию о модулях в текущем слое.
        """
        # получаем список всех модулей, находящихся в текущем слое
        settings = self.execute_manager_command(command_name="user_layer", state="get_layer", layer_id=layer_id)
        layer_info = self.h.parse_result(result=settings, key="layer") or dict()

        # проходя по каждому модулю, извлекаем из него информацию
        result = []
        for module in layer_info.get('module_descs'):
            module_id, base_module_type = module.get('uuid'), module.get('type_id')
            module_type = base_module_type if is_int_type else CODE_NAME_MAP.get(base_module_type, base_module_type)

            # имя модуля в этих настройках не указано - подгружаем отдельно и формируем общий результат
            module_setting = self.execute_manager_command(
                command_name="user_iface", state="load_settings", module_id=module_id)
            module_info = self.h.parse_result(result=module_setting, key="settings") or dict()
            result.append([module_id, module_info.get('title', str()), module_type])
        return result

    @timing
    def get_module_list(self, sid: str = None) -> List:
        """
        [ID-3123] Возвращает список модулей в активном слое в заданной (или текущей) сессии.
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :return: (list) список вида [[module_id, module_name, module_type], [...], ...],
            содержащий информацию о модулях на активном слое.
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                module_list = bl_test.get_module_list()
                output: [["module_id", "module_name', "module_type"], [...], ...] - список модулей в активном слое
                    в текущей сессии.
            3. Вызов метода с передачей валидного sid:
                sid = "valid_sid"
                module_list = bl_test.get_module_list(sid)
                output: [["module_id", "module_name', "module_type"], [...], ...] - список модулей
                    в активном слое в заданной сессии.
            4. Вызов метода с передачей невалидного sid:
                sid = "invalid_sid"
                module_list = bl_test.get_module_list(sid)
                output: exception "Session does not exist".
        """
        # если указан идентификатор сессии, то обращаемся к нему
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.get_module_list()

        # получаем идентификатор активного слоя
        active_layer_id = self.get_active_layer_id()
        if not active_layer_id:
            self.current_exception = "Active layer not set!"
            if self.jupiter:
                return self.current_exception
            raise Exception(self.current_exception)

        return self._get_modules_in_layer(active_layer_id, False)

    @timing
    def set_module_focus(self, module: str, sid: str = None):
        """
        [ID-3122] Установка фокуса на заданный модуль. Слой, на котором находится модуль, также становится активным.
        Ничего не возвращает.
        :param module: идентификатор/название модуля.
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                module = "module_id_or_module_name"
                bl_test.set_module_focus(module=module)
            3. Вызов метода с передачей валидного sid:
                module, sid = "module_id_or_module_name", "valid_sid"
                bl_test.set_module_focus(module=module, sid=sid)
            4. Вызов метода с передачей невалидного sid:
                module, sid = "module_id_or_module_name", "invalid_sid"
                bl_test.set_module_focus(module=module, sid=sid)
                output: exception "Session does not exist".
            5. Вызов метода с передачей неверного идентификатора/названия модуля:
                module = "invalid_module_id_or_invalid_module_name"
                bl_test.set_module_focus(module=module)
                output: exception "Module cannot be found by ID or name".
        """
        # если указан идентификатор сессии, то обращаемся к нему
        if sid:
            session_bl = self._get_session_bl(sid)
            session_bl.set_module_focus(module)
            return

        # получаем все слои; layers имеет вид [[layer_id, layer_name], [...], ...]
        layers = self.get_layer_list()

        # проходя по каждому слою, получаем список его модулей
        for layer in layers:
            layer_id = layer[0]
            modules_info = self._get_modules_in_layer(layer_id)

            # module_info имеет формат [module_id, module_name, module_type]
            # перебираем все модули в текущем слое
            for module_info in modules_info:
                if module in module_info:
                    # делаем активным текущий слой
                    self.set_layer_focus(layer_id)

                    # делаем активным искомый модуль
                    self._set_multisphere_module_id(module_info[0])
                    return

        # если дошло сюда - модуль с таким именем/идентификатором не найден, бросаем ошибку
        self.current_exception = "Module cannot be found by ID or name"
        if self.jupiter:
            return self.current_exception
        raise Exception(self.current_exception)

    @timing
    def manual_update_cube(self, cube_name: str) -> [Dict, str]:
        """
        Запуск обновления мультисферы вручную.
        :param cube_name: (str) название мультисферы
        """
        self.cube_name = cube_name
        # получение списка описаний мультисфер
        result = self.execute_manager_command(command_name="user_cube", state="list_request")
        if "ERROR" in str(result):
            if self.jupiter:
                return result
            else:
                raise Exception(str(result))
        cubes_list = self.h.parse_result(result=result, key="cubes")
        if "ERROR" in str(cubes_list):
            if self.jupiter:
                return cubes_list
            else:
                raise Exception(str(cubes_list))
        # получить cube_id из списка мультисфер
        try:
            self.cube_id = self.h.get_cube_id(cubes_list, cube_name)
        except ValueError as e:
            logger.exception("EXCEPTION!!! %s", e)
            logger.info("APPLICATION STOPPED")
            self.current_exception = str(e)
            if self.jupiter:
                return self.current_exception
            raise
        # запуск обновления мультисферы вручную
        result = self.execute_manager_command(command_name="user_cube", state="manual_update", cube_id=self.cube_id)
        if "ERROR" in str(result):
            if self.jupiter:
                return result
            else:
                raise Exception(str(result))
        return result

    @timing
    def module_fold(self, module_id: list, minimize: bool, sid: str = None):
        """
        [ID-2993] Свернуть/развернуть модули с заданными идентификаторами. Применимо не только к OLAP-модулям.
        :param module_id: (str or list) id/названия модулей, которые нужно свернуть/развернуть.
            Параметр может принимать как строку, так и массив строк.
            Пример 1. module_id = "id or name" - будет свёрнут/развёрнут только заданный модуль (если он есть).
            Пример 2. module_id = ["id or name", "id or name", ...] -
                    будут свёрнуты/развёрнуты все указанные идентификаторы.
        :param minimize: (bool) True - свернуть модуль / False - развернуть модуль.
        :param sid: (str) 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущее значение.
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                module, minimize = "module_id_or_module_name", "True or False"
                bl_test.module_fold(module_id=module, minimize=minimize)
            3. Вызов метода с передачей валидного sid:
                module, minimize, sid = "module_id_or_module_name", "True or False", "valid_sid"
                bl_test.module_fold(module_id=module, minimize=minimize, sid=sid)
            4. Вызов метода с передачей невалидного sid:
                module, minimize, sid = "module_id_or_module_name", "True or False", "invalid_sid"
                bl_test.module_fold(module_id=module, minimize=minimize, sid=sid)
                output: exception "Session does not exist".
            5. Вызов метода с передачей неверного идентификатора/названия модуля:
                module, minimize, sid = "invalid_module_id_or_invalid_module_name", "True or False", "invalid_sid"
                bl_test.module_fold(module_id=module, minimize=minimize, sid=sid)
                output: exception "The following modules were not found: {module}"
        """
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.module_fold(module_id=module_id, minimize=minimize)

        # в module_id может быть как идентификатор/название мультисферы, так и список идентификаторов/названий
        if isinstance(module_id, str):
            ms_ids = [module_id]
        elif isinstance(module_id, (list, set)):
            ms_ids = module_id
        else:
            raise ValueError("Arg 'module_id' must be str OR list!")

        # проверка параметра minimize
        if minimize not in [True, False]:
            raise ValueError("Arg 'minimize' can only be True OR False!")

        # сворачиваем/разворачиваем каждый заданный модуль
        error_modules = []
        for ms_id in ms_ids:
            # находим модуль с заданным идентификатором
            _, current_module_id = self._find_module(ms_id)
            if not current_module_id:
                error_modules.append(ms_id)
                continue
            # получаем текущие настройки заданного модуля
            settings = self.execute_manager_command(
                command_name="user_iface", state="load_settings", module_id=current_module_id)
            current_module_settings = self.h.parse_result(settings, 'settings')
            # сохраняем новые настройки
            current_module_settings.update({"minimize": minimize})
            self.execute_manager_command(
                command_name="user_iface",
                state="save_settings",
                module_id=current_module_id,
                settings=current_module_settings
            )

        # генерируем ошибки/предупреждения
        if error_modules:
            message = 'The following modules were not found: {}'.format(str(error_modules)[1:-1])
            # если все заданные модули были не найдены - бросаем ошибку, иначе предупреждение
            if len(error_modules) == len(ms_ids):
                return self._raise_exception(PolymaticaException, message, with_traceback=False)
            else:
                logger.warning(message)

    @timing
    def graph_create(self, g_type: [int, str] = 1, settings: str = str(), grid: int = 3, labels: dict = None,
                    other: dict = None, olap_module_id: str = str()) -> str:
        """
        Создать график с заданными параметрами на основе активной или заданной мультисферы.
        Описание параметров:

        :param g_type: тип графика; можно задавать как целочисленное значение, так и строковое.
            Возможные значения (указаны целочисленные и строковые варианты):
                [1, "lines"] - линии
                [2, "cylinders"] - цилиндры
                [3, "cumulative_cylinders"] - цилиндры с накоплением
                [4, "area"] - области
                [5, "cumulative_area"] - области с накоплением
                [6, "pies"] - пироги
                [7, "radar"] - радар
                [8, "circles"] - круги
                [9, "circles_series"] - серии кругов
                [10, "balls"] - шары
                [11, "pools"] - бассейны
                [12, "3d_pool"] - 3D-бассейны
                [13, "corridor"] - коридор
                [14, "surface"] - поверхность
                [15, "graph"] - граф
                [16, "sankey"] - санкей
                [17, "chord"] - хордовая
                [18, "point"] - точечный
                [19, "point_series"] - серии точек.
            По-умолчанию (если не задан параметр) будет построен тип [1, "lines"] - линии.

        :param settings: битмап-строка настроек графиков, значениями могут быть только 0 или 1.
            Каждый тип графика имеет свой битмап настроек:
                1. {Заголовок, Легенда, Названия осей, Подписи на осях, Вертикальная ось справа} - актуально для типов:
                    [1, "lines"], [2, "cylinders"], [3, "cumulative_cylinders"], [4, "area"], [5, "cumulative_area"],
                    [8, "circles"], [9, "circles_series"], [11, "pools"], [13, "corridor"],
                    [18, "point"], [19, "point_series"].
                    По-умолчанию имеет значение "11110".
                2. {Заголовок, Легенда, Показывать подписи} - актуально для типов: [6, "pies"].
                    По-умолчанию имеет значение "111".
                3. {Заголовок, Легенда, Названия осей, Отображать метки на осях} - актуально для типов: [7, "radar"].
                    По-умолчанию имеет значение "1111".
                4. {Заголовок, Легенда, Названия осей, Подписи на осях} - актуально для типов:
                    [10, "balls"], [12, "3d_pool"].
                    По-умолчанию имеет значение "1111".
                5. {Заголовок, Названия осей, Подписи на осях} - актуально для типов: [14, "surface"].
                    По-умолчанию имеет значение "111".
                6. {Заголовок, Подсвечивать узлы} - актуально для типов: [15, "graph"].
                    По-умолчанию имеет значение "11".
                7. {Заголовок} - актуально для типов: [16, "sankey"].
                    По-умолчанию имеет значение "1".
                8. {Заголовок, Легенда} - актуально для типов: [17, "chord"].
                    По-умолчанию имеет значение "11".

        :param grid: настройка сетки.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [6, "pies"], [7, "radar"], [10, "balls"], [12, "3d_pool"],
                [14, "surface"], [15, "graph"], [16, "sankey"], [17, "chord"]
            Все остальные типы графиков имеют одно из следующих значений:
                0 - Все линии, 1 - Горизонтальные линии, 2 - Вертикальные линии, 3 - Без сетки.
            Значение по-умолчанию (если не задан параметр) - 3.

        :param labels: настройка подписей на графиках.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [6, "pies"], [7, "radar"], [14, "surface"], [16, "sankey"], [17, "chord"]
            Для типов графиков [1, "lines"], [2, "cylinders"], [3, "cumulative_cylinders"] это словарь вида:
                {'OX': <value>, 'OY': <value>, 'short_format': <value>}, где
                    OX - частота подписей по оси OX (от 5 до 30 с шагом 5); по-умолчанию 10
                    OY - частота подписей по оси OY (от 5 до 30 с шагом 5); по-умолчанию 10
                    short_format - нужно ли сокразать подпись (True/False); по-умолчанию False

        :param other: дополнительные настройки графиков.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [4, "area"], [7, "radar"], [16, "sankey"]
            Для типа графика [1, "lines"] это словарь вида:
                {'hints': <value>, 'show_points': <value>}, где
                    hints - нужно ли отображать подсказки к точкам (True/False); по-умолчанию False
                    show_points - нужно ли показывать точки (True/False); по-умолчанию True
            Для типа графика [2, "cylinders"] это словарь вида:
                {'hints': <value>, 'ident': <value>, 'ident_value': <value>}, где
                    hints - нужно ли отображать подсказки к цилиндрам (True/False); по-умолчанию False
                    ident - отображать цилиндры с отступом (True/False); по-умолчанию True
                    ident_value - значение отступа (от 0 до 1 с шагом 0.05); по-умолчанию 1
            Для типа графика [3, "cumulative_cylinders"] это словарь вида:
                {'hints': <value>, 'graph_type': <value>}, где:
                    hints - нужно ли отображать подсказки к цилиндрам (True/False); по-умолчанию False
                    graph_type - вид графика, значения: 'values'-значения, 'percents'-проценты; по-умолчанию 'values'
            Помимо этого, все типы графиков в словаре принимают поле 'name' - название графика (по-умолчанию False).

        :param olap_module_id: идентификатор OLAP-модуля, на основе которого будет строиться график;
            если параметр не задан, то график будет строиться на основе текущего активного OLAP-модуля;
            если и текущий активный OLAP-модуль не задан, то будет сгенерирована ошибка.
        """
        try:
            graph_instance = Graph(
                self,
                g_type,
                settings,
                grid,
                labels or dict(),
                other or dict(),
                olap_module_id or self.multisphere_module_id
            )
            graph_module_id = graph_instance.create()
        except Exception as ex:
            return self._raise_exception(GraphError, str(ex))
        self._set_graph_module_id(graph_module_id)
        return graph_module_id

    @timing
    def graph_modify(self, g_type: [int, str] = 1, settings: str = str(), grid: int = 3, labels: dict = None,
                    other: dict = None, graph_id: str = str()) -> str:
        """
        Изменить уже существующий график по заданным параметрам.
        Описание параметров:

        :param g_type: тип графика; можно задавать как целочисленное значение, так и строковое.
            Возможные значения (указаны целочисленные и строковые варианты):
                [1, "lines"] - линии
                [2, "cylinders"] - цилиндры
                [3, "cumulative_cylinders"] - цилиндры с накоплением
                [4, "area"] - области
                [5, "cumulative_area"] - области с накоплением
                [6, "pies"] - пироги
                [7, "radar"] - радар
                [8, "circles"] - круги
                [9, "circles_series"] - серии кругов
                [10, "balls"] - шары
                [11, "pools"] - бассейны
                [12, "3d_pool"] - 3D-бассейны
                [13, "corridor"] - коридор
                [14, "surface"] - поверхность
                [15, "graph"] - граф
                [16, "sankey"] - санкей
                [17, "chord"] - хордовая
                [18, "point"] - точечный
                [19, "point_series"] - серии точек.
            По-умолчанию (если не задан параметр) будет построен тип [1, "lines"] - линии.

        :param settings: битмап-строка настроек графиков, значениями могут быть только 0 или 1.
            Каждый тип графика имеет свой битмап настроек:
                1. {Заголовок, Легенда, Названия осей, Подписи на осях, Вертикальная ось справа} - актуально для типов:
                    [1, "lines"], [2, "cylinders"], [3, "cumulative_cylinders"], [4, "area"], [5, "cumulative_area"],
                    [8, "circles"], [9, "circles_series"], [11, "pools"], [13, "corridor"],
                    [18, "point"], [19, "point_series"].
                    По-умолчанию имеет значение "11110".
                2. {Заголовок, Легенда, Показывать подписи} - актуально для типов: [6, "pies"].
                    По-умолчанию имеет значение "111".
                3. {Заголовок, Легенда, Названия осей, Отображать метки на осях} - актуально для типов: [7, "radar"].
                    По-умолчанию имеет значение "1111".
                4. {Заголовок, Легенда, Названия осей, Подписи на осях} - актуально для типов:
                    [10, "balls"], [12, "3d_pool"].
                    По-умолчанию имеет значение "1111".
                5. {Заголовок, Названия осей, Подписи на осях} - актуально для типов: [14, "surface"].
                    По-умолчанию имеет значение "111".
                6. {Заголовок, Подсвечивать узлы} - актуально для типов: [15, "graph"].
                    По-умолчанию имеет значение "11".
                7. {Заголовок} - актуально для типов: [16, "sankey"].
                    По-умолчанию имеет значение "1".
                8. {Заголовок, Легенда} - актуально для типов: [17, "chord"].
                    По-умолчанию имеет значение "11".

        :param grid: настройка сетки.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [6, "pies"], [7, "radar"], [10, "balls"], [12, "3d_pool"],
                [14, "surface"], [15, "graph"], [16, "sankey"], [17, "chord"]
            Все остальные типы графиков имеют одно из следующих значений:
                0 - Все линии, 1 - Горизонтальные линии, 2 - Вертикальные линии, 3 - Без сетки.
            Значение по-умолчанию (если не задан параметр) - 3.

        :param labels: настройка подписей на графиках.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [6, "pies"], [7, "radar"], [14, "surface"], [16, "sankey"], [17, "chord"]
            Для типов графиков [1, "lines"], [2, "cylinders"], [3, "cumulative_cylinders"] это словарь вида:
                {'OX': <value>, 'OY': <value>, 'short_format': <value>}, где
                    OX - частота подписей по оси OX (от 5 до 30 с шагом 5); по-умолчанию 10
                    OY - частота подписей по оси OY (от 5 до 30 с шагом 5); по-умолчанию 10
                    short_format - нужно ли сокразать подпись (True/False); по-умолчанию False

        :param other: дополнительные настройки графиков.
            Типы графиков, не имеющие данной настройки (если для перечисленных типов данный параметр будет задан,
            то он будет проигнорирован):
                [4, "area"], [7, "radar"], [16, "sankey"]
            Для типа графика [1, "lines"] это словарь вида:
                {'hints': <value>, 'show_points': <value>}, где
                    hints - нужно ли отображать подсказки к точкам (True/False); по-умолчанию False
                    show_points - нужно ли показывать точки (True/False); по-умолчанию True
            Для типа графика [2, "cylinders"] это словарь вида:
                {'hints': <value>, 'ident': <value>, 'ident_value': <value>}, где
                    hints - нужно ли отображать подсказки к цилиндрам (True/False); по-умолчанию False
                    ident - отображать цилиндры с отступом (True/False); по-умолчанию True
                    ident_value - значение отступа (от 0 до 1 с шагом 0.05); по-умолчанию 1
            Для типа графика [3, "cumulative_cylinders"] это словарь вида:
                {'hints': <value>, 'graph_type': <value>}, где:
                    hints - нужно ли отображать подсказки к цилиндрам (True/False); по-умолчанию False
                    graph_type - вид графика, значения: 'values'-значения, 'percents'-проценты; по-умолчанию 'values'
            Помимо этого, все типы графиков в словаре принимают поле 'name' - название графика (по-умолчанию False).

        :param graph_id: идентификатор изменяемого модуля графики;
            если параметр не задан, то будет изменён текущий активный график;
            если и текущий активный модуль графики не задан, то будет сгенерирована ошибка.
        """
        try:
            graph_instance = Graph(
                self,
                g_type,
                settings,
                grid,
                labels or dict(),
                other or dict(),
                graph_id or self.graph_module_id
            )
            graph_module_id = graph_instance.update()
        except Exception as ex:
            return self._raise_exception(GraphError, str(ex))
        self._set_graph_module_id(graph_module_id)
        return graph_module_id

    @timing
    def column_resize(self, module: str = None, sid: str = None, width: int = 200, olap_resize: bool = False) -> Dict:
        """
        [ID-2997] Расширение колонок фактов (чтобы текст на них становился видимым) на заданную ширину.
        Некая имитация интерфейсной кнопки "Показать контент". Актуально только для OLAP-модулей (мультисфер).
        Если пользователем не указан идентификатор модуля, то расширяется текущий активный OLAP-модуль.
        :param module: название/идентификатор OLAP-модуля;
            если модуль указан, но такого нет - сгенерируется исключение;
            если модуль не указан, то берётся текущий (активный) модуль (если его нет - сгенерируется исключение).
        :param sid: 16-ричный идентификатор сессии; в случае, если он отсутствует, берётся текущая сессия.
        :param width: ширина, на которую будет меняться каждая колонка фактов; можно указать отрицательное значение,
            тогда ширина колонок будет уменьшаться; при указании положительного значения - ширина колонок увеличится.
        :param olap_resize: нужно ли расширять окно мультисферы (True - нужно, False - не нужно). По-умолчанию False.
        :return: command_name="user_iface", state="save_settings".
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода без передачи sid:
                module, width, olap_resize = "module_id_or_module_name", "width", "olap_resize"
                bl_test.column_resize(module=module, width=width, olap_resize=olap_resize)
            3. Вызов метода с передачей валидного sid:
                module, width, olap_resize = "module_id_or_module_name", "width", "olap_resize"
                sid = "valid_sid"
                bl_test.column_resize(module=module, sid=sid, width=width, olap_resize=olap_resize)
            4. Вызов метода с передачей невалидного sid:
                module, width, olap_resize = "module_id_or_module_name", "width", "olap_resize"
                sid = "invalid_sid"
                bl_test.column_resize(module=module, sid=sid, width=width, olap_resize=olap_resize)
                output: exception "Session does not exist".
            5. Вызов метода с передачей неверного идентификатора/названия модуля:
                module, width, olap_resize = "invalid_module_id_or_invalid_module_name", "width", "olap_resize"
                bl_test.column_resize(module=module, width=width, olap_resize=olap_resize)
                output: exception "Module {} not found".
        """
        if sid:
            session_bl = self._get_session_bl(sid)
            return session_bl.column_resize(module=module, width=width, olap_resize=olap_resize)

        # проверка значений
        if not isinstance(olap_resize, bool):
            raise ValueError('Wrong param "olap_resize"! It can only be "True" or "False"!')

        # получаем идентификатор OLAP-модуля
        module_id = self._get_olap_module_id(module)

        # вычисляем новую ширину каждой ячейки фактов
        measure_widths, olap_width = self._get_current_widths(module_id)
        new_measure_widths = list(map(lambda x: x + width, measure_widths))

        # вычисляем новую ширину OLAP-модуля
        olap_width += 0 if olap_resize is False else width * len(measure_widths)

        # сохраняем новые настройки, где текущую ширину колонок увеличиваем на значение, заданное пользователем
        settings = {"dimAndFactShow": True, "itemWidth": new_measure_widths, "geometry": {"width": olap_width}}
        return self.execute_manager_command(
            command_name="user_iface", state="save_settings", module_id=module_id, settings=settings)

    @timing
    def _get_current_widths(self, module_id) -> Union[List, int]:
        """
        Получает текущие настройки интерфейса и возвращает ширину фактов в заданной мультисфере, а также ширину
        самого окна мультисферы. Если интерфейсные настройки не заданы, возвращаются значения по-умолчанию.
        :param module_id: идентификатор OLAP-модуля; гарантируется, что такой модуль точно существует.
        :return: (list) список, содержащий значение ширины каждого факта.
        :return: (int) значение ширины окна мультисферы.
        """
        # считаем количество фактов мультисферы
        multisphere_data = self.get_multisphere_data()
        measure_count = len(multisphere_data.get('facts', []))
        # получаем настройки
        settings = self.execute_manager_command(command_name="user_iface", state="load_settings", module_id=module_id)
        current_settings = self.h.parse_result(result=settings, key="settings")
        measure_widths = current_settings.get('itemWidth', [50] * measure_count)
        olap_width = current_settings.get('geometry', {}).get('width', 790)
        return measure_widths, olap_width

    @timing
    def get_cubes_list(self) -> 'json':
        """
        Возвращает список кубов.
        :return: (json) информация по каждому кубу в формате JSON.
        """
        result = self.execute_manager_command(command_name="user_cube", state="list_request")
        return self.h.parse_result(result=result, key="cubes")

    @timing
    def get_cube_permissions(self) -> List:
        """
        Возвращает доступность кубов для текущего пользователя.
        :return: (List) список кубок в следующем формате:
            [{'cube_id': "cube_id", 'cube_name': "cube_name", 'accessible': "accessible"}, ...], где
            cube_id и cube_name - идентификатор и имя куда соответственно,
            accessible - доступность куба для текущего пользователя (True - куб доступен, False - не доступен)
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода: permission_data = bl_test.get_cube_permissions()
        """
        try:
            # ---------------------- пересмотреть закомменченное решение в рамках Polymatica 5.7 ----------------------
            # # получаем uuid текущего пользователя
            # users_result = self.execute_manager_command(command_name="user", state="list_request")
            # users_data = self.h.parse_result(result=users_result, key="users")
            # for user in users_data:
            #     if user.get('login') == self.login:
            #         requested_uuid = user.get('uuid')
            #         break

            # # для найденного пользователя получаем информацию о доступности кубов
            # cube_permission_result = self.execute_manager_command(
            #     command_name="user_cube", state="user_permissions_request", user_id=requested_uuid)
            # cube_permission_data = self.h.parse_result(result=cube_permission_result, key="permissions")
            # ---------------------------------------------------------------------------------------------------------

            cubes_data = self.execute_manager_command(command_name="user_cube", state="list_request")
            cubes_list = self.h.parse_result(result=cubes_data, key="cubes") or list()
            cube_permission_data = list()
            for cube in cubes_list:
                cube_permission_data.append({
                    'cube_id': cube.get('uuid'), 'cube_name': cube.get('name'), 'accessible': True})
        except Exception as ex:
            return self._raise_exception(PolymaticaException, str(ex))
        return cube_permission_data

    @timing
    def get_last_update_date(self, script_uuid: str) -> str:
        """
        [ID-2860] Возвращает дату последнего обновления мультисферы, входящей в заданный сценарий. Если мультисфер
        несколько, вернётся наибольшая из дат обновления.
        В методе учитывается тот факт, что текущий пользователь может не иметь прав на мультисферы, входящие в сценарий.
        Есть несколько случаев:
            1. Пользователь не имеет прав на ВСЕ мультисферы, входящие в сценарий. В таком случае сгенерируется
               ошибка ScenarioError.
            2. Пользователь не имеет прав на НЕКОТОРЫЕ мультисферы, входящие в сценарий. В таком случае в логи запишется
               соответствующее сообщение, но метод продолжит работу - вернётся наибольшая из дат обновления мультисфер,
               доступных пользователю.
        :param script_uuid: (str) uuid сценария.
        :return: (str) дата обновления в строковом формате (ISO).
        :call_example:
            1. Инициализируем класс: bl_test = sc.BusinessLogic(login="login", password="password", url="url")
            2. Вызов метода с передачей валидного script_uuid:
                script_uuid = "script_uuid"
                bl_test.get_last_update_date(script_uuid)
            3. Вызов метода с передачей невалидного script_uuid:
                script_uuid = "invalid_script_uuid"
                bl_test.get_last_update_date(script_uuid)
                output: exception "Ошибка получения мультисфер, входящих в сценарий.
                    Возможно, сценарий с идентификатором "{}" не существует".
        """
        script_cube_ids = set()

        # получаем идентификаторы кубов в заданном сценарии
        try:
            res = self.execute_manager_command(command_name="script", state="list_cubes_request", script_id=script_uuid)
            script_cube_ids = set(self.h.parse_result(res, "cube_ids"))
        except Exception as ex:
            err_msg = 'Ошибка получения мультисфер, входящих в сценарий. ' \
                'Возможно, сценарий с идентификатором "{}" не существует!'.format(script_uuid)
            return self._raise_exception(ScenarioError, err_msg)

        # ситуации, когда в сценарии нет ни одного куба, в принципе быть не может;
        # поэтому, если список идентификаторов кубов пуст - что-то не так, генерируем ошибку
        if not script_cube_ids:
            return self._raise_exception(
                ScenarioError, 'В сценарии "{}" ни одна мультисфера не найдена!'.format(script_uuid))

        # получаем список мультисфер и для мультисфер, входящих в заданный сценарий, извлекаем дату обновления
        cubes_info = self.get_cubes_list()
        update_times = [cube.get('update_time') for cube in cubes_info if cube.get('uuid') in script_cube_ids]

        # список дат обновлений может быть пуст (не полон), если не найдены мультисферы, входящие в сценарий;
        # это в свою очередь может быть из-за того, что у текущего пользователя нет прав на эти мультисферы.
        # 1. Если список дат обновлений пуст, т.е. у текущего пользователя нет прав ни на одну мультисферу
        #    из списка мультисфер заданного сценария - генерируем ошибку.
        # 2. Если же список дат обновлений не полон, т.е. у текущего пользователя нет прав только на некоторые
        #    мультисферы из списка мультисфер заданного сценария - кидаем предупреждение в логи.
        if not update_times:
            error_msg = 'У текущего пользователя нет прав ни на одну мультисферу, входящую в заданный сценарий!'
            return self._raise_exception(ScenarioError, error_msg)
        if len(script_cube_ids) != len(update_times):
            warning_msg = 'У текущего пользователя нет прав на некоторые мультисферы, входящие в заданный сценарий!'
            logger.warning(warning_msg)

        # берём максимальную дату (т.к. она в мс, то делим на миллион) и приводим к формату ISO
        max_update_time = int((max(update_times)) / 10 ** 6)
        return datetime.datetime.fromtimestamp(max_update_time).strftime(ISO_DATE_FORMAT)

    def _find_olap_module(self, olap_data: str) -> Union[str, str]:
        """
        Поиск OLAP-модуля с заданным именем/идентификатором. Если искомый модуль не найден, вернётся ('', '').
        :param olap_data: (str) идентификатор или имя OLAP-модуля.
        :return: (str) идентификатор слоя, на котором находится искомый модуль.
        :return: (str) идентификатор найденного модуля (uuid).
        """
        return self._find_module(olap_data, MULTISPHERE_ID)

    def _find_graph_module(self, graph_data: str) -> Union[str, str]:
        """
        Поиск модуля графиков с заданным именем/идентификатором. Если искомый модуль не найден, вернётся ('', '').
        :param graph_data: (str) идентификатор или имя модуля графиков.
        :return: (str) идентификатор слоя, на котором находится искомый модуль.
        :return: (str) идентификатор найденного модуля (uuid).
        """
        return self._find_module(graph_data, GRAPH_ID)

    def _find_module(self, module_data: str, module_type: int = None) -> Union[str, str]:
        """
        Поиск произвольного модуля с заданным именем/идентификатором. Если такой модуль не найден, вернётся ('', '').
        :param module_data: (str) идентификатор или имя модуля.
        :param module_type: (int) тип модуля, среди которого нужно искать искомый модуль (например, 500 - OLAP и тд).
        :return: (str) идентификатор слоя, на котором находится искомый модуль.
        :return: (str) идентификатор найденного модуля (uuid).
        """
        # проверка на пустоту
        if not module_data:
            return str(), str()

        # получаем список слоёв
        layer_list = self.get_layer_list()
        if not layer_list:
            return str(), str()

        # проходя по каждому слою, получаем список его модулей и ищем сопоставления
        for layer in layer_list:
            # param layer is ['layer_id', 'layer_name']
            layer_id = layer[0]
            module_list = self._get_modules_in_layer(layer_id)
            for module in module_list:
                # param module is ['module_uuid', 'module_name', 'module_int_type']
                if (module_type is None or module[2] == module_type) and (module_data in [module[0], module[1]]):
                    return layer_id, module[0]

        # если по итогу ничего не найдено - вернём значения по-умолчанию
        return str(), str()

    def change_total_mode(self) -> Dict:
        """
        Изменение режима показа тоталов (промежуточных сумм, обозначающихся как "всего") в мультисфере.
        Если до вызова данного метода тоталов в таблице не было, то они отобразятся, и наоборот.
        :return: (Dict) command ("view", "change_show_inter_total_mode")
        """
        return self.execute_olap_command(command_name="view", state="change_show_inter_total_mode")


class GetDataChunk:
    """ Класс для получения данных чанками """

    def __init__(self, sc: BusinessLogic):
        """
        Инициализация класса GetDataChunk
        :param sc: экземпляр класса BusinessLogic
        """
        logger.info("GetDataChunk init")

        # флаг работы в Jupiter Notebook
        self.jupiter = sc.jupiter

        # helper class
        self.h = Helper(self)

        # экзмепляр класса BusinessLogic
        self.sc = sc

        # хранит функцию-генератор исключений
        self._raise_exception = raise_exception(self.sc)

        # флаги наличия дубликатов размерностей и фактов
        self.measure_duplicated, self.dim_duplicated = False, False

        # получаем левые/верхние размерности, считаем их количество
        self.left_dims, self.top_dims = self._get_active_dims()
        self.left_dims_qty, self.top_dims_qty, self.facts_qty = len(self.left_dims), len(self.top_dims), 0

        # обязательное условие: чтобы получить данные, должна быть вынесена хотя бы одна левая размерность
        if not self.left_dims:
            error_msg = 'Для постраничной загрузки мультисферы должна быть вынесена хотя бы одна левая размерность!'
            return self._raise_exception(PolymaticaException, error_msg, with_traceback=False)

        # список имён активных размерностей
        self.dim_lst = []

        # получаем количество строк в мультисфере
        result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                              num_row=1, num_col=1)
        self.total_row = self.h.parse_result(result, "total_row")

        # словарь типов размерностей Полиматики; т.к. все значения этого словаря уникальны, его можно "перевернуть"
        self.olap_types = self.sc.server_codes.get("olap", {}).get("olap_data_type", {})
        self.reversed_olap_types = {value: key for key, value in self.olap_types.items()}

        # список колонок в формате
        # {"data_type": <dimension/fact/fact_dimension>, "name": <column name>, "type": <column type>}
        self.columns = self._get_col_types()

        # общее количество колонок
        self.total_cols = self.left_dims_qty + self.facts_qty # можно ещё так: self.total_cols = len(self.columns)

        # сохраняем отдельно названия колонок, чтобы их не вычислять по несколько раз
        self.column_names = [column.get('name') for column in self.columns]

    def _get_active_dims(self) -> List:
        """
        Возвращает список левых и верхних размерностей мультисферы.
        """
        result = self.sc.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=1, num_col=1)
        return self.h.parse_result(result, "left_dims") or [], self.h.parse_result(result, "top_dims") or []

    def _get_data(self) -> List:
        """
        Получение первой строки данных. Необходимо для дальнейшего определения типов столбцов.
        """
        columns_data = self.sc.execute_olap_command(
            command_name="view", state="get_2", from_row=0, from_col=0, num_row=10, num_col=1000)
        data = self.h.parse_result(columns_data, "data")
        return data[self.top_dims_qty + 1] if self.top_dims_qty + 1 < len(data) else []

    def _get_all_dims(self) -> List:
        """
        Получение всех размерностей мультисферы.
        """
        all_dims_data = self.sc.execute_olap_command(command_name="dimension", state="list_rq")
        return self.h.parse_result(all_dims_data, "dimensions")

    def _get_measures(self) -> List:
        """
        Получение всех фактов мультисферы.
        """
        all_measures_data = self.sc.execute_olap_command(command_name="fact", state="list_rq")
        return self.h.parse_result(all_measures_data, "facts")

    def _get_dim_type(self, olap_type: int) -> str:
        """
        Возвращает тип размерности.
        """
        return list(self.olap_types.keys())[list(self.olap_types.values()).index(olap_type)]

    def _update_or_append_key(self, dict_container: dict, key: str):
        """
        Добавляет ключ в словарь, если его ещё там нет, иначе значение ключа увеличивает на 1.
        """
        if key not in dict_container:
            dict_container.update({key: 1})
        else:
            dict_container[key] += 1

    def _get_active_measure_ids(self) -> List:
        """
        Получение активных фактов (т.е. фактов, отображаемых в таблице мультисферы)
        """
        data = self.sc.execute_olap_command(
            command_name="view", state="get", from_row=0, from_col=0, num_row=10, num_col=1000)
        top, measure_data = self.h.parse_result(data, "top"), dict()
        for i in top:
            if "fact_id" in str(i):
                measure_data = i
                break
        return [measure.get("fact_id") for measure in measure_data]

    def _get_col_types(self) -> List:
        """
        [ID-3169] Получить текущие колонки мультисферы в заданном формате.
        :return: (list) колонки мультисферы в формате
            [{"name": "column_name", "type": "column_type", "data_type": "column_data_type"}, ...]
        """
        # список колонок,
        # содержащий словари вида {"name": <column_name>, "type": <column_type>, "data_type": <column_data_type>}
        columns = list()
        exists_columns = set()

        # получение первой строки, содержащей данные мультисферы
        # если по какой-то причине данных нет - выдаём ошибку
        data = self._get_data()
        if not data:
            error_msg = 'Для постраничной загрузки мультисферы в ней должны быть данные!'
            return self._raise_exception(PolymaticaException, error_msg, with_traceback=False)

        # получение списка всех размерностей
        all_dims = self._get_all_dims()
        dim_name_list = [dim.get("name") for dim in all_dims]

        # получение всех фактов и формирование из них вспомогательных данных
        measures_data = self._get_measures()
        measure_id_map = {measure.get("id"): measure.get("name") for measure in measures_data}
        measures_name_list = [measure.get("name") for measure in measures_data]

        # для накопления списка всех размерностей-дубликатов и фактов-дубликатов
        dims_dups, measure_dups = dict(), dict()

        # добавление размерностей в список колонок
        for my_dim in self.left_dims:
            for dim in all_dims:
                if my_dim == dim.get("id"):
                    dim_name = dim.get("name")
                    if dim_name in exists_columns:
                        self._update_or_append_key(dims_dups, dim_name)
                        dim_name = "{} (dim{})".format(dim_name, dims_dups.get(dim_name))
                        self.dim_duplicated = True

                    # составляем итоговый словарь и добавляем его в список колонок
                    dim_data = {
                        "name": dim_name,
                        "type": self._get_dim_type(dim.get("olap_type")),
                        # "type": self.reversed_olap_types.get(dim.get("olap_type")), # альтернатива
                        "data_type": "fact_dimension" if dim_name in measures_name_list else "dimension"
                    }
                    columns.append(dim_data)
                    exists_columns.add(dim_name)
                    self.dim_lst.append(dim_name)
                    break

        # получение идентификаторов активных фактов
        measure_ids = self._get_active_measure_ids()

        # добавление фактов в список колонок
        for measure_id in measure_ids:
            measure_name = measure_id_map.get(measure_id)
            check_measure_name = measure_name
            if measure_name in exists_columns:
                self._update_or_append_key(measure_dups, measure_name)
                measure_name = "{} (fact{})".format(measure_name, measure_dups.get(measure_name))
                self.measure_duplicated = True

            # получаем элемент для определения типа факта
            current_elem = data[len(columns)]

            # составляем итоговый словарь и добавляем его в список колонок
            measure_data = {
                "name": measure_name,
                "type": "double" if isinstance(current_elem, float) else "uint32",
                "data_type": "fact_dimension" if check_measure_name in self.dim_lst else "fact"
            }
            columns.append(measure_data)
            exists_columns.add(measure_name)
            self.facts_qty += 1

        return columns

    def load_sphere_chunk(self, units: int = 100) -> Dict:
        """
        Генератор, подгружающий мультисферу постранично (порциями строк). При этом в мультисфере не должно быть
        вынесенных вверх размерностей (только левые размерности). В противном случае будет сгенерировано исключение.
        :param units: (int) количество подгружаемых строк; по-умолчанию 100.
        :return: (Dict) словарь {имя колонки: значение колонки}.
        :call_example:
            1. Инициализируем класс БЛ: bl_test = BusinessLogic(login="login", password="password", url="url", **args)
            2. Вызов метода:
                gen = bl_test.load_sphere_chunk(units="units")
                row_data = next(gen)
        """
        # проверка на вынесенные вверх размерности
        _, top_dims = self._get_active_dims()
        if top_dims:
            error_msg = 'Постраничная загрузка мультисферы невозможна, т.к. обнаружены вынесенные вверх размерности! ' \
                'Необходимо предварительно переместить все размерности влево ' \
                'посредством вызова метода "move_up_dims_to_left()" класса BusinessLogic. ' \
                'Также для получения корректных данных рекомендуется развернуть все размерности мультисферы. ' \
                'Это можно сделать вызовом метода "expand_all_dims()" класса BusinessLogic.'
            return self._raise_exception(PolymaticaException, error_msg, with_traceback=False)

        # проверка на количество подгружаемых строк
        error_handler.checks(self.sc, 'load_sphere_chunk', units)

        start, total_row = 0, self.total_row
        while total_row > 0:
            total_row -= units

            # получаем информацию о представлении
            result = self.sc.execute_olap_command(
                command_name="view",
                state="get_2",
                from_row=start,
                from_col=0,
                num_row=units + 1,
                num_col=self.total_cols
            )
            rows_data = self.h.parse_result(result=result, key="data")

            # т.к. верхних размерностей нет, то начиная с первого индекса гарантированно идут данные
            for item in rows_data[1:]:
                yield dict(zip(self.column_names, item))
            start += units
