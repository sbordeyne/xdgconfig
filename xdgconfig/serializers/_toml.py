import toml as toml_


def dumps(*a, **kw):
    kw.pop('indent', None)
    return toml_.dumps(*a, **kw)


loads = toml_.loads
