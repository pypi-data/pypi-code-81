"""Models"""
from typing import Callable, Optional

from composite_field import CompositeField
from django.conf import settings
from django.db.models import TextField
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

MarkdownCompiler = Callable[[str], str]


def get_setting(key, default):
    """Returns key from SETTINGS if exists and default if it does not"""
    return getattr(settings, key, default)


class CustomMarkdownxField(MarkdownxField):
    """Markdownx Field which updates the entire composite field when updated"""
    def get_name(self):
        """Shortcut for getting composite field name"""
        return self.attname.split("_")[0]

    def save_form_data(self, instance, data):
        setattr(instance, self.get_name(), data)


class HiddenTextField(TextField):
    """Text field hidden in form used for caching purposes"""
    def formfield(self, **kwargs):
        return None


class CachedMarkdownField(CompositeField):
    """
    Composite markdown field which caches and compiles markdown to html on every update.
    Saves on compiling costs on every request.
    """
    markdown = CustomMarkdownxField()
    cached = HiddenTextField(null=True)

    # pylint: disable=too-many-arguments
    def __init__(self, compiler: Optional[MarkdownCompiler] = None, prefix=None, default=None,
                 verbose_name=None, help_text=None):
        """
        Creates new CachedMarkdownField

        :param compiler: Callable, which takes Markdown text and returns html text
        :param prefix: Prefix for generated fields, passed to CompositeField
        :param default: Default value, passed to CompositeField
        :param verbose_name: Verbose name
        :param help_text: Help text
        """

        super().__init__(prefix, default, verbose_name)
        self.compiler = compiler or markdownify
        if verbose_name:
            self['markdown'].verbose_name = verbose_name
        if help_text:
            self['markdown'].help_text = help_text

    def get(self, model):
        proxy = self.get_proxy(model)
        markdown, cached = proxy.markdown, proxy.cached
        if not get_setting("MARKDOWN_CACHE", True):
            return self.render(markdown)

        if cached:
            return cached

        if not get_setting("MARKDOWN_CACHE_RUNTIME", True):
            raise ValueError("Attempted to access markdown field which wasn't cached, cache it manually or set "
                             "MARKDOWN_CACHE_RUNTIME to true ")
        value = self.render(markdown)
        proxy.cached = self.render(value)
        # pylint: disable=protected-access
        proxy._model.save()
        return value

    def set(self, model, value):
        proxy = self.get_proxy(model)
        if get_setting("CACHE_MARKDOWN", True):
            proxy.cached = self.render(value)
        proxy.markdown = value

    def render(self, value: str) -> str:
        """Compiles text value to Markdown"""
        return self.compiler(value)
