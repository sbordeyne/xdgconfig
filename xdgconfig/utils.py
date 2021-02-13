from copy import deepcopy
import re
from typing import Any, Dict

from xdgconfig.defaultdict import defaultdict


def cast(value: str) -> Any:
    if value in ('yes', 'no', 'true', 'false'):
        return value in ('yes', 'true')
    if value.isdigit():
        return int(value)
    if re.search(r'\d+\.\d+', value):
        return float(value)
    if value[2:].isdigit():
        if value.startswith('0x'):
            return int(value, base=16)
        if value.startswith('0o'):
            return int(value, base=8)
        if value.startswith('0b'):
            return int(value, base=2)
    return value


def path_to_dict(path: str, option: str, value: str) -> Dict[str, Any]:
    parts = path.split('.')

    def pack(parts):
        if parts:
            return {parts[0]: pack(parts[1:])}
        return {option: cast(value)}

    return pack(parts)


def default_to_dict(data: defaultdict) -> dict:
    data_ = deepcopy(dict(data))
    for k, v in data_.items():
        if isinstance(v, defaultdict):
            data_[k] = dict(default_to_dict(v))
    return data_


def dict_to_default(data: dict) -> defaultdict:
    data_ = deepcopy(dict(data))
    for k, v in data_.items():
        if isinstance(v, dict):
            data_[k] = defaultdict(dict_to_default(v))
    return data_
