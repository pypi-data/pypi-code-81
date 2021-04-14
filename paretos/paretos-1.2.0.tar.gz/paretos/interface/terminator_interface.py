from .progress_interface import ProgressInterface


class TerminatorInterface:
    """Interface to describe Environments"""

    def should_terminate(self, progress: ProgressInterface) -> bool:
        """
        Interface method to guarantee that child classes implement this. Should be true
        when termination is desired
        :param progress: Progress to check whether termination should happen
        """
        raise NotImplementedError()
