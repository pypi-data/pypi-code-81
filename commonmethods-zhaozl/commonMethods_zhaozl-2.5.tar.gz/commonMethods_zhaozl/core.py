import os
import time
import datetime as dt
import errno
import io
import math
import os
import re
import struct
import sys
import warnings

import pymysql  # PyMySQL==0.10.0
import numpy as np  # numpy==1.18.5
import pandas as pd  # pandas==1.1.0
import matplotlib.pyplot as plt  # matplotlib==3.3.0
from sklearn import preprocessing  # sklearn==0.0
import joblib  # joblib==0.16.0

from .Method_comtradeParse import Method_comtradeParse as Method

pd.set_option('display.max_columns', 10000, 'display.width', 10000, 'max_rows', 50,
              'display.unicode.east_asian_width', True)


class bpNetworkRun:
	"""
	【注意】：默认的网络模型存储地址为...netWork \n
	【执行流程与参数说明】 \n
		①网络参数调取 \n
		e.g:
			savePath = 'E:\\99.Python_Develop\\[98]Common_Methods\\commonMethods' \n
			bpNetworkRun.printTrainedNetwork(savePath)  # 调取网络参数 \n
		②网络参数设置 \n
		e.g:
			networkParams = {'b': b,'b0': b0, 'b1': b1,'b2': b2, 'iw0': iw0,'iw1': iw1,'iw2':iw2, 'lw': lw}
		③网络计算 \n
		e.g:
			res = bpNetworkRun(_networkParams=networkParams, _savePath=savePath, _inputSamples=inputSample, _targetSamples=targetSample).networkOutput  # 使用网络参数计算

	    ④param:
			inputSample，网络的输入，dataframe，形如“DF([input1, input2], columns=['input1', 'input2'])” \n
			networkOutput，网络的输出，ndarray，形如“[[77.2], [77.1], [77.4], ...]”

	"""

	def __init__(self, **kwargs):
		self.networkOutput = []
		if '_networkParams' in kwargs.keys():
			self.b = kwargs['_networkParams']['b']
			self.b0 = kwargs['_networkParams']['b0']
			self.b1 = kwargs['_networkParams']['b1']
			self.b2 = kwargs['_networkParams']['b2']
			self.iw0 = kwargs['_networkParams']['iw0']
			self.iw1 = kwargs['_networkParams']['iw1']
			self.iw2 = kwargs['_networkParams']['iw2']
			self.lw = kwargs['_networkParams']['lw']
		if '_savePath' in kwargs.keys():
			savePath = kwargs['_savePath'] + '\\netWork\\'
		else:
			savePath = os.getcwd() + '\\netWork\\'
		if '_inputSamples' in kwargs.keys() and '_targetSamples' in kwargs.keys():
			inputSamples = kwargs['_inputSamples']
			targetSamples = kwargs['_targetSamples']
			# ===== Load scalers of input and output ===== #
			self.scalerInput = joblib.load(savePath + 'scalerInput')
			self.scalerTarget = joblib.load(savePath + 'scalerTarget')
			# ===== Transfer input and output to std ===== #
			self.inputSamplesStd = self.scalerInput.transform(inputSamples)
			self.targetSamplesStd = self.scalerTarget.transform(targetSamples)

		def sigmoid(x_Array):
			res = np.zeros_like(x_Array)
			rows, cols = np.shape(x_Array)
			for col in range(cols):
				for row in range(rows):
					x = x_Array[row, col]
					res[row, col] = 1 / (1 + np.exp(-x))
			return res

		def tanh(x_Array):
			res = np.zeros_like(x_Array)
			rows, cols = np.shape(x_Array)
			for col in range(cols):
				for row in range(rows):
					x = x_Array[row, col]
					res[row, col] = (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))
			return res

		cache = sigmoid(np.add(np.matmul(self.inputSamplesStd, self.iw0), self.b0))
		cache = sigmoid(np.add(np.matmul(cache, self.iw1), self.b1))
		cache = sigmoid(np.add(np.matmul(cache, self.iw2), self.b2))
		resFromFormula = tanh(np.add(np.matmul(cache, self.lw), self.b))
		self.networkOutput = self.scalerTarget.inverse_transform(resFromFormula)

	@staticmethod
	def printTrainedNetwork(_savePath, _docName='netWork'):
		from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file  # tensorflow==2.1.0

		# ===== Print Network Params ===== #
		model_path = _savePath + '\\' + _docName + '\\Network.ckpt'
		print_tensors_in_checkpoint_file(model_path, tensor_name="", all_tensors=True)


