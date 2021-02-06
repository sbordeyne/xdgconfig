import pathlib

from pyconfig import TomlConfig
from tests.utils import TestCase, MockMixin


class MockedTomlConfig(MockMixin, TomlConfig):
    ...


class TestTomlConfig(TestCase):
    CONFIG_NAME = 'config.toml'

    def test_config_saved(self):
        '''
        Tests that the config file is created correctly.
        '''
        config = self.make_config(MockedTomlConfig)
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
        config = self.make_config(MockedTomlConfig)
        config['string'] = 'string'
        config['integer'] = 0
        config['float'] = 0.1
        config['dict'] = {}
        config['list'] = []
        config.save()

        conf = self.make_config(MockedTomlConfig)
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
        config = self.make_config(MockedTomlConfig)
        config['foo']['bar'] = 'baz'
        self.assertEqual(
            config, {'foo': {'bar': 'baz'}}
        )
