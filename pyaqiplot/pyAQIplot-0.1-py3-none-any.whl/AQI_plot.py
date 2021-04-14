# -*- coding: utf-8 -*-
# Author: TAO Nianze (Augus)
import os
import json
import pandas as pd
import subprocess as sp
import matplotlib.pyplot as plt
import matplotlib.dates as m_date
from PIL import Image
from .colorbar import create_colorbar
from datetime import datetime
from .structure import (
    rgb,
    _classes,
    defeat_settings,
)

"""
Note: the size of words in the output figure will be affected by
      the scaling set in Windows. Scaling from 100% to 140% looks
      the same; >= 150% will make the figure look weird.
      Or change settings in settings.json.
"""
# 用来正常显示中文和日文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False


def _settings(set_file: str):
    """
    load settings from JSON file

    :param set_file: settings.json
    :return: a tuple of settings parameter
    """
    with open(
            file=set_file,
            mode='r',
            encoding='utf-8',
    ) as f:
        settings = json.load(f)
    s_size = settings["scatter size"]
    y_label_size = settings["y label size"]
    title_size = settings["title size"]
    subtitle_size = settings["subtitle size"]
    date_format = settings["date format"]
    frequency = settings["frequency"]
    return (
        s_size,
        y_label_size,
        title_size,
        subtitle_size,
        date_format,
        frequency
    )


def _data(file_name: str):
    """

    :param file_name: the import file is expected to
                      be a CSV file downloaded from
                      https://waqi.info/
    :return: 7 groups of data from the CSV file
    """
    dates = []
    date = pd.read_csv(
        file_name,
        usecols=[0],
    ).sort_values(
        by='date',
        ascending=True,
    ).values
    r_data = pd.read_csv(
        file_name,
    ).sort_values(
        by='date',
        ascending=True,
    )
    for date_i in date:
        dates.append(str(date_i[0]))
    data_pm25 = r_data[' pm25']
    data_pm10 = r_data[' pm10']
    data_o3 = r_data[' o3']
    data_no2 = r_data[' no2']
    data_so2 = r_data[' so2']
    data_co = r_data[' co']
    data_pm25 = data_pm25.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_pm10 = data_pm10.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_o3 = data_o3.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_no2 = data_no2.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_so2 = data_so2.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_co = data_co.apply(
        pd.to_numeric,
        errors='coerce',
    ).fillna(-15)
    data_pm25 = data_pm25.dropna().values.astype('int')
    data_pm10 = data_pm10.dropna().values.astype('int')
    data_o3 = data_o3.dropna().values.astype('int')
    data_no2 = data_no2.dropna().values.astype('int')
    data_so2 = data_so2.dropna().values.astype('int')
    data_co = data_co.dropna().values.astype('int')
    return (
        dates,
        data_pm25,
        data_pm10,
        data_o3,
        data_no2,
        data_so2,
        data_co,
    )


def _split(data: _data):
    """
    this function is used to classify data
    according to AQI classification standard.

    :param data: should be one group of data
                 outputted from _data(.) but
                 not the first one
    :return: a list that has be classified
    """
    _g = [
        list(),
        list(),
        list(),
        list(),
        list(),
        list(),
        list(),
        list(),
        list(),
        list(),
        list()
    ]
    for item in data:
        for key, c in enumerate(_classes):
            if c.contains(item):
                _g[key].append(item)
            else:
                _g[key].append(-15)
    return _g


def _plot(date: _data,
          data: _data,
          title: str,
          s_size: int,
          y_label_size: int,
          title_size: int,
          date_format: str,
          frequency: str,
          show: bool = False,):
    """

    :param date: the first group of data
                 outputted from _data(.)
    :param data: should be one group of data
                 outputted from _data(.) but
                 not the first one
    :param title: the title of the plot;
                  LaTex supported;
                  Chinese and Japanese supported
    :param show: if show=True => show the plot
                 if show=False => does not show the plot
    :return: None
    """
    _data_ = _split(data)
    xd = [datetime.strptime(d, '%Y/%m/%d').date() for d in date]
    ax = plt.gca()
    ax.xaxis.set_major_formatter(
        m_date.DateFormatter(date_format),
    )
    ax.xaxis.set_major_locator(
        m_date.DayLocator(),
    )
    plt.xticks(
        pd.date_range(
            date[0],
            date[-1],
            freq=frequency,
        ),
    )
    plt.scatter(xd, _data_[0], color=rgb[0], s=s_size)
    plt.scatter(xd, _data_[1], color=rgb[1], s=s_size)
    plt.scatter(xd, _data_[2], color=rgb[2], s=s_size)
    plt.scatter(xd, _data_[3], color=rgb[3], s=s_size)
    plt.scatter(xd, _data_[4], color=rgb[4], s=s_size)
    plt.scatter(xd, _data_[5], color=rgb[5], s=s_size)
    plt.scatter(xd, _data_[6], color=rgb[6], s=s_size)
    plt.scatter(xd, _data_[7], color=rgb[7], s=s_size)
    plt.scatter(xd, _data_[8], color=rgb[8], s=s_size)
    plt.scatter(xd, _data_[9], color=rgb[9], s=s_size)
    plt.scatter(xd, _data_[10], color=rgb[10], s=s_size)
    plt.ylim(0, )
    plt.gcf().autofmt_xdate()
    plt.ylabel(
        'AQI',
        fontsize=y_label_size,
    )
    plt.title(
        title,
        fontsize=title_size,
    )
    if show:
        plt.show()
    if not show:
        plt.tight_layout()


