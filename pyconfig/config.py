from collections import defaultdict
import pathlib
from typing import Any


class Config(dict):
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
        super().__setitem__(key, value)
        if self.autosave:
            self.save()

    def __missing__(self, key: str) -> defaultdict:
        print('missing : %s' % key)
        return defaultdict(dict)

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
                return self.SERIALIZER.loads(fp.read())
        except FileNotFoundError:
            return {}
