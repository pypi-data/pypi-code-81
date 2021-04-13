import pandas as pd
import numpy as np
import re

from arthurai.explainability.arthur_explainer import ArthurExplainer
from arthurai.common.constants import InputType, OutputType


def test_arthur_explainer_nlp_regression() -> None:
    def regression_predict(feature_vecs):
        results = []
        for fv in feature_vecs:
            results.append(np.array([0.2, 0.8]))
        return np.array(results)

    sample_data = pd.DataFrame([
        ['this is a test'],
        ['a second test with more words'],
        ['and a third test']
    ])

    explainer = ArthurExplainer(model_type=OutputType.Regression,
                                model_input_type=InputType.NLP,
                                num_predicted_attributes=1,
                                predict_func=regression_predict,
                                data=sample_data,
                                enable_shap=False,
                                label_mapping=[None])

    raw_feat_vecs = [
        ['first test test'],
        ['and a longer second test']
    ]
    exps = explainer.explain_nlp("lime", raw_feature_vectors=raw_feat_vecs, nsamples=100)

    # confirm we got 2 explanations
    assert len(exps) == 2

    for i, exp in enumerate(exps):
        # ensure single class
        assert len(exp) == 1
        # assert one explanation per unique word
        assert len(exp[0]) == len(re.split(explainer.text_delimiter, raw_feat_vecs[i][0]))


def test_arthur_explainer_nlp_classification() -> None:
    def regression_predict(feature_vecs):
        results = []
        for fv in feature_vecs:
            results.append(np.array([0.2, 0.7, 0.1]))
        return np.array(results)

    sample_data = pd.DataFrame([
        ['this is a test'],
        ['a second test with more words'],
        ['and a third test']
    ])

    explainer = ArthurExplainer(model_type=OutputType.Multiclass,
                                model_input_type=InputType.NLP,
                                num_predicted_attributes=3,
                                predict_func=regression_predict,
                                data=sample_data,
                                enable_shap=False,
                                label_mapping=[None])

    raw_feat_vecs = [
        ['first test test'],
        ['and a longer second test']
    ]
    exps = explainer.explain_nlp("lime", raw_feature_vectors=raw_feat_vecs, nsamples=100)

    # confirm we got 2 explanations
    assert len(exps) == 2

    for i, exp in enumerate(exps):
        # ensure single class
        assert len(exp) == 3
        # assert one explanation per unique word
        assert len(exp[0]) == len(re.split(explainer.text_delimiter, raw_feat_vecs[i][0]))
