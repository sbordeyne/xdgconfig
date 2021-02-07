# XDGConfig

Easy access to `~/.config`.


## Features

- `Config` objects use a shared single reference.
- Serializing to many common formats, including JSON, XML, TOML, YAML, and INI
- `dict`-like interface
- Autosaving on mutation of the `Config` object.


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
    SERIALIZER = MySerializer


class MyConfig(MySerializerMixin, Config):
    ...

```
