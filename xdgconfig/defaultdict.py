from copy import deepcopy
from typing import Any


class defaultdict(dict):
    _DEFAULTS = {}

    def __init__(self, *args, _parent=None, **kwargs):
        self._parent = _parent or kwargs.pop('_parent', None)
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> Any:
        if key not in self and '.' not in key:
            default = self._default
            if isinstance(default, dict):
                default = defaultdict(default, _parent=self)
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
    def _rootpath(self):
        path = [self]
        strpath = []
        while path[-1]._parent is not None:
            path.append(path[-1]._parent)
        path = list(reversed(path))
        for i in range(len(path) - 1):
            dd = path[i]
            for k, v in dd.items():
                if path[i + 1] == v:
                    key = k
                    break
            else:
                raise Exception()
            strpath.append(key)
        return '.'.join(strpath)

    @property
    def _default(self) -> Any:
        return self._DEFAULTS.get(
            self._rootpath, defaultdict(_parent=self)
        )
