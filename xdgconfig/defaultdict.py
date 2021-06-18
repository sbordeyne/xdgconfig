from typing import Any


class defaultdict(dict):
    _DEFAULTS = {}

    def __init__(self, *args, **kwargs):
        '''
        A defaultdict which recursively replace dicts inside with itself.
        Supports a `_DEFAULTS` class attribute to specify defaults for each key.

        :param parent: The parent key. Defaults to None
        :type parent: str, optional
        :param defaults: The defaults to assign to the `_DEFAULTS`
                         class attribute. Defaults to dict().
        :type defaults: dict, optional
        '''
        parent = kwargs.pop('_parent', None)
        defaults = kwargs.pop('_defaults', {})
        super().__init__(*args, **kwargs)
        self._parent = parent
        self._DEFAULTS = defaults

    def __setitem__(self, key: str, value: Any):
        if '.' in key:
            k, *rest = key.split('.')
            if k not in self:
                self[k] = defaultdict(
                    self._default(k), _parent=key,
                    _defaults=self._DEFAULTS
                )
            self[k]['.'.join(rest)] = value
            return
        super().__setitem__(key, value)

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
            k, *rest = key.split('.')
            return self[k]['.'.join(rest)]
        return super().__getitem__(key)

    def _default(self, key: str) -> Any:
        '''
        Returns the default value for a given key.

        :param key: The key to get the default value of.
        :type key: str
        :return: The default value associated with the key
        :rtype: Any
        '''
        if self._parent:
            path = f'{self._parent}.{key}'
        else:
            path = key
        return self._DEFAULTS.get(
            path, defaultdict(
                _parent=path, _defaults=self._DEFAULTS,
            )
        )

    def flat(self, parent_key='', sep='.'):
        items = []
        for k, v in self.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, defaultdict):
                items.extend(v.flat(new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
