import Orange
from collections import OrderedDict

import numpy
from AnyQt.QtWidgets import QTableWidget, QTableWidgetItem

import Orange.data
import Orange.classification
import Orange.evaluation
from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
import warnings
from Orange.widgets import gui, settings
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets.widget import OWWidget, Input
from Orange.evaluation.testing import Results

from bayes_opt import BayesianOptimization
from bayes_opt import UtilityFunction
import warnings
warnings.filterwarnings("ignore")


data = Orange.data.Table("iris.tab")
print("dataset shuffle")
data.shuffle()
score ={}
def black_box_function(n_estimators):
    s = {}
    n_estimators = int(n_estimators)
    rf = Orange.classification.RandomForestLearner(n_estimators=n_estimators)
    res = Orange.evaluation.CrossValidation(data, [rf], k=10)

    s[n_estimators] = Orange.evaluation.scoring.CA(res)[0]
    if n_estimators not in score.keys():
        score[n_estimators] = [s[n_estimators],Orange.evaluation.scoring.AUC(res)[0], Orange.evaluation.scoring.Precision(res, average='macro')[0], Orange.evaluation.scoring.Recall(res, average='macro')[0]]
    else:
        if score[n_estimators][0] < s[n_estimators]:
            score[n_estimators] = [s[n_estimators],Orange.evaluation.scoring.AUC(res)[0], Orange.evaluation.scoring.Precision(res, average='macro')[0], Orange.evaluation.scoring.Recall(res, average='macro')[0]]

    return Orange.evaluation.scoring.CA(res)[0]



optimizer = BayesianOptimization(
    f=black_box_function,
    pbounds={'n_estimators': (1, 5)},
    verbose=5
)
print("search hyper-parameters using bayesian optimization")
optimizer.maximize(init_points=50, n_iter=5, acq='ei', xi=0.6)
print("optimal hyper-parameters:", optimizer.max)
print(score)
'''
print("CA", Orange.evaluation.scoring.CA(res))
print("AUC", Orange.evaluation.scoring.AUC(res)[0])
print("Precision", Orange.evaluation.scoring.Precision(rf, average='macro'))
print("Recall", Orange.evaluation.scoring.Recall(res))'''