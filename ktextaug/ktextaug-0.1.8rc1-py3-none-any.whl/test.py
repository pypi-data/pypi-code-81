from file_utils import checkout

# checkout()

# import ktextaug.transformative
# import ktextaug
# print(ktextaug.__package__)


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

# import .ktextaug  # relative-import the *package* containing the templates
import ktextaug
pkg_resources.read_text(ktextaug, 'stopwords-ko.txt')