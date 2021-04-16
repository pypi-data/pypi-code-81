
import optuna
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_predict
EPS = 1e-8
from kolibri.optimizers.metric import Metric
from kolibri.core.pipeline import Pipeline
import warnings
from copy import deepcopy
from sklearn.model_selection import train_test_split
from kdmt.objects import class_from_module_path, class_name
warnings.filterwarnings("ignore")



class Objective:
    def __init__(
        self,
        X,
        y,
        estimator,
        sample_weight,
        eval_metric=Metric({"name": "f1-score"}),
        random_state=41,
        n_jobs=-1,
        sample_weight_validation=None,
        direction='maximize'
        ):
        self.X = X
        self.y = y
        self.sample_weight = sample_weight
        self.parameters=deepcopy(estimator.hyperparameters)
        self.eval_metric = Metric({"name": "f1-score"})
        self.eval_metric_name="f1-score"
        self.n_jobs = n_jobs
        self.seed = random_state
        self.sample_weight_validation = sample_weight_validation
        self.estimator=estimator
        self.direction=direction

    def get_parameters(self, trial):
        params = deepcopy(self.parameters)
        for component, component_val in params.items():
            path=str(component)
            tunable=component_val["tunable"]
            path=path+".tunable"
            if tunable:
                for tuneable_key, tuneable_val in tunable.items():
                    if "type" in tuneable_val:
                        path2=path+"."+tuneable_key
                        if tuneable_val["type"] == "categorical" and "values" in tuneable_val:
                            tuneable_val["value"] = trial.suggest_categorical(path2, tuneable_val["values"])
                        elif tuneable_val["type"] == "integer" and "values" in tuneable_val:
                            tuneable_val["value"] = trial.suggest_int(path2, low=tuneable_val["values"][0],
                                                                      high=tuneable_val["values"][-1])
                        elif tuneable_val["type"] == "integer" and "range" in tuneable_val:
                            tuneable_val["value"] = trial.suggest_int(path2, low=tuneable_val["range"][0],
                                                                      high=tuneable_val["range"][-1])
                        elif tuneable_val["type"] == "float" and "values" in tuneable_val:
                            tuneable_val["value"] = trial.suggest_float(path2, low=tuneable_val["values"][0],
                                                                       high=tuneable_val["values"][-1])
                        elif tuneable_val["type"] == "float" and "range" in tuneable_val:
                            tuneable_val["value"] = trial.suggest_float(path2, low=tuneable_val["range"][0],
                                                                       high=tuneable_val["range"][-1])

                    else:
                        tuneable_val["value"] = tuneable_val["value"]

        return params

    def __call__(self, trial):
        raise NotImplementedError



class EstimatorObjective(Objective):

    def get_parameters3(self, original_params, trial, path=""):

        for tuneable_key, tuneable_val in original_params.items():
            if isinstance(tuneable_val, dict):
                if path == "":
                    path = tuneable_key
                else:
                    path += "." + tuneable_key
                if "type" in tuneable_val and "values" in tuneable_val:
                    if tuneable_val["type"] == "categorical":
                        tuneable_val["value"] = trial.suggest_categorical(path, tuneable_val["values"])
                    elif tuneable_val["type"] == "integer":
                        tuneable_val["value"] = trial.suggest_int(path, low=tuneable_val["values"][0],
                                                                 high=tuneable_val["values"][-1])
                    elif tuneable_val["type"] == "float":
                        tuneable_val["value"] = trial.suggest_float(path, low=tuneable_val["values"][0],
                                                                   high=tuneable_val["values"][-1])
                    path='.'.join(path.split('.')[:-1])
                elif isinstance(tuneable_val, dict):
                    self.get_parameters3(tuneable_val, trial, path)
                else:
                    tuneable_val[tuneable_key] = tuneable_val["value"]
            elif isinstance(tuneable_val, list):
                for i, val in enumerate(tuneable_val):
                    if isinstance(val, dict):
                        path+="."+str(i)
                        self.get_parameters3(val, trial, path)

                        path='.'.join(path.split('.')[:-1])

        return original_params

    # def get_parameters(self, trial):
    #     params = {}
    #     for tuneable_key, tuneable_val in self.parameters["parameters"].items():
    #         if isinstance(tuneable_val, dict):
    #             if "type" in tuneable_val:
    #                 if tuneable_val["type"] == "categorical":
    #                     params[tuneable_key] = trial.suggest_categorical(tuneable_key, tuneable_val["values"])
    #                 elif tuneable_val["type"] == "integer":
    #                     params[tuneable_key] = trial.suggest_int(tuneable_key, low=tuneable_val["values"][0],
    #                                                              high=tuneable_val["values"][-1])
    #                 elif tuneable_val["type"] == "float":
    #                     params[tuneable_key] = trial.suggest_float(tuneable_key, low=tuneable_val["values"][0],
    #                                                                high=tuneable_val["values"][-1])
    #             else:
    #                 params[tuneable_key] = tuneable_val["value"]
    #
    #     return params

    def get_parameters2(self, original_params, trial, path=""):
        params = {}
        for tuneable_key, tuneable_val in original_params.items():
            if isinstance(tuneable_val, dict):
                if path == "":
                    path = tuneable_key
                else:
                    path += "." + tuneable_key
                if "type" in tuneable_val:
                    if tuneable_val["type"] == "categorical":
                        params[tuneable_key] = trial.suggest_categorical(path, tuneable_val["values"])
                    elif tuneable_val["type"] == "integer":
                        params[tuneable_key] = trial.suggest_int(path, low=tuneable_val["values"][0],
                                                                 high=tuneable_val["values"][-1])
                    elif tuneable_val["type"] == "float":
                        params[tuneable_key] = trial.suggest_float(path, low=tuneable_val["values"][0],
                                                                   high=tuneable_val["values"][-1])
                    path='.'.join(path.split('.')[:-1])
                elif isinstance(tuneable_val, dict):
                    params.update(self.get_parameters2(tuneable_val, trial, path))
                else:
                    params[tuneable_key] = tuneable_val["value"]
            elif isinstance(tuneable_val, list):
                for i, val in enumerate(tuneable_val):
                    if isinstance(val, dict):
                        path+="."+str(i)
                        params.update(self.get_parameters2(val, trial, path))
                        path='.'.join(path.split('.')[:-1])

        return params

    def __call__(self, trial):
        try:
            params=self.get_parameters3(deepcopy(self.parameters), trial)


            model = class_from_module_path(class_name(self.estimator))(params)

            preds=cross_val_predict(model.model, self.X, self.y, cv=4, n_jobs=self.n_jobs)


            score = self.eval_metric(self.y, preds)
            if self.direction=='maximize':
                score *= -1.0

        except optuna.exceptions.TrialPruned as e:
            raise e
        except Exception as e:
            print("Exception in EstimatorObjective", str(e))
            if self.direction=="maximize":
                return -100000
            else:
                return 100000


        return score



class PipelineObjective(Objective):

    def __call__(self, trial):
        try:
            params=self.get_parameters(trial)


            pipeline = Pipeline.from_configs(params)


            X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size = 0.3, random_state = 42)


            pipeline.fit(X_train, y_train)
            pred=pipeline.predict(X_test)
            pred=[p['name'] for p in pred['label']]


            score = self.eval_metric(y_test, pred)
            if self.direction=='maximize':
                score *= -1.0

        except optuna.exceptions.TrialPruned as e:
            raise e
        except Exception as e:
            print("Exception in EstimatorObjective", str(e))
            if self.direction=="maximize":
                return -100000
            else:
                return 100000


        return score


