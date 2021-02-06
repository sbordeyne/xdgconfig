import os
import pathlib

from pyconfig.config import Config


class UnixConfig(Config):
    @property
    def base_path(self):
        return pathlib.Path(
            os.getenv('XDG_CONFIG_HOME', '~/.config')
        ).expanduser()

    def load(self):
        default_config_path = (
            pathlib.Path('/etc') / self.app_name / self.config_name
        )
        data = {}

        if default_config_path.exists():
            with open(default_config_path, 'r') as fp:
                data.update(self.SERIALIZER.loads(fp.read()))
        data.update(super().load())
        return data
