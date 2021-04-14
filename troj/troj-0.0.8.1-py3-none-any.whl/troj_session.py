import numpy as np
import json


"""

"""


class TrojSession:
    def __init__(self):
        super().__init__()
        # thing that makes requests to the troj api
        self.client = None
        # dataframe with the user's testing data

    def create_project(self, project_name: str):
        return self.client.create_project(project_name)

    def create_dataset(self, project_name: str, dataset_name: str):
        return self.client.create_dataset(project_name, dataset_name)

    def upload_dataframe(
        self, dataframe, project_name: str, dataset_name: str, drop_na=True
    ):
        if drop_na == True:
            dataframe = dataframe.dropna()
        # self.dataset.dataframe = self.dataset.dataframe[self.dataset.dataframe["stage"] == "train"]
        jsonified_df = json.loads(dataframe.to_json(orient="index"))

        return self.client.upload_df_results(project_name, dataset_name, jsonified_df)


def CreateClassifierInstance(
    model, input_shape, num_classes, loss_func=None, framework="pt"
):
    if framework == "pt":
        if loss_func is not None:
            from art.estimators.classification import PyTorchClassifier

            # ensure model is in eval mode, not sure how to check that rn
            classifier = PyTorchClassifier(model, loss_func, input_shape, num_classes)
        else:
            print("Pass in loss function with pytorch classifier!")

    elif framework == "tf":
        # ensure model is compiled tensorflow
        from art.estimators.classification import KerasClassifier

        if True:
            classifier = KerasClassifier(model)
    return classifier
