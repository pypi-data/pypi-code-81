#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Содержит вспомогательные (служебные) методы, использующиеся в основном модуле работы с Полиматикой """

from typing import List, Dict, Tuple
from itertools import count
import logging
import time
from .exceptions import ParseError, CubeNotFoundError, ScenarioError, PolymaticaException
from .common import raise_exception

class Helper:
    def __init__(self, sc):
        """
        Инициализация вспомогательного класса.
        :param sc: экземпляр класса BusinessLogic
        """
        self.sc = sc
        self.jupiter = sc.jupiter
        # хранит функцию-генератор исключений
        self._raise_exception = raise_exception(self.sc)

    def get_cube_id(self, cubes_list: List, cube_name: str) -> [str, bool]:
        """
        Получить id мультисферы (куба).
        :param cubes_list: список мультисфер
        :param cube_name: название мультисферы
        :return: id мультисферы
        """
        for cube in cubes_list:
            if cube["name"] == cube_name:
                return cube["uuid"]
        raise ValueError("No such cube \"{}\" in cubes list!".format(cube_name))

    def get_measure_or_dim_id(self, multisphere_data: Dict, measure_dim: str, name) -> [str, bool]:
        """
        Получить id факта/размерности по имени.
        :param multisphere_data: рабочая область мультисферы
        :param measure_dim: "facts" / "dimensions"
        :param name: название размерности / факта
        :return: id размерности / факта
        """
        for item in multisphere_data[measure_dim]:
            if item["name"].rstrip() == name.rstrip():
                return item["id"]
        error_msg = 'No such {}: "{}"'.format(measure_dim[:-1], name)
        return self._raise_exception(ValueError, error_msg)

    def get_dim_id(self, multisphere_data: Dict, name: str, cube_name: str) -> str:
        """
        Получить идентификатор размерности по её названию.
        :param multisphere_data: рабочая область мультисферы.
        :param name: название размерности.
        :param cube_name: название текущей мультисферы.
        :return: Идентификатор размерности.
        """
        for item in multisphere_data["dimensions"]:
            if item.get("name", '').rstrip() == name.rstrip():
                return item.get("id")
        error_msg = 'Dimension name "{}" is not valid for Multisphere "{}"!'.format(name, cube_name)
        logging.error(error_msg)
        logging.info("APPLICATION STOPPED")
        if self.jupiter:
            return error_msg
        raise ValueError(error_msg)

    def get_measure_id(self, multisphere_data: Dict, name: str, cube_name: str) -> [str, bool]:
        """
        Получить идентификатор факта по его названию.
        :param multisphere_data: информация по рабочей области мультисферы.
        :param name: название факта.
        :param cube_name: название текущей мультисферы.
        :return: идентификатор факта.
        """
        # поиск идентификатора факта по его названию
        name = name.strip()
        for item in multisphere_data.get("facts"):
            if item.get("name").strip() == name:
                return item.get("id")
        # если не найдено ничего - бросаем ошибку
        error_msg = 'Measure name "{}" is not valid for Multisphere "{}"'.format(name, cube_name)
        return self._raise_exception(PolymaticaException, error_msg, with_traceback=False)

    def get_measure_or_dim_name_by_id(self, id_: str, type_: str) -> str:
        """
        Получить название факта/размерности по идентификатору.
        :param id_: (str) идентификатор факта/размерности.
        :param type_: (str) принимает одно из значений: "facts" или "dimensions".
        :return: (str) название факта/размерности.
        """
        # проверка
        if self.sc.multisphere_module_id == str():
            raise ValueError('First create cube and get data from it!')

        # получить словать с размерностями, фактами и данными
        self.sc.get_multisphere_data()

        # поиск нужного имени
        data = self.sc.multisphere_data.get(type_)
        for item in data:
            if item.get("id") == id_:
                return item.get("name")
        return 'No {} with id "{}" in the multisphere!'.format('measure' if type_ == 'facts' else 'dimension', id_)

    def get_measure_type(self, name: str) -> [bool, int]:
        """
        return Вид факта (value)
        :param name: Вид факта
        :return: Вид факта (id)
        """
        measure_types = {
            "Значение": 0,
            "Процент": 1,
            "Ранг": 2,
            "Количество уникальных": 3,
            "Среднее": 4,
            "Отклонение": 5,
            "Минимум": 6,
            "Максимум": 7,
            "Изменение": 8,
            "Изменение в %": 9,
            "Нарастающее": 10,
            "ABC": 11,
            "Медиана": 12,
            "Количество": 13,
            "UNKNOWN": 14
        }
        if name not in measure_types:
            error_msg = "ERROR!!! No such measure type: {}".format(name)
            logging.exception(error_msg)
            logging.info("APPLICATION STOPPED")
            if self.jupiter:
                return error_msg
            raise ValueError(error_msg)
        return measure_types[name]

    def join_splited_measures(self, formula_lst: List, join_iterations: int):
        """
        если в фактах есть пробелы, склеивает их обратно
        :param formula_lst: (List) формула, разбитая на список (разделитель - пробел)
        :param join_iterations: (int) количество итераций == количеству "[" в формуле
        :return: (List) formula_lst со склееными фактами
        """
        # если кол-во итераций закончилось (факты закончились) - выйти из функции
        if join_iterations == 0:
            return formula_lst
        # кол-во "[" и "]"
        openning_sqr_braket = 0
        closing_sqr_braket = 0

        # если все [факты с пробелами] и так склеены - вернуть formula_lst
        for idx, elem in enumerate(formula_lst):
            openning_sqr_braket += elem.count("[")
            closing_sqr_braket += elem.count("]")
            if openning_sqr_braket != closing_sqr_braket:
                break
            if (openning_sqr_braket == closing_sqr_braket) and (idx == len(formula_lst) - 1):
                return formula_lst

        # здесь будет сохранен [Факт, соединенный обратно по пробелу]
        joined_measure = ""
        # кол-во "[" и "]"
        openning_sqr_braket = 0
        closing_sqr_braket = 0
        # индексы, которые занимает рассплитенный факт в списке:
        measure_indexes = []

        for idx, elem in enumerate(formula_lst):
            # если факт и так не разделен по пробелу
            # и если в формуле есть функции corr, top, total, if - переход к след. итерации
            if ("[" in elem and "]" in elem) and ("corr(" not in joined_measure) and ("top(" not in joined_measure) and \
                    ("total(" not in joined_measure) and ("if(" not in joined_measure):
                continue
            openning_sqr_braket += elem.count("[")
            closing_sqr_braket += elem.count("]")
            # если в рассплитенном списке есть [Факт
            # конкатенировать его с joined_measure
            if openning_sqr_braket > 0:
                joined_measure += elem
                joined_measure += " "
            # если факт в виде [Факт
            # добавить индекс к списку measure_indexes
            if (openning_sqr_braket != 0) and (closing_sqr_braket == 0):
                measure_indexes.append(idx)
            # если элемент == факт, и этот факт в виде [Факт]
            # добавить индекс к списку measure_indexes и выйти из цикла
            if (openning_sqr_braket != 0) and (closing_sqr_braket != 0):
                if openning_sqr_braket == closing_sqr_braket:
                    measure_indexes.append(idx)
                    break

        # удалить рассплитенный факт из formula_lst
        for _ in measure_indexes:
            formula_lst.pop(measure_indexes[0])
        joined_measure = joined_measure.rstrip()

        # добавить в formula_lst [Факт, соединенный обратно по пробелу]
        formula_lst.insert(measure_indexes[0], joined_measure)

        # уменьшить кол-во итераций (кол-во фактов) на 1
        join_iterations -= 1

        # рекурсивно вызвать join_splited_measures()
        return self.join_splited_measures(formula_lst, join_iterations)

    def get_scenario_id_by_name(self, script_descs: Dict, scenario_name: str) -> str:
        """
        Получение идентификатор сценария по его имени.
        :param script_descs: (Dict) данные по всем сценариям.
        :param scenario_name: (str) название сценария.
        :return: идентификатор сценария
        """
        for script in script_descs:
            if script.get("name") == scenario_name:
                return script.get("uuid")
        return self._raise_exception(
            ScenarioError, 'Сценарий с именем "{}" не найден!'.format(scenario_name), with_traceback=False)

    def get_scenario_name_by_id(self, script_descs: Dict, scenario_id: str) -> str:
        """
        Получение идентификатор сценария по его имени.
        :param script_descs: (Dict) данные по всем сценариям.
        :param scenario_id: (str) идентификатор сценария.
        :return: название сценария
        """
        for script in script_descs:
            if script.get("uuid") == scenario_id:
                return script.get("name")
        return self._raise_exception(
            ScenarioError, 'Сценарий с идентификатором "{}" не найден!'.format(scenario_id), with_traceback=False)

    def wait_scenario_layer_loaded(self, sc_layer: str) -> Tuple:
        """
        Ожидание загрузки слоя с заданным сценарием.
        :param sc_layer: (str) идентификатор слоя с запускаемым сценарием.
        :return: (Tuple) количество обращений к серверу для получения текущего статуса, число законченных шагов.
        """
        need_check_progress, count_of_requests, finished_steps = True, 0, 0
        while need_check_progress:
            # периодичностью раз в полсекунды запрашиваем результат с сервера и проверяем статус загрузки слоя
            # если не удаётся получить статус - скорее всего нет ответа от сервера - сгенерируем ошибку
            # в таком случае считаем, что сервер не ответил и генерируем ошибку
            time.sleep(0.5)
            count_of_requests += 1
            try:
                progress = self.sc.execute_manager_command(
                    command_name="script", state="run_progress", layer_id=sc_layer)
                status = self.parse_result(result=progress, key="status") or {}
                status_code, status_message = status.get('code', -1), status.get('message', 'Unknown error!')
            except Exception as ex:
                # если упала ошибка - не удалось получить ответ от сервера: возможно, он недоступен
                return self._raise_exception(ScenarioError, 'Failed to load script! Possible server is unavailable.')

            # проверяем код статуса
            if status_code == 206:
                # сценарий в процессе воспроизведения
                need_check_progress = True
            elif status_code == 207:
                # сценарий полностью выполнен
                need_check_progress = False
            elif status_code == 208:
                # ошибка: сценарий остановлен пользователем (довольно редкий случай)
                return self._raise_exception(
                    ScenarioError, 'Script loading was stopped by user!', with_traceback=False)
            elif status_code == -1:
                # ошибка: не удалось получить код текущего статуса
                return self._raise_exception(ScenarioError, 'Unable to get status code!', with_traceback=False)
            else:
                # прочие ошибки
                return self._raise_exception(ScenarioError, status_message, with_traceback=False)
        return count_of_requests, self.parse_result(result=progress, key="finished_steps_count")

    def parse_result(self, result: Dict, key: str, nested_key: str = None):
        """
        Парсит и проверяет на ошибки ответ в виде ['queries'][0]['command']['значение']['необязательное значение'].
        :param result: (Dict) нераспарсенный ответ от API
        :param key: (str) ключ, значение которого нужно распарсить
        :param nested_key: (str) вложенный ключ, значение которого нужно распарсить
        :return: итоговое значение
        """
        base_error_msg = "ERROR while parsing response: ['queries'][0]['command']"
        request_queries = result.get("queries")
        request_queries = next(iter(request_queries))
        request_command = request_queries.get("command")
        value = request_command.get(key)
        if value is None:
            error_msg = "{}['{}']".format(base_error_msg, key)
            logging.error(error_msg)
            logging.info("APPLICATION STOPPED")
            if self.jupiter:
                return error_msg
            raise ParseError(error_msg)
        if nested_key is not None:
            nested_value = value.get(nested_key)
            if nested_value is None:
                error_msg = "{}['{}']['{}']".format(base_error_msg, key, nested_key)
                logging.error(error_msg)
                logging.info("APPLICATION STOPPED")
                if self.jupiter:
                    return error_msg
                raise ParseError(error_msg)
            return nested_value
        return value

    def get_rows_cols(self, num_row: int = None, num_col: int = None) -> Dict:
        """
        Загрузить строки и колонки мультисферы
        :param num_row: (int) количество строк мультисферы
        :param num_col: (int) количество колонок мультисферы
        :return: (Dict) command_name="view", state="get_2"
        """

        if (num_row is not None) and (num_col is not None):
            return self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                                num_row=num_row,
                                                num_col=num_col)

        # 1000, 2000, 3000, ...
        gen = count(1000, 1000)

        prev_data = []

        result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                              num_row=next(gen),
                                              num_col=next(gen))
        data = self.parse_result(result=result, key="data")

        while len(prev_data) < len(data):
            prev_data = data
            result = self.sc.execute_olap_command(command_name="view", state="get_2", from_row=0, from_col=0,
                                                  num_row=next(gen), num_col=next(gen))
            data = self.parse_result(result=result, key="data")
        return result

    def get_filter_rows(self, dim_id: str) -> Dict:
        """
        Загрузить строки и колонки мультисферы
        :param dim_id: (str) id размерности
        :return: (Dict) command_name="view", state="get_2"
        """

        # 1000, 2000, 3000, ...
        gen = count(1000, 1000)

        prev_data = []

        result = self.sc.execute_olap_command(command_name="filter",
                                              state="pattern_change",
                                              dimension=dim_id,
                                              pattern="",
                                              # кол-во значений отображается на экране, после скролла их становится больше:
                                              # num=30
                                              num=next(gen))

        data = self.parse_result(result=result, key="data")

        while len(prev_data) < len(data):
            prev_data = data
            result = self.sc.execute_olap_command(command_name="filter",
                                                  state="pattern_change",
                                                  dimension=dim_id,
                                                  pattern="",
                                                  # кол-во значений отображается на экране, после скролла их становится больше:
                                                  # num=30
                                                  num=next(gen))
            data = self.parse_result(result=result, key="data")
        return result
