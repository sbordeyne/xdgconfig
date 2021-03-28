from pathlib import Path


class Asset:
    def __init__(self, path: Path):
        self.path = path
        self._data = None


    @property
    def data(self):
        raise NotImplementedError()
