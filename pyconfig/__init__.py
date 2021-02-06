# flake8: noqa
from platform import system

import pyconfig.mixins as mixins


__version__ = '0.0.1'


if system() == 'Windows':
    from pyconfig.config_win import WinConfig as Config
elif system() in ('Darwin', 'Linux') or system().startswith('CYGWIN'):
    from pyconfig.config_unix import UnixConfig as Config
else:
    raise ImportError(
        "PyConfig is not available on this platform : %s" % system()
    )


class JsonConfig(mixins.JsonMixin, Config):
    ...


class IniConfig(mixins.IniMixin, Config):
    ...


class XmlConfig(mixins.XmlMixin, Config):
    ...


if hasattr(mixins, 'YamlMixin'):
    class YamlConfig(mixins.YamlMixin, Config):
        ...
else:
    print((
        'PyYAML is not installed. '
        'Run pip install pyconfig[yaml] to install it.'
    ))

if hasattr(mixins, 'TomlMixin'):
    class TomlConfig(mixins.TomlMixin, Config):
        ...
else:
    print((
        'TOML is not installed. '
        'Run pip install pyconfig[toml] to install it.'
    ))
