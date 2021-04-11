from flask_scenario_testing.analysis.support.Measurement import Measurement
import numpy as np

from flask_scenario_testing.support.pick import pick


class MeasurementsSegment(object):
    def __init__(self, time, measurements: [Measurement], start, end):
        self.time = time
        self.measurements = measurements
        self.start = start
        self.end = end

    def mean(self):
        if len(self.measurements) == 0:
            return None

        return np.median(pick(self.measurements, 'value'))
