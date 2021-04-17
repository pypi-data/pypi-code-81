"""Declares :class:`BaseLoader`."""
import abc

import marshmallow
from unimatrix.lib.datastructures import ImmutableDTO


class BaseLoaderMetaclass(abc.ABCMeta):

    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        if name in ['BaseLoader']:
            return super_new(cls, name, bases, attrs)

        # Inspect the attributes for marshmallow.fields.Field instances
        # and create a schema to parse the configuration options.
        fields = {}
        for attname, value in list(dict.items(attrs)):
            if not isinstance(value, marshmallow.fields.Field):
                continue
            fields[attname] = attrs.pop(attname)

        ConfigSchema = type('ConfigSchema', (marshmallow.Schema,), {
            **fields,
            'dict_class': ImmutableDTO
        })
        attrs['schema'] = ConfigSchema()

        return super_new(cls, name, bases, attrs)


class BaseLoader(metaclass=BaseLoaderMetaclass):
    """The base class for all secret loaders. :class:`BaseLoader` specifies
    the interface used to create, read, modify and delete secrets.
    """
    __module__ = 'unimatrix.ext.secrets.loaders'

    #: Specifies the native datatype in which secrets are persisted in the
    #: storage backend. Legal values are ``'plain'`` or ``'composite'``. For
    #: storage backends that use a plain datatype, an additional encoding
    #: (such as UTF-8) may be specified using the :attr:`native_encoding`
    #: attribute (see below). Otherwise, the :class:`BaseLoader` implementation
    #: is expected to implement secret deserialization (e.g. from JSON or YAML).
    native_type = 'plain'

    @property
    def opts(self):
        """Return the configuration options that were provided on instance
        initialization.
        """
        return self.__opts

    def __init__(self, opts):
        self.__opts = self.schema.load(opts)

    async def prefetch(self):
        """Prefetches all secrets from the storage backend."""
        raise NotImplementedError("Subclasses must override this method.")

    def decode(self, pt):
        """Decodes the plaintext that was returned from the secret storage
        backend.
        """
        pass
