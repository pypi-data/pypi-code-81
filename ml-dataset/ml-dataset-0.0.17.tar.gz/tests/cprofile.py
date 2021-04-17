#!/usr/bin/env python

"""Tests for `datasets` package.
    ref : https://docs.python.org/zh-cn/3/library/unittest.html
"""

import unittest
import cProfile
import os
import tensorflow as tf

from datasets import TextlineParser, SeqParser
from datasets import TFDataset
from datasets.utils import TokenDicts, DataSchema

def run_tf_dataset_session_parser():
        token_dicts = TokenDicts('tests/data/dicts', {'query': 0})
        data_field_list = []
        # param = ["name", "processor", "type", "dtype", "shape", "max_len", "token_dict_name"]
        data_field_list.append(DataSchema(name='query', processor='to_tokenid',
                                          dtype='int32', shape=(None, None,), is_with_len=False, token_dict_name='query', has_session=True))
        data_field_list.append(DataSchema(name='width', processor='to_np', dtype='float32', shape=(None, 4,), has_session=True))
        label_field = DataSchema(name='label', processor='to_np', dtype='float32', shape=(1,))
        parser = SeqParser(token_dicts, data_field_list, label_field)
        generator = TFDataset(parser=parser, file_path='tests/data/seq_datasets', file_suffix='simple_seq.input')
        #print('Shapes', generator._get_shapes(is_training=True))
        dataset = generator.generate_dataset(
            batch_size=12, num_epochs=10, is_shuffle=False)
        for _ in enumerate(dataset):
            pass

if __name__ == '__main__':
    #cProfile.run('run_tf_dataset_session_parser()')
    run_tf_dataset_session_parser()