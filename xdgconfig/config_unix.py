import os
import pathlib

from xdgconfig.config import Config


class UnixConfig(Config):
    @property
    def _base_path(self):
        return pathlib.Path(
            os.getenv('XDG_CONFIG_HOME', '~/.config')
        ).expanduser()

    def _load(self):
        default_config_path = (
            pathlib.Path('/etc') / f'{self._app_name}.d' / self._config_name
        )
        data = {}

        if default_config_path.exists():
            with open(default_config_path, 'r') as fp:
                data.update(self._SERIALIZER.loads(fp.read()))
        data.update(super()._load())
        return data
