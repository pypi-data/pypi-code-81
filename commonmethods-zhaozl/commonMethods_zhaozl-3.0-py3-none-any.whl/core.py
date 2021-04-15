"""
内容包括：
timeTrans
code2Name
printWithColor
mysqlOperator
bpNetworkTrain
bpNetworkRun
comtradeParse
processBar
trendAnalyzer
bounceAnalyzer
evennessDetermine

Classes
----------
* timeTrans: 通过输入list(int)或者int形式的时间戳unixTimestamp，与形如'%Y/%m/%d %H:%M:%S'的formation，对时间戳进行计算并输出string
* mysqlOperator: mysql数据库操作， 包括创建table、添加列、新增数据、更新数据、查询数据
* bpNetworkTrain: BP神经网络训练，默认三层，包括输出层
* bpNetworkRun: BP神经网络计算
* comtradeParser: 通过输入符合comtrade规范的文件名，对数据内容进行输出
* processBar: 在打印的循环体中输出进度条
* trendAnalyzer:
	** trendAnalyzer: 使用三阶滑动平均与一阶导对输入数据的快速/缓慢的上升/下降状态进行判断

	** trendPredict: 通过不断输入一时间序列的数值，顺序地对所定义窗口1内的数值进行三阶滑动平均处理，并计算所定义窗口2内的时序数据一阶导，通过
	对所定义窗口3内一阶导数据均值进行判断，以确定原始数据的上升/下降情况，包括：是否处理上升/下降状态，是否处于快速/慢速    变化状态
* bounceAnalyzer: 对新传入的数据进行缓存记录，通过平均值计算等方法对跳变状态与持续跳变状态进行判断
* evennessDetermine: 包括两种方法
    ** compareWithOthersAverage, 同类测点温度值稳定，单一测点温度测量在正常范围内，但明显高于除本测点外的同类平均值

    ** circleSimilarity, 全体测点与均值圆的相似度, 使用向量间的相似度进行衡量

	** modulo， 向量的模计算

	** angleCal， 向量间夹角余弦值计算

Functions
----------
* code2Name: 通过输入词典对传入code进行转译同时使用_verbose控制是否显示对字典的预检验
* printWithColor: 打印具有颜色和特定格式的字符串

Example
----------
>>> from Method_trendAnalyzer import trendAnalyzer, trendPredict

"""

import numpy as np  # numpy==1.18.5
import pandas as pd  # pandas==1.1.0


pd.set_option('display.max_columns', 10000, 'display.width', 10000, 'max_rows', 50,
              'display.unicode.east_asian_width', True)


def code2Name(_kksCodes: list, _dictNames: list, _kksCode: list, _verbose=True):
	"""
	通过输入词典对传入code进行转译同时使用_verbose控制是否显示对字典的预检验

	[1] 参数
	----------
	_kksCodes:
	    list, 编码的字典
	_dictNames:
	    list, 名称的字典
	_kksCode:
	    list, 需要转译的编码
	_verbose:
	    Boolean, 是否显示对输入字典和待转译编码的检查结果

	[3] 返回
	-------
	-/-:
	    list, 转译完成的名称

	[4] 示例1
	--------
	>>> a = code2Name(kksCode, dictName, ['ED009HP2MUB01UU008AA01J3DG006EA01'])
	>>> print(a)
	"""
	# 检查输入的清单是否符合基本要求
	len_kksCodes = len(_kksCodes)
	len_kksCodes_unique = len(pd.unique(_kksCodes))
	len_dictNames = len(_dictNames)
	len_dictNames_unique = len(pd.unique(_dictNames))
	if _verbose:
		checkStr01 = "待检编码中有重复项 X " if isinstance(_kksCode, list) and len(np.unique(_kksCode)) != len(
			_kksCode) else "待检编码中没有重复项 √ "
		checkStr02 = "编码中没有重复项 √ " if len_kksCodes == len_kksCodes_unique else "编码中有重复项 X "
		checkStr03 = "名称中没有重复项 √ " if len_dictNames == len_dictNames_unique else "名称中有重复项 (允许) "
		print("#" * 2 * (2 + max([len(checkStr01), len(checkStr02), len(checkStr03)])))
		print('\t', checkStr01, '\n\t', checkStr02, '\n\t', checkStr03)
		print("#" * 2 * (2 + max([len(checkStr01), len(checkStr02), len(checkStr03)])))
	# 字典以中文名称为依据，升序排列
	_dict = pd.DataFrame({'kksCodes': _kksCodes, 'dictNames': _dictNames}).sort_values(by=['dictNames'])
	# 查询
	_kksName = []
	if isinstance(_kksCode, list):
		for eachCode_toReplace in _kksCode:
			queryRes = _dict.query("kksCodes.str.contains(\'" + eachCode_toReplace + "\')", engine='python')
			res = queryRes['dictNames'].values
			if np.shape(res)[0] == 0:
				print(">>> 注意：对象kksCode未找到kksName，此kksCode是 %s" % (eachCode_toReplace))
			elif np.shape(res)[0] >= 2:
				print(">>> 错误: 单个kksCode对应了多个kksName，这些kksCode是%s，这些kksName是%s" % (
					queryRes['kksCodes'].values, queryRes['dictNames'].values))
			if res:
				_kksName = _kksName + res.tolist()
			else:
				_kksName.append(eachCode_toReplace)
		return _kksName


def printWithColor(_msg, _prefix="\n\n", _suffix="\n",
                   _displayStyle="default",
                   _fontColor="white",
                   _backColor=None):
	"""
	打印具有颜色和特定格式的字符串

	:param _msg: str, 需要打印的信息
	:param _displayStyle: str, 需要呈现的模式, 可选项, ['default', 'bold', 'italic', 'underline', 'reverse'], default, "default"
	:param _fontColor: str, 字体颜色, 可选项, ['white', 'red', 'green', 'yellow', 'blue', 'purple', 'grey'], default, "white"
	:param _backColor: str, 背景色, 可选项, ['white', 'red', 'green', 'yellow', 'blue', 'purple', 'grey'], default, None
	:param _prefix: str, 前缀
	:param _suffix: str, 后缀
	:returns: e.g printWithColor("11111111111111", _displayStyle='bold', _fontColor='red', _backColor='grey')
	"""
	displayDict = ['default', 'bold', '-', 'italic', 'underline', '-', '-', 'reverse', '-']
	fontDict = ['white', 'red', 'green', 'yellow', 'blue', 'purple', '-', 'grey']
	backDict = ['white', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'grey']
	if _backColor:
		_display = str(displayDict.index(_displayStyle))
		_font = "3" + str(fontDict.index(_fontColor))
		_back = "4" + str(backDict.index(_backColor))
		print(_prefix + "\033[" + _display + ";" + _font + ";" + _back + "m" + _msg + "\033[0m" + _suffix)
	else:
		_display = str(displayDict.index(_displayStyle))
		_font = "3" + str(fontDict.index(_fontColor))
		print(_prefix + "\033[" + _display + ";" + _font + "m" + _msg + "\033[0m" + _suffix)







