import sys
import pandas as pd
import numpy as np
from scipy import linalg
import logging


def _pre_data(data_file, id, tpoint, trait, gmat_file, na_method='omit'):
    logging.info('Data file: ' + data_file)
    data_df = pd.read_csv(data_file, sep='\s+', header=0)
    logging.info('NA method: ' + na_method)
    if na_method == 'omit':
        data_df = data_df.dropna()
    elif na_method == 'include':
        data_df = data_df.fillna(method='ffill')
        data_df = data_df.fillna(method='bfill')
    else:
        logging.info('na_method does not exist: ' + na_method)
        sys.exit()
    col_names = data_df.columns
    logging.info('The column names of data file: {}'.format(col_names))
    logging.info('Note: Variates beginning with a capital letter is converted into factors.')
    class_vec = []
    for val in col_names:
        if not val[0].isalpha():
            logging.info("The first character of columns names must be alphabet!")
            sys.exit()
        if val[0] == val.capitalize()[0]:
            class_vec.append(val)
            data_df[val] = data_df[val].astype('str')
        else:
            try:
                data_df[val] = data_df[val].astype('float')
            except Exception as e:
                logging.info(e)
                logging.info("{} may contain string, please check!".format(val))
                sys.exit()
    data_df = data_df.sort_values(by=[id, tpoint])  # sort the data frame by id and time points.
    id_in_gmat = list(pd.read_csv(gmat_file + '.id', sep='\s+', header=None, dtype={0: 'str'}).iloc[:, 0])
    logging.info('Individual column: ' + id)
    if id not in class_vec:
        logging.info('The initial letter of {} should be capital'.format(id))
        sys.exit()
    id_order = []   # id in order
    ind_keep = []
    for val in data_df[id]:
        if val in id_in_gmat:
            ind_keep.append(True)
            if val not in id_order:
                id_order.append(val)
        else:
            ind_keep.append(False)
    data_df = data_df.iloc[ind_keep, :]
    logging.info('Time points column: ' + tpoint)
    if tpoint in class_vec:
        logging.info('The initial letter of {} should be lowercase'.format(tpoint))
        sys.exit()
    logging.info('Trait column: ' + trait)
    if trait in class_vec:
        logging.info('The initial letter of {} should be lowercase'.format(trait))
        sys.exit()
    logging.info("The genomic relationship matrix file is: {}.agrm.id_fmt".format(gmat_file))
    id_dct = dict(zip(id_order, range(len(id_order))))
    ag = np.zeros((len(id_order), len(id_order)))
    with open(gmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as e:
                del e
    id_code = []  # code the id in the data file from 0 to ...
    for val in data_df[id]:
        id_code.append(id_dct[val])
    return data_df, ag, id_code, id_order