class bpNetworkTrain:
	"""
	【注意】：训练结束前需要保证savePath下具有路径netWork \n
	【执行流程与参数说明】 \n
		①数据准备 \n
		e.g:
			# ===== 数据准备 ===== # \n
			databaseName = 'bearing_pad_temper' \n
			tableName = '轴承瓦温20200320_20200327_原始数据' \n
			content = "汽机转速,汽机润滑油冷油器出口总管油温1,发电机励端轴瓦温度" \n
			condition = "(时间戳>='2020-03-20 16:18:03') and (时间戳<='2020-03-25 16:20:11')" \n
			mysqlObj = mysqlOperator(databaseName=databaseName, tableName=tableName) \n
			data = mysqlObj.selectData(content=content, condition=condition) \n
			speed = data['汽机转速'] \n
			outletMainPipeOilTemper = data['汽机润滑油冷油器出口总管油温1'] \n
			exciteBearingPadTemper = data['发电机励端轴瓦温度'] \n
			# ===== Step:1 ===== # \n
			inputSample = pd.concat([speed, outletMainPipeOilTemper], axis=1) \n
			targetSample = pd.DataFrame(exciteBearingPadTemper) \n
		②网络参数设置 \n
		e.g:
			# ===== Net Params ===== # \n
			_neuronNum0, _neuronNum1, _neuronNum2 = 5, 1, 1 \n
			_batch, _epochSize, _trainGroupSize = 10, 20, 60000 \n
			_exponential_decay_param = {"learning_rate": 0.7, "global_step": 1000, "decay_steps": 1000, "decay_rate": 0.7} \n
			_inputSamples = inputSample \n
			_targetSamples = targetSample \n
		③网络训练 \n
		e.g:
			# ===== Net Train ===== # \n
			bpNetworkTrain(_neuronNum0, _neuronNum1, _neuronNum2, \n
			               _batch, _epochSize, _trainGroupSize, \n
			               _exponential_decay_param, \n
			               _inputSamples, _targetSamples, \n
			               verbose=True, \n
			               save=True, \n
			               savePath="E:\\99.Python_Develop\\[98]Common_Methods\\commonMethods")
		④param:
			_inputSamples，网络的输入，dataframe，形如“DF([input1, input2], columns=['input1', 'input2'])” \n
			_targetSamples，网络的输出，dataframe，形如“DF([output], columns=['output'])” \n
			_neuronNum0，神经元个数，int，形如“5” \n
			_neuronNum1，神经元个数，int，形如“1” \n
			_neuronNum2，神经元个数，int，形如“1” \n
			_batch，每次进入训练的样本个数，int，形如“10” \n
			_epochSize，循环迭代次数，int，形如“20” \n
			_trainGroupSize，训练样本个数，剩余为测试样本，int，形如“60000” \n
			_exponential_decay_param，指数衰减参数，dict，形如{learning_rate": 0.7, "global_step": 1000, "decay_steps": 1000, "decay_rate": 0.7} \n
			learning_rate，初始化学习率，float，形如“0.7” \n
			global_step，全局学习率更新样本数，int，形如“1000” \n
			decay_steps，学习率更新样本数，int，形如“1000” \n
			decay_rate，学习率的更新率，float，形如“0.7” \n
	"""

	def __init__(self, _neuronNum0: int, _neuronNum1: int, _neuronNum2: int,
	             _batch: int, _epochSize: int, _trainGroupSize: int,
	             _exponential_decay_param: dict or None,
	             _inputSamples: pd.DataFrame, _targetSamples: pd.DataFrame,
	             verbose=True, **kwargs):
		import tensorflow as tf  # tensorflow==2.1.0

		tf.compat.v1.disable_eager_execution()
		# ===== Params Check ===== #
		if ('save' not in kwargs.keys()) and ('savePath' not in kwargs.keys()):
			msg = 'Parameters [save] and [savePath] are not both set.'
			printWithColor(_msg=msg, _displayStyle='bold', _fontColor='white', _backColor='red', _prefix='', _suffix='')
			exit(-1)
		elif 'savePath' in kwargs.keys():
			savePath = kwargs['savePath']
		else:
			msg = 'Parameter [savePath] are not set, set save path to Current.'
			printWithColor(_msg=msg, _displayStyle='bold', _fontColor='red', _backColor='yellow', _prefix='',
			               _suffix='')
			savePath = os.getcwd()
		_exponential_decay_param_default = {"learning_rate": 0.7, "global_step": 1000, "decay_steps": 1000,
		                                    "decay_rate": 0.7}
		if "_exponential_decay_param" in kwargs.keys():
			_cache = kwargs['_exponential_decay_param']
		else:
			_cache = _exponential_decay_param_default
		learning_rate = _cache['learning_rate']
		global_step = _cache['global_step']
		decay_steps = _cache['decay_steps']
		decay_rate = _cache['decay_rate']
		# ===== Samples Define ===== #
		errorRecord = []
		varNum = np.shape(_inputSamples.values)[1]
		trainInput = _inputSamples.values[0:_trainGroupSize, :]
		trainTarget = _targetSamples.values[0:_trainGroupSize, :]
		valInput = _inputSamples.values[_trainGroupSize:, :]
		valOutput = _targetSamples.values[_trainGroupSize:, :]
		# ===== Samples Scale ===== #
		scalerInput = preprocessing.MinMaxScaler(feature_range=(0, 1))
		scalerInput.fit(_inputSamples)
		_trainInputSamplesStd = scalerInput.transform(trainInput)
		scalerTarget = preprocessing.MinMaxScaler(feature_range=(0, 1))
		scalerTarget.fit(_targetSamples)
		_trainTargetSamplesStd = scalerTarget.transform(trainTarget)
		_valInputSamplesStd = scalerInput.transform(valInput)
		_valOutputSamplesStd = scalerTarget.transform(valOutput)
		# ===== Define Network Params ===== #
		neuronNum0 = _neuronNum0
		neuronNum1 = _neuronNum1
		neuronNum2 = _neuronNum2
		batch = _batch
		epochSize = _epochSize
		trainGroupSize = _trainGroupSize
		iterSize = int(trainGroupSize / batch)
		# ===== Network Initiate ===== #
		placeholderInit = tf.compat.v1.placeholder
		variableInit = tf.compat.v1.Variable
		randomInit = tf.compat.v1.random.uniform
		inputHolder = placeholderInit(dtype=float, name='inputHolder')
		outputHolder = placeholderInit(dtype=float, name='outputHolder')
		iw0 = variableInit(randomInit(shape=(varNum, neuronNum0), minval=-1, maxval=1, dtype=float), name='iw0')
		b0 = variableInit(randomInit(shape=(1, neuronNum0), minval=-1, maxval=1, dtype=float), name='b0')
		iw1 = variableInit(randomInit(shape=(neuronNum0, neuronNum1), minval=-1, maxval=1, dtype=float), name='iw1')
		b1 = variableInit(randomInit(shape=(1, neuronNum1), minval=-1, maxval=1, dtype=float), name='b1')
		iw2 = variableInit(randomInit(shape=(neuronNum1, neuronNum2), minval=-1, maxval=1, dtype=float), name='iw2')
		b2 = variableInit(randomInit(shape=(1, neuronNum2), minval=-1, maxval=1, dtype=float), name='b2')
		lw = variableInit(randomInit(shape=(neuronNum2, 1), minval=-1, maxval=1, dtype=float), name='lw')
		b = variableInit(randomInit(shape=(1, 1), minval=-1, maxval=1, dtype=float), name='b')
		# ===== Define Network Function ===== #
		output = tf.tanh(
			tf.add(tf.matmul(tf.sigmoid(tf.add(tf.matmul(tf.sigmoid(tf.add(tf.matmul(tf.sigmoid(tf.add(tf.matmul(
				inputHolder, iw0), b0)), iw1), b1)), iw2), b2)), lw), b),
			name='predictModel')
		loss = tf.reduce_mean(tf.square(tf.subtract(outputHolder, output)), axis=0, name='loss')
		learningRateParams = tf.compat.v1.train.exponential_decay(learning_rate=learning_rate,
		                                                          global_step=global_step,
		                                                          decay_steps=decay_steps,
		                                                          decay_rate=decay_rate)
		optimizer = tf.compat.v1.train.AdadeltaOptimizer(learningRateParams).minimize(loss)
		initiator = tf.compat.v1.global_variables_initializer()
		# ===== Training ===== #
		sess = tf.compat.v1.Session()
		sess.run(initiator)

		if verbose:
			plt.figure(1)

		epoch = 1
		while epoch <= epochSize:
			for i in np.arange(iterSize) + 1:
				if i * batch <= trainGroupSize:
					sess.run(optimizer, feed_dict={inputHolder: _trainInputSamplesStd[(i - 1) * batch: i * batch, :],
					                               outputHolder: _trainTargetSamplesStd[(i - 1) * batch: i * batch, :]})
			error = sess.run(loss, feed_dict={inputHolder: _trainInputSamplesStd, outputHolder: _trainTargetSamplesStd})
			print('Error of epoch %d / %d, is ===> %f ' % (epoch, epochSize, error))
			epoch = epoch + 1
			errorRecord.append(error[0])

			if verbose >= 1:
				plt.xlim((0, epochSize))
				plt.plot(errorRecord, 'b-')
				plt.pause(0.2)
		# ===== Validation ===== #
		predictResultStd = sess.run(output, feed_dict={inputHolder: _valInputSamplesStd})
		predictResult = scalerTarget.inverse_transform(predictResultStd)
		# ===== Output Figuring ===== #
		if verbose:
			plt.figure(2)
			plt.subplot(411)
			plt.plot(predictResult)
			plt.plot(valOutput)
			plt.legend()
			plt.subplot(412)
			plt.plot(predictResult - valOutput)
			plt.subplot(413)
			plt.plot(errorRecord)
			plt.xlim(1, 30)
			plt.subplot(414)
			plt.hist(predictResult - valOutput, bins=200)
			plt.show()
		# ===== Model Saving ===== #
		saveOrNot = 'y'  # input('Save Model <=== Y/N:')
		if saveOrNot in ['y', 'Y']:
			modelSaveAddress = savePath + '\\netWork\\'
			joblib.dump(scalerInput, modelSaveAddress + 'scalerInput')
			joblib.dump(scalerTarget, modelSaveAddress + 'scalerTarget')
			tf.compat.v1.train.Saver().save(sess, modelSaveAddress + 'Network.ckpt')
		sess.close()


