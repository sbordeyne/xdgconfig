import contextlib

from pyconfig.serializers import json, ini


__all__ = [
    'JsonMixin', 'IniMixin',
]


class JsonMixin:
    SERIALIZER = json


class IniMixin:
    SERIALIZER = ini


with contextlib.suppress(ImportError):
    from pyconfig.serializers import xml
    __all__.append('XmlMixin')

    class XmlMixin:
        SERIALIZER = xml



with contextlib.suppress(ImportError):
    from pyconfig.serializers import toml
    __all__.append('TomlMixin')

    class TomlMixin:
        SERIALIZER = toml


with contextlib.suppress(ImportError):
    from pyconfig.serializers import yaml
    __all__.append('YamlMixin')

    class YamlMixin:
        SERIALIZER = yaml
