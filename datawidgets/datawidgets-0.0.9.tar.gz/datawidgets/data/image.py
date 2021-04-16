from datawidgets.imports import *
from ..interface import *
from .image_mixins import *
from .mark_mixins import *
from .abstract import *


# from icevision.core.class_map import ClassMap


class ImageDataItem(AbstractDataItem, ClassificationLabelsMixin, NoteMixin):
    ""

    def __init__(
        self,
        numeric_id: int,
        source: Union[str, Path, Any],
        class_map: ClassMap = None,
        labels: Union[str, List[str]] = [],
        is_multilabel: bool = True,
        width: int = 100,
        parent_dataset=None,
    ):
        self.numeric_id = numeric_id
        if not isinstance(self.numeric_id, int):
            raise TypeError(
                f"Expected `numeric_id` to be of type {int} but got {type(self.numeric_id)} instead"
            )

        if class_map is None:
            class_map = ClassMap(classes=[], background=None)
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

        # This calls `AbstractInterface`'s init
        super().__init__(source=source, width=width)

    def setup_mark_selected(self):
        "Sets up mouse interaction events - select / unselect on click"

        def on_mouse_enter(*args):
            if not self.is_selected:
                self.item.add_class(CSS_NAMES.IMG_BOX_HOVER)

        def on_mouse_leave(*args):
            if not self.is_selected:
                self.item.remove_class(CSS_NAMES.IMG_BOX_HOVER)

        self.setup_mouse_interaction(
            on_mouse_enter_callbacks=[on_mouse_enter],
            on_mouse_leave_callbacks=[on_mouse_leave],
            on_mouse_click_callbacks=[self.toggle_selected_status],
        )

    def load_item_bytes(self):
        if "https://" in self.source:
            self.item.value = requests.get(self.source).content
        else:
            self.item.value = Path(self.source).read_bytes()

    def load_item(self):
        self.item = widgets.Image(width=f"100%")
        self.item.add_class(CSS_NAMES.IMG_BOX)
        self.load_item_bytes()

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
        self.id_display = widgets.HTML(value=f"ID: {self.numeric_id}")
        self.id_display.add_class(CSS_NAMES.NUMERIC_ID)

    def update_view_minimal(self):
        # Not needed? Better safe than sorry.
        if self.is_loaded:
            self.view.children = [self.item]
            self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER)
            self.view.add_class(CSS_NAMES.IMG_BOX_CONTAINER_MINIMAL)

    # # NOTE: This is a simpler `update_view` left here to better
    # # understand the core of what happens inside the function
    # def update_view(self):
    #     if self.is_loaded:
    #         self.view = VBox([])
    #         self.view.layout = Layout(width=f"{self.width}%")
    #         self.view.add_class(f"{CSS_NAMES.IMG_BOX_CONTAINER}")
    #         self.view.children = [self.item]

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
                self.item,
                self.note,
                HBox(
                    [
                        self.toggle_note_button,
                        self.searchbox,
                        self.id_display,
                    ]
                ),
                self.label_buttons.buttons,
            ]
            self.view.add_class(f"{CSS_NAMES.IMG_BOX_CONTAINER}")
            self.view.remove_class(CSS_NAMES.IMG_BOX_CONTAINER_MINIMAL)
        else:
            pass
