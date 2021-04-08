#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2021/4/6 5:42
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : backend.py
@Desc    : 
"""


from abc import ABCMeta, abstractmethod, abstractproperty

import six


@six.add_metaclass(ABCMeta)
class Backend(object):

    @abstractproperty
    def api_address(self):
        pass

    @abstractproperty
    def display_address(self):
        pass

    @abstractmethod
    def create_dataset(self, name, zone, data_type, json_data, desc):
        pass

    @abstractmethod
    def upload_dataset(self, dataset_id, path):
        pass

    @abstractmethod
    def download_dataset_artifact(self, dataset_id, path, destination):
        pass

    @abstractmethod
    def download_dataset_artifacts(self, dataset_id, destination):
        pass

    @abstractmethod
    def create_model(self, app_id, name, desc):
        pass

    @abstractmethod
    def register_model(self, model_id, name, mode, art_id):
        pass

    @abstractmethod
    def download_model(self, model_id, version, destination):
        pass

