# -*- coding:utf-8 -*-
"""

Author:
    TS K

Reference:


"""
import tensorflow as tf

from ..feature_column import build_input_features, get_linear_logit, input_from_feature_columns
from ..layers.core import DNN, PredictionLayer
from ..layers.utils import concat_func, add_func


def NNCNN15(linear_feature_columns, dnn_feature_columns, 
         conv_kernel_width=(5, 5, 3), conv_filters=(64, 64, 64),
         mlp_feat_filters=((22, 22), (22, 22), (22, 22)), feat_pooling_width=((3, 3), (3,3)), feat_pooling_stride=((2,2), (2,2)), dnn_hidden_units=(128, 64),
         l2_reg_linear=1e-5, l2_reg_embedding=1e-5, l2_reg_dnn=0, pooling_dropout=0, dnn_dropout=0,
         seed=1024, task='binary'):
    """Instantiates the Convolutional Click Prediction Model architecture.

    :param linear_feature_columns: An iterable containing all the features used by linear part of the model.
    :param dnn_feature_columns: An iterable containing all the features used by deep part of the model.
    :param conv_kernel_width: list,list of positive integer or empty list,the width of filter in each conv layer.
    :param conv_filters: list,list of positive integer or empty list,the number of filters in each conv layer.
    :param l2_reg_linear: float. L2 regularizer strength applied to linear part
    :param l2_reg_embedding: float. L2 regularizer strength applied to embedding vector
    :param l2_reg_dnn: float. L2 regularizer strength applied to DNN
    :param dnn_dropout: float in [0,1), the probability we will drop out a given DNN coordinate.
    :param init_std: float,to use as the initialize std of embedding vector
    :param task: str, ``"binary"`` for  binary logloss or  ``"regression"`` for regression loss
    :return: A Keras model instance.
    """

    if not len(conv_kernel_width) == len(conv_filters):
        raise ValueError(
            "conv_kernel_width must have same element with conv_filters")

    features = build_input_features(linear_feature_columns + dnn_feature_columns)
    inputs_list = list(features.values())

    linear_logit = get_linear_logit(features, linear_feature_columns, seed=seed,
                                    l2_reg=l2_reg_linear)

    sparse_embedding_list, _ = input_from_feature_columns(features, dnn_feature_columns, l2_reg_embedding,
                                                          seed, support_dense=False)

    n = len(sparse_embedding_list)
    l = len(conv_filters)

    x = concat_func(sparse_embedding_list, axis=1)
    x = tf.keras.layers.Lambda(lambda x: tf.expand_dims(x, axis=3))(x) 

    for i in range(1, l + 1):
        filters = conv_filters[i - 1]
        width = conv_kernel_width[i - 1]
        f_filters = mlp_feat_filters[i - 1]
        
        x = tf.keras.layers.Conv2D(filters=filters, kernel_size=(1, width), strides=(1, 1), padding='same',
                                             activation='elu', use_bias=True, )(x)
        
        # transform to (batch, channel, width, height)
        x = tf.transpose(x, [0, 3, 2, 1])
        
        # Feature NiN
        x = tf.keras.layers.Conv2D(filters=f_filters[0], kernel_size=(1, 1), strides=(1, 1), padding='same',
                                             activation='elu', use_bias=True)(x)
        x = tf.keras.layers.Conv2D(filters=f_filters[1], kernel_size=(1, 1), strides=(1, 1), padding='same',
                                             activation='elu', use_bias=True)(x)
        
        # return to (batch, height, width, channel)  
        x = tf.transpose(x, [0, 3, 2, 1])
        
        if i < l:
           p_width = feat_pooling_width[i - 1]
           p_stride = feat_pooling_stride[i - 1]
           x = tf.keras.layers.MaxPooling2D(pool_size=(p_width[0], p_width[1]), strides=(p_stride[0], p_stride[1]))(x)
           x = tf.keras.layers.Dropout(rate = pooling_dropout, seed=seed,)(x)
        
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Flatten()(x)
    final_logit = tf.keras.layers.Dense(1, use_bias=False, kernel_initializer=tf.keras.initializers.glorot_normal(seed))(x)

    output = PredictionLayer(task)(final_logit)
    model = tf.keras.models.Model(inputs=inputs_list, outputs=output)
    return model