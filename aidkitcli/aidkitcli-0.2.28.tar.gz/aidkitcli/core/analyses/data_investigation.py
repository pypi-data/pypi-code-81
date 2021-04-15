"""Create a RequestModel for a Data Investigation analysis."""

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def data_investigation(
    data: str, model: str, target_output: int = 0, title="Config Data Investigation Analysis"
) -> RequestModel:
    """
    Create a Request model to analyze the statistics and distribution of the
    provided data through five plots and the value of four metrics. If the
    model has multiple outputs, only the output whose index is given by
    target_output is considered.

    The plots displayed after executing this request are:
        - "File Length Plot" - comparison between the different lengths of the
        provided data files
        - "Box Plots of Input Variables" - boxplots that show the distribution
        of each numerical input variable over the data files through their
        quartiles, i.e. minimum and maximum value, median, Q1 and Q3
        - "Output Statistics" - boxplot that shows the development of the mean,
        minimum, 50% and maximum values of the output variable over all the
        different files. If there is only one file the boxplot shows the
        development of these values of the output variable in that single file.
        - "Input Correlations" - Pearson correlations between each numerical
        input variable
        - "Output Correlations" - Pearson correlations between each numerical
        input variable to the output

    The metrics calculated are:
        - number of data files
        - mean value of the length of the provided data files
        - minimum value of length of the provided data files
        - maximum value of length of the provided data files

    This analysis supports the following models:
        - Keras (multi-)regression recursive models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models
    The data set must have more than 4 quantitative variables.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param target_output: the index of the output column used for the
                          statistical calculations (only relevant for
                          multivariable regression)
    :param title: title of the configuration (default: "Config Data
        Investigation Analysis")
    :return: a RequestModel instance containing all the information needed to
        execute a Data Investigation Analysis
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        data_investigation={"target_output": target_output},
    )
    return RequestModel(toml_dict)
