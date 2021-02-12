from argparse import ArgumentParser

from xdgconfig.cli_tools import argparse_config

from tests.utils import TestCase
from tests.mocks import MockedJsonConfig


class TestArgparseConfig(TestCase):
    CONFIG_NAME = 'config.json'

    def test_config_parsing(self):
        config = self.make_config(MockedJsonConfig, 'argparse')

        parser = ArgumentParser()
        sp = parser.add_subparsers()
        sp = argparse_config(sp, config)
        args = vars(parser.parse_args(['config', '--global', 'key', 'value']))
        self.assertEqual(args['_global'], True)
        self.assertEqual(args['config_key'], 'key')
        self.assertEqual(args['config_value'], 'value')

        args.pop('callback')(**args)
        self.assertDictEqual(config, {'key': 'value'})
