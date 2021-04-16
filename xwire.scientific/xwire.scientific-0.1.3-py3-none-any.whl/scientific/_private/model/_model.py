from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load


def random_forest(n_estimators: int) -> RandomForestClassifier:
    return RandomForestClassifier(n_estimators=n_estimators)


def train_model(classifier, features, labels):
    classifier.fit(features, labels)


def persist_model(classifier, filename: str):
    dump(classifier, filename)


def load_model(filename: str):
    return load(filename)