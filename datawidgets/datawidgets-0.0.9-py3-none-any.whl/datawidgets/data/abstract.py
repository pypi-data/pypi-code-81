from datawidgets.imports import *
from ..interface import *
from .image_mixins import *
from .mark_mixins import *


# TODO: Combine `AbstractDataItem` and `AbstractItemInterface` into one class
# Simply putting them together leads to some weird `__init__` error for downstream
# classes that inherit from the combined class. This is due to some weird Python
# behavior that I'm not entirely familiar with
class AbstractDataItem(
    AbstractItemInterface,
    MarkAsSelectedMixin,
    MarkAsDeletedMixin,
    MarkAsCompletedMixin,
    MarkAsReviewMixin,
):
    """
    Abstract data item base class. Sets up an API that works with the higher level dataset classes
    """

    @abstractmethod
    def load_item_bytes(self):
        pass

    @abstractmethod
    def load_item(self):
        pass

    def load(self):
        self.load_item()
        self.is_loaded = True
        self.needs_refresh = False

        self.setup_mark_selected()
        self.setup_mark_deleted()
        self.setup_mark_completed()
        self.setup_mark_review()

    def unload(self):
        self.needs_refresh = True
        self.item.value = b""

    def refresh(self):
        self.needs_refresh = False
        self.load_item_bytes()

    def setup(self):
        # Do nothing here for speedy instantiantion
        # Instead, call `.load()` when needed
        pass

    def setup_view(self):
        # Instantiate to blank view for speedy instantiantion
        self.view = None
