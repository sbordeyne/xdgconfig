
from pyconfig.serializers import json, ini, xml


__all__ = [
    'JsonMixin', 'IniMixin',
    'XmlMixin',
]


class JsonMixin:
    SERIALIZER = json


class IniMixin:
    SERIALIZER = ini


class XmlMixin:
    SERIALIZER = xml


try:
    from pyconfig.serializers import toml
    __all__.append('TomlMixin')

    class TomlMixin:
        SERIALIZER = toml

except ImportError:
    pass


try:
    from pyconfig.serializers import yaml
    __all__.append('YamlMixin')

    class YamlMixin:
        SERIALIZER = yaml

except ImportError:
    pass
