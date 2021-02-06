# PyConfig

Easy access to `~/.config`.


## Usage

```python
from pyconfig import JsonConfig

# Instanciate the Config object
# This will save your configuration under `~/.config/PROG/config
config = Config('PROG', autosave=True)

config['foo'] = 'bar'  # Save a value to the config

# Access the value later on
print(config['foo'])

# It behaves like a collections.defaultdict as well
config['foo']['bar'] = 'baz'

# Prints {'foo': {'bar': 'baz'}}
print(config)

```
