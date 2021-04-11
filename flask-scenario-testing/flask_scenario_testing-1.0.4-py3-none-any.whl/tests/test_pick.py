from collections import namedtuple

from flask_scenario_testing.support.pick import pick


def test_pick():
    Point = namedtuple('Point', ['x', 'y'])

    points = [Point(x=3, y=5), Point(x=4, y=0)]

    assert pick(points, 'x')[0] == 3
    assert pick(points, 'x')[1] == 4

    assert pick(points, 'y')[0] == 5
    assert pick(points, 'y')[1] == 0
