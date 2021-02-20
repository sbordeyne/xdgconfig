# XDGConfig

[![Discord](https://img.shields.io/discord/812645240611536906?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2)](https://discord.gg/kDgyr9Uzwj)
[![GitHub license](https://img.shields.io/github/license/Dogeek/xdgconfig.svg)](https://github.com/Dogeek/xdgconfig/blob/master/LICENSE)
[![PyPI version shields.io](https://img.shields.io/pypi/v/xdgconfig.svg)](https://pypi.python.org/pypi/xdgconfig/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/xdgconfig.svg)](https://pypi.python.org/pypi/xdgconfig/)

Easy access to `~/.config`.


## Installation

### Using pip

Simply run `pip3 install --upgrade xdgconfig`.

By default, `xdgconfig` only supports JSON as its serializer, but you can install support for
other serializers by specifiying the format in square brackets, i.e. `pip3 install xdgconfig[xml]`.
The following are available:

- `jsonc`: JSON, with comments
- `ini`: INI files
- `xml`: eXtensible Markup Language files
- `toml`: Tom's Markup language files
- `yaml`: YAML Ain't Markup Language files

Furthermore there is an `all` recipe to install support for every markup supported,
and you can combine them by using a `+` between 2 targets, i.e. `pip3 install xdgconfig[xml+toml]`

### From source

Simply clone this repo and run `python3 setup.py install`.

## Features

- `Config` objects use a shared single reference.
- Serializing to many common formats, including JSON, XML, TOML, YAML, and INI
- `dict`-like interface
- Autosaving on mutation of the `Config` object.
- Smart config loading, especially on Unix-based platforms
  - looks in `/etc/prog/config`, then in `~/.config/prog/config`
  - Supports setting a config file path in an environment variable named `PROG_CONFIG_PATH`
- Accessing the config using dot notation (`config.key` for instance). See limitations for guidance.


## Usage

```python
from xdgconfig import JsonConfig

# Instanciate the JsonConfig object
# If you'd rather use a different format, there also are config classes
# for TOML, YAML, INI (configparser), and XML.
# This will save your configuration under `~/.config/PROG/config
config = JsonConfig('PROG', autosave=True)

config['foo'] = 'bar'  # Save a value to the config

# Access the value later on
print(config['foo'])

# It behaves like a collections.defaultdict as well
config['oof']['bar'] = 'baz'

# Prints {'oof': {'bar': 'baz'}, 'foo': 'bar'}
print(config)

```

## Adding onto the library

### Custom serializers

You can add custom serializers support by using a Mixin class, as well as
a serializer class which must have a `dumps` and a `loads` method, which will
be used to store and load data from the config file. The data is always
represented as a python `dict` object, but you can serialize any data you want
inside of it.

Look at the following example for an implementation guide.

```python
from typing import Any, Dict

from xdgconfig import Config


class MySerializer:
    def dumps(data: Dict[str, Any]) -> str:
        return '\n'.join(f'{k}:{v}' for k, v in data.items())

    def loads(contents: str) -> Dict[str, Any]:
        return dict(s.split(':') for s in contents.split('\n'))


class MySerializerMixin:
    _SERIALIZER = MySerializer


class MyConfig(MySerializerMixin, Config):
    ...

```

### Setting default values

You can set default values by creating a `Mixin` class with a `_DEFAULTS` class attribute, such as :

```python
from pathlib import Path
from pprint import pprint

from xdgconfig import JsonConfig


class DefaultConfig:
    _DEFAULTS = {
        'logger.level': 'info',
        'logger.verbosity': 3,
        'app.path': str(Path.cwd()),
        'app.credentials.username': 'user',
        'app.credentials.password': 'password',
    }


class Config(DefaultConfig, JsonConfig):
    ...


config = Config('PROG', 'config.json')
pprint(config)
# Prints the following dict :
# {
#     'logger': {
#         'level': 'info',
#         'verbosity': 3
#     },
#     'app': {
#         'path': '$CWD',
#         'credentials': {
#             'username': 'user',
#             'password': 'password'
#         }
#     }
# }

```


## Known limitations

- Using an `IniConfig` object prevents you from using periods (`.`) in key names, as they are separators for subdicts.
- Methods and attributes of the `Config` object all start with a leading underscore (`_`), hence, using key names with the same convention is discouraged, as it could break the object due to the way dot (`.`) accessing works. The only exception is the `save` method, which doesn't start with a leading underscore.
- There can only be one document per config file, and a config file is a dictionary.
- Depending on the serializer used, some data types may or may not be available. You can circumvent that by using custom serializers.
- Configuration files with comments will have their comments dropped when the configuration is saved.
