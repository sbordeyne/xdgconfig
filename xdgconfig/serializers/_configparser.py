import configparser
import io
import json

from mergedeep import merge

from xdgconfig.utils import path_to_dict


__all__ = [
    'loads', 'dumps'
]


def _to_string(value):
    if isinstance(value, bool):
        return 'yes' if value else 'no'
    if isinstance(value, bytes):
        return value.decode('utf8')
    if isinstance(value, (list, tuple, set, frozenset, dict)):
        return json.dumps(value)
    if value is None:
        return ''
    return str(value)

def loads(contents, **kw):  # noqa
    config = configparser.ConfigParser()
    config.read_string(contents)

    data = {}
    for section in config.sections():
        for option in config.options(section):
            merge(
                data,
                path_to_dict(
                    section, option,
                    config.get(section, option)
                )
            )
    return data


def dump_recurse(config, data, previous_section=''):
    for section, contents in data.items():
        if previous_section:
            section_name = f'{previous_section}.{section}'
        else:
            section_name = section
        if isinstance(contents, dict):
            config = dump_recurse(config, contents, section_name)
            config[section_name] = {}
            for option, value in contents.items():
                if isinstance(value, dict):
                    continue
                config[section_name][option] = _to_string(value)
    return config


def dumps(data, **kw):  # noqa
    fp = io.StringIO()
    config = configparser.ConfigParser()
    config = dump_recurse(config, data)
    config.write(fp)
    fp.seek(0)
    return fp.read()
