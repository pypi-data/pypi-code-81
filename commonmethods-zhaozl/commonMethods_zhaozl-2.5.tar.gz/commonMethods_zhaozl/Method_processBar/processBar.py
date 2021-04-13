import sys
import time


class processBar:
	"""
	在打印的循环体中输出进度条

	[1] 参数
	----------
	_before:
		str, 进度条未执行时的样式, 一个字符, optional, default "="
	_after:
		str, 进度条已执行时的样式, 一个字符, optional, default ">"
	_coef:
		int, 进度条总长度系数, optional, default 1
	_total:
		int, 进度条总长度, optional, default 100

	[2] 方法
	----------
	_refresh:
		更新一次进度条

	[×] 返回
	-------

	[4] 示例1
	--------
	>>> barObj = processBar()
	>>> for i in range(100):
	>>>     barObj.refresh()
	>>>     time.sleep(0.1)

	[5] 示例2
	--------
	>>> barObj = processBar(_before='#', _after='>', _coef=1)
	>>> for i in range(100):
	>>>     barObj.refresh()
	>>>     time.sleep(0.1)

	[×] 备注
	-----

	"""

	def __init__(self, **kwargs):
		self.before = "=" if "_before" not in kwargs.keys() else kwargs['_before']
		self.after = ">" if "_after" not in kwargs.keys() else kwargs['_after']
		self.coef = 1 if "_coef" not in kwargs.keys() else kwargs['_coef']
		self.left = 100 * self.coef if "_total" not in kwargs.keys() else kwargs['_total']
		self.current = 0
		self.format = "\r【%3.0f%%】 %s"

	def refresh(self):
		self.current = self.current + 1 * self.coef
		self.left = self.left - 1 * self.coef
		_percent = 100 * self.current/(self.current + self.left)
		_percentage = self.after * self.current + self.before * self.left
		sys.stdout.write(self.format % (_percent, _percentage))