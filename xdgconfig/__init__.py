# flake8: noqa
from platform import system

import xdgconfig.mixins as mixins


__version__ = '1.0.1'


if system() == 'Windows':
    from xdgconfig.config_win import WinConfig as Config
elif system() in ('Darwin', 'Linux') or system().startswith('CYGWIN'):
    from xdgconfig.config_unix import UnixConfig as Config
else:
    raise ImportError(
        "xdgconfig is not available on this platform : %s" % system()
    )

from xdgconfig.config import LocalConfig


class JsonConfig(mixins.JsonMixin, Config):
    ...


class LocalJsonConfig(mixins.JsonMixin, LocalConfig):
    ...


class IniConfig(mixins.IniMixin, Config):
    ...


class LocalIniConfig(mixins.IniMixin, LocalConfig):
    ...


if hasattr(mixins, 'XmlMixin'):
    class XmlConfig(mixins.XmlMixin, Config):
        ...

    class LocalXmlConfig(mixins.XmlMixin, LocalConfig):
        ...

if hasattr(mixins, 'YamlMixin'):
    class YamlConfig(mixins.YamlMixin, Config):
        ...


    class LocalYamlConfig(mixins.YamlMixin, LocalConfig):
        ...

if hasattr(mixins, 'TomlMixin'):
    class TomlConfig(mixins.TomlMixin, Config):
        ...

    class LocalTomlConfig(mixins.TomlMixin, LocalConfig):
        ...
