# How to use


## Basic Usage

This library adds several objects that represent configuration for an app.
These objects all have the same programming interface, with a few key differences:

- The serializer used is different for each `Config` object. `JsonConfig` serializes the configuration as JSON, while `TomlConfig` does it in a TOML markup.
- Depending on the platform, the configuration path differs
  - On windows, the configuration is stored in `~/AppData/Roaming/prog/config.ext`, with `prog`, and `config.ext` being set by the initializer of the `Config` object.
  - On UNIX-like systems (`Cygwin`, `MacOS` and `Linux` flavors), the configuration is stored in `~/.config/prog/config.ext`.

There are 6 different serializers available. Limitations may apply to different serializers.
- JSON (JSONC)
- TOML
- INI
- Python files
- YAML
- XML

Some serializers may require third-party libraries to work properly. In that case, you can install them using the `extra` syntax (`pip3 install xdgconfig[xml]` for instance). The `json`, `python` and `ini` serializers are always available.

Each `Config` object accesses its values through a dictionary-like interface, for instance:

```python
from xdgconfig import JsonConfig

# Will save in ~/.config/PROG/config
config = JsonConfig('PROG', autosave=True)
config['foo'] = 'bar'
print(config['foo'])
```

It also automatically adds dictionaries when needed, so the following syntax is valid :

```python
config['bar']['baz'] = 'tar'
print(config)
# Prints {'bar': {'baz': 'tar'}, 'foo': 'bar'}
```

### Note about the python serializer :

The python serializer treats the file as a python module, and imports it using `importlib`.
It's quite powerful as the full python capabilities are available to configure an app, but can
also be dangerous as the import can run malicious code if that code is in the config file if the
app has sufficient permissions. It should be used with caution, and for apps not destined to be
run with root privileges.

The python serializer is also unable to serialize back into python code without significant
data losses, hence, auto saving, and saving the config is disabled when using that serializer.

Like with all serializers, you still get a dict to play with at the end. Variables starting with a
leading underscore (`_`) are deemed to be private, and thus are not loaded (or available in the parsed config).

## Setting default values

You may need some values in the configuration to have defaults. Not to worry, `xdgconfig` has you covered. You simply need to mixin an object with a `_DEFAULTS` class attribute with the `Config` object of your choosing. For instance :

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

config = Config('PROG')
print(config['app']['credentials']['username'])  # Prints 'user'
config['app']['credentials']['username'] = 'foobar'
print(config['app']['credentials']['username'])  # Prints 'foobar'
```

In this example, accessing the value directly will return the default unless it has been set on the config object already.

## Using xdgconfig in CLIs

`xdgconfig` comes with subparsers for most popular CLI libraries such as `click`, `argparse` and `typer`. Below is an example with the `argparse` library. These parsers are of course, optional, but provide a convenient way to add configuration to any CLI.

```python
import argparse

from xdgconfig import JsonConfig
from xdgconfig.cli_tools import argparse_config

config = JsonConfig('PROG', 'config.json', autosave=True)

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
subparsers = argparse_config(subparsers, config)
args = vars(parser.parse_args())
args.pop('callback', lambda *a: None)(**args)
```