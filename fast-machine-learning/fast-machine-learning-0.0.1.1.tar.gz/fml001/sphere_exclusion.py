# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:57:30 2018

@author: ly931
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

def perm_rng(X, Y, indexes, percent=0.15, random_state=None):
    
    from sklearn.utils import check_random_state
    import math, random
    if random_state is None:
        random_state = random.randint(0, 999)
    rng = check_random_state(random_state)
    length = len(Y)
    train_length = math.floor((1 - percent) * length)
    perm = rng.permutation(length)
    X = X[perm]
    Y = Y[perm]
    indexes = indexes[perm]
    X_train = X[:train_length,:]
    Y_train = Y[:train_length]
    X_test = X[train_length:,:]
    Y_test = Y[train_length:]
    return X_train, Y_train, X_test, Y_test, indexes[:train_length], indexes[train_length:]

def sphere_exclusion_array(X, Y, indexes, percent=0.15):
    
    matrix = np.array(X).astype(float)
    matrix = MinMaxScaler().fit_transform(matrix)
    distances = np.zeros(len(matrix))
    split_step = int(round(1 / percent, 0))
    
    for index in range(len(distances)):
        distance = 0
        rowA = matrix[index]
        for row in matrix:
            distance += ( rowA - row ) ** 2
        distances[index] = distance.sum()
    distances = distances ** 0.5 / (len(distances) - 1)
    
    sorted_index = np.array([ item[0] for item in sorted(zip(list(range(len(Y))), distances), key=lambda x: x[1], reverse=True) ])
    test_index = [ index for index in range(0, len(Y), split_step) ]
    train_index = [ index for index in range(len(Y)) if index not in test_index ]
    
    return X[sorted_index[train_index], :], Y[sorted_index[train_index]], X[sorted_index[test_index], :], Y[sorted_index[test_index]], sorted_index

def target_exclusion_array(X, Y, indexes, percent=0.15, random_state=0):
    matrix = np.array(X).astype(float)
    matrix = MinMaxScaler().fit_transform(matrix)
    split_step = int(round(1 / percent, 0))

    sorted_index = np.array([ item[0] for item in sorted(zip(indexes, Y), key=lambda x: x[1], reverse=True) ])
    test_index = [ index for index in range(0, len(X), split_step) ]
    train_index = [ index for index in range(len(X)) if index not in test_index ]

    return X[sorted_index[train_index], :], Y[sorted_index[train_index]], X[sorted_index[test_index], :], Y[sorted_index[test_index]], train_index, test_index

def nosplit(data, tar_col=1, testing_size=0.15):
    tar_col = tar_col - 1
    targets = data.pop(data.columns[tar_col])
    descriptors = data
    return descriptors, targets, 0, 0

def sphere_exclution(data, tar_col=1, testing_size=0.15):
    if testing_size == 0:
        return nosplit(data=data, tar_col=tar_col, testing_size=testing_size)
    else:
        tar_col = tar_col - 1
        targets = data.pop(data.columns[tar_col])
        descriptors = data
        matrix = np.array(descriptors).astype(float)
        matrix = MinMaxScaler().fit_transform(matrix)
        distances = np.zeros(len(matrix))
        split_step = int(round(1 / testing_size, 0))
    
        for index in range(len(distances)):
            distance = 0
            rowA = matrix[index]
            for row in matrix:
                distance += ( rowA - row ) ** 2
            distances[index] = distance.sum()
        distances = distances ** 0.5 / (len(distances) - 1)
    
        sorted_index = np.array([ item[0] for item in sorted(zip(descriptors.index, distances), key=lambda x: x[1], reverse=True) ])
        test_index = [ index for index in range(0, len(descriptors), split_step) ]
        train_index = [ index for index in range(len(descriptors)) if index not in test_index ]
    
        return descriptors.loc[sorted_index[train_index], :], targets[sorted_index[train_index]], descriptors.loc[sorted_index[test_index], :], targets[sorted_index[test_index]]

def target_exclution(data, tar_col=1, testing_size=0.15):
    if testing_size == 0:
        return nosplit(data=data, tar_col=tar_col, testing_size=testing_size)
    else:
        tar_col = tar_col - 1
        targets = data.pop(data.columns[tar_col])
        descriptors = data
        matrix = np.array(descriptors).astype(float)
        matrix = MinMaxScaler().fit_transform(matrix)
        split_step = int(round(1 / testing_size, 0))
    
        sorted_index = np.array([ item[0] for item in sorted(zip(descriptors.index, targets), key=lambda x: x[1], reverse=True) ])
        test_index = [ index for index in range(0, len(descriptors), split_step) ]
        train_index = [ index for index in range(len(descriptors)) if index not in test_index ]
    
        return descriptors.loc[sorted_index[train_index], :], targets[sorted_index[train_index]], descriptors.loc[sorted_index[test_index], :], targets[sorted_index[test_index]]

def random_exclution(data, tar_col=1, testing_size=0.15):
    if testing_size == 0:
        return nosplit(data=data, tar_col=tar_col, testing_size=testing_size)
    else:
        tar_col = tar_col - 1
        targets = data.pop(data.columns[tar_col])
        descriptors = data
        index = np.arange(descriptors.shape[0])
        train_index, test_index = train_test_split(index, test_size=testing_size, shuffle=True)
    
        return descriptors.iloc[train_index, :], targets.iloc[train_index], descriptors.iloc[test_index, :], targets.iloc[test_index]
    



if __name__ == "__main__":
    from glob import glob
    from pydataset import ReadFile
    from preprocessing import nasd
    import pandas as pd
    
    dataset = ReadFile("../dataset.csv").dataframe
    columns = dataset.columns
    no_col = dataset.pop(columns[0])
    dataset.index = no_col
    targets = dataset.pop(columns[1])
    descriptors = dataset
    descriptors = nasd(descriptors)
    a, b, c, d = random_exclution(descriptors, targets)
    
    
    # targets = pd.read_excel(glob("../dataset.xlsx")[0], sheet_name=['Sheet1'])['Sheet1']
    # targets = targets[targets["结构类型"] == "链"]
    # targets = targets[targets["代号与文件是否相同"] == True]
    # targets = targets[targets["复杂分子"] != 1]
    # targets = targets[targets["短分子"] != 1]
    # targets.index = targets["分子代号"]
    # targets = targets.iloc[:, 4]
    # descriptors = ReadFile(glob("../*.txt")[0]).dataframe
    # descriptors.index = descriptors.pop("NAME")
    # descriptors.pop("No.")
    # descriptors = descriptors.loc[targets.index, :]
    # descriptors = nasd(descriptors)
    # x_train, y_train, x_test, y_test = sphere_exclution(descriptors, targets)
    
    
    # matrix = np.array(descriptors).astype(float)
    # matrix = MinMaxScaler().fit_transform(matrix)
    # distances = np.zeros(len(matrix))
    # split_step = int(round(1 / 0.16, 0))
    
    # sorted_index = [ item for item in sorted(zip(descriptors.index, targets), key=lambda x: x[1], reverse=True) ]
