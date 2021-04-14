from datawidgets.imports import *
from ..interface import *
from .image_mixins import *
from .mark_mixins import *


# from icevision.core.class_map import ClassMap


class ImageDataPoint(
    AbstractInterface,
    ImageLoaderMixin,
    MarkAsSelectedMixin,
    MarkAsDeletedMixin,
    MarkAsCompletedMixin,
    MarkAsReviewMixin,
):
    is_modified = False
    is_loaded = False
    is_selected = False
    is_deleted = False
    is_completed = False
    is_under_review = False
    needs_refresh = False

    def load(self):
        self.load_img()
        self.setup_mark_selected()
        self.setup_mark_deleted()
        self.setup_mark_completed()
        self.setup_mark_review()

    def unload(self):
        self.unload_img_bytes()

    def setup(self):
        # Do nothing here for speedy instantiantion
        # Instead, call `.load()` when needed
        pass

    def setup_view(self):
        # Instantiate to blank view for speedy instantiantion
        self.view = None

    def update_view(self):
        if self.is_loaded:
            self.view = VBox([])
            self.view.layout = Layout(width=f"{self.width}%")
            self.view.add_class(f"{CSS_NAMES.IMG_BOX_CONTAINER}")
            self.view.children = [self.img]

    def setup_mouse_interaction(
        self,
        on_mouse_enter_callbacks: List[Callable] = [],
        on_mouse_leave_callbacks: List[Callable] = [],
        on_mouse_click_callbacks: List[Callable] = [],
        event_source: Optional[widgets.Widget] = None,
    ):
        """
        Generalised mechanism for setting up mouse hover and click events.
        Simply pass in callback functions to the respective arguments

        By default, `self.img` is watched, but this can be altered by passing
        in a custom widget / element to `event_source`
        """

        def mouse_interaction(event):
            if event["type"] == "mouseenter":
                self.log("Mouse entered image region")
                for cb in on_mouse_enter_callbacks:
                    cb()

            elif event["type"] == "mouseleave":
                self.log("Mouse left image region")
                for cb in on_mouse_leave_callbacks:
                    cb()

            elif event["type"] == "click":
                self.log("Image clicked")
                for cb in on_mouse_click_callbacks:
                    cb()

        ev = Event(
            source=self.img if event_source is None else event_source,
            watched_events=["click", "mouseenter", "mouseleave"],
        )
        ev.on_dom_event(mouse_interaction)

    def __repr__(self):
        if self.view is None:
            if not self.is_loaded:
                return f"Unloaded {self.__class__}. Call `.load()` and `.update_view()`"
            else:
                return f"Call `.update_view()` to view image"
        return ""


class ImageWithLabels(ImageDataPoint, ClassificationLabelsMixin, NoteMixin):
    ""

    def __init__(
        self,
        class_map: ClassMap,
        source: Union[str, Path, Any],
        labels: Union[str, List[str]] = [],
        is_multilabel: bool = False,
        width: int = 100,
        parent_dataset=None,
    ):
        self.class_map = class_map
        self.classes = self.class_map._id2class
        self.is_multilabel = is_multilabel
        self.dset = parent_dataset

        if isinstance(labels, str):
            labels = [labels]
        if not isinstance(labels, list):
            raise TypeError(f"Expected a list of labels, got {type(labels)}")

        # HACK ...fuck this...
        self._labels = labels

        super().__init__(source=source, width=width)

    def load(self):
        super().load()
        self.setup_note()
        self.setup_mouse_interaction()
        self.setup_labelling()

    def setup(self):
        # Call mixins' setup methods
        super().setup()

    def sync_dset_width_slider(self):
        "Syncs `self.view`'s width to the dataset's width slider"

        if self.dset is not None:
            if hasattr(self.dset, "width_slider"):
                # self.view.layout = Layout(width=f"{self.dset.width_slider.value}%")
                self.dset.width_slider.observe(
                    lambda x: setattr(
                        self.view,
                        "layout",
                        Layout(width=f"{self.dset.width_slider.value}%"),
                    ),
                    "value",
                )

    def setup_dset_interaction_events(self):
        """
        Sets up mouse click events to update elements of the parent dataset
        when the image is clicked
        """
        if self.dset is not None:
            self.setup_mouse_interaction(
                on_mouse_click_callbacks=[
                    self.dset.update_batch_labelling_descriptions,
                    self.dset.update_info,
                ]
            )

    def setup_view(self):
        self.view = None

    def update_view_minimal(self):
        # Not needed? Better safe than sorry.
        if self.is_loaded:
            self.view.children = [self.img]
            self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER)
            self.view.add_class(CSS_NAMES.IMG_BOX_CONTAINER_MINIMAL)

    def update_view(self):
        if self.is_loaded:
            if self.view is None:
                # Don't reinitialise if already created
                self.view = VBox([])

                if self.dset is not None:
                    self.view.layout = Layout(width=f"{self.dset.width_slider.value}%")
                else:
                    self.view.layout = Layout(width=f"{self.width}%")

                self.sync_dset_width_slider()
                self.setup_dset_interaction_events()

            self.view.children = [
                self.img,
                self.note,
                HBox([self.toggle_note_button, self.searchbox]),
                self.label_buttons.buttons,
            ]
            self.view.add_class(f"{CSS_NAMES.IMG_BOX_CONTAINER}")
            self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER_MINIMAL)
        else:
            pass
