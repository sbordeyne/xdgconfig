import importlib.util


class Plugin:
    def __init__(self, config, name):
        self.name = name
        base_path = config._config_path.parent
        spec = importlib.util.spec_from_file_location(
            f'plugins.{name}',
            base_path / name / '__init__.py'
        )
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        if hasattr(self.module, 'on_load'):
            func = getattr(self.module, 'on_load')
            if callable(func):
             func(config['plugins'][name])

    def __getattr__(self, attr):
        if attr in ('name', 'module'):
            return super().__getattribute__(attr)
        return getattr(self.module, attr)
