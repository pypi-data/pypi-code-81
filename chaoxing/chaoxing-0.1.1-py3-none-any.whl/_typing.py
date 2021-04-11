'''
Date: 2021-03-25 19:30:09
LastEditors: lisonge
Author: lisonge
LastEditTime: 2021-04-09 15:42:25
'''
from typing import TypedDict, Literal


class LoginResp(TypedDict):
    result: bool
    status: str


class LoginSuccessResp(LoginResp):
    uid: int
    result: Literal[True]


class LoginFailedResp(LoginResp):
    result: Literal[False]
    errorMsg: str


class YzPanUserValidResp(TypedDict):
    result: bool
    _token: str


class YzPanUploadRespData(TypedDict):
    creator: int
    resid: int
    crc: str
    objectId: str
    name: str


class YzPanUploadResp(TypedDict):
    result: bool
    msg: str
    data: YzPanUploadRespData
