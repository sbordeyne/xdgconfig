import configparser
import io
import json


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

    data = {
        section: {
            option: config.get(section, option)
            for option in config.options(section)
        } for section in config.sections()
    }
    return data


def dumps(data, **kw):  # noqa
    fp = io.StringIO()
    config = configparser.ConfigParser()
    for section, contents in data.items():
        config.add_section(section)
        for option, value in contents.items():
            config.set(option, _to_string(value))
    config.write(fp)
    fp.seek(0)
    return fp.read()
