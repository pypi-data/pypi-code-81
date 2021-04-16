#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Реализация графика типа "Линии".
"""

from .base_graph import BaseGraph

class Lines(BaseGraph):
    """
    Реализация графика типа "Линии".
    """
    def __init__(self, base_bl: 'BusinessLogic', settings: str, grid: str, labels: dict,
                other: dict, common_params: dict):
        super().__init__(base_bl, settings, grid, labels, other, common_params, 'plot-2d-lines', -1)

    def _get_settings(self) -> dict:
        """
        Получение актуальных настроек по заданному битмапу.
        :return: {
            'titleShow': <value>,
            'legend': <value>,
            'axis': <value>,
            'axis_notes': <value>,
            'vertical_right_axix': <value>
        }
        """
        return self.get_actual_settings(['titleShow', 'legend', 'axis', 'axis_notes', 'vertical_right_axix'])

    def _get_labels_settings(self) -> dict:
        """
        Получение настроек графика по параметру labels.
        :return: {'OX': <value>, 'OY': <value>, 'short_format': <value>}.
        """
        values_dict = {'OX': self.labels.get('OX', 10), 'OY': self.labels.get('OY', 10)}
        self.check_frequency_axis_5_30_5(values_dict)
        short_format = self.labels.get('short_format', False)
        if not self.check_bool(short_format):
            raise ValueError('Param "short_format" must be bool type!')
        values_dict.update({'short_format': short_format})
        return values_dict

    def _get_other_settings(self) -> dict:
        """
        Получение прочих настроек графика.
        :return: {'show_points': <value>, 'hints': <value>}.
        """
        show_points, hints = self.other.get('show_points', True), self.other.get('hints', False)
        if not self.check_bool(show_points):
            raise ValueError('Param "show_points" must be bool type!')
        if not self.check_bool(hints):
            raise ValueError('Param "hints" must be bool type!')
        return {"show_points": show_points, "hints": hints}

    def draw(self):
        """
        Отрисовка графика. Состоит из нескольких этапов:
        1. Проверка данных для текущего типа графика;
        2. Формирование конфигурации графика;
        3. Выхов команды, отрисовывающей график.
        """
        # проверка данных и получение всех настроек
        self.check_olap_configuration(1, 0, 1, None)
        settings = self._get_settings()
        labels_settings = self._get_labels_settings()
        other_settings = self._get_other_settings()

        # получение базовых настроек и их дополнение на основе заданных пользователем значений
        graph_config = self.get_graph_config().copy()
        base_setting = {
            "titleShow": settings.get('titleShow'),
            "legend": settings.get('legend'),
            "axis": settings.get('axis'),
            "axisNotes": settings.get('axis_notes'),
            "axisPosition": settings.get('vertical_right_axix'),
            "wireShow": self.grid,
            "axisNotesPeriodX": labels_settings.get('OX'),
            "axisNotesPeriodY": labels_settings.get('OY'),
            "axisXShortFormat": labels_settings.get('short_format')
        }
        lines_setting = {"showPoints": other_settings.get('show_points'), "hints": other_settings.get('hints')}
        graph_config['plotData'][self.graph_type]['config'].update({
            'base': base_setting,
            'lines': lines_setting
        })
        graph_config['plotData'][self.graph_type]['state']['title'] = self.graph_name

        # и, наконец, сохраняя настройки, отрисовываем сам график
        self.base_bl.execute_manager_command(
            command_name="user_iface",
            state="save_settings",
            module_id=self.common_params.get('graph_module_id'),
            settings=graph_config
        )
