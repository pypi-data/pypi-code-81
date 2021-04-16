import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import get_scorer
from .kaggle import make_sub
from joblib import dump
from .df import read_dataset


def analysis(model, y_column, eval_method='cv', path=None, path_test=None, path_out=None,
             ds=None, ds_test=None, export_test_set=False, sample_path=None,
             rounds=1, eval_model=True, target_transform_fn=None, scorer=None,
             export_model_path=None, export_model=False, verbose=False, cv=5,
             feature_selection_support=None, feature_selection_cols=None, train_model=True,
             test_size=0.25, ignore=[], sample_size=None, stratify=True):

    X, y = read_dataset(ds, path, y_column, feature_selection_support, feature_selection_cols,
                        ignore, sample_size, stratify)

    if eval_model:
        if verbose: print("Evaluation...")
        if eval_method == 'cv':
            print(f'Score (cv={cv}): ', np.array(
                [abs(cross_val_score(model, X, y, n_jobs=-1, scoring=scorer, cv=cv).mean()) for _ in range(rounds)]
            ).mean())
        elif eval_method == 'test':
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            print(f'Score (test={X_test.shape[0]}): ', abs(get_scorer(scorer)._score_fn(y_test, preds)))

    if train_model and eval_method != 'test':
        if verbose: print("Training...")
        model.fit(X, y)

    if export_model and export_model_path is not None:
        dump(model, export_model_path)

    if export_test_set and \
            path_out is not None and \
            sample_path is not None and \
            (path_test is not None or ds_test is not None):
        if ds_test is None:
            ds_test = pd.read_csv(path_test)

        if verbose: print("Prediction...")
        preds = model.predict(ds_test)

        if target_transform_fn is not None:
            preds = target_transform_fn(preds)
        make_sub(preds, path_out, sample_path, y_column)

    if verbose: print("Done")
    return model
