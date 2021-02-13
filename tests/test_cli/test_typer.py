from typer import Typer
from typer.testing import CliRunner

from xdgconfig.cli_tools import typer_config, make_ctx_settings

from tests.utils import TestCase
from tests.mocks import MockedJsonConfig


class TestArgparseConfig(TestCase):
    CONFIG_NAME = 'config.json'

    def test_config_parsing(self):
        config = self.make_config(MockedJsonConfig, 'argparse')
        runner = CliRunner()

        app = Typer()
        app.add_typer(
            typer_config, name='config',
            context_settings=make_ctx_settings(config)
        )
        result = runner.invoke(app, ['config', '--global', 'key', 'value'])
        print(result.stdout)
        self.assertEqual(result.exit_code, 0)
        self.assertDictEqual(config, {'key': 'value'})
