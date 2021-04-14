"""
Simulation data recorder.

Maxwell X. Cai, April 2021.

"""


class SimulationDataRecorder(object):

    def __init__(self, particles=None, quantities=['a', 'ecc', 'inc'], buffer_len=0):

        self._monitored_particles = particles
        self._monitored_quantities = quantities
        self._buffer_len = 0
        self._buffer_cursor = 0

        # initialize storage
        self.data_dict = dict()

    def reset(self):
        del self.data_dict
        self.data_dict = dict()
 
    def record(self, state_dict):
        if self._monitored_quantities is not None:
            for i, qty in enumerate(self._monitored_quantities):
                if qty in state_dict:
                    if self.data_dict[quantities] is not None: