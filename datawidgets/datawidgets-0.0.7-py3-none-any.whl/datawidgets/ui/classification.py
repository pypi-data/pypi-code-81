from datawidgets.imports import *
from .ui_components import *
from .style import *


class InvalidLabelError(Exception):
    pass


class ClassificationLabelButtons:
    def __init__(
        self,
        class_map: ClassMap,
        labels: Sequence[str] = [],
        callbacks: Sequence[Callable] = [],
    ):
        self.callbacks = callbacks
        self.classes = class_map._id2class
        self.buttons = Box(
            children=[self.create_button(l) for l in labels],
            layout=CSS_LAYOUTS.flex_layout,
        )

    def check_label_validity(self, label: str):
        if not label in self.classes:
            raise InvalidLabelError

    def create_button(self, label: str, callbacks=[]):
        self.check_label_validity(label)
        button = label_button(
            label,
            callbacks=[lambda x: self.remove(button.description)],
        )
        for cb in self.callbacks + callbacks:
            button.on_click(cb)
        return button

    @property
    def labels(self):
        return [l.description for l in self.buttons.children]

    def append(self, label: str, callbacks=[]):
        "Add `label` to self.labels"
        # Skip if duplicate label
        if label in self.labels:
            return

        buttons = list(self.buttons.children)
        buttons.append(self.create_button(label, callbacks=callbacks))
        self.buttons.children = buttons

    def remove(self, label: str):
        "Remove `label` from self.labels"
        self.buttons.children = [
            l for l in self.buttons.children if not l.description == label
        ]

    def _repr_html_(self):
        display(self.buttons)

    def __len__(self):
        return len(self.labels)

    def __repr__(self):
        info = [f"Label Buttons Container with {len(self)} labels:", f"{self.labels}"]
        return " ".join(info)