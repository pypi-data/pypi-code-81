"""Create a RequestModel to execute a Data Investigation analysis."""

from typing import Dict

from aidkitcli.core.analyses.data_investigation import data_investigation as request_factory
from aidkitcli.data_access.analysis import post_analysis


def data_investigation(data: str, model: str,
                       title: str = "Config Data Investigation Analysis") -> Dict[str, int]:
    """
    Analyze the statistics and distribution of the provided data through five
    plots and the value of four metrics.

    The plots displayed are:

    - "File Length Plot" - comparison between the different lengths of the
      provided data files
    - "Box Plots of Input Variables" - boxplots that show the distribution of
      each numerical input variable over the data files through their quartiles,
      i.e. minimum and maximum value, median, Q1 and Q3
    - "Output Statistics" - boxplot that shows the development of the mean,
      minimum, 50% and maximum values of the output variable over all the
      different files. If there is only one file the boxplot shows the
      development of these values of the output variable in that single file.
    - "Input Correlations" - Pearson correlations between each numerical input
      variable
    - "Output Correlations" - Pearson correlations between each numerical
      input variable to the output

    The metrics calculated are:

    - number of data files
    - mean value of the length of the provided data files
    - minimum value of length of the provided data files
    - maximum value of length of the provided data files

    This analysis supports the following models:

    - Keras regression recursive models
    - Keras classification feedforward models
    - scikit-learn classification feedforward models

    The data set must have more than 4 quantitative variables.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param title: title of the configuration (default: "Config Data
        Investigation Analysis")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
    )
    return post_analysis(request_model=request_model)
