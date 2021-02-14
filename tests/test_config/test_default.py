import unittest

from tests.utils import TestCase
from tests.mocks import MockedJsonConfig


class DefaultConfig:
    _DEFAULTS = {
        'logger.level': 'info',
        'logger.verbosity': 3,
        'app.path': '/path/to/app',
        'app.credentials.username': 'user',
        'app.credentials.password': 'password',
    }


class MockedConfig(DefaultConfig, MockedJsonConfig):
    ...


class TestDefaultConfig(TestCase):
    CONFIG_NAME = 'config.json'

    def test_default_values(self):
        config = self.make_config(MockedConfig, name='defaults.json')
        self.assertEqual(config['logger']['level'], 'info')
        self.assertEqual(config['logger']['verbosity'], 3)
        self.assertEqual(config['app']['path'], '/path/to/app')
        self.assertEqual(config['app']['credentials']['username'], 'user')
        self.assertEqual(config['app']['credentials']['password'], 'password')


if __name__ == '__main__':
    unittest.main()
