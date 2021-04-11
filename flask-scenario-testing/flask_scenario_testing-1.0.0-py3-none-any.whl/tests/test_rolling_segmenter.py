from datetime import datetime, timedelta

from flask_scenario_testing.analysis.segmenters.RollingSegmenter import RollingSegmenter
from flask_scenario_testing.analysis.support.Measurement import Measurement

now = datetime.now()
segmenter = RollingSegmenter(3)


def test_segmenting_window_size_equals_array_size():
    inputs = [
        Measurement(value=9, time=now),
        Measurement(value=12, time=now + timedelta(seconds=5)),
        Measurement(value=15, time=now + timedelta(seconds=10)),
    ]

    segments = segmenter.segment(inputs)
    assert len(segments) == 1

    assert segments[0].time == now + timedelta(seconds=5)

    assert len(segments[0].measurements) == 3

    assert segments[0].measurements[0].value == 9
    assert segments[0].measurements[1].value == 12
    assert segments[0].measurements[2].value == 15


def test_segmenting_window_size_smaller_than_array_size():
    inputs = [
        Measurement(value=9, time=now),
        Measurement(value=12, time=now + timedelta(seconds=5)),
    ]

    results = segmenter.segment(inputs)

    assert len(results) == 0


def test_segmenting_window_size_larger_than_array_size():
    inputs = [
        Measurement(value=100, time=now),
        Measurement(value=200, time=now + timedelta(seconds=5)),
        Measurement(value=300, time=now + timedelta(seconds=10)),
        Measurement(value=400, time=now + timedelta(seconds=15)),
        Measurement(value=500, time=now + timedelta(seconds=20)),
    ]

    results = segmenter.segment(inputs)

    assert len(results) == 3

    # First segment
    assert results[0].measurements[0].value == 100
    assert results[0].measurements[1].value == 200
    assert results[0].measurements[2].value == 300

    # Second segment
    assert results[1].measurements[0].value == 200
    assert results[1].measurements[1].value == 300
    assert results[1].measurements[2].value == 400

    # Third segment
    assert results[2].measurements[0].value == 300
    assert results[2].measurements[1].value == 400
    assert results[2].measurements[2].value == 500
