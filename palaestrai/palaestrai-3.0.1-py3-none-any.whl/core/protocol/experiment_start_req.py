from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.experiment import Experiment


class ExperimentStartRequest:
    """Request to a :class:`RunGovernor` to start a new experiment

    * Sender: :class:`Executor`
    * Receiver: class:`RunGovernor`

    :param experiment: The :class:`Experiment` that should be run
    :param experiment_run_id: Identification for this run of the given
        experiment
    """

    def __init__(self, experiment: Experiment, experiment_run_id):
        self._experiment = experiment
        self._experiment_id = experiment_run_id

    @property
    def experiment(self):
        return self._experiment

    @experiment.setter
    def experiment(self, value):
        self._experiment = value

    @property
    def experiment_run_id(self):
        return self._experiment_id

    @experiment_run_id.setter
    def experiment_run_id(self, value):
        self._experiment_id = value

    def __str__(self):
        return "ExperimentStartRequest for Experiment=%s" % self._experiment.id