def sta(data: _data):
    """
    print the information

    :param data: should be one group of data
                 outputted from _data(.) but
                 not the first one
    :return: list
    """
    _sta = []
    _data_ = _split(data)
    for item in _data_:
        i = 0
        for d in item:
            if d != -15.0:
                i += 1
        _sta.append(str(i))
    return _sta


class Frame:
    def __init__(self,
                 file_path: str,
                 start_time=None,
                 end_time=None):
        self.date = _data(file_path)[0]
        self.data = _data(file_path)[1:]
        self.set_file = file_path+'-settings.json'
        self.colorbar_file = os.path.join(
            os.path.dirname(file_path),
            'colorbar.png',
        )
        if not os.path.exists(self.set_file):
            # create -settings.json file with
            # defeat settings parameters
            with open(
                file=self.set_file,
                mode='w',
                encoding='utf-8',
            ) as o:
                json.dump(
                    defeat_settings,
                    o,
                    sort_keys=True,
                    indent=4,
                    separators=(",", ": "),
                )
                print(
                    'write defeat settings to '
                    '{}'.format(self.set_file),
                )
        if (start_time and end_time) is not None:
            self.s_t = self.date.index(start_time)
            self.e_t = self.date.index(end_time)
            self.date = self.date[self.s_t:self.e_t]
            self.data = (
                self.data[0][self.s_t:self.e_t],
                self.data[1][self.s_t:self.e_t],
                self.data[2][self.s_t:self.e_t],
                self.data[3][self.s_t:self.e_t],
                self.data[4][self.s_t:self.e_t],
                self.data[5][self.s_t:self.e_t],
            )

    def _set(self):
        (
            self.s_size,
            self.y_label_size,
            self.title_size,
            self.subtitle_size,
            self.date_format,
            self.frequency,
        ) = _settings(self.set_file)

    def ind(self,
            title: str,
            select: int = 1,
            color_bar=False):
        """

        :param title: the title of the plot
        :param select: select=0 => pm2.5
                       select=1 => pm10
                       select=2 => O3
                       select=3 => NO2
                       select=4 => SO2
                       select=5 => CO
        :param color_bar: color_bar=True =>
                          show the colour bar
        :return: None
        """
        self._set()
        if color_bar:
            if not os.path.exists(
                    self.colorbar_file,
            ):
                create_colorbar(
                    self.colorbar_file,
                )
            img = Image.open(
                self.colorbar_file,
            )
            plt.subplot(2, 1, 1), _plot(
                self.date,
                self.data[select],
                title=title,
                s_size=self.s_size,
                y_label_size=self.y_label_size,
                title_size=self.title_size,
                date_format=self.date_format,
                frequency=self.frequency,
                show=False,
            )
            (
                plt.subplot(2, 1, 2),
                plt.imshow(img),
                plt.axis('off'),
            )
            plt.tight_layout()
            plt.show()
        else:
            _plot(
                self.date,
                self.data[select],
                title=title,
                s_size=self.s_size,
                y_label_size=self.y_label_size,
                title_size=self.title_size,
                date_format=self.date_format,
                frequency=self.frequency,
                show=True,
            )

    def gro(self,
            title: str):
        """

        :param title: the title of the plot
        :return: None
        """
        self._set()
        plt.subplot(3, 2, 1), _plot(
            self.date,
            self.data[0],
            r'PM$_{2.5}$',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.subplot(3, 2, 2), _plot(
            self.date,
            self.data[1],
            r'PM$_{10}$',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.subplot(3, 2, 3), _plot(
            self.date,
            self.data[2],
            r'O$_{3}$',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.subplot(3, 2, 4), _plot(
            self.date,
            self.data[3],
            r'NO$_{2}$',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.subplot(3, 2, 5), _plot(
            self.date,
            self.data[4],
            r'SO$_{2}$',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.subplot(3, 2, 6), _plot(
            self.date,
            self.data[5],
            r'CO',
            s_size=self.s_size,
            y_label_size=self.y_label_size,
            title_size=self.title_size,
            date_format=self.date_format,
            frequency=self.frequency,
        )
        plt.suptitle(
            title,
            fontsize=self.subtitle_size,
        )
        # do not use this under Python > 3.8.3
        # plt.tight_layout()
        figure = plt.get_current_fig_manager()
        try:  # full size show
            # if backend is Qt
            figure.resize(
                *figure.window.maxsize(),
            )
        except AttributeError:
            try:
                # if backend is WX
                figure.frame.Maximized(True)
            except AttributeError:
                # if backend is Tk
                figure.window.showMaximized()
        finally:
            plt.show()

    def statistics(self):
        s1 = sta(self.data[0])
        s2 = sta(self.data[1])
        s3 = sta(self.data[2])
        s4 = sta(self.data[3])
        s5 = sta(self.data[4])
        s6 = sta(self.data[5])
        inf = '             PM2.5     PM10     O3     NO2     SO2     CO\n' \
              '[  0, 25 ]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '( 25, 50 ]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '( 50, 75 ]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '( 75, 100]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(100, 125]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(125, 150]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(150, 175]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(175, 200]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(200, 300]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(300, 400]   {}{}{}{}{}{}{}{}{}{}{}\n' \
              '(400, +oo)   {}{}{}{}{}{}{}{}{}{}{}'. \
            format(
                s1[0],
                ' ' * (10 - len(s1[0])),
                s2[0],
                ' ' * (9 - len(s2[0])),
                s3[0],
                ' ' * (7 - len(s3[0])),
                s4[0],
                ' ' * (8 - len(s4[0])),
                s5[0],
                ' ' * (8 - len(s5[0])),
                s6[0],
                s1[1],
                ' ' * (10 - len(s1[1])),
                s2[1],
                ' ' * (9 - len(s2[1])),
                s3[1],
                ' ' * (7 - len(s3[1])),
                s4[1],
                ' ' * (8 - len(s4[1])),
                s5[1],
                ' ' * (8 - len(s5[1])),
                s6[1],
                s1[2],
                ' ' * (10 - len(s1[2])),
                s2[2],
                ' ' * (9 - len(s2[2])),
                s3[2],
                ' ' * (7 - len(s3[2])),
                s4[2],
                ' ' * (8 - len(s4[2])),
                s5[2],
                ' ' * (8 - len(s5[2])),
                s6[2],
                s1[3],
                ' ' * (10 - len(s1[3])),
                s2[3],
                ' ' * (9 - len(s2[3])),
                s3[3],
                ' ' * (7 - len(s3[3])),
                s4[3],
                ' ' * (8 - len(s4[3])),
                s5[3],
                ' ' * (8 - len(s5[3])),
                s6[3],
                s1[4],
                ' ' * (10 - len(s1[4])),
                s2[4],
                ' ' * (9 - len(s2[4])),
                s3[4],
                ' ' * (7 - len(s3[4])),
                s4[4],
                ' ' * (8 - len(s4[4])),
                s5[4],
                ' ' * (8 - len(s5[4])),
                s6[4],
                s1[5],
                ' ' * (10 - len(s1[5])),
                s2[5],
                ' ' * (9 - len(s2[5])),
                s3[5],
                ' ' * (7 - len(s3[5])),
                s4[5],
                ' ' * (8 - len(s4[5])),
                s5[5],
                ' ' * (8 - len(s5[5])),
                s6[5],
                s1[6],
                ' ' * (10 - len(s1[6])),
                s2[6],
                ' ' * (9 - len(s2[6])),
                s3[6],
                ' ' * (7 - len(s3[6])),
                s4[6],
                ' ' * (8 - len(s4[6])),
                s5[6],
                ' ' * (8 - len(s5[6])),
                s6[6],
                s1[7],
                ' ' * (10 - len(s1[7])),
                s2[7],
                ' ' * (9 - len(s2[7])),
                s3[7],
                ' ' * (7 - len(s3[7])),
                s4[7],
                ' ' * (8 - len(s4[7])),
                s5[7],
                ' ' * (8 - len(s5[7])),
                s6[7],
                s1[8],
                ' ' * (10 - len(s1[8])),
                s2[8],
                ' ' * (9 - len(s2[8])),
                s3[8],
                ' ' * (7 - len(s3[8])),
                s4[8],
                ' ' * (8 - len(s4[8])),
                s5[8],
                ' ' * (8 - len(s5[8])),
                s6[8],
                s1[9],
                ' ' * (10 - len(s1[9])),
                s2[9],
                ' ' * (9 - len(s2[9])),
                s3[9],
                ' ' * (7 - len(s3[9])),
                s4[9],
                ' ' * (8 - len(s4[9])),
                s5[9],
                ' ' * (8 - len(s5[9])),
                s6[9],
                s1[10],
                ' ' * (10 - len(s1[10])),
                s2[10],
                ' ' * (9 - len(s2[10])),
                s3[10],
                ' ' * (7 - len(s3[10])),
                s4[10],
                ' ' * (8 - len(s4[10])),
                s5[10],
                ' ' * (8 - len(s5[10])),
                s6[10],

            )
        print('\nUnit: day(s)')
        print('*' * 60)
        print(inf)
        print('*' * 60)

    def settings(self):
        sp.call(
            'explorer '+self.set_file,
            shell=True,
        )
        self._set()


if __name__ == '__main__':
    print(
        'This is a library file.',
    )
