import os
import pathlib

from xdgconfig.config import Config


class WinConfig(Config):
    @property
    def _base_path(self):
        return pathlib.Path(
            os.getenv('XDG_CONFIG_HOME', '~/AppData/Roaming')
        ).expanduser()
