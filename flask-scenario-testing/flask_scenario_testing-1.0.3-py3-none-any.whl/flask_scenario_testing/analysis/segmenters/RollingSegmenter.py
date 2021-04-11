from flask_scenario_testing.analysis.segmenters.Segmenter import Segmenter
from flask_scenario_testing.analysis.support.Measurement import Measurement
from flask_scenario_testing.analysis.support.MeasurementsSegment import MeasurementsSegment


class RollingSegmenter(Segmenter):
    """
        Segments measurements by using a rolling window. Example for N=3:

        [1,2,3,4,5,6,7] => [1,2,3], [2,3,4], [4,5,6], [5,6,7]
    """

    def __init__(self, n, step=1):
        self.n = n
        self.step = step

    def segment(self, measurements: [Measurement]) -> [MeasurementsSegment]:
        center = int(self.n / 2)

        segments = []

        while center + (self.n - int(self.n / 2)) <= len(measurements):
            time = measurements[center].time

            relevant_measurements = measurements[center - int(self.n / 2): center + int(self.n / 2) + 1]

            segments.append(MeasurementsSegment(
                time=time,
                measurements=relevant_measurements,
                start=relevant_measurements[0].time,
                end=relevant_measurements[-1].time
            ))

            center += self.step

        return segments
