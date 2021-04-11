import pytest
from datawidgets.ui.classification import *
from icevision.core.class_map import ClassMap

LABELS = ["high", "low"]
CLASS_MAP = ClassMap(classes=["high", "low", "aerial"], background=None)


def test_classification():
    # labels = ["high", "low"]
    btns = ClassificationLabelButtons(class_map=CLASS_MAP, labels=LABELS)

    assert btns.labels == LABELS
    assert len(btns.buttons.children) == len(LABELS)


def test_fail_invalid_label():
    btns = ClassificationLabelButtons(class_map=CLASS_MAP, labels=LABELS)

    with pytest.raises(InvalidLabelError):
        btns.append("overhead")


@pytest.mark.parametrize(
    ["source", "add_label", "result"],
    [
        (LABELS, "low", ["high", "low"]),
        (LABELS, "aerial", ["high", "low", "aerial"]),
    ],
)
def test_add_label(source, add_label, result):
    # labels = ["high", "low"]
    btns = ClassificationLabelButtons(class_map=CLASS_MAP, labels=source)
    btns.append(add_label)

    assert btns.labels == result
    assert len(btns.buttons.children) == len(result)


@pytest.mark.parametrize(
    ["source", "remove_label", "result"],
    [
        (LABELS, "high", ["low"]),
        (LABELS, "doesn't-exist...wont-be-removed", LABELS),
        ([], "doesn't exist...nothing-to-remove", []),
    ],
)
def test_remove_label(source, remove_label, result):
    btns = ClassificationLabelButtons(class_map=CLASS_MAP, labels=source)
    btns.remove(remove_label)

    assert btns.labels == result
    assert len(btns.buttons.children) == len(result)


@pytest.mark.parametrize(
    ["source", "remove_label", "result"],
    [
        (LABELS, "high", ["low"]),
    ],
)
def test_remove_label_on_click(source, remove_label, result):
    btns = ClassificationLabelButtons(class_map=CLASS_MAP, labels=source)
    btns.buttons.children[0].click()

    assert len(btns.labels) == 1
    assert btns.labels == ["low"]


class Store:
    value = ["one", "two"]
    class_map = ClassMap(classes=["one", "two"], background=None)

    # Callbacks must accept *args, or at least one positional arg
    def reset(self, *args):
        self.value = []


def test_additional_on_click_callback():
    store = Store()
    btns = ClassificationLabelButtons(
        class_map=store.class_map,
        labels=["one", "two"],
        callbacks=[store.reset],
    )
    btns.buttons.children[0].click()
    assert store.value == []
