"""
包括trendAnalyzer, trendPredict两个类

Classes
----------
trendAnalyzer: 使用三阶滑动平均与一阶导对输入数据的快速/缓慢的上升/下降状态进行判断

trendPredict: 通过不断输入一时间序列的数值，顺序地对所定义窗口1内的数值进行三阶滑动平均处理，并计算所定义窗口2内的时序数据一阶导，通过对所定义窗口3内一阶导数据均值进行判断，以确定原始数据的上升/下降情况，包括：是否处理上升/下降状态，是否处于快速/慢速    变化状态

Example
----------
>>> from Method_trendAnalyzer import trendAnalyzer, trendPredict

"""

import numpy as np
import matplotlib.pyplot as plt


class trendAnalyzer:
    """
    通过不断输入一时间序列的数值，顺序地对所定义窗口1内的数值进行三阶滑动平均处理，
    并计算所定义窗口2内的时序数据一阶导，通过对所定义窗口3内一阶导数据均值进行判断，
    以确定原始数据的上升/下降情况，包括：是否处理上升/下降状态，是否处于快速/慢速
    变化状态

    [1] 参数
    ----------
    smoothWindowSize:
        int, 进行窗口平滑处理的窗口尺寸, optional, default 30
    kValueWindowSize:
        int, 进行斜率计算单额窗口尺寸, 过大会导致判断滞后, 过小会导致各种状态快速变化, optional, default 130
    raiseThreshold:
        float, 用于判断数据上升状态的斜率阈值, 较大时表示判断结果为快速上升, optional, default 0.000001
    dropThreshold:
        float, 用于判断数据下降状态的斜率阈值, 较大时表示判断结果为快速下降, optional, default -0.000001

    [2] 方法
    ----------
    update:
        用于新增数据
    plotDualYAxisFig:
        用于绘制对数据上升/下降的判断结果图形

    [3] 返回
    -------
    status:
        int, -1是下降状态, 1是上升状态, 0是平缓状态

    kValues:
        list, 斜率计算结果, kValues[-1]为当前斜率

    [4] 示例
    --------
    >>> res = []
    >>> analyzer = trendAnalyzer(smoothWindowSize=30, raiseThreshold=0.001, dropThreshold=-0.001)
    >>> for i in range(dataQuant):
    >>>     analyzer.update(data[i])
    >>>     res.append(analyzer.status)
    >>> analyzer.plotDualYAxisFig([data], res, -1)
    """

    def __init__(self, **kwargs):
        self.smoothWindowSize = 30 if 'smoothWindowSize' not in kwargs.keys() else kwargs['smoothWindowSize']
        self.kValueWindowSize = 130 if 'kValueWindowSize' not in kwargs.keys() else kwargs['kValueWindowSize']
        self.statusWindowSize = 200 if 'statusWindowSize' not in kwargs.keys() else kwargs['statusWindowSize']
        self.raiseThreshold = 0.000001 if 'raiseThreshold' not in kwargs.keys() else kwargs['raiseThreshold']
        self.dropThreshold = -0.000001 if 'dropThreshold' not in kwargs.keys() else kwargs['dropThreshold']
        self.__valueCheck()
        self.data = list([0] * self.smoothWindowSize)
        self.kValues = list([0] * self.kValueWindowSize)
        self.status = []
        self.statusRecords = list([0] * self.statusWindowSize)
        self.bounceStatus = []

    # 输入检查
    def __valueCheck(self):
        # 类型检查
        if not isinstance(self.smoothWindowSize, int):
            raise TypeError("smoothWindowSize 似乎不是int类型")
        if not isinstance(self.kValueWindowSize, int):
            raise TypeError("kValueWindowSize 似乎不是int类型")
        if not isinstance(self.raiseThreshold, float):
            raise TypeError("raiseThreshold 似乎不是float类型")
        if not isinstance(self.dropThreshold, float):
            raise TypeError("dropThreshold 似乎不是float类型")
        # 定义域检查
        if not self.raiseThreshold > 0:
            raise ValueError("raiseThreshold 应当为正数")
        if not self.dropThreshold < 0:
            raise ValueError("dropThreshold 应当为负数")

    # 插入数据并计算变化率
    def update(self, _ele):
        def moveOneStep(_data, _newEle) -> list:
            _data.append(_newEle)
            _data.pop(0)
            return _data

        # 3阶平滑
        avgRecord_1st = moveOneStep(self.data, _ele)
        avgRecord_2st = moveOneStep(avgRecord_1st, np.average(avgRecord_1st))
        avgRecord_3st = moveOneStep(avgRecord_2st, np.average(avgRecord_2st))
        # 计算k值
        self.kValues = moveOneStep(self.kValues, np.diff(avgRecord_3st)[-1])
        # 判断k值是否为快速/平缓的上升/下降状态
        if np.average(self.kValues) > self.raiseThreshold:
            self.status = 1
        elif np.average(self.kValues) < self.dropThreshold:
            self.status = -1
        else:
            self.status = 0

    @staticmethod
    # 绘制单图
    def plotDualYAxisFig(_records, _status, _size=-1):
        """
        :param _records: list[list], 需要绘制在1#Y轴的数据, 可以为多个列表
        :param _status: list, 需要绘制在2#Y轴的数据
        :param _size: int, -1 表示绘制全量数据, default, -1
        :return: None
        """
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        # 其它数据绘制
        _otherDataQuant = np.shape(_records)[0]
        for i in range(_otherDataQuant):
            ax1.plot(_records[i][0:_size])
        if _size == -1:
            size = np.shape(_status)[0]
        else:
            size = _size
        # 状态绘制
        y0 = np.zeros_like(_status[0:size])
        y1 = np.ones_like(_status[0:size])
        y2 = _status[0:size]
        ax2.fill_between(np.arange(0, size, 1), y0, np.abs(y2), where=y0 < y2, facecolor='green', alpha=0.5)  # 上升段
        ax2.fill_between(np.arange(0, size, 1), y0, np.abs(y2), where=y0 > y2, facecolor='red', alpha=0.5)  # 下降段
        ax2.fill_between(np.arange(0, size, 1), y0, y1, where=y0 == y2, facecolor='yellow', alpha=0.5)  # 稳定段
        plt.show()


