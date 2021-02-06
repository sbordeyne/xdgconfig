import os
import pathlib

from pyconfig.config import Config


class WinConfig(Config):
    @property
    def base_path(self):
        return pathlib.Path(
            os.getenv('XDG_CONFIG_HOME', '~/AppData/Roaming')
        ).expanduser()
