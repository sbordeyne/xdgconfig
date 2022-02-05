from importlib.util import module_from_spec, spec_from_loader


def loads(source: str):
    module_name = 'config'
    spec = spec_from_loader(module_name, loader=None)
    module = module_from_spec(spec)
    exec(source, module.__dict__)
    data = {k: v for k, v in vars(module).items() if not k.startswith('_')}
    return data


def dumps(data: dict, **_):
    return
