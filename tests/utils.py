import pathlib
import shutil
import unittest


class MockMixin:
    @property
    def base_path(self):
        return pathlib.Path('./tmp').resolve()


class TestCase(unittest.TestCase):
    CONFIG_NAME = 'config'

    def tearDown(self):
        shutil.rmtree(pathlib.Path('./tmp'), ignore_errors=True)

    def assertFileExists(self, filepath: pathlib.Path) -> None:
        if filepath.exists():
            return
        raise AssertionError('File %s does not exist.' % filepath)

    def make_config(self, klass):
        return klass(
            self.__class__.__name__,
            self.CONFIG_NAME,
            autosave=False,
        )
