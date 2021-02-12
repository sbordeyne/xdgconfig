import argparse
from functools import partial

from xdgconfig import Config
from xdgconfig.cli_tools.common import HELP_TEXT


def config(
    subparsers: argparse.Action, config: Config,
    infer_type: bool = True,
) -> argparse.Action:
    '''
    Configuration function that returns a pregenerated argparse subparser
    to add to your CLIs using `xdgconfig`. The subparser has a callback
    attached to it, which you can call with the arguments from itself.
    Example :
        args = vars(parser.parse_args())
        callback = args.pop('callback', lambda *a, **kw: None)
        callback(**args)

    :param subparsers: The return value of argparse.add_subparsers
    :type subparsers: argparse._SubParsersAction
    :param config: The configuration object from xdgconfig.
    :type config: xdgconfig.Config
    :param infer_type: Whether to infer types from the value apparent
                       type, defaults to True
    :type infer_type: bool, optional
    :return: The modified argparse._SubParsersAction
    :rtype: argparse._SubParsersAction
    '''

    config_p = subparsers.add_parser(
        'config', help=HELP_TEXT,
    )

    config_p.add_argument(
        'config_key', type=str, help='Config key to edit'
    )
    config_p.add_argument(
        'config_value', type=str, help='Value to assign to the config key.'
    )
    config_p.add_argument(
        '--global', action='store_true', dest='_global',
        help='Whether to assign to value to the global configuration'
    )
    config_p.set_defaults(
        callback=partial(
            config._cli_callback, infer_type=infer_type,  # noqa
        ),
    )
    return subparsers
