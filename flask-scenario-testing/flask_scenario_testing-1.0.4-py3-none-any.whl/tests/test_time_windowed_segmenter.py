from datetime import timedelta, datetime

from flask_scenario_testing.analysis.segmenters.TimeWindowedSegmenter import TimeWindowedSegmenter
from flask_scenario_testing.analysis.support.Measurement import Measurement

segmenter = TimeWindowedSegmenter(timedelta(seconds=6))
now = datetime.now()


def test_stuff():
    inputs = [
        Measurement(value=9, time=now),
        Measurement(value=12, time=now + timedelta(seconds=4)),
        Measurement(value=15, time=now + timedelta(seconds=8)),
    ]

    segments = segmenter.segment(inputs)

    assert len(segments) == 2

    # Check segment 1
    assert len(segments[0].measurements) == 2
    assert segments[0].measurements[0].value == 9
    assert segments[0].measurements[1].value == 12
    assert segments[0].time == now + timedelta(seconds=3)

    # Check segment 2
    assert len(segments[1].measurements) == 1
    assert segments[1].measurements[0].value == 15
    assert segments[1].time == now + timedelta(seconds=9)


def test_with_measurements_on_the_border_of_windows():
    inputs = [
        Measurement(value=9, time=now),
        Measurement(value=12, time=now + timedelta(seconds=6)),
        Measurement(value=15, time=now + timedelta(seconds=12)),
    ]

    segments = segmenter.segment(inputs)

    # Segment 1
    assert len(segments[0].measurements) == 1
    assert segments[0].measurements[0].value == 9
    assert segments[0].time == now + timedelta(seconds=3)

    # Segment 2
    assert len(segments[1].measurements) == 1
    assert segments[1].measurements[0].value == 12
    assert segments[1].time == now + timedelta(seconds=9)

    # Segment 3
    assert len(segments[2].measurements) == 1
    assert segments[2].measurements[0].value == 15
    assert segments[2].time == now + timedelta(seconds=15)
