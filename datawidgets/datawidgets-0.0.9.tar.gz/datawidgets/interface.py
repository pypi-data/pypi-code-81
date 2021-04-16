from datawidgets.imports import *


class AbstractInterface(ABC):
    """
    Base class for singular data items as well as datasets

    Subclasses must implement the following methods:
    1. setup() - where all the backend components are initialised
    2. setup_view() - where all the UI components are created and
                      set to `self.view`

    * Subclasses have logging support via `self.log` and
      logs can be viewed in `self.logs`
    * Some subclasses may define a custom `__init__`. When they do,
      it's usually a good idea to call `super().__init__` at the end
      of the custom `__init__` definition
    """

    def __init__(self, source: Union[str, Path, Any], width: int = 100):
        # Store filepath, create image, setup logs
        self.source = str(source)
        self.width = width

        self.setup()
        self.setup_logging()
        self.setup_view()
        self.update_view()

    def load(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def setup_view(self):
        pass

    def update_view(self):
        pass

    def setup_logging(self):
        self.logs = widgets.Output()
        self.log("Logging initialised")

    def log(self, message):
        with self.logs:
            print(message)

    def _repr_html_(self):
        display(self.view)

    def __repr__(self):
        return ""


class AbstractItemInterface(AbstractInterface):
    # Main data item
    item = None

    # Mark attributes
    is_modified = False
    is_loaded = False
    is_selected = False
    is_deleted = False
    is_completed = False
    is_under_review = False
    needs_refresh = False

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def refresh(self):
        pass

    @abstractmethod
    def update_view(self):
        pass

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

        By default, `self.item` is watched, but this can be altered by passing
        in a custom widget / element to `event_source`
        """

        def mouse_interaction(event):
            if event["type"] == "mouseenter":
                self.log("Mouse entered item region")
                for cb in on_mouse_enter_callbacks:
                    cb()

            elif event["type"] == "mouseleave":
                self.log("Mouse left item region")
                for cb in on_mouse_leave_callbacks:
                    cb()

            elif event["type"] == "click":
                self.log("Item clicked")
                for cb in on_mouse_click_callbacks:
                    cb()

        ev = Event(
            source=self.item if event_source is None else event_source,
            watched_events=["click", "mouseenter", "mouseleave"],
        )
        ev.on_dom_event(mouse_interaction)

    def __repr__(self):
        if self.view is None:
            if not self.is_loaded:
                return f"Unloaded {self.__class__}. Call `.load()` and `.update_view()`"
            else:
                return f"Call `.update_view()` to view item"
        return ""
