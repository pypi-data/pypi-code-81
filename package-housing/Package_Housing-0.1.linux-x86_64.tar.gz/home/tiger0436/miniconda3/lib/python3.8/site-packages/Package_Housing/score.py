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
# model folder, dataset folder, file to score
args = parser.parse_args()
 

parser = argparse.ArgumentParser()
parser.add_argument('-i', action='append', nargs='+')
args = parser.parse_args()


parser = argparse.ArgumentParser()
parser.add_argument('-i', action='append', nargs='+')
args = parser.parse_args()

if (args.i==None):
    args.i=[['/mnt/d/Mars/MLE/Assignment_2_To_submit/MLE/data/processed/model_outputs/','/mnt/d/Mars/MLE/Assignment_2_To_submit/MLE/data/processed/']]
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)  
logger.info("Log is getting recorded") 
# print(args.i[0][1])
if (len(args.i[0])==2):
    stream_handler=logging.StreamHandler()
    logger.addHandler(stream_handler)

else: 
    file_handler=logging.FileHandler('score.log')
    logger.addHandler(file_handler)



lin_reg = pickle.load(open(args.i[0][0]+'lin_reg.sav', 'rb'))
imputer=pickle.load(open(args.i[0][0]+'imputer.sav', 'rb'))
tree_reg = pickle.load(open(args.i[0][0]+'tree_reg.sav', 'rb'))
housing_prepared=pd.read_pickle(args.i[0][0]+"housing_prepared.pkl")
housing_predictions = lin_reg.predict(housing_prepared)
strat_train_set=pd.read_csv(args.i[0][1]+'train_data.csv')
strat_test_set=pd.read_csv(args.i[0][1]+'test_data.csv')
housing_labels = strat_train_set["median_house_value"].copy()
lin_mse = mean_squared_error(housing_labels, housing_predictions)
lin_rmse = np.sqrt(lin_mse)
lin_rmse


lin_mae = mean_absolute_error(housing_labels, housing_predictions)
lin_mae



housing_predictions = tree_reg.predict(housing_prepared)
tree_mse = mean_squared_error(housing_labels, housing_predictions)
tree_rmse = np.sqrt(tree_mse)
tree_rmse


param_distribs = {
    "n_estimators": randint(low=1, high=200),
    "max_features": randint(low=1, high=8),
}

forest_reg = RandomForestRegressor(random_state=42)
rnd_search = RandomizedSearchCV(
    forest_reg,
    param_distributions=param_distribs,
    n_iter=10,
    cv=5,
    scoring="neg_mean_squared_error",
    random_state=42,
)
rnd_search.fit(housing_prepared, housing_labels)
cvres = rnd_search.cv_results_
for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    print(np.sqrt(-mean_score), params)


param_grid = [
    # try 12 (3×4) combinations of hyperparameters
    {"n_estimators": [3, 10, 30], "max_features": [2, 4, 6, 8]},
    # then try 6 (2×3) combinations with bootstrap set as False
    {"bootstrap": [False], "n_estimators": [3, 10], "max_features": [2, 3, 4]},
]

forest_reg = RandomForestRegressor(random_state=42)
# train across 5 folds, that's a total of (12+6)*5=90 rounds of training
grid_search = GridSearchCV(
    forest_reg,
    param_grid,
    cv=5,
    scoring="neg_mean_squared_error",
    return_train_score=True,
)
grid_search.fit(housing_prepared, housing_labels)

grid_search.best_params_
cvres = grid_search.cv_results_
for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    print(np.sqrt(-mean_score), params)

feature_importances = grid_search.best_estimator_.feature_importances_
sorted(zip(feature_importances, housing_prepared.columns), reverse=True)


final_model = grid_search.best_estimator_

X_test = strat_test_set.drop("median_house_value", axis=1)
y_test = strat_test_set["median_house_value"].copy()

X_test_num = X_test.drop("ocean_proximity", axis=1)
X_test_prepared = imputer.transform(X_test_num)
X_test_prepared = pd.DataFrame(
    X_test_prepared, columns=X_test_num.columns, index=X_test.index
)
X_test_prepared["rooms_per_household"] = (
    X_test_prepared["total_rooms"] / X_test_prepared["households"]
)
X_test_prepared["bedrooms_per_room"] = (
    X_test_prepared["total_bedrooms"] / X_test_prepared["total_rooms"]
)
X_test_prepared["population_per_household"] = (
    X_test_prepared["population"] / X_test_prepared["households"]
)

X_test_cat = X_test[["ocean_proximity"]]
X_test_prepared = X_test_prepared.join(pd.get_dummies(X_test_cat, drop_first=True))


final_predictions = final_model.predict(X_test_prepared)
final_mse = mean_squared_error(y_test, final_predictions)
final_rmse = np.sqrt(final_mse)
logger.info("Final Root Mean Square error is {}".format(final_rmse))
logger.info("Successfully Completed!!!")

