# -*- coding: utf-8 -*-

"""这里是一些Master的基础API接口。
"""


def BanUser(uid, banTime, reason):
	# type: (int, int, str) -> bool
	"""
	封禁某个玩家

	Args:
		uid            int            玩家uid
		banTime        int            封禁时间，单位为秒，-1表示永封
		reason         str            封禁原因，使用utf8编码。

	Returns:
		bool           True设置成功，False表示失败。失败后请延迟一帧后重试
	"""
	pass


def GetCommonConfig():
	"""
	获取服务器公共配置，包括所有服务器和db的配置，具体参见备注

	Returns:
		dict           配置内容
	"""
	pass


def IsService(serverId):
	# type: (int) -> bool
	"""
	服务器是否是service服

	Args:
		serverId       int            服务器id

	Returns:
		bool           True表示是service，False不是service
	"""
	pass


def SetLoginStratege(func):
	# type: (function) -> bool
	"""
	设置玩家登陆选服策略，要求服务器启动后加载mod时候设置

	Args:
		func           function       计算玩家登陆服务器，包含两个参数：第一个参数为玩家uid；第二个参数为回调函数，执行后续登陆逻辑，无论登陆是否成功，必须要执行，回调函数只有一个参数，也即目标服务器。

	Returns:
		bool           True设置成功，False表示失败。失败后请延迟一帧后重试
	"""
	pass


def SilentByUID(uid, banTime, reason):
	# type: (int, int, str) -> bool
	"""
	禁言某个玩家

	Args:
		uid            int            玩家uid
		banTime        int            禁言时间，单位为秒，-1表示永封
		reason         str            禁言原因，使用utf8编码

	Returns:
		bool           True设置成功，False表示失败。失败后请延迟一帧后重试
	"""
	pass


def UnBanUser(uid):
	# type: (int) -> bool
	"""
	解除某个玩家的封禁

	Args:
		uid            int            玩家uid

	Returns:
		bool           True设置成功，False表示失败。失败后请延迟一帧后重试
	"""
	pass


def UnSilentByUID(uid):
	# type: (int) -> bool
	"""
	解除某个玩家的禁言

	Args:
		uid            int            玩家uid

	Returns:
		bool           True设置成功，False表示失败。失败后请延迟一帧后重试
	"""
	pass

