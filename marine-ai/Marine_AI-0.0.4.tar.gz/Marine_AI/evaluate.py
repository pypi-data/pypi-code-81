import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from sklearn.preprocessing import StandardScaler
from netCDF4 import Dataset
tf.compat.v1.disable_eager_execution()


def build_model(input_shape=(72,24,33)):
    inp = Input(shape=input_shape)

    x = Conv2D(30, (8, 4), padding='SAME')(inp)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2,2))(x)
    x = Dropout(0.5)(x)

    x = Conv2D(30, (8, 4), padding='SAME')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((2,2))(x)
    x = Dropout(0.5)(x)

    x = Conv2D(30, (4, 2), padding='SAME')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Flatten()(x)
    x = Dropout(0.5)(x)

    x = Dense(120)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    x = GRU(30, return_sequences = True)(tf.reshape(x, [-1,12,10]))
    x = Dropout(0.2)(x)
    x = GRU(30)(x)
    x = Dropout(0.2)(x)

    output = Dense(16, activation='linear')(x)
    output = x.reshape((4,4))

    model = Model(inputs = inp, outputs = output)
    model.summary()

    model.compile(optimizer='adam', loss='mse')

    return model