import argparse
import logging
import os
import pickle
import tarfile

import matplotlib as mpl  # noqa
import matplotlib.pyplot as plt  # noqa
import numpy as np
import pandas as pd
from scipy.stats import randint
from six.moves import urllib
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedShuffleSplit,
    train_test_split,
)
from sklearn.tree import DecisionTreeRegressor

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='append', nargs='+')
args = parser.parse_args()


parser = argparse.ArgumentParser()
parser.add_argument('-i', action='append', nargs='+')
args = parser.parse_args()

if (args.i==None):
    args.i=[['/mnt/d/Mars/MLE/Assignment_2_To_submit/MLE/data/processed/','/mnt/d/Mars/MLE/Assignment_2_To_submit/MLE/data/processed/model_outputs/']]
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)  
logger.info("Log is getting recorded") 
# print(args.i[0][1])
if (len(args.i[0])==2):
    stream_handler=logging.StreamHandler()
    logger.addHandler(stream_handler)

else: 
    file_handler=logging.FileHandler('train.log')
    logger.addHandler(file_handler)


strat_train_set=pd.read_csv(args.i[0][0]+'train_data.csv')
strat_test_set=pd.read_csv(args.i[0][0]+'test_data.csv')
housing = strat_train_set.copy()
housing.plot(kind="scatter", x="longitude", y="latitude")
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

corr_matrix = housing.corr()
corr_matrix["median_house_value"].sort_values(ascending=False)
housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
housing["population_per_household"] = housing["population"] / housing["households"]

housing = strat_train_set.drop(
    "median_house_value", axis=1
)  # drop labels for training set
housing_labels = strat_train_set["median_house_value"].copy()

imputer = SimpleImputer(strategy="median")

housing_num = housing.drop("ocean_proximity", axis=1)

imputer.fit(housing_num)
X = imputer.transform(housing_num)

housing_tr = pd.DataFrame(X, columns=housing_num.columns, index=housing.index)
housing_tr["rooms_per_household"] = housing_tr["total_rooms"] / housing_tr["households"]
housing_tr["bedrooms_per_room"] = (
    housing_tr["total_bedrooms"] / housing_tr["total_rooms"]
)
housing_tr["population_per_household"] = (
    housing_tr["population"] / housing_tr["households"]
)

housing_cat = housing[["ocean_proximity"]]
housing_prepared = housing_tr.join(pd.get_dummies(housing_cat, drop_first=True))


lin_reg = LinearRegression()
lin_reg.fit(housing_prepared, housing_labels)

tree_reg = DecisionTreeRegressor(random_state=42)
tree_reg.fit(housing_prepared, housing_labels)
filename='imputer.sav'
pickle.dump(imputer, open(args.i[0][1]+filename, 'wb'))

filename = 'lin_reg.sav'
pickle.dump(lin_reg, open(args.i[0][1]+filename, 'wb'))
filename = 'tree_reg.sav'
pickle.dump(tree_reg, open(args.i[0][1]+filename, 'wb'))
housing_prepared.to_pickle(args.i[0][1]+'housing_prepared.pkl')
logger.info("The dimension of the dataset is {}".format(housing_prepared.shape))
logger.info("All models trained Successfully")
