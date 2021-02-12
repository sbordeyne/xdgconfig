from copy import deepcopy
import os
import pathlib
from typing import Any

from xdgconfig.utils import cast


class defaultdict(dict):
    def __getitem__(self, key: str) -> Any:
        if key not in self:
            self[key] = defaultdict()
        return super().__getitem__(key)

    def __getattr__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__getattribute__(key)
        if key in self:
            return self[key]
        k = key.replace(' ', '_').replace("'", '')
        if k in self:
            return self[k]
        raise AttributeError(
            f'Attribute `{key}` does not exist on class `{type(self).__name__}`'
        )

    def __setattr__(self, key:str, value:Any) -> None:
        if key in self:
            self[key] = value
        k = key.replace(' ', '_').replace("'", '')
        if k in self:
            self[k] = value
        super().__setattr__(key, value)


def fix(data: defaultdict) -> dict:
    data_ = deepcopy(dict(data))
    for k, v in data_.items():
        if isinstance(v, defaultdict):
            data_[k] = dict(fix(v))
    return data_


def unfix(data: dict) -> defaultdict:
    data_ = deepcopy(dict(data))
    for k, v in data_.items():
        if isinstance(v, dict):
            data_[k] = defaultdict(unfix(v))
    return data_


class ConfigMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        for argname, arg in zip(('app_name', 'config_name'), args):
            kwargs[argname] = arg
        instance_name = kwargs['app_name'] + '.' + kwargs['config_name']
        if instance_name not in cls._instances:
            cls._instances[instance_name] = super(
                ConfigMeta, cls
            ).__call__(**kwargs)
        return cls._instances[instance_name]


class Config(defaultdict, metaclass=ConfigMeta):
    _SERIALIZER = None

    def __init__(
        self, app_name: str, config_name: str = 'config', *,
        autosave: bool = True
    ) -> None:
        '''
        An object representing a configuration for an application

        :param app_name: The name of your app
        :type name: str
        :param config_name: The name of the config file, defaults to 'config'
        :type config_name: str
        :param autosave: Whether to autosave the config on mutation,
                         defaults to True
        :type autosave: bool, optional
        '''
        self._app_name = app_name
        self._config_name = config_name
        self._autosave = autosave

        for key, value in self._load().items():
            super().__setitem__(key, value)

    def __setitem__(self, key: str, value: Any):
        if isinstance(value, dict):
            value = defaultdict(value)
        super().__setitem__(key, value)
        if self._autosave:
            self.save()

    @property
    def _base_path(self) -> pathlib.Path:
        '''
        Abstract method that returns the base path of the config directory

        :return: The path to the configuration directory.
        :rtype: pathlib.Path
        '''
        raise NotImplementedError()

    @property
    def _config_path(self) -> pathlib.Path:
        return self._base_path / self._app_name / self._config_name

    def save(self) -> None:
        '''
        Saves the config to a file.
        '''
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self._config_path, 'w') as fp:
            data = self._SERIALIZER.dumps(fix(self), indent=4)
            fp.write(data)

    def _load(self) -> dict:
        '''
        Loads the config into memory

        :return: A dictionnary representing the loaded configuration.
        :rtype: dict
        '''
        try:
            with open(self._config_path, 'r') as fp:
                data = self._SERIALIZER.loads(fp.read())
        except FileNotFoundError:
            data = defaultdict()

        # PROG_CONFIG_PATH environment variable can be used to point to
        # a configuration file that will take precedence over the user config.
        environ = os.getenv(f'{self._app_name.upper()}_CONFIG_PATH')
        if environ and os.path.exists(environ):
            with open(environ) as fp:
                data.update(self._SERIALIZER.loads(fp.read()))
        return unfix(data)

    def _cli_callback(
        self, config_key: str, config_value: str,
        _global: bool = False, infer_type: bool = True,
    ) -> int:
        if not _global:
            return self._local._cli_callback(config_key, config_value)  # noqa

        if infer_type:
            config_value = cast(config_value)
        self[config_key] = config_value
        return 0


class LocalConfig(Config):
    def __init__(
        self, config_name: str = 'config', *,
        autosave: bool = True
    ) -> None:
        super().__init__(
            self._base_path.name,
            config_name, autosave=autosave
        )

    @property
    def _base_path(self):
        return pathlib.Path.cwd().resolve()
