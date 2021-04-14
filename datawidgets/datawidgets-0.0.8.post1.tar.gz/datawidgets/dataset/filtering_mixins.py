from datawidgets.imports import *
from datawidgets.utils import *
from datawidgets.data import *
from .image_dataset import *


def num_matches(this: Collection[str], that: Collection[str]):
    return len(set(this).intersection(that))


def no_match(this: Collection[str], that: Collection[str]):
    return num_matches(this, that) == 0


def any_match(this: Collection[str], that: Collection[str]):
    return num_matches(this, that) >= 1


def all_match(this: Collection[str], that: Collection[str]):
    "Is all of `this` in `that`?"
    return num_matches(this, that) == len(this)


class ClassMapFilterMixin:
    """
    Adds positive + negative filtering support for any combination
      of labels from `self<DatasetClass>.class_map`.
    """

    _works_with = "ImageClassificationDataset"
    _requires = "ImageGridMixin"

    strict_positive_matching = False

    def setup_class_map_filtering(self):
        self.class_map_positive_buttons = ClassMapButtons(options=self.classes)
        self.class_map_negative_buttons = ClassMapButtons(options=self.classes)
        self.positive_matching_toggle = widgets.ToggleButton(
            value=self.strict_positive_matching, description="Exact Matching Mode"
        )
        self.positive_matching_toggle.observe(self.switch_positive_toggle_mode)

    def switch_positive_toggle_mode(self, *args):
        self.strict_positive_matching = not self.strict_positive_matching

    @property
    def positive_class_map_filter(self):
        if self.strict_positive_matching:
            positive_filter = self._get_filter(
                self.class_map_positive_buttons, all_match
            )
        else:
            positive_filter = self._get_filter(
                self.class_map_positive_buttons, any_match
            )

        if self.class_map_positive_buttons.value == ():
            positive_filter = ~positive_filter  # set all to True

        return positive_filter

    @property
    def negative_class_map_filter(self):
        return self._get_filter(self.class_map_negative_buttons, no_match)

    @property
    def class_map_subset_filter(self):
        return self.positive_class_map_filter & self.negative_class_map_filter

    def _get_filter(self, class_map_buttons, func: Callable):
        return self.df[self.label_col].apply(
            lambda label: func(class_map_buttons.value, label)
        )

    def generate_class_map_filtering_button(self, global_callbacks=[]):
        button = Button(description="Filter Dataset")

        button.on_click(self.update_grid)
        for cb in global_callbacks:
            button.on_click(cb)

        return button

    def setup_class_map_filtering_view(self, global_callbacks):
        positive_heading = widgets.HTML("Positive Filters")
        negative_heading = widgets.HTML("Negative Filters")

        positive_controls = VBox(
            [
                positive_heading,
                self.class_map_positive_buttons,
            ]
        )
        negative_controls = VBox(
            [
                negative_heading,
                self.class_map_negative_buttons,
            ]
        )

        self.class_map_filter_button = self.generate_class_map_filtering_button(
            global_callbacks=global_callbacks
        )
        self.class_map_filtering_controls = VBox(
            [
                HBox(
                    [self.class_map_filter_button, self.positive_matching_toggle],
                ),
                HBox(
                    [positive_controls, negative_controls],
                ),
            ]
        )

        # Add CSS Classes & Layouts
        positive_heading.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_HEADING)
        positive_controls.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_CONTAINER)
        self.class_map_positive_buttons.layout = CSS_LAYOUTS.class_map_positive_buttons
        self.class_map_positive_buttons.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_BUTTONS)
        self.positive_matching_toggle.add_class(CSS_NAMES.TOGGLE_BUTTON)
        self.positive_matching_toggle.add_class(CSS_NAMES.TOGGLE_MATCHING_MODE)

        negative_heading.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_HEADING)
        negative_controls.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_CONTAINER)
        self.class_map_negative_buttons.layout = CSS_LAYOUTS.class_map_negative_buttons
        self.class_map_negative_buttons.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_BUTTONS)

        self.class_map_filtering_controls.layout = CSS_LAYOUTS.flex_layout_col
