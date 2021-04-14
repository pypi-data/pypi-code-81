"""Create a RequestModel for a Black-Box attack."""
from typing import List

from aidkitcli.core.utils import create_toml
from aidkitcli.core.request_model import RequestModel
from aidkitcli.data_access.stored_model_access import load_stored_model


def blackbox(data: str,
             model: str,
             epsilon: List[float],
             start_index: int = 0,
             perturbation_length: int = 100000,
             population_nr: int = 100,
             selection_nr: int = 10,
             evolutionary_step: int = 5,
             ascend: bool = True,
             mask: List[int] = [],
             step_length: List[int] = [],
             title="Config Black-Box Attack"
             ) -> RequestModel:
    """
    Create a RequestModel for a Black-Box Attack. The execution of this request
    creates one perturbation per file in the data set. The perturbation is then
    added to every eligible data point in the corresponding data file. Finally,
    the performance of the model on the clean and the perturbed data is
    displayed on a plot.

    By default, all the data points are eligible to be perturbed. This changes
    if step_length determines that a certain number of consecutive
    perturbations should be the same or if start_index/perturbation_length
    limits the number of data points that can be perturbed in a data file.

    The perturbations are generated via an evolutionary algorithm, where
    the fitness function is determined by the output neuron of the given
    regression model. Population candidates are generated via a uniform
    distribution, and the crossover is given by an addition and clipping
    operation.

    Currently, this attack strategy can be applied to Keras regression
    recurrent ML models and the data set must consist only of quantitative
    variables.

    :param data: name of the data set
    :param model: path to the TOML file that contains the model information
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
    :param title: title of the configuration (default: "Config Black-Box
        Attack")
    :return: a RequestModel instance containing all the information needed to
        execute a Black-Box Attack
    """
    stored_model = load_stored_model(path=model)
    toml_dict = create_toml(
        title=title,
        data=data,
        stored_model=stored_model,
        adversarial_attack={"blackbox": {
            "epsilon": epsilon,
            "start_index": start_index,
            "perturbation_length": perturbation_length,
            "population_nr": population_nr,
            "selection_nr": selection_nr,
            "evolutionary_step": evolutionary_step,
            "ascend": ascend,
            "mask": mask,
            "step_length": step_length,
            "saver": 1
        }}
    )
    return RequestModel(toml_dict)
