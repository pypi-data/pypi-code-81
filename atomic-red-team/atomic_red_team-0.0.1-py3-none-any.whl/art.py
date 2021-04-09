import os
import logging

from .atomic.parser import Parser
from .utils.exceptions import IncorrectParameters
__LOGGER__ = logging.getLogger(__name__)
from .helpers import Helpers


class AtomicRedTeam:

    __techniques = None

    def __init__(self, atomics_path=None):
        self.__helper = Helpers()
        if not atomics_path:
            # TODO: Add ability to download from remote source
            self.atomics_path = atomics_path
        else:
            self.atomics_path = os.path.abspath(os.path.expanduser(os.path.expandvars(atomics_path)))

    def __get_techniques(self):
        if not self.__techniques:
            self.__techniques = self.__helper.load_techniques(self.atomics_path)
        return self.__techniques

    def run(self, technique: str='All', position: int=0, dependencies=True, cleanup=True, **kwargs):
        if self.__get_techniques().get(technique):
            # process this technique
            # execute this technique
            pass
        elif technique == 'All':
            # process all techniques
            for key,val in self.__techniques.items():
                __LOGGER__.info(f"Processing Technique {val.get('attack_technique')} ({val.get('display_name')})")
                parsed = Parser().parse(val)
                print(parsed.__dict__)
                input('press')
            pass
        else:
            pass
