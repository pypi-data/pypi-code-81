'''
Description: 进度条的实现
version:
Author: TianyuYuan
Date: 2021-04-02 23:56:05
LastEditors: TianyuYuan
LastEditTime: 2021-04-06 21:25:10
'''
from datetime import datetime

from rich import print as rprint


class ProgressBar():
    """类：进度条，可用于显示普通迭代的进度"""

    def __init__(self, task, length, batchs=50):
        """类：进度条，可用于显示迭代的进度
        - task: 任务名称，可填入·函数名·或者·字符串·,若填入函数名，则可自动获取该函数的名字描述
        - length: 任务长度，通常为可迭代对象的长度，即len(iter_files)
        - batch: 进度条的份数，默认为100个单位，以百分制显示进度
        """
        if isinstance(task, str):
            self.task_name = task
        else:
            self.task_name = task.__name__
        self.length = length
        if self.length < batchs:
            self.batchs = self.length
            self.batch_size = 1
        else:
            self.batchs = batchs
            self.batch_size = self.length / self.batchs
        self.begin_time = datetime.now()

    def progress_layout(self):
        # TODO 进度条布局模块化
        layout = ""
        return layout

    def time_countdown(self, progress):
        if progress == 0:
            return "--:--"
        now_time = datetime.now()
        time_cost = now_time - self.begin_time
        time_cost = time_cost.seconds
        predict_time = round(time_cost / progress * self.batchs)
        time_cost = round(time_cost)
        return time_cost, predict_time

    def print_progressbar(self, i):
        """
        - i: 迭代到了第i个job
        """
        progress = int(i / self.batch_size)
        p_bar = "[" + "[bold green]>[/bold green]" * progress + "]"
        p_propotion = "[green]{}[/green]/[red]{}[/red]".format(i, self.length)
        p_percentage = ":rocket: {}%".format(round(i / self.length * 100))
        p_time = "[cyan]{}/{}s[/cyan]".format(*self.time_countdown(progress))
        if i < self.length:
            rprint(f"{self.task_name}  {p_percentage}  {p_time} :{p_bar}  {p_propotion}", end="\r")
        else:
            rprint(f"{self.task_name}  {p_percentage}  {p_time} :{p_bar}  {p_propotion}")
