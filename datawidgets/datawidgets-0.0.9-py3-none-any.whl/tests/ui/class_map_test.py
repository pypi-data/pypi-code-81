import pytest
from datawidgets.ui.class_map import *


def test_class_map_buttons():
    labels = ["high", "low"]
    btns = ClassMapButtons(options=labels)

    assert btns.value == ()

    btns.children[0].value = True
    assert btns.value == ("high",)

    for i in btns.children:
        i.value = True
    assert btns.value == ("high", "low")
