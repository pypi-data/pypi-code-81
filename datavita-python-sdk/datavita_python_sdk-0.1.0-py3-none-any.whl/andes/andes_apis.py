#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-05 15:08
    @Author : Yin Jian
    @Version：V 0.1
    @File : andes_apis.py
    @desc :
"""
andes_apis_dict = {'get_dataset_by_tagcode': '{base_url}/api/v1/tag/dataset?tagCode={tag_code}',
                   'get_data_by_dataset_name': '{base_url}/api/v1/dataset/dataDict',
                   'get_data_by_industry': '{base_url}/api/v1/industry/dataDict?industryName={industry_name}',
                   'get_data_by_datacode': '{base_url}/api/v1/dataCode/data',
                   'get_untsd_data_by_dataset_id': '{base_url}/api/v1/unTsd/data',
                   'get_data_by_dataname': '{base_url}/api/v1/dataName/data',
                   'get_data_by_wind_code': '{base_url}/api/v1/windCode/data',
                   'realtime_news': '{base_url}/api/v1/news/list',
                   }
