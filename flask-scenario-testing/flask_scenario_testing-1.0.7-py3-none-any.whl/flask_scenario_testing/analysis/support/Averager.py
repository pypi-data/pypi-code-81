
from flask_scenario_testing.analysis.segmenters.Segmenter import Segmenter
from flask_scenario_testing.analysis.support.Measurement import Measurement


class Averager(object):
    def __init__(self, segmenter: Segmenter, should_round: bool = False):
        self.segmenter = segmenter
        self.should_round = should_round

    def average(self, data):
        segments = self.segmenter.segment(data)

        return [
            Measurement(time=s.time, value=round(s.mean()) if self.should_round else s.mean())
            for s in segments
        ]
