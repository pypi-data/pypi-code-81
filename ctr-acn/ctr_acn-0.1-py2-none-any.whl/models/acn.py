# -*- coding:utf-8 -*-
"""

Author:
   T-S K

Reference:
    [...

"""
import tensorflow as tf

from ..feature_column import build_input_features, get_linear_logit, input_from_feature_columns
from ..layers.core import PredictionLayer
from ..layers.interaction import FECNNLayer, ANLayer
from ..layers.utils import concat_func, add_func


def ACN(linear_feature_columns, dnn_feature_columns, 
        conv_kernel_width=(7, 7, 7, 7), conv_filters=(14, 16, 18, 20), pooling_width=(2, 2, 2, 2),
        attention_factor=8,
        l2_reg_linear=1e-5, l2_reg_embedding=1e-5, l2_reg_att=1e-5, acn_dropout=0, seed=1024,
        task='binary'):
    """Instantiates the Attentional Factorization Machine architecture.

    :param linear_feature_columns: An iterable containing all the features used by linear part of the model. iterable: member를 하나씩 반환할 수 있는 object: list, tuple, dict 등
    :param dnn_feature_columns: An iterable containing all the features used by deep part of the model.
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
    
    if not (len(conv_kernel_width) == len(conv_filters) == len(pooling_width)):
        raise ValueError(
            "conv_kernel_width, conv_filters and pooling_width must have same length")

    # Input layer 설정(OrderedDict type), linear_feature_columns, dnn_feature_columns: 피쳐에 대한 이름, voca size, embedding size 정보가 담긴 리스트
    features = build_input_features(dnn_feature_columns) 

    inputs_list = list(features.values()) 
    
    linear_logit = get_linear_logit(features, linear_feature_columns, seed=seed, prefix='linear',
                                    l2_reg=l2_reg_linear)

    embedding_dict, _ = input_from_feature_columns(features, dnn_feature_columns, l2_reg_embedding, seed) # embedding layer 설정

    cnn_input = concat_func(embedding_dict, axis=1)
    ext_features = FECNNLayer(conv_filters, conv_kernel_width, pooling_width)(cnn_input)      
    acn_logit = ANLayer(attention_factor, l2_reg_att, acn_dropout, seed)(ext_features)

    final_logit = add_func([linear_logit, acn_logit])
    output = PredictionLayer(task)(final_logit)

    model = tf.keras.models.Model(inputs=inputs_list, outputs=output)
    return model
