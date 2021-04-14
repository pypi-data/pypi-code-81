"""Create a RequestModel to execute a Key Robustness Indicator analysis."""
from typing import List, Union

from aidkitcli.core.analyses.kri import BlackboxDistribution, ConstantDistribution, CorrelationDistribution, \
    Distribution, FGSMDistribution, IncreaseDistribution, PeakDistribution, RandomDistribution, \
    RelativeConstantDistribution
from aidkitcli.core.analyses.kri import kri as request_factory
from aidkitcli.core.execute_analysis import execute_analysis
from aidkitcli.core.report import Report


def constant_distribution_factory(variable_name: str,
                                  constant: Union[float, str],
                                  start_index: int = 0,
                                  perturbation_length: int = 100000
                                  ) -> ConstantDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Constant Corruption. This object can then be fed to the KRI
    function to determine a robustness risk score.

    When a Constant Corruption is executed, the values of the selected variable
    are replaced with a constant value given by the constant parameter.

    This corruption can be applied to both quantitative and categorical input
    variables. The supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param constant: constant value of the perturbation
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = ConstantDistribution(
        variable_name=variable_name,
        constant=constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def relative_constant_distribution_factory(variable_name: str,
                                           relative_constant: float,
                                           start_index: int = 0,
                                           perturbation_length: int = 100000
                                           ) -> RelativeConstantDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Relative Constant Corruption. This object can then be fed to the
    KRI function to determine a robustness risk score.

    When a Relative Constant Corruption is executed, the values of the selected
    variable are increased or decreased by a constant value relative_constant.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param relative_constant: constant value added to the original data
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = RelativeConstantDistribution(
        variable_name=variable_name,
        relative_constant=relative_constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def increase_distribution_factory(variable_name: str,
                                  step_length: int,
                                  start_constant: float,
                                  end_constant: float,
                                  start_index: int = 0,
                                  perturbation_length: int = 100000
                                  ) -> IncreaseDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Increase Corruption. This object can then be fed
    to the KRI function to determine a robustness risk score.

    When an Increase Corruption is executed, the values of the selected
    variable are first set to the start_constant value and then changed every
    step_length data points in the file. Depending on whether end_constant is
    bigger or smaller than start_constant, the values are increased or
    decreased after step_length data points.

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param step_length: number of data points with a constant value before
        the next increase/decrease
    :param start_constant: starting value of the perturbation
    :param end_constant: maximal corruption value that should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = IncreaseDistribution(
        variable_name=variable_name,
        step_length=step_length,
        start_constant=start_constant,
        end_constant=end_constant,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def random_distribution_factory(variable_name: str,
                                step_length: int,
                                lower_bound: float,
                                upper_bound: float,
                                start_index: int = 0,
                                perturbation_length: int = 100000
                                ) -> RandomDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Random Corruption. This object can then be fed to the KRI
    function to determine a robustness risk score.

    When a Random Corruption is executed, the values of the selected variable
    are set to random values sampled from a uniform distribution within the
    fixed range [lower_bound, upper_bound].

    This corruption can only be applied to quantitative input variables. The
    supported ML models are:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models

    :param variable_name: name of the variable to corrupt
    :param step_length: number of data points with a constant value before
        the next increase/decrease
    :param lower_bound: minimal corruption value which should not be surpassed
    :param upper_bound: maximal corruption value which should not be surpassed
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    """
    distribution = RandomDistribution(
        variable_name=variable_name,
        step_length=step_length,
        lower_bound=lower_bound,
        upper_bound=upper_bound,
        start_index=start_index,
        perturbation_length=perturbation_length,
        saver=1
    )
    return distribution


def fgsm_distribution_factory(epsilon: List[float],
                              start_index: int = 0,
                              perturbation_length: int = 100000,
                              iteration_step: int = 10,
                              ascend: bool = True,
                              mask: List[int] = [],
                              step_length: List[int] = [],
                              target_output: int = 0,
                              ) -> FGSMDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute an FGSM Attack. This object can then be fed to the KRI function to
    determine a robustness risk score.

    An FGSM Attack creates a perturbation per eligible data point in each file
    of the data set and return a plot showing the performance of the model on
    the clean and the perturbed data.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated using the gradient of the neural network
    following this formula:
        x_perturbed = x + epsilon * sign[grad_x(loss(x, y, params))]

    The idea is to add a perturbation - scaled by epsilon - whose direction is
    the same as the gradient of the loss function w.r.t. the data.

    If the task of the attacked model is regression, the perturbation tries to
    increase or decrease - depending on the value of ascend - the value of the
    output node (the loss). For multiregression models, it tries to increase
    or decrease the value of the output node whose index is given by
    target_output. If the task is classification, the perturbation
    tries to decrease the probability value of the original prediction.

    Currently, this attack strategy can be applied to:
        - Keras regression recurrent models
        - Keras classification feedforward models
        - scikit-learn classification feedforward models
    The data set must consist only of quantitative variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param ascend: whether the output value should increase (True) or decrease
        (False). Only needed if the attack is applied to a regression model
    :param mask: list of binary values that decide whether a variable can be
        perturbed by the attack, the list length must be the number of
        variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    :param target_output: the index of the output neuron the algorithm tries
                          to modify (only relevant for multiregression models)
    """
    distribution = FGSMDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        ascend=ascend,
        mask=mask,
        step_length=step_length,
        target_output=target_output,
        saver=1
    )
    return distribution


def correlation_distribution_factory(epsilon: List[float],
                                     start_index: int = 0,
                                     perturbation_length: int = 100000,
                                     iteration_step: int = 10,
                                     mask: List[int] = [],
                                     step_length: List[int] = [],
                                     target_output: int = 0,
                                     ) -> CorrelationDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Correlation Attack. This object can then be fed to the KRI
    function to determine a robustness risk score.

    A Correlation Attack creates a perturbation per eligible data point in each
    file of the data set and return a plot showing the performance of the model
    on the clean and the perturbed data.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated via a gradient-based optimization
    algorithm whose objective function penalizes the correlation between the
    predicted values and the true labels. For multiregression models, the
    objective function considers the output coordinate given by target_output.

    Currently, this attack strategy can be applied to Keras (multi-)regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param mask: list of binary values that decide whether a variable can be
        perturbed by the attack, the list length must be the number of
        variables
    :param step_length: number of time steps with constant value before next
        increase or decrease
    """
    distribution = CorrelationDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        mask=mask,
        step_length=step_length,
        target_output=target_output,
        saver=1
    )
    return distribution


def peak_distribution_factory(epsilon: List[float],
                              start_index: int = 0,
                              perturbation_length: int = 100000,
                              iteration_step: int = 10,
                              mask: List[int] = [],
                              step_length: List[int] = [],
                              target_output: int = 0,
                              ) -> PeakDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Peak Attack. This object can then be fed to the KRI function to
    determine a robustness risk score.

    A Peak Attack creates a perturbation per eligible data point in each file
    of the data set and return a plot showing the performance of the model on
    the clean and the perturbed data.

    The perturbations affect perturbation_length values starting at some point
    after start_index. The attack compares the MSE values of the different
    perturbations and using gradient information it optimizes the deviation of
    the predictions from the labels to find the consecutive data points in the
    data set where the highest possible "peak" error is achieved. For
    multiregression models, only the error of the output variable whose index
    is given by target_output is considered.

    The idea is to find the area in the file after start_index where the
    perturbation of perturbation_length values has the biggest impact.

    Currently, this attack strategy can be applied to Keras (multi-)regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param iteration_step: number of iterations in the attack
    :param mask: list of binary values that decide whether a variable can be
        perturbed by the attack, the list length must be the number of
        variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    :param target_output: the index of the output neuron the algorithm tries
                          to maximize the error of (only relevant for
                          multiregression models)
    """
    distribution = PeakDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        mask=mask,
        step_length=step_length,
        target_output=target_output,
        saver=1
    )
    return distribution


def blackbox_distribution_factory(epsilon: List[float],
                                  start_index: int = 0,
                                  perturbation_length: int = 100000,
                                  population_nr: int = 100,
                                  selection_nr: int = 10,
                                  evolutionary_step: int = 5,
                                  ascend: bool = True,
                                  mask: List[int] = [],
                                  step_length: List[int] = [],
                                  target_output: int = 0,
                                  ) -> BlackboxDistribution:
    """
    Create a distribution object containing all the parameters needed to
    execute a Black-Box Attack. This object can then be fed to the KRI function
    to determine a robustness risk score.

    A Black-Box Attack creates one perturbation per file in the data set. The
    perturbation is then added to every eligible data point in the corresponding
    data file. Finally, the performance of the model on the clean and the
    perturbed data is displayed on a plot.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive perturbations
    should be the same or if start_index/perturbation_length limits the number
    of data points that can be perturbed in a data file.

    The perturbations are generated via an evolutionary algorithm, where
    the fitness function is determined by the output neuron of the given
    regression model. Population candidates are generated via a uniform
    distribution, and the crossover is given by an addition and clipping
    operation. If the given model is a multiregression model, the algorithm
    aims to change the output neuron with the index given by target_output.

    Currently, this attack strategy can be applied to Keras (multi-)regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param epsilon: array of maximal L^inf perturbations for every variable
    :param start_index: data points before this index will not be perturbed
    :param perturbation_length: number of data points perturbed
    :param population_nr: number of potential perturbations (candidates) in
    one population
    :param selection_nr: number of perturbations selected from population
    :param evolutionary_step: number of evolutions (crossover/mutations)
    :param ascend: whether the output value should increase (True) or decrease
        (False)
    :param mask: list of binary values that decide whether a variable can be
        perturbed by the attack, the list length must be the number of
        variables
    :param step_length: number of time steps with constant value before next
    increase or decrease
    :param target_output: the index of the output neuron the algorithm tries
                          to modify (only relevant for multiregression models)
    """
    distribution = BlackboxDistribution(
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        population_nr=population_nr,
        selection_nr=selection_nr,
        evolutionary_step=evolutionary_step,
        ascend=ascend,
        mask=mask,
        step_length=step_length,
        target_output=target_output,
        saver=1
    )
    return distribution


def kri(data: str, model: str,
        p_x: List[float], p_cond: List[float],
        distributions: List[Distribution],
        title: str = "Config KRI Analysis"
        ) -> Report:
    """
    Calculate the key robustness indicators (KRI) of the model on the basis of
    a given data set and realistic distributions for the deployment context.
    The relevance (probability of occurrence) of the data files and the
    distributions is given by the probability vectors p_x and p_cond. The method
    returns three different risk scores, based on different severity estimation:

    - Average Absolute Error of the predictions w.r.t. the labels (useful for
      regression)
    - Maximal Error of the predictions w.r.t. the labels (useful for
      regression)
    - Percentage of Errors / Accuracy (useful for classification)

    A more detailed explanation of this analysis can be found in the following
    paper: https://arxiv.org/abs/2011.04328

    The analysis can be executed using different corruption distributions
    and adversarial attacks:

    - "constant" - Constant Corruption
    - "relative_constant" - Relative Constant Corruption
    - "increase" - Increase Corruption
    - "random" - Random Corruption
    - "fgsm" - Fast Gradient Sign Method Attack
    - "correlation" - Correlation Attack
    - "peak" - Peak Attack
    - "blackbox" - Black-Box Attack

    Each distribution has its own parameters. Check the documentation of each
    factory method (<distribution_name>_distribution_factory) for a more
    detailed explanation of the different corruptions and attacks and their
    parameters.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
    :param p_x: list of the probabilities of occurrence of a data file in the
        deployment context, the length of the list must be equal to the number
        of data files in the provided data set and the probabilities must sum
        up to 1
    :param p_cond: list of the probabilities of each distribution
        (corruption/attack) given a data set, the length of the list must be
        equal to the number of distributions and the probabilities must sum up
        to 1
    :param distributions: list of the distributions (corruptions/attacks) for
        the KRI analysis, each distribution is created by its corresponding
        factory method <distribution_name>_distribution_factory
    :param title: title of the configuration (default: "Config KRI Analysis")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        p_x=p_x,
        p_cond=p_cond,
        distributions=distributions
    )
    return execute_analysis(request_model=request_model)
