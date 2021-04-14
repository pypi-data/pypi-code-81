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