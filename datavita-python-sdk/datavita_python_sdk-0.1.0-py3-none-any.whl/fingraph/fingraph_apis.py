#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 hcyjs.com, Inc. All Rights Reserved

"""
    @Time : 2021-02-05 15:08
    @Author : Yin Jian
    @Version：V 0.1
    @File : fingraph_apis.py
    @desc :
"""
fingraph_apis_dict = {'get_fingraph_data_by_group_id': '{base_url}/api/v1/group/dataDict?groupId={group_id}',
                      'query_node_detail': '{base_url}/api/v1/graph/nodeName/node',
                      'query_node': '{base_url}/api/v1/graph/nodeId/node',
                      'query_node_data_bind_info': '{base_url}/api/v1/graph/factor/data/node',
                      'traversal_group_node': '{base_url}/api/v1/graph/group/unData/node',
                      'traversal_group_relationship': '{base_url}/api/v1/graph/group/unData/triple',
                      'traversal_group_data_relationship': '{base_url}/api/v1/graph/group/data/triple',
                      'path_traversal': '{base_url}/api/v1/graph/path',
                      'path_search': '{base_url}/api/v1/graph/step/path',
                      'get_label_property': '{base_url}/api/v1/graph/label/attr'
                      }
