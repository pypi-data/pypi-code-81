import argparse
import logging
import os
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
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)  
if (args.i==None):
    args.i=[['/mnt/d/Mars/MLE/Assignment_2_To_submit/MLE/data/processed/']]

if (len(args.i[0])==1):
    stream_handler=logging.StreamHandler()
    logger.addHandler(stream_handler)

else: 
    file_handler=logging.FileHandler('ingest_data.log')
    logger.addHandler(file_handler)

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

fetch_housing_data()
logger.info(os.getcwd())
logger.info("Log is getting recorded")
def load_housing_data(housing_path=HOUSING_PATH):
    cur_dir=os.getcwd()
    csv_path =cur_dir+"/"+housing_path+"/housing.csv"
    return pd.read_csv(csv_path)



housing = load_housing_data(HOUSING_PATH)
 


train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)

housing["income_cat"] = pd.cut(
    housing["median_income"],
    bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
    labels=[1, 2, 3, 4, 5],
)


split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]


def income_cat_proportions(data):
    return data["income_cat"].value_counts() / len(data)
train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
compare_props = pd.DataFrame(
    {
        "Overall": income_cat_proportions(housing),
        "Stratified": income_cat_proportions(strat_test_set),
        "Random": income_cat_proportions(test_set),
    }
).sort_index()
compare_props["Rand. %error"] = (
    100 * compare_props["Random"] / compare_props["Overall"] - 100
)
compare_props["Strat. %error"] = (
    100 * compare_props["Stratified"] / compare_props["Overall"] - 100
)

for set_ in (strat_train_set, strat_test_set):
    set_.drop("income_cat", axis=1, inplace=True)



strat_train_set.to_csv(args.i[0][0]+"train_data.csv",index=False)
strat_test_set.to_csv(args.i[0][0]+"test_data.csv",index=False)

