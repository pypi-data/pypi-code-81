"""Create a RequestModel to execute an FGSM attack."""
from typing import List

from aidkitcli.core.analyses.fgsm import fgsm as request_factory
from aidkitcli.core.execute_analysis import execute_analysis
from aidkitcli.core.report import Report


def fgsm(data: str,
         model: str,
         epsilon: List[float],
         start_index: int = 0,
         perturbation_length: int = 100000,
         iteration_step: int = 10,
         ascend: bool = True,
         mask: List[int] = [],
         step_length: List[int] = [],
         title: str = "Config FGSM Attack"
         ) -> Report:
    """
    Execute a Fast Gradient Sign Method Attack that creates a perturbation per
    eligible data point in each file of the data set and return a plot showing
    the performance of the model on the clean and the perturbed data.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive
    perturbations should be the same or if start_index/perturbation_length
    limits the number of data points that can be perturbed in a data file.

    The perturbations are generated using the gradient of the neural network
    following this formula:

    x_perturbed = x + epsilon * sign[grad_x(loss(x, y, params))]

    The idea is to add a perturbation - scaled by epsilon - whose direction is
    the same as the gradient of the loss function w.r.t. the data.

    If the task of the attacked model is regression, the perturbation tries to
    increase or decrease - depending on the value of ascend - the value of the
    output node (the loss). If the task is classification the perturbation
    tries to decrease the probability value of the original prediction.

    Currently, this attack strategy can be applied to:

    - Keras regression recurrent models
    - Keras classification feedforward models
    - scikit-learn classification feedforward models

    The data set must consist only of quantitative variables.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
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
    :param title: title of the configuration (default: "Config FGSM Attack")
    """
    request_model = request_factory(
        title=title,
        data=data,
        model=model,
        epsilon=epsilon,
        start_index=start_index,
        perturbation_length=perturbation_length,
        iteration_step=iteration_step,
        ascend=ascend,
        mask=mask,
        step_length=step_length,
    )
    return execute_analysis(request_model=request_model)
