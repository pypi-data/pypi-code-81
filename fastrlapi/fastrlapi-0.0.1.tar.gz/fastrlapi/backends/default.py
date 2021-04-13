from typing import Type, Dict

from fastrlapi.backends import core as bcore
import fastrlapi.core


class TensorforceNotActiveAgent(bcore.BackendAgent):

    def __init__(self, model_config: fastrlapi.core.ModelConfig, backend_name: str):
        raise NotImplementedError(
            "Call agents.activate_tensorforce() to activate tensorforce before instantiating the first agent."
            "This agent is implemented by tensorforce. Due to an incompatibility"
            "between tensorforce and tfagents their agents can not be instantiated in the"
            "same python runtime instance (conflicting excpectations on tensorflows eager execution mode)."
        )


class TfAgentsNotActiveAgent(bcore.BackendAgent):

    def __init__(self, model_config: fastrlapi.core.ModelConfig, backend_name: str):
        raise NotImplementedError(
            "Do not call agents.activate_tensorforce() before instantiating a tfagents based agent."
            "This agent is implemented by tfagents. Due to an incompatibility"
            "between tensorforce and tfagents their agents can not be instantiated in the"
            "same python runtime instance (conflicting excpectations on tensorflows eager execution mode)."
        )


class SetTensorforceBackendAgent(bcore.BackendAgent):

    def __init__(self, model_config: fastrlapi.core.ModelConfig, backend_name: str):
        raise NotImplementedError(
            "Set the backend='tensorforce' argument in the fastrlapi constructor call. "
            "This agents default implementation is implemented by tfagents. Due to an incompatibility"
            "between tensorforce and tfagents their agents can not be instantiated in the"
            "same python runtime instance (conflicting excpectations on tensorflows eager execution mode)."
        )


class NotImplementedYetAgent(bcore.BackendAgent):

    def __init__(self, model_config: fastrlapi.core.ModelConfig, backend_name: str):
        raise NotImplementedError("fastrlapi implementation is pending.")


class DefaultAgentFactory(bcore.BackendAgentFactory):
    """Backend which redirects all calls to the some default implementation."""

    def __init__(self, register_tensorforce: bool):
        self.register_tensorforce = register_tensorforce

    backend_name = 'default'

    def get_algorithms(self) -> Dict[Type, Type[fastrlapi.backends.core.BackendAgent]]:
        """Yields a mapping of EasyAgent types to the implementations provided by this backend."""
        #                fastrlapi.agents.CemAgent: fastrlapi.backends.kerasrl.KerasRlCemAgent,
        #                fastrlapi.agents.DoubleDqnAgent: fastrlapi.backends.kerasrl.KerasRlDoubleDqnAgent,
        if self.register_tensorforce:
            import fastrlapi.backends.tforce

            result = {
                fastrlapi.agents.DqnAgent: SetTensorforceBackendAgent,
                fastrlapi.agents.DoubleDqnAgent: TfAgentsNotActiveAgent,
                fastrlapi.agents.DuelingDqnAgent: fastrlapi.backends.tforce.TforceDuelingDqnAgent,
                fastrlapi.agents.PpoAgent: SetTensorforceBackendAgent,
                fastrlapi.agents.RandomAgent: SetTensorforceBackendAgent,
                fastrlapi.agents.ReinforceAgent: SetTensorforceBackendAgent,
                fastrlapi.agents.SacAgent: TfAgentsNotActiveAgent}
        else:
            import fastrlapi.backends.tfagents

            result = {
                fastrlapi.agents.DqnAgent: fastrlapi.backends.tfagents.TfDqnAgent,
                fastrlapi.agents.DoubleDqnAgent: NotImplementedYetAgent,
                fastrlapi.agents.DuelingDqnAgent: TensorforceNotActiveAgent,
                fastrlapi.agents.PpoAgent: fastrlapi.backends.tfagents.TfPpoAgent,
                fastrlapi.agents.RandomAgent: fastrlapi.backends.tfagents.TfRandomAgent,
                fastrlapi.agents.ReinforceAgent: fastrlapi.backends.tfagents.TfReinforceAgent,
                fastrlapi.agents.SacAgent: fastrlapi.backends.tfagents.TfSacAgent}
        return result
