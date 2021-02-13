import typer

from xdgconfig import Config
from xdgconfig.cli_tools.common import HELP_TEXT


typer_config = typer.Typer()


@typer_config.callback(invoke_without_command=True)
def config(
    context: typer.Context,
    config_key: str, config_value:str,
    _global: bool = typer.Option(False, '--global'),
):
    config = context.default_map.get('config')
    infer_type = context.default_map.get('infer_type', True)

    if config is None:
        raise typer.Exit(1)

    config._cli_callback(
        config_key, config_value,
        _global=_global, infer_type=infer_type
    )


def make_ctx_settings(config, infer_type=True):
    return {
        'default_map': {
            'config': config,
            'infer_type': infer_type,
        }
    }
