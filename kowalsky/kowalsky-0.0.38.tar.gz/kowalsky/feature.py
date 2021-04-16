import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from kowalsky.logs.utils import LivePyPlot
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
import matplotlib.pyplot as plt
from sklearn.metrics import get_scorer
import numpy as np
import math


def calc_score(model, X, y, type='cv', scoring=None, cv=5):
    if type == 'cv':
        return abs(cross_val_score(model, X, y, scoring=scoring, cv=cv, n_jobs=-1, verbose=10).mean())
    elif type == 'test':
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        return abs(get_scorer(scoring)._score_func(y_test, preds))
    else:
        raise Exception(f'Wrong type: {type} (use cv/test)')


def rfe_analysis(model, y_column, scoring, direction, cv=3, ranking=None, path=None, ds=None,
                 sample_size=None, n_features_to_select=5, precision=1e-3, stratify=False, eval_type='cv'):
    if ds is None:
        ds = pd.read_csv(path)

    if sample_size is not None:
        ds, _ = train_test_split(ds, train_size=sample_size, stratify=ds[y_column] if stratify else None)

    X, y = ds.drop(y_column, axis=1), ds[y_column]

    if ranking is None:
        rfe = RFE(model, step=1, verbose=10, n_features_to_select=n_features_to_select)
        try:
            rfe.fit(X, y)
        except KeyboardInterrupt:
            print("Stopped with keyboard")
            return
        ranking = rfe.ranking_
    else:
        ranking = np.array(ranking)

    print(pd.DataFrame({
        'column': X.columns,
        'ranking': ranking
    }).sort_values(by='ranking').values)

    live = LivePyPlot(direction=direction, show_true_value=True)

    best_score = -math.inf if direction == 'maximize' else math.inf
    best_columns = None

    try:
        for rank in range(1, np.max(ranking) + 1):
            rank_columns = X.columns[ranking <= rank]
            score = calc_score(model, X[rank_columns], y, type=eval_type, cv=cv, scoring=scoring)
            live(score, sum(ranking <= rank))

            is_better_score = score > best_score + precision if direction == 'maximize' else score < best_score - precision
            if is_better_score:
                best_score = score
                best_columns = ranking <= rank
    except KeyboardInterrupt:
        print("Stopped with keyboard")

    live.clear()

    return best_columns, ranking


def sfs_analysis(model, y_label, scoring, k_features, cv=3, forward=True, floating=False, path=None,
                 sample_size=None, stratify=False, ds=None):
    if ds is None:
        ds = pd.read_csv(path)

    if sample_size is not None:
        ds, _ = train_test_split(ds, train_size=sample_size, stratify=ds[y_label] if stratify else None)

    X, y = ds.drop(y_label, axis=1), ds[y_label]

    selector = SFS(model, forward=forward, floating=floating, verbose=10,
                   scoring=scoring, cv=cv, n_jobs=-1, k_features=k_features)
    try:
        selector.fit(X, y)
    except KeyboardInterrupt:
        print("Stopped with keyboard")

    plot_sfs(selector.get_metric_dict(), kind='std_dev')

    plt.grid()
    plt.show()

    return selector.get_metric_dict()
