# -*- coding:utf-8 -*-
"""

Author:
    Weichen Shen,wcshen1994@163.com

Reference:
    [1] Xiao J, Ye H, He X, et al. Attentional factorization machines: Learning the weight of feature interactions via attention networks[J]. arXiv preprint arXiv:1708.04617, 2017.
    (https://arxiv.org/abs/1708.04617)

"""
import tensorflow as tf

from ..feature_column import build_input_features, get_linear_logit, DEFAULT_GROUP_NAME, input_from_feature_columns
from ..layers.core import PredictionLayer
from ..layers.interaction import AFMLayer, FM
from ..layers.utils import concat_func, add_func


def AFM(linear_feature_columns, dnn_feature_columns, fm_group=DEFAULT_GROUP_NAME, use_attention=True,
        attention_factor=8,
        l2_reg_linear=1e-5, l2_reg_embedding=1e-5, l2_reg_att=1e-5, afm_dropout=0, seed=1024,
        task='binary'):
    """Instantiates the Attentional Factorization Machine architecture.

    :param linear_feature_columns: An iterable containing all the features used by linear part of the model. iterable: member를 하나씩 반환할 수 있는 object: list, tuple, dict 등
    :param dnn_feature_columns: An iterable containing all the features used by deep part of the model.
    :param fm_group: list, group_name of features that will be used to do feature interactions.
    :param use_attention: bool,whether use attention or not,if set to ``False``.it is the same as **standard Factorization Machine**
    :param attention_factor: positive integer,units in attention net
    :param l2_reg_linear: float. L2 regularizer strength applied to linear part
    :param l2_reg_embedding: float. L2 regularizer strength applied to embedding vector
    :param l2_reg_att: float. L2 regularizer strength applied to attention net
    :param afm_dropout: float in [0,1), Fraction of the attention net output units to dropout.
    :param seed: integer ,to use as random seed.
    :param task: str, ``"binary"`` for  binary logloss or  ``"regression"`` for regression loss
    :return: A Keras model instance.
    """

    # Input layer 설정(OrderedDict type), linear_feature_columns, dnn_feature_columns: 피쳐에 대한 이름, voca size, embedding size 정보가 담긴 리스트
    features = build_input_features(
        linear_feature_columns + dnn_feature_columns) 
    # input_list 는 피쳐 별 Input()들의 리스트 형 
    inputs_list = list(features.values()) 

    group_embedding_dict, _ = input_from_feature_columns(features, dnn_feature_columns, l2_reg_embedding, # embedding layer 설정
                                                         seed, support_dense=False, support_group=True)

    linear_logit = get_linear_logit(features, linear_feature_columns, seed=seed, prefix='linear',
                                    l2_reg=l2_reg_linear)

    if use_attention:
        fm_logit = add_func([AFMLayer(attention_factor, l2_reg_att, afm_dropout,
                                      seed)(list(v)) for k, v in group_embedding_dict.items() if k in fm_group])
    else:
        fm_logit = add_func([FM()(concat_func(v, axis=1))
                             for k, v in group_embedding_dict.items() if k in fm_group])

    final_logit = add_func([linear_logit, fm_logit])
    output = PredictionLayer(task)(final_logit)

    model = tf.keras.models.Model(inputs=inputs_list, outputs=output)
    return model
