import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras.layers import *
from tensorflow.keras.models import *
from sklearn.preprocessing import StandardScaler
from netCDF4 import Dataset
tf.compat.v1.disable_eager_execution()

def build_model():
    inp = Input(shape=(72,24,33))

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

    output = Dense(24, activation='linear')(x)

    model = Model(inputs = inp, outputs = output)
    model.summary()

    model.compile(optimizer='adam', loss='mse')

    return model

def scale(data): #data(N, n, 24, 72)
    sc = StandardScaler()
    X = data.reshape(-1,1)
    X_scaled = sc.fit_transform(X)
    X_scaled[X == 0] = 0
    X_scaled = X_scaled.reshape((data.shape))
    return X_scaled #(N, n, 24,72)

def difference(data):
    return np.diff(data,axis=1,n=1), np.diff(data,axis=1,n=2)


def load_data(data_path, label_path):
    data = Dataset(data_path, 'r')
    label = Dataset(label_path, 'r')

    return data, label

