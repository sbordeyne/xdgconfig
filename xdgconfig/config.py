import os
import pathlib
from typing import Any


class defaultdict(dict):
    def __getitem__(self, key: str) -> Any:
        if key not in self:
            self[key] = defaultdict()
        return super().__getitem__(key)


class Config(defaultdict):
    SERIALIZER = None

    def __init__(self, app_name: str, config_name: str = 'config', autosave: bool = True) -> None:
        '''
        An object representing a configuration for an application

        :param app_name: The name of your app
        :type name: str
        :param config_name: The name of the config file, defaults to 'config'
        :type config_name: str
        :param autosave: Whether to autosave the config on mutation, defaults to True
        :type autosave: bool, optional
        '''
        self.app_name = app_name
        self.config_name = config_name
        self.autosave = autosave

        for key, value in self.load().items():
            super().__setitem__(key, value)

    def __setitem__(self, key: str, value: Any):
        if isinstance(value, dict):
            value = defaultdict(value)
        super().__setitem__(key, value)
        if self.autosave:
            self.save()

    @property
    def base_path(self) -> pathlib.Path:
        '''
        Abstract method that returns the base path of the config directory

        :return: The path to the configuration directory.
        :rtype: pathlib.Path
        '''
        raise NotImplementedError()

    @property
    def config_path(self) -> pathlib.Path:
        return self.base_path / self.app_name / self.config_name

    def save(self) -> None:
        '''
        Saves the config to a file.
        '''
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as fp:
            data = self.SERIALIZER.dumps(dict(self.items()), indent=4)
            fp.write(data)

    def load(self) -> dict:
        '''
        Loads the config into memory

        :return: A dictionnary representing the loaded configuration.
        :rtype: dict
        '''
        try:
            with open(self.config_path, 'r') as fp:
                data = self.SERIALIZER.loads(fp.read())
        except FileNotFoundError:
            data = defaultdict()

        # PROG_CONFIG_PATH environment variable can be used to point to
        # a configuration file that will take precedence over the user config.
        environ = os.getenv(f'{self.app_name.upper()}_CONFIG_PATH')
        if environ and os.path.exists(environ):
            with open(environ) as fp:
                data.update(self.SERIALIZER.loads(fp.read()))
        return data
