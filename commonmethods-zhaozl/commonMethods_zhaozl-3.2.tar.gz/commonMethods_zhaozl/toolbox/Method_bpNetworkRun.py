"""
包括bpNetworkRun一个类

Classes
----------
bpNetworkRun: BP神经网络计算

Example
----------
>>> from commonMethods_zhaozl.toolbox.Method_bpNetworkRun import bpNetworkRun

"""

import os

import numpy as np  # numpy==1.18.5
import joblib  # joblib==0.16.0
import tensorflow as tf  # tensorflow==2.1.0

from tensorflow.python.tools.inspect_checkpoint import print_tensors_in_checkpoint_file  # tensorflow==2.1.0

tf.compat.v1.disable_eager_execution()


class bpNetworkRun:
	"""
	BP神经网络计算

	[1] 参数
	----------
	inputSample:
		dataframe, 网络的输入，形如DF([input1, input2], columns=['input1', 'input2'])

	[2] 返回
	-------
	networkOutput:
		ndarray, 网络的输出，形如[[77.2], [77.1], [77.4], ...]

	[3] 调取网络参数
	--------
	>>> savePath = 'E:\\99.Python_Develop\\[98]Common_Methods\\commonMethods'
	>>> bpNetworkRun.printTrainedNetwork(savePath)

	[4] 网络参数设置
	--------
	>>> networkParams = {'b': b,'b0': b0, 'b1': b1,'b2': b2, 'iw0': iw0,'iw1': iw1,'iw2':iw2, 'lw': lw}

	[5] 网络计算
	--------
	>>> res = bpNetworkRun(_networkParams=networkParams, _savePath=savePath, _inputSamples=inputSample,
	>>> _targetSamples=targetSample).networkOutput

	[6] 备注
	--------
	* 默认的网络模型存储地址为……/……/netWork
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
		"""
		根据提供的模型文件地址和名称提取并打印网络参数

		:param _savePath: str, 地址
		:param _docName: str, 模型名称
		:return: None
		"""
		# ===== Print Network Params ===== #
		model_path = _savePath + '\\' + _docName + '\\Network.ckpt'
		print_tensors_in_checkpoint_file(model_path, tensor_name="", all_tensors=True)