from typing import Any


class defaultdict(dict):
    _DEFAULTS = {}

    def __init__(self, *args, **kwargs):
        parent = kwargs.pop('_parent', None)
        defaults = kwargs.pop('_defaults', {})
        super().__init__(*args, **kwargs)
        self._parent = parent
        self._DEFAULTS = defaults

    def __getitem__(self, key: str) -> Any:
        if key not in self and '.' not in key:
            default = self._default(key)
            if isinstance(default, dict):
                if self._parent is not None:
                    parent = f'{self._parent}.{key}'
                else:
                    parent = key
                default = defaultdict(
                    default, _parent=parent,
                    _defaults=self._DEFAULTS,
                )
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

    def _default(self, key: str) -> Any:
        if self._parent:
            path = f'{self._parent}.{key}'
        else:
            path = key
        return self._DEFAULTS.get(
            path, defaultdict(
                _parent=path, _defaults=self._DEFAULTS,
            )
        )
