import re
from typing import Any, Dict, Union


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
