import contextlib

from xdgconfig.serializers import ini, json


__all__ = [
    'JsonMixin', 'IniMixin',
]


class JsonMixin:
    _SERIALIZER = json


class IniMixin:
    _SERIALIZER = ini


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import xml
    __all__.append('XmlMixin')

    class XmlMixin:
        _SERIALIZER = xml


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import toml
    __all__.append('TomlMixin')

    class TomlMixin:
        _SERIALIZER = toml


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import yaml
    __all__.append('YamlMixin')

    class YamlMixin:
        _SERIALIZER = yaml
