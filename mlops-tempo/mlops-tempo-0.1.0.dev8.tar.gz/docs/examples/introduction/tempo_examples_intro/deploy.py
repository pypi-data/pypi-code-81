import numpy as np
from typing import Tuple
from tempo.serve.metadata import ModelFramework
from tempo.serve.model import Model
from tempo.serve.pipeline import PipelineModels, Pipeline
from tempo.seldon.protocol import SeldonProtocol
from tempo.serve.utils import pipeline
from tempo_examples_intro.models import SKLearnFolder, XGBoostFolder


PipelineFolder = "classifier"


def get_tempo_artifacts(artifacts_folder:str) -> Pipeline:
    sklearn_model = Model(
        name="test-iris-sklearn",
        platform=ModelFramework.SKLearn,
        protocol=SeldonProtocol(),
        local_folder=f"{artifacts_folder}/{SKLearnFolder}",
        uri="s3://tempo/basic/sklearn"
    )

    xgboost_model = Model(
        name="test-iris-xgboost",
        platform=ModelFramework.XGBoost,
        protocol=SeldonProtocol(),
        local_folder=f"{artifacts_folder}/{XGBoostFolder}",
        uri="s3://tempo/basic/xgboost"
    )

    @pipeline(
         name="classifier",
         uri="s3://tempo/basic/pipeline",
         local_folder=f"{artifacts_folder}/{PipelineFolder}",
         models=PipelineModels(sklearn=sklearn_model, xgboost=xgboost_model)
    )
    def classifier(payload: np.ndarray) -> Tuple[np.ndarray,str]:
        res1 = classifier.models.sklearn(payload)

        if res1[0][0] > 0.5:
            return res1, "sklearn prediction"
        else:
            return classifier.models.xgboost(payload), "xgboost prediction"

    return classifier