class trendPredict:
    """
    使用三次指数平滑法根据前序数据对当前数据的预测值进行计算

    [1] 参数
    ----------
    _windowSize:
        int, 平滑处理的数据窗口尺寸, 不可大于7, 不可小于2, optional, default 5
    _smoothParam:
        float, 学习率, optional, default 0.9

    [2] 方法
    ----------
    varsInitiate:
        变量recorder, X, S1, S2, S3, P初始化
    update:
        读取并记录新数据
    trendPredict:
        通过近期数据对当前数据的预测值进行计算

    [3] 返回
    -------
    P:
        预测值, P[-1]有效
    [4] 示例1
    --------
    >>> pred = []
    >>> trendObj = trendPredict(_windowSize=5, _smoothParam=0.9)
    >>> recorder, X, S1, S2, S3, P = trendObj.varsInitiate()
    >>> for i in range(dataQuant):
    >>>     recorder = trendObj.update(_newData=data[i], _recorder=recorder)
    >>>     X, S1, S2, S3, P = trendObj.trendPredict(recorder, X, S1, S2, S3, P)
    >>>     pred.append(P[-1])
    """

    # ===== 属性初始化 ===== #
    def __init__(self, **kwargs):
        self.windowSize = 5 if '_windowSize' not in kwargs.keys() else kwargs['_windowSize']
        self.smoothParam = 0.9 if '_smoothParam' not in kwargs.keys() else kwargs['_smoothParam']
        self._recordShape = []
        self.lineRecord = []

    # ===== 变量初始化 ===== #
    def varsInitiate(self):
        self._recordShape = 10 - (self.windowSize - 1)  # 预测对象数据缓存量
        recorder = np.zeros(self._recordShape, dtype=float)
        X = np.zeros([self._recordShape, 1], dtype=float)
        S1 = np.zeros([2, 1], dtype=float)
        S2 = np.zeros([2, 1], dtype=float)
        S3 = np.zeros([2, 1], dtype=float)
        P = [0]*2
        return recorder, X, S1, S2, S3, P

    # ===== 数据记录 ===== #
    def update(self, _newData: float, _recorder: list) -> np.ndarray:
        """
        :param _newData: float, 新入库数据, 如46.3
        :param _recorder: list[float], 近期记录的数据, 如[0. 0. 0. 0. 0. 0.]
        :return: np.ndarray[float], 新入库后数据所组成的矩阵，如[[46.3], [46.3], [46.3], [46.3], [46.3], [46.3]]
        """
        if sum(_recorder) == 0:  # 如果_recorder是初始化的值，则将新入数据复制展开
            _lineRecord = np.reshape([_newData]*np.shape(_recorder)[0], (-1, 1))
        else:
            _lineRecord = np.concatenate((_recorder, np.mat(_newData)), 0)
        res = _lineRecord[-self._recordShape:, :]
        return res

    # ===== 趋势计算 ===== #
    def trendPredict(self, _recorder, _X, _S1, _S2, _S3, _P):
        """
        [1] 参数
        ----------
        _recorder:
            list[float], 近期记录的数据, 如[0. 0. 0. 0. 0. 0.]
        _P:
            list[float, float]， 预测值， _P[-1]根据前序数据对当期数据的预测值
        [2] 返回
        -------
        _P:
            list[float, float]， 预测值， _P[-1]根据前序数据对当期数据的预测值 \n
        _X, _S1, _S2, _S3:
            缓存量
        [3] 备注
        -----
        *  _X _S1 _S2 _S3 _P 是必要的缓存量
        """
        # ===== 平滑处理 ==== #
        for i in range(np.shape(_recorder)[0]):
            if i + self.windowSize <= np.shape(_recorder)[0]:
                _X[i, :] = np.mean(_recorder[i:i + self.windowSize, :], axis=0)
        _X = _X[0: np.shape(_recorder)[0] - (self.windowSize - 1), :]
        # ===== 检查S1 S2 S3 是否更新 ==== #
        if (_S1 == np.zeros_like(_S1)).all():
            _S1[0, :] = np.average(_X, axis=0)
            _S2[0, :] = np.average(_X, axis=0)
            _S3[0, :] = np.average(_X, axis=0)
        else:
            _S1 = np.concatenate((_S1, np.zeros((1, np.shape(_S1)[1]))))[-2:, :]
            _S2 = np.concatenate((_S2, np.zeros((1, np.shape(_S2)[1]))))[-2:, :]
            _S3 = np.concatenate((_S3, np.zeros((1, np.shape(_S3)[1]))))[-2:, :]
        # ===== 计算S1 S2 S3 ==== #
        S_1 = lambda a, X_t, S1_t_1: a * X_t + (1 - a) * S1_t_1
        S_2 = lambda a, S1_t, S2_t_1: a * S1_t + (1 - a) * S2_t_1
        S_3 = lambda a, S2_t, S3_t_1: a * S2_t + (1 - a) * S3_t_1
        for i in range(np.shape(_S1)[1]):
            _S1[-1, i] = S_1(self.smoothParam, _X[-1, i], _S1[0, i])
            _S2[-1, i] = S_2(self.smoothParam, _S1[-1, i], _S2[0, i])
            _S3[-1, i] = S_3(self.smoothParam, _S2[-1, i], _S3[0, i])
        # ===== 计算At Bt Ct ==== #
        A_t = lambda S1_t, S2_t, S3_t: 3 * S1_t - 3 * S2_t + S3_t
        B_t = lambda a, S1_t, S2_t, S3_t: a / (2 * (1 - a) ** 2) * (
                (6 - 5 * a) * S1_t - 2 * (5 - 4 * a) * S2_t + (4 - 3 * a) * S3_t)
        C_t = lambda a, S1_t, S2_t, S3_t: (a ** 2 / 2 / (1 - a) ** 2) * (S1_t - 2 * S2_t + S3_t)
        At = np.zeros((1, np.shape(_recorder)[1]))
        Bt = np.zeros((1, np.shape(_recorder)[1]))
        Ct = np.zeros((1, np.shape(_recorder)[1]))
        for i in range(np.shape(_S1)[1]):
            At[0, i] = A_t(_S1[-1, i], _S2[-1, i], _S3[-1, i])
            Bt[0, i] = B_t(self.smoothParam, _S1[-1, i], _S2[-1, i], _S3[-1, i])
            Ct[0, i] = C_t(self.smoothParam, _S1[-1, i], _S2[-1, i], _S3[-1, i])
        # ===== 计算P ==== #
        P_T = lambda at, bt, ct, T: at + bt * T + ct * T ** 2
        cacheP = []
        for i in range(np.shape(_S1)[1]):
            cacheP.append(P_T(At[0, i], Bt[0, i], Ct[0, i], 1))
        P = _P + cacheP
        return _X, _S1, _S2, _S3, P[-2:]
