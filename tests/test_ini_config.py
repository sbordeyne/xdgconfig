import pathlib

from pyconfig import IniConfig
from tests.utils import TestCase, MockMixin


class MockedIniConfig(MockMixin, IniConfig):
    ...


class TestIniConfig(TestCase):
    CONFIG_NAME = 'config.ini'

    def test_config_saved(self):
        '''
        Tests that the config file is created correctly.
        '''
        config = MockedIniConfig(
            self.__class__.__name__,
            self.CONFIG_NAME,
            autosave=False,
        )
        config['string'] = 'string'
        config['integer'] = 0
        config['float'] = 0.1
        config['dict'] = {}
        config['list'] = []
        self.assertEqual(
            config,
            {
                'string': 'string',
                'integer': 0,
                'float': 0.1,
                'dict': {},
                'list': []
            }
        )
        config.save()
        self.assertFileExists(
            pathlib.Path('./tmp') / self.__class__.__name__ / self.CONFIG_NAME
        )

    def test_config_loaded(self):
        config = MockedIniConfig(
            self.__class__.__name__,
            self.CONFIG_NAME,
            autosave=False,
        )
        config['string'] = 'string'
        config['integer'] = 0
        config['float'] = 0.1
        config['dict'] = {}
        config['list'] = []
        config.save()

        conf = MockedIniConfig(
            self.__class__.__name__,
            self.CONFIG_NAME,
            autosave=False,
        )
        self.assertEqual(
            conf,
            {
                'string': 'string',
                'integer': 0,
                'float': 0.1,
                'dict': {},
                'list': []
            }
        )

    def test_mutating_subkey(self):
        '''
        Test that mutating a non-existing subkey generates the proper
        tree-like structure.
        '''
        config = self.make_config(MockedIniConfig)
        config['foo']['bar'] = 'baz'
        self.assertEqual(
            config, {'foo': {'bar': 'baz'}}
        )
