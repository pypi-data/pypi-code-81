import optuna
from lightgbm import LGBMRegressor
from lightgbm import LGBMClassifier
from xgboost import XGBRegressor
from xgboost import XGBClassifier
from optuna.samplers import TPESampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.svm import SVC
from catboost import CatBoostClassifier
from catboost import CatBoostRegressor
from sklearn.metrics import get_scorer
from kowalsky.logs.utils import LivePyPlot
import math
from .df import read_dataset


family_params = {
    'lgb': {
        'learning_rate': ('uniform', 0.0000001, 1),
        'n_estimators': ('int', 1, 800),
        'max_depth': ('int', 2, 25),
        'num_leaves': ('int', 2, 3000),
        'min_child_samples': ('int', 3, 200)
    },
    'dt': {
        'max_depth': ('int', 2, 25),
        'min_samples_split': ('int', 2, 20),
        'min_weight_fraction_leaf': ('uniform', 0.0, 0.5),
        'min_samples_leaf': ('int', 1, 15)
    },
    'xgb': {
        'learning_rate': ('uniform', 0.0000001, 2),
        'n_estimators': ('int', 2, 800),
        'max_depth': ('int', 2, 25),
        'gamma': ('uniform', 0.0000001, 1),
        'random_state': 666
    },
    'rf': {
        'min_samples_leaf': ('int', 1, 15),
        'min_samples_split': ('uniform', 0.05, 1.0),
        'n_estimators': ('int', 2, 800),
        'max_depth': ('int', 2, 25),
        'random_state': 666
    },
    'et': {
        'min_samples_leaf': ('int', 1, 15),
        'min_samples_split': ('uniform', 0.05, 1.0),
        'max_depth': ('int', 2, 25),
        'random_state': 666
    },
    'bagg': {
        'n_estimators': ('int', 2, 300),
        'max_samples': ('int', 1, 400),
        'random_state': 666
    },
    'kn': {
        'n_neighbors': ('int', 2, 100)
    },
    'ada': {
        'n_estimators': ('int', 2, 800),
        'learning_rate': ('uniform', 0.0001, 1.0)
    },
    'svm': {
        'kernel': ('categorical', ['linear', 'poly']),
        'tol': ('uniform', 1e-5, 1),
        'C': ('loguniform', 1e-10, 1e10)
    },
    'cb': {
        'learning_rate': ('uniform', 0.0001, 1.0),
        'depth': ('int', 2, 16)
    }
}

models = {

    # Gradient Boosts
    'xgbR': (XGBRegressor, 'xgb'),
    'xgbC': (XGBClassifier, 'xgb'),
    'lgbR': (LGBMRegressor, 'lgb'),
    'lgbC': (LGBMClassifier, 'lgb'),

    # Trees
    'rfR': (RandomForestRegressor, 'rf'),
    'rfC': (RandomForestClassifier, 'rf'),
    'dtR': (DecisionTreeRegressor, 'dt'),
    'dtC': (DecisionTreeClassifier, 'dt'),
    'etR': (ExtraTreeRegressor, 'et'),
    'etC': (ExtraTreeClassifier, 'et'),

    # Ensemble
    'baggC': (BaggingClassifier, 'bagg'),
    'baggR': (BaggingRegressor, 'bagg'),
    'adaR': (AdaBoostRegressor, 'ada'),
    'adaC': (AdaBoostClassifier, 'ada'),
    'cbR': (CatBoostRegressor, 'cb'),
    'cbC': (CatBoostClassifier, 'cb'),

    # KNeighbors
    'knC': (KNeighborsClassifier, 'kn'),
    'knR': (KNeighborsRegressor, 'kn'),

    # SVM
    'svR': (SVR, 'svm'),
    'svC': (SVC, 'svm'),
}


def get_model(model_name, trial, custom_params={}):
    model, family = models[model_name]
    default_params = family_params[family]
    custom_params.update(default_params)
    params = {col: values[0] if len(values) == 1 else getattr(trial, f'suggest_{values[0]}')(col, *values[1:])
              for col, values in custom_params.items()}
    return model(**params)


class EarlyStoppingError(Exception):
    pass


class EarlyStopping:

    def __init__(self, direction, patience=100, threshold=1e-3):
        self.best = -math.inf if direction == 'maximize' else math.inf
        self.fn = max if direction == 'maximize' else min
        self.count = 0
        self.threshold = threshold
        self.patience = patience

    def __call__(self, value):
        new_value = self.fn(self.best, value)
        if abs(new_value - self.best) < self.threshold:
            self.count += 1
            if self.count > self.patience:
                raise EarlyStoppingError()
        else:
            self.count = 0
            self.best = new_value


def optimize(model_name, scorer, y_column, trials=30, sampler=TPESampler(seed=666),
             direction='maximize', patience=100, threshold=1e-3, feature_selection_support=None,
             feature_selection_cols=None, ds=None, path=None, sample_size=None, stratify=True,
             custom_params={}, ignore=[]):

    X_ds, y_ds = read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols, ignore,
                              sample_size, stratify)

    X_train, X_val, y_train, y_val = train_test_split(X_ds, y_ds)

    live = LivePyPlot(direction)
    stopping = EarlyStopping(direction, patience, threshold)

    def objective(trial):
        model = get_model(model_name, trial, custom_params)
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        error = get_scorer(scorer)._score_func(y_val, preds)
        live(error)
        stopping(error)
        return error

    study = optuna.create_study(direction=direction, sampler=sampler)

    try:
        study.optimize(objective, n_trials=trials, n_jobs=-1)
    except KeyboardInterrupt:
        print("Stopped with keyboard")
    except EarlyStoppingError:
        print("Stopped with early stopping")
    live.clear()

    return live.best, study.best_params
