"""
包括bpNetworkTrain一个类

Classes
----------
bpNetworkTrain: BP神经网络训练，默认三层，包括输出层

Example
----------
>>> from commonMethods_zhaozl.toolbox.Method_bpNetworkTrain import bpNetworkTrain

"""

import os

import numpy as np  # numpy==1.18.5
import pandas as pd  # pandas==1.1.0
import matplotlib.pyplot as plt  # matplotlib==3.3.0
import joblib  # joblib==0.16.0
import tensorflow as tf  # tensorflow==2.1.0

from sklearn import preprocessing  # sklearn==0.0

tf.compat.v1.disable_eager_execution()


class bpNetworkTrain:
	"""
	BP神经网络训练，默认三层，包括输出层

	[1] 参数
	----------
	_inputSamples:
		dataframe, 网络的输入，形如DF([input1, input2], columns=['input1', 'input2'])
	_targetSamples:
		dataframe, 网络的输出，形如DF([output], columns=['output'])
	_neuronNum0:
		int, 神经元个数，形如5
	_neuronNum1:
		int, 神经元个数，形如1
	_neuronNum2:
		int, 神经元个数，形如1
	_batch:
		int, 每次进入训练的样本个数，形如10
	_epochSize:
		int, 循环迭代次数，形如20
	_trainGroupSize:
		int, 训练样本个数，剩余为测试样本，形如60000
	_exponential_decay_param:
		dict, 指数衰减参数，形如{learning_rate": 0.7, "global_step": 1000, "decay_steps": 1000, "decay_rate": 0.7}
	learning_rate:
		float, 初始化学习率，形如0.7
	global_step:
		int, 全局学习率更新样本数，形如1000
	decay_steps:
		int, 学习率更新样本数，形如1000
	decay_rate:
		float, 学习率的更新率，形如0.7

	[2] 数据准备
	--------
	>>> databaseName = 'bearing_pad_temper'
	>>> tableName = '轴承瓦温20200320_20200327_原始数据'
	>>> content = "汽机转速,汽机润滑油冷油器出口总管油温1,发电机励端轴瓦温度"
	>>> condition = "(时间戳>='2020-03-20 16:18:03') and (时间戳<='2020-03-25 16:20:11')"
	>>> mysqlObj = mysqlOperator(databaseName=databaseName, tableName=tableName)
	>>> data = mysqlObj.selectData(content=content, condition=condition)
	>>> speed = data['汽机转速']
	>>> outletMainPipeOilTemper = data['汽机润滑油冷油器出口总管油温1']
	>>> exciteBearingPadTemper = data['发电机励端轴瓦温度']
	>>> # ===== Step:1 ===== #
	>>> inputSample = pd.concat([speed, outletMainPipeOilTemper], axis=1)
	>>> targetSample = pd.DataFrame(exciteBearingPadTemper)

	[3] 网络参数设置
	--------
	>>> _neuronNum0, _neuronNum1, _neuronNum2 = 5, 1, 1
	>>>	_batch, _epochSize, _trainGroupSize = 10, 20, 60000
	>>>	_exponential_decay_param = {"learning_rate": 0.7, "global_step": 1000, "decay_steps": 1000, "decay_rate": 0.7}
	>>>	_inputSamples = inputSample
	>>>	_targetSamples = targetSample

	[4] 网络训练
	--------
	>>> bpNetworkTrain(_neuronNum0, _neuronNum1, _neuronNum2, _batch, _epochSize, _trainGroupSize,
	>>> _exponential_decay_param, _inputSamples, _targetSamples, verbose=True, save=True,
	>>> savePath="E:\\99.Python_Develop\\[98]Common_Methods\\commonMethods")
	"""
	def __init__(self, _neuronNum0: int, _neuronNum1: int, _neuronNum2: int,
	             _batch: int, _epochSize: int, _trainGroupSize: int,
	             _exponential_decay_param: dict or None,
	             _inputSamples: pd.DataFrame, _targetSamples: pd.DataFrame,
	             verbose=True, **kwargs):

		# ===== Params Check ===== #
		if ('save' not in kwargs.keys()) and ('savePath' not in kwargs.keys()):
			msg = 'Parameters [save] and [savePath] are not both set.'
			print(msg)
			exit(-1)
		elif 'savePath' in kwargs.keys():
			savePath = kwargs['savePath']
		else:
			msg = 'Parameter [savePath] are not set, set save path to Current.'
			print(msg)
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
