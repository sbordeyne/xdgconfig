'''
Mixins for xdgconfig.config.Config objects.
'''

import contextlib

from xdgconfig.serializers import ini, json


__all__ = [
    'JsonMixin', 'IniMixin',
]


class JsonMixin:
    '''
    Mixin to use a JSON serializer.
    '''
    _SERIALIZER = json


class IniMixin:
    '''
    Mixin to use an INI serializer.
    '''
    _SERIALIZER = ini


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import xml
    __all__.append('XmlMixin')

    class XmlMixin:
        '''
        Mixin to use an XML serializer.
        '''
        _SERIALIZER = xml


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import toml
    __all__.append('TomlMixin')

    class TomlMixin:
        '''
        Mixin to use a TOML serializer.
        '''
        _SERIALIZER = toml


with contextlib.suppress(ImportError):
    from xdgconfig.serializers import yaml
    __all__.append('YamlMixin')

    class YamlMixin:
        '''
        Mixin to use a YAML serializer.
        '''
        _SERIALIZER = yaml
