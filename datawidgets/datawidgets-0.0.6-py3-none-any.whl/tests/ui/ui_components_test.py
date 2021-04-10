import pytest
from datawidgets.ui.ui_components import *


class Store:
    value = ["one", "two"]

    # Callbacks must accept *args, or at least one positional arg
    def reset(self, *args):
        self.value = []


def test_label_button():
    store = Store()

    btn = label_button("blah", callbacks=[store.reset])
    btn.click()

    assert store.value == []
