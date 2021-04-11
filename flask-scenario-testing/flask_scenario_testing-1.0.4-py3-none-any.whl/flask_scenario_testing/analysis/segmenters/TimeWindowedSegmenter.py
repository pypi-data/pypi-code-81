from datetime import timedelta

from flask_scenario_testing.analysis.segmenters.Segmenter import Segmenter
from flask_scenario_testing.analysis.support.Measurement import Measurement
from flask_scenario_testing.analysis.support.MeasurementsSegment import MeasurementsSegment


class TimeWindowedSegmenter(Segmenter):

    def __init__(self, window_size: timedelta):
        self.window_size = window_size

    def segment(self, measurements: [Measurement]) -> [MeasurementsSegment]:
        if len(measurements) == 0:
            return []
        
        window_from = measurements[0].time

        idx = 0
        segments = []

        while window_from <= measurements[-1].time:
            measurements_group = []

            while idx < len(measurements) and measurements[idx].time < window_from + self.window_size:
                measurements_group.append(measurements[idx])

                idx += 1

            segment = MeasurementsSegment(
                start=window_from,
                time=window_from + self.window_size / 2,
                end=window_from + self.window_size,
                measurements=measurements_group
            )
            segments.append(segment)

            window_from = window_from + self.window_size

        return segments