class mysqlOperator:
	"""
    【执行流程与参数说明】 \n
    ①实例化对象
    e.g:
            obj = objectMySQL(databaseName='bearing_pad_temper') \n
            print(obj)
    param:
            databaseName，数据库名称，str，必要参数，形如“bearing_pad_temper” \n
            tableName，数据表名称，str，必要参数，形如“轴承瓦温20200320_20200327_原始数据” \n
            host，数据库名称，int，默认值“localhost” \n
            port，数据库名称，int，默认值3306 \n
            userID，数据库名称，str，默认值“root” \n
            password，数据库名称，str，默认值“000000” \n
    """

	def __init__(self, **kwargs):
		self.dataBaseName = kwargs['databaseName']
		self.tableName = kwargs['tableName']
		host = kwargs['host'] if 'host' in kwargs.keys() else 'localhost'
		port = kwargs['port'] if 'port' in kwargs.keys() else 3306
		userID = kwargs['userID'] if 'userID' in kwargs.keys() else 'root'
		password = kwargs['password'] if 'password' in kwargs.keys() else '000000'
		self.__con__ = pymysql.connect(host=host, port=port, db=self.dataBaseName, user=userID, passwd=password,
		                               charset='utf8mb4')
		self.__cur__ = self.__con__.cursor()

	def createTable(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；columns：列名+数据类型+缺省控制，字符串形如'test01 float null'
        :return: None
        '''
		self.__cur__.execute('create table if not exists ' + kwargs['tableName'] + '(' + kwargs['columns'] + ')')
		self.__cur__.close()
		self.__con__.close()

	def addColumn(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；column：初始列名、数据类型、缺省值，字符串形如'test02 float null'
        :return: None
        '''
		self.__cur__.execute(
			'alter table ' + self.dataBaseName + '.' + kwargs['tableName'] + ' add column ' + kwargs['column'])
		self.__cur__.close()
		self.__con__.close()

	def insertRow(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；values：新增值，字符串形如'510, 512'
        :return: None
        '''
		self.__cur__.execute('insert into ' + kwargs['tableName'] + ' value ' + '(' + kwargs['values'] + ')')
		self.__cur__.close()
		self.__con__.close()

	def updateValue(self, **kwargs):
		'''
        :param kwargs: tableName：表单名；targetColumn：更新列名，字符串形如'test02'；value：更新值，字符串形如'110'
        :return: None
        '''
		com = 'update ' + self.dataBaseName + '.' + kwargs['tableName'] + ' set ' + kwargs['targetColumn'] + '=' + \
		      kwargs['value']
		self.__cur__.execute(com)
		self.__cur__.close()
		self.__con__.close()

	def selectData(self, **kwargs):
		"""
            content: 需要调用的列名，str，默认为查询数据的样本数"count(*)"，形如”'汽机润滑油冷油器出口总管油温1,发电机励端轴瓦温度'“  \n
            condition: 调用数据的条件，str，默认为全部数据，形如“'(时间戳>=\'2020-03-20 16:18:03\') and (时间戳<=\'2020-03-20 16:18:11\')'”  \n
            return: 调取的数据，df
            【执行流程与参数说明】 \n
            e.g:
                obj = objectMySQL(databaseName='bearing_pad_temper', tableName='轴承瓦温20200320_20200327_原始数据') \n
                data = obj.selectData(content=content, condition=condition) \n
                print(data) \n
        """
		condition = kwargs['condition'] if 'condition' in kwargs.keys() else False
		content = kwargs['content'] if 'content' in kwargs.keys() else 'count(*)'
		if condition:
			com = 'select ' + content + ' from ' + self.dataBaseName + '.' + self.tableName + ' where ' + kwargs[
				'condition']
		else:
			com = 'select ' + content + ' from ' + self.dataBaseName + '.' + self.tableName
		self.__cur__.execute(com)
		res = self.__cur__.fetchall()
		self.__cur__.close()
		self.__con__.close()
		if content != 'count(*)':
			res = pd.DataFrame(res, columns=content.split(","))
		else:
			res = pd.DataFrame({'inspectedDataSize': [res[0][0]]})
		return res


def code2Name(_kksCodes: list, _dictNames: list, _kksCode: list, _verbose=True):
	"""
	:param _kksCodes: 编码的字典 list
	:param _dictNames: 名称的字典 list
	:param _kksCode: 需要转译的编码 list
	:param _verbose: 是否显示对输入字典和待转译编码的检查结果 Boolean
	:return: 转译完成的名称 list
	【执行流程与参数说明】 \n
	e.g:
		a = code2Name(kksCode, dictName, ['ED009HP2MUB01UU008AA01J3DG006EA01'])
		print(a)
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


class timeTrans:
	"""
	【执行流程与参数说明】 \n
	①实例化对象
    e.g:
            timestamp = [1617159398000, 1617259398000, 1617359398000, 1617359398] \n
			obj = timeTrans(unixTime=timestamp, format='%Y/%m/%d %H:%M:%S') \n
			print(obj.timeStr) \n
    param:
            unixTime:秒级或毫秒级时间，int or list，形如1616059398000或[1617159398000, 1617259398000, 1617359398000, 1617359398] \n
            format:字符串型时间，str or None，形如“%Y/%m/%d %H:%M:%S” \n
	"""

	def __init__(self, **kwargs):
		def unixTime2strTime(_unixTime, _format):
			unixTimeLength = len(str(_unixTime))
			second = _unixTime if unixTimeLength == 10 else _unixTime / 1000
			_strTime = time.strftime(_format, time.localtime(second))
			return _strTime

		self.unixTime = kwargs['unixTime']
		self.format = kwargs['format'] if 'format' in kwargs.keys() else "%Y-%m-%d %H:%M:%S"
		isInt = isinstance(self.unixTime, int)
		isTuple = isinstance(self.unixTime, list)
		if isInt:
			self.timeStr = unixTime2strTime(self.unixTime, self.format)
		elif isTuple:
			timeStr = []
			for item in self.unixTime:
				_timeStr = unixTime2strTime(item, self.format)
				timeStr.append(_timeStr)
			self.timeStr = timeStr
		else:
			self.timeStr = None


def printWithColor(_msg, _prefix="\n\n", _suffix="\n",
                   _displayStyle="default",
                   _fontColor="white",
                   _backColor=None):
	"""
	e.g:
	    printWithColor("11111111111111", _displayStyle='bold', _fontColor='red', _backColor='grey')
	:param _msg: 信息,str
	:param _displayStyle: 呈现模式,str,可选项['default', 'bold', 'italic', 'underline', 'reverse']
	:param _fontColor: 字体颜色,str,可选项['white', 'red', 'green', 'yellow', 'blue', 'purple', 'grey']
	:param _backColor: 背景色,str,可选项['white', 'red', 'green', 'yellow', 'blue', 'purple', 'grey']
	:param _prefix: 前缀,str
	:param _suffix: 后缀,str
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


# from commonMethods_zhaozl.Method_comtradeParse import ComtradeParser
# from commonMethods_zhaozl.Method_processBar import processBar
# from commonMethods_zhaozl.Method_trendAnalyzer import trendAnalyzer, trendPredict