# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from typing import Tuple, Callable


class SCUStudent(metaclass=ABCMeta):
    @abstractmethod
    def session_valid_required(func: Callable):
        '''
        装饰器，用于确保session有效
        '''

    @abstractmethod
    def set_baseinfo(self, stid: str, passwd: str, hashed: bool = False):
        '''
        @stid(str)    学号
        @passwd(str)  密码
        @hashed(bool) 密码是否已经过md5加密 default=False
        '''

    @abstractmethod
    def session_valid(self) -> bool:
        '''
        @brief 返回网站会话是否有效，在有效的情况下才可以获取个人信息
               如果session过期，则需要获取验证码重新登陆
        @param[out] valid(bool)  网站会话是否有效
        '''

    @abstractmethod
    def get_captcha(self, filepath: str = None) -> Tuple[bool, str]:
        '''
        @brief 获取验证码
        @param[in]  filepath(str)  [可选的] 存储验证码图像的全路径，使用**.jpg**格式
        @param[out] success(bool)  操作是否成功
        @param[out] str(bool)      验证码图像base64编码
        '''

    @abstractmethod
    def login(self, catpcha: str, remember_me: bool) -> Tuple[bool, ]:
        '''
        @brief 模拟登陆
        @param[in] captcha(str) 通过get_captcha获取的验证码识别后的字符串
        @param[in] remember_me(bool) 是否开启两周内快速登录
        @param[out] success(bool) 是否登录成功
        '''

    @session_valid_required
    @abstractmethod
    def get_student_name(self) -> Tuple[bool, str]:
        '''
        @brief 获取学生姓名
        @param[out] success(bool) 是否获取成功
        @param[out] student_name(str) 学生姓名/失败反馈内容
        '''

    @session_valid_required
    @abstractmethod
    def get_student_pic(self, filepath: str = None) -> Tuple[bool, str]:
        '''
        @brief 获取学生照片
        @param[in]  filepath(str) 存储图片的全路径，使用**.jpg**格式
        @param[out] success(bool) 是否获取成功
        @param[out] student_pic(str) 图片的base64编码
        '''
    
    @session_valid_required
    @abstractmethod
    def get_all_term_scores(self, pagesize: int = -1) -> dict:
        '''
        @brief 获取学生所有学期的成绩
        @param[in]  pagesize(int) 最近多少门课的成绩，默认-1为取全部课成绩
        @param[out] 获取的原始数据 json=>dict
        '''
