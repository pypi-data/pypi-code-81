from sklearn import datasets
from sklearn.linear_model import LogisticRegression
import joblib
from xgboost import XGBClassifier
import numpy as np

SKLearnFolder = "sklearn"
XGBoostFolder = "xgboost"


def load_iris() -> (np.ndarray, np.ndarray):
    iris = datasets.load_iris()
    X = iris.data  # we only take the first two features.
    y = iris.target
    return (X,y)

def train_sklearn(X: np.ndarray, y: np.ndarray, artifacts_folder: str):
    logreg = LogisticRegression(C=1e5)
    logreg.fit(X, y)
    logreg.predict_proba(X[0:1])
    with open(f"{artifacts_folder}/{SKLearnFolder}/model.joblib","wb") as f:
        joblib.dump(logreg, f)


def train_xgboost(X: np.ndarray, y:np.ndarray, artifacts_folder: str):
    clf = XGBClassifier()
    clf.fit(X, y)
    clf.save_model(f"{artifacts_folder}/{XGBoostFolder}/model.bst")