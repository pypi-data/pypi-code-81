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

    strict_positive_matching_class_map = False

    def setup_class_map_filtering(self):
        self.class_map_positive_buttons = MultiChoiceButtons(options=self.classes)
        self.class_map_negative_buttons = MultiChoiceButtons(options=self.classes)
        self.class_map_matching_mode_toggle = widgets.ToggleButton(
            value=self.strict_positive_matching_class_map,
            description="Strict Matching Mode",
        )
        self.class_map_matching_mode_toggle.observe(self.switch_class_map_matching_mode)

    def switch_class_map_matching_mode(self, *args):
        self.strict_positive_matching_class_map = (
            not self.strict_positive_matching_class_map
        )

    @property
    def positive_class_map_filter(self):
        if self.strict_positive_matching_class_map:
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
        filtering_controls = VBox(
            [
                HBox(
                    [self.class_map_filter_button, self.class_map_matching_mode_toggle],
                ),
                HBox(
                    [positive_controls, negative_controls],
                ),
            ]
        )
        filtering_controls = widgets.Accordion(children=[filtering_controls])
        filtering_controls.set_title(0, f"  Class Map Filtering Controls")
        filtering_controls.add_class(CSS_NAMES.FILTERING_CONTROLS_ACCORDION)
        self.class_map_filtering_controls = filtering_controls

        # Add CSS Classes & Layouts
        positive_heading.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_HEADING)
        positive_controls.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_CONTAINER)
        self.class_map_positive_buttons.layout = CSS_LAYOUTS.class_map_positive_buttons
        self.class_map_positive_buttons.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_BUTTONS)
        self.class_map_matching_mode_toggle.add_class(CSS_NAMES.TOGGLE_BUTTON)
        self.class_map_matching_mode_toggle.add_class(CSS_NAMES.TOGGLE_MATCHING_MODE)

        negative_heading.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_HEADING)
        negative_controls.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_CONTAINER)
        self.class_map_negative_buttons.layout = CSS_LAYOUTS.class_map_negative_buttons
        self.class_map_negative_buttons.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_BUTTONS)

        self.class_map_filtering_controls.layout = CSS_LAYOUTS.flex_layout_col


class MetadataFilterMixin:
    """
    Adds positive + negative filtering support for any combination
      of labels from `self<DatasetClass>.class_map`.
    """

    _works_with = "ImageClassificationDataset"
    _requires = "ImageGridMixin"

    strict_positive_matching_metadata = False

    def setup_metadata_filtering(self):
        self.metadata_positive_buttons = MultiChoiceButtons(
            options=self.metadata_classes
        )
        self.metadata_negative_buttons = MultiChoiceButtons(
            options=self.metadata_classes
        )
        self.metadata_matching_mode_toggle = widgets.ToggleButton(
            value=self.strict_positive_matching_metadata,
            description="Strict Matching Mode",
        )
        self.metadata_matching_mode_toggle.observe(self.switch_metadata_matching_mode)

    def switch_metadata_matching_mode(self, *args):
        self.strict_positive_matching_metadata = (
            not self.strict_positive_matching_metadata
        )

    @property
    def positive_metadata_filter(self):
        if self.strict_positive_matching_metadata:
            positive_filter = self._get_metadata_filter(
                self.metadata_positive_buttons, all_match
            )
        else:
            positive_filter = self._get_metadata_filter(
                self.metadata_positive_buttons, any_match
            )

        if self.metadata_positive_buttons.value == ():
            positive_filter = ~positive_filter  # set all to True

        return positive_filter

    @property
    def negative_metadata_filter(self):
        return self._get_metadata_filter(self.metadata_negative_buttons, no_match)

    @property
    def metadata_subset_filter(self):
        return self.positive_metadata_filter & self.negative_metadata_filter

    def _get_metadata_filter(self, metadata_buttons, func: Callable):
        return self.df[self.metadata_col].apply(
            lambda label: func(metadata_buttons.value, label)
        )

    def generate_metadata_filtering_button(self, global_callbacks=[]):
        button = Button(description="Filter Metadata")

        button.on_click(self.update_grid)
        for cb in global_callbacks:
            button.on_click(cb)

        return button

    def setup_metadata_filtering_view(self, global_callbacks):
        positive_heading = widgets.HTML("Positive Metadata Filters")
        negative_heading = widgets.HTML("Negative Metadata Filters")

        positive_controls = VBox(
            [
                positive_heading,
                self.metadata_positive_buttons,
            ]
        )
        negative_controls = VBox(
            [
                negative_heading,
                self.metadata_negative_buttons,
            ]
        )

        self.metadata_filter_button = self.generate_metadata_filtering_button(
            global_callbacks=global_callbacks
        )
        filtering_controls = VBox(
            [
                HBox(
                    [
                        self.metadata_filter_button,
                        self.metadata_matching_mode_toggle,
                    ],
                ),
                HBox(
                    [positive_controls, negative_controls],
                ),
            ]
        )
        filtering_controls = widgets.Accordion(children=[filtering_controls])
        filtering_controls.set_title(0, f"  Metadata Filtering Controls")
        filtering_controls.add_class(CSS_NAMES.FILTERING_CONTROLS_ACCORDION)
        self.metadata_filtering_controls = filtering_controls

        # Add CSS Classes & Layouts
        positive_heading.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_HEADING)
        positive_controls.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_CONTAINER)
        self.metadata_positive_buttons.layout = CSS_LAYOUTS.class_map_positive_buttons
        self.metadata_positive_buttons.add_class(CSS_NAMES.CLASS_MAP_POSITIVE_BUTTONS)
        self.metadata_matching_mode_toggle.add_class(CSS_NAMES.TOGGLE_BUTTON)
        self.metadata_matching_mode_toggle.add_class(CSS_NAMES.TOGGLE_MATCHING_MODE)

        negative_heading.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_HEADING)
        negative_controls.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_CONTAINER)
        self.metadata_negative_buttons.layout = CSS_LAYOUTS.class_map_negative_buttons
        self.metadata_negative_buttons.add_class(CSS_NAMES.CLASS_MAP_NEGATIVE_BUTTONS)

        self.metadata_filtering_controls.layout = CSS_LAYOUTS.flex_layout_col
