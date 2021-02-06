# flake8: noqa

'''
Serializers for pyconfig. Each serializer is a module exposing a
`loads` and `dumps` function. These functions behave like `json.loads` and
`json.dumps`.

The `dumps` function needs a keyword argument named `indent` which behaves
exactly like the `indent` keyword argument in the `json` module.
'''

import contextlib

from pyconfig.serializers import _json as json
from pyconfig.serializers import _configparser as ini
from pyconfig.serializers import _xml as xml

with contextlib.suppress(ImportError):
    from pyconfig.serializers import _toml as toml

with contextlib.suppress(ImportError):
    from pyconfig.serializers import _yaml as yaml
