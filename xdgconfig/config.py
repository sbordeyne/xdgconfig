import os
import pathlib
from typing import Any

from xdgconfig.utils import cast, default_to_dict, dict_to_default
from xdgconfig.defaultdict import defaultdict


__all__ = ('Config', 'LocalConfig')


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
    '''An object representing a configuration for an application'''

    _SERIALIZER = None

    def __init__(
        self, app_name: str, config_name: str = 'config', *,
        autosave: bool = True
    ) -> None:
        '''
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
        self._parent = None
        self._local = LocalConfig()
        self._local._SERIALIZER = self._SERIALIZER

        for key, value in self._load().items():
            super().__setitem__(key, value)

    def __setitem__(self, key: str, value: Any):
        if isinstance(value, dict):
            value = defaultdict(value, _parent=key, _defaults=self._DEFAULTS)
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
        '''Returns the path to the config file'''
        return self._base_path / self._app_name / self._config_name

    def save(self) -> None:
        '''
        Saves the config to a file.
        '''
        self._config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self._config_path, 'w') as fp:
            data = self._SERIALIZER.dumps(default_to_dict(self), indent=4)
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
            data = dict()

        # PROG_CONFIG_PATH environment variable can be used to point to
        # a configuration file that will take precedence over the user config.
        environ = os.getenv(f'{self._app_name.upper()}_CONFIG_PATH')
        if environ and os.path.exists(environ):
            with open(environ) as fp:
                data.update(self._SERIALIZER.loads(fp.read()))
        return dict_to_default(data)

    def _cli_callback(
        self, config_key: str, config_value: str,
        _global: bool = True, infer_type: bool = True,
    ) -> int:
        '''
        Callback for CLIs to set the proper data in this object

        :param config_key: The key to set on the config object
        :type config_key: str
        :param config_value: The value associated with that key
        :type config_value: str
        :param _global: Whether to use the global config scope, defaults to True
        :type _global: bool, optional
        :param infer_type: Whether to infer the type from the value string, defaults to True
        :type infer_type: bool, optional
        :return: The exit code (0=OK)
        :rtype: int
        '''

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
        '''
        Represents a configuration file in the current working directory.

        :param config_name: the name of the config, defaults to 'config'
        :type config_name: str, optional
        :param autosave: Whether to save the config automatically on mutation, defaults to True
        :type autosave: bool, optional
        '''
        super().__init__(
            '.' + self._base_path.name,
            config_name, autosave=autosave
        )

    @property
    def _base_path(self):
        return pathlib.Path.cwd().resolve()
