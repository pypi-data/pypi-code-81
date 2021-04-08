"""Abstract our TOML and structure its components."""
from typing import List


class RequestModel:
    """TOML abstraction."""

    def __init__(self, config: dict):
        """
        :param config: name of the config in the config folder
        """
        self._config = config
        self._verify_model()
        self._verify_data()
        self._verify_analyses()

    @property
    def dict(self) -> dict:
        """Get configuration dict."""
        return self._config

    @property
    def model(self) -> dict:
        """Obtain model dict."""
        return self.dict.get('model')

    @property
    def data(self) -> str:
        """Obtain list of data strings."""
        return self.dict.get('data')

    @property
    def analyses(self) -> dict:
        """Obtain dict of analyses."""
        return self.dict.get('analyses')

    def _verify_model(self):
        """Check if model is correctly implemented."""
        assert 'model' in self.dict, "Config needs model attribute."

        parameters = {
            "checkpoints", "task", "type", "framework",
            "input", "output", "start_eval", "prediction_window"
        }
        model_parameters = set(self.model.keys())
        assert parameters <= model_parameters, \
            f"Model is missing the {parameters - model_parameters} keys."

        if isinstance(self.model["checkpoints"], str):
            self.model["checkpoints"] = [self.model["checkpoints"]]

        assert len(self.model["checkpoints"]) == 1, "Only support one checkpoint."
        self.model["checkpoints"] = self.model["checkpoints"][0]

        input = self.model["input"]
        for input_column in input:
            column_dict = input[input_column]
            assert "type" in column_dict, "You must specify the type of the data column."
            continuous_col = 'min_value' in column_dict and 'max_value' in column_dict
            categorical_col = 'categories' in column_dict
            assert continuous_col or categorical_col, \
                "You must specify the range or provide categories for the data column."

        output = self.model["output"]
        for output_column in output:
            column_dict = output[output_column]
            assert "type" in column_dict, "You must specify the type of the data column."
            continuous_col = 'min_value' in column_dict and 'max_value' in column_dict
            categorical_col = 'categories' in column_dict
            assert continuous_col or categorical_col, \
                "You must specify the range or provide categories for the data column."

    def _verify_data(self):
        """Check if data is correctly specified."""
        assert 'data' in self.dict, "Config needs data attribute."
        assert self.data, "Please specify a data set."

        if isinstance(self.data, str):
            self._config["data"] = [self._config["data"]]
        assert len(self.data) == 1, "We only support one data set right now."
        self._config["data"] = self.data[0]

    def _verify_analyses(self):
        """Check if analyses are specified correctly."""
        assert "analyses" in self.dict, "Config needs analyses attribute."

        formatted_analyses = dict()
        for analysis in self.analyses:
            formatted_analyses[name2key(analysis)] = self.analyses[analysis]

        self._config["analyses"] = formatted_analyses


def name2key(name: str):
    """Converts a analysis name to according toml keys."""
    return name.lower().replace(" ", "_").replace("_/", "")
