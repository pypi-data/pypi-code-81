#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/9 13:19
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : model.py
@Desc    : 
"""

import logging
from waveletai.constants import ModelRegisterMode

_logger = logging.getLogger(__name__)


class Model(object):

    def __init__(self, backend, id, name, desc, app_id, create_time, create_user_id, update_time, update_user_id):
        self._backend = backend
        self.id = id
        self.name = name
        self.desc = desc
        self.app_id = app_id
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.update_time = update_time
        self.update_user_id = update_user_id

    def register_model_version(self, path, desc, mode=ModelRegisterMode.PYFUNC.value):
        """
        注册模型库版本
        :param mode: 注册模式,默认为自定义
        :param path: 注册文件路径，可以是文件夹,当为docker模式时，此处为docker-image,可以用save命令导出  eg：deployment.tar
        :return:
        """
        self._backend.register_model_version(self.id, desc, path, mode)

    def get_model_version(self, version):
        pass

    def update_model_version(self, version, desc):
        pass

    def transition_model_version_stage(self, version, stage):
        pass

    def list_registered_models(self):
        """fetch a list of all registered models in the registry with a simple method."""
        pass

    def search_model_versions(self, desc, stage):
        """search for a specific stage or desc and list its version details"""
        pass

    def delete_model_version(self):
        pass


class ModelVersion(object):
    def __init__(self, backend, id, version, desc, model_id, model_name, mode, create_user_name, create_time,
                 create_user_id):
        self._backend = backend
        self.id = id
        self.version = version
        self.desc = desc
        self.model_id = model_id
        self.mode = mode
        self.create_time = create_time
        self.create_user_id = create_user_id
        self.create_user_name = create_user_name
        self.model_name = model_name

    def list_releases(self):
        pass
