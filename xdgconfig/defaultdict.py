from copy import deepcopy
from typing import Any


class defaultdict(dict):
    _DEFAULTS = {}

    def __init__(self, *args, __parent=None, **kwargs):
        self.__parent = __parent or kwargs.pop('__parent', None)
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> Any:
        if key not in self and '.' not in key:
            default = self.__default
            if isinstance(default, dict):
                default = defaultdict(default, __parent=self)
            self[key] = default
        if '.' in key:
            return self['.'.join(key.split('.')[1:])]
        return super().__getitem__(key)

    def __getattr__(self, key: str) -> Any:
        if key in dir(self) or key in self.__dict__:
            return self.__getattribute__(key)
        if key in self:
            return self[key]
        k = key.replace(' ', '_').replace("'", '')
        if k in self:
            return self[k]
        raise AttributeError(
            f'Attribute `{key}` does not exist on class `{type(self).__name__}`'
        )

    def __setattr__(self, key:str, value: Any) -> None:
        if key in self:
            self[key] = value
        k = key.replace(' ', '_').replace("'", '')
        if k in self:
            self[k] = value
        super().__setattr__(key, value)

    @property
    def __rootpath(self):
        path = [self]
        while path[-1].__parent is not None:
            path.append(path[-1].__parent)
        return '.'.join(reversed(path))

    @property
    def __default(self) -> Any:
        return self._DEFAULTS.get(
            self.__rootpath, defaultdict(__parent=self)
        )
