# -*- coding: utf-8 -*-
from nn_sdk.py_tf_csdk import csdk_object

'''
    支持多子图,支持图多输入多输出.
    支持tensorflow 1 pb , tensorflow 2 pb , tensorflow ckpt
    net_stage 
'''
config = {
    "model_dir": r'./model.ckpt',
    "log_level": 4, # 0 fatal , 2 error , 4 info , 8 debug
    "model_type": 1,  # 0 pb format   if 1 ckpt format
    "ConfigProto": {
        "log_device_placement": False,
        "allow_soft_placement": True,
        "gpu_options": {
            "allow_growth": True
        },
    },
    "graph_inf_version": 1,  # the format of tensorflow pb model [1,2]
    "graph": [
        {
            "input": ["input_ids:0","input_mask:0"], #tf1 sample ["input_ids:0"],  tf2 sample ["input_ids"]
            "output": ["pred_ids:0"], #tf1 sample ["pred_ids:0"],  tf2 sample ["pred_ids"]
        }
    ]}

seq_length = 4
input_ids = [[10.] * seq_length]
input_mask = [[1] * seq_length]
sdk_inf = csdk_object(config)
if sdk_inf.valid():
    net_stage = 0
    ret, out = sdk_inf.process(net_stage, input_ids,input_mask)
    print(ret)
    print(out)
    sdk_inf.close()