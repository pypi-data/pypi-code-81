from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from stackboost.loss_functions import MSE, SquareLoss
from stackboost.utils.data_operation import mean_squared_error
import numpy as np
from catboost import CatBoostRegressor
from stackboost.loss_functions import SquareLoss
from stackboost import ErrorTreeRegressor, DispersionTreeRegressor, SimilarityTreeRegressor
from stackboost import StackedGradientBoostingRegressor

X, y = load_boston(return_X_y=True)
from sklearn.model_selection import KFold

kf = KFold(n_splits=5, shuffle=True, random_state=42)
kf.get_n_splits(X)

ws = []
gs = []
ds = []
dis = []
xs = []

c = 0
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    dtc = SimilarityTreeRegressor(n_quantiles=33, l2_leaf_reg=0.1, max_depth=7)
    dtc.fit(X_train, y_train)
    preds = dtc.predict(X_test)
    score = mean_squared_error(y_test, preds)
    print(score)
    ws.append(score)

    # SGBR = StackedGradientBoostingRegressor(estimator=SimilarityTreeRegressor(l2_leaf_reg=0, n_quantiles=40, loss_function=MSE()), n_estimators=100, learning_rate=0.04, loss_function=MSE())
    # SGBR.fit(X_train, y_train, eval_set=(X_test, y_test), cat_features=np.array([3, 8]), use_best_model=True)
    # preds = SGBR.predict(X_test)
    # score = mean_squared_error(y_test, preds)
    # print(score)
    # gs.append(score)
    # SGBR.plot()



    print("<------------>")


print("Wave", sum(ws) / len(ws))
print("GBR", sum(gs) / len(gs))
# print("DTR", sum(ds) / len(ds))
# print("ADA", sum(ads) / len(ads))
# print("DIS", sum(dis) / len(dis))
# print("XGBR", sum(xs) / len(xs))

