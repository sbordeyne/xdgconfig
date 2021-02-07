import pathlib
import shutil
import unittest


class MockMixin:
    @property
    def base_path(self):
        return pathlib.Path('./__tmp__').resolve()


class TestCase(unittest.TestCase):
    CONFIG_NAME = 'config'

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(pathlib.Path('./__tmp__'), ignore_errors=True)

    def assertFileExists(self, filepath: pathlib.Path) -> None:
        if filepath.exists():
            return
        raise AssertionError('File %s does not exist.' % filepath)

    def make_config(self, klass, name=''):
        return klass(
            self.__class__.__name__,
            f'{name}_{self.CONFIG_NAME}',
            autosave=False,
        )
