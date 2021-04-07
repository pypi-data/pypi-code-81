# -*- coding: utf-8 -*-
"""Testing the from_xy module"""
import pytest

from pytojcamp import from_xy


def test_from_xy(make_dataset):
    """Test conversion from x/y data"""
    x, y = make_dataset  # pylint:disable=invalid-name

    with pytest.raises(ValueError):
        from_xy(x)

    jcamp_string = from_xy(
        (x, y),
        "TestTile",
        "TestOwner",
        "TestOrigin",
        "TestData",
        "cm",
        "kg",
        {"hello": "world"},
    )

    expected_string = """##TITLE=TestTile
##JCAMP-DX=4.24
##DATA TYPE=TestData
##ORIGIN=TestOrigin
##OWNER=TestOwner
##XUNITS=cm
##YUNITS=kg
##FIRSTX=0
##LASTX=9
##FIRSTY=10
##LASTY=19
##NPOINTS=10
##$hello=world
##PEAK TABLE=(XY..XY)
0  10
1  11
2  12
3  13
4  14
5  15
6  16
7  17
8  18
9  19
##END"""

    assert jcamp_string == expected_string

    with pytest.raises(ValueError):
        jcamp_string = from_xy(
            (x, y),
            "TestTile",
            "TestOwner",
            "TestOrigin",
            "TestData",
            "cm",
            "kg",
            "meta",
        )
