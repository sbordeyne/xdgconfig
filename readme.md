# PyConfig

Easy access to `~/.config`.


## Usage

```python
from pyconfig import JsonConfig

# Instanciate the JsonConfig object
# If you'd rather use a different format, there also are config classes
# for TOML, YAML, INI (configparser), and XML.
# This will save your configuration under `~/.config/PROG/config
config = JsonConfig('PROG', autosave=True)

config['foo'] = 'bar'  # Save a value to the config

# Access the value later on
print(config['foo'])

# It behaves like a collections.defaultdict as well
config['foo']['bar'] = 'baz'

# Prints {'foo': {'bar': 'baz'}}
print(config)

```
