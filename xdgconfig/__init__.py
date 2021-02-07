# flake8: noqa
from platform import system

import xdgconfig.mixins as mixins


__version__ = '0.0.4'


if system() == 'Windows':
    from xdgconfig.config_win import WinConfig as Config
elif system() in ('Darwin', 'Linux') or system().startswith('CYGWIN'):
    from xdgconfig.config_unix import UnixConfig as Config
else:
    raise ImportError(
        "xdgconfig is not available on this platform : %s" % system()
    )


class JsonConfig(mixins.JsonMixin, Config):
    ...


class IniConfig(mixins.IniMixin, Config):
    ...


if hasattr(mixins, 'XmlMixin'):
    class XmlConfig(mixins.XmlMixin, Config):
        ...
else:
    print((
        'xmltodict is not installed. '
        'Run pip install xdgconfig[xml] to install it.'
    ))

if hasattr(mixins, 'YamlMixin'):
    class YamlConfig(mixins.YamlMixin, Config):
        ...
else:
    print((
        'PyYAML is not installed. '
        'Run pip install xdgconfig[yaml] to install it.'
    ))

if hasattr(mixins, 'TomlMixin'):
    class TomlConfig(mixins.TomlMixin, Config):
        ...
else:
    print((
        'TOML is not installed. '
        'Run pip install xdgconfig[toml] to install it.'
    ))
