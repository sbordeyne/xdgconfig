from xdgconfig import (
    YamlConfig, JsonConfig, XmlConfig,
    TomlConfig, IniConfig,
)

from tests.utils import MockMixin


class MockedYamlConfig(MockMixin, YamlConfig):
    ...


class MockedXmlConfig(MockMixin, XmlConfig):
    ...


class MockedJsonConfig(MockMixin, JsonConfig):
    ...


class MockedTomlConfig(MockMixin, TomlConfig):
    ...


class MockedIniConfig(MockMixin, IniConfig):
    ...
