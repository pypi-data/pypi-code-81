"""Helper utilities."""
import typing as t

from fw_utils import AnyFile, BinFile

AnyFile = t.Union[AnyFile, BinFile]


class AttrMixin:
    """Mixin for exposing dictionary keys as attributes.

    The magic methods `__getattr__`, `__setattr__` and `__delattr__` are simply
    wrapping calls to `__getitem__`, `__setitem__` and `__delitem__`.

    Subclasses need to use `object.__setattr__` to set actual attributes
    the first time, ideally in the constructor.  Once an attribute has been
    set using `object.__setattr__` it can be updated and accessed using the
    normal attribute access.
    """

    getattr_proxy = None

    def __getattr__(self, name: str) -> t.Any:
        """Get an attribute - syntax sugar using __getitem__.

        If getattr_proxy is set, attempt getattr through it first.
        """
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            pass
        if self.getattr_proxy:
            try:
                return getattr(self.getattr_proxy, name)
            except AttributeError:
                pass
        try:
            return self.__getitem__(name)
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: t.Any) -> None:
        """Set an attribute - syntax sugar using __setitem__."""
        try:
            object.__getattribute__(self, name)
            object.__setattr__(self, name, value)
        except AttributeError:
            self.__setitem__(name, value)

    def __delattr__(self, name: str) -> None:
        """Delete an attribute - syntax sugar using __delitem__."""
        try:
            self.__delitem__(name)
        except KeyError as exc:
            raise AttributeError(name) from exc


class FieldsMixin:
    """Mixin for data types where parsed data can be represented as dictionary."""

    fields: dict

    @staticmethod
    def canonize_key(key):
        """Default implementation of canonize key which returns the original key."""
        return key

    def __getitem__(self, key: str) -> t.Any:
        """Get field value by name."""
        return self.fields[self.canonize_key(key)]

    def __setitem__(self, key: str, value: t.Any) -> None:
        """Set field value by name."""
        self.fields[self.canonize_key(key)] = value

    def __delitem__(self, key: str) -> None:
        """Delete a field by name."""
        del self.fields[self.canonize_key(key)]

    def __iter__(self):
        """Return an iterator of the field names."""
        return iter(self.fields)

    def __len__(self) -> int:
        """Return the number of parsed fields."""
        return len(self.fields)

    def __dir__(self) -> t.List[str]:
        """Return list of attributes including field names."""
        return list(super().__dir__()) + list(self.fields.keys())
