try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree


def loads(contents, **kw):  # noqa
    ...


def dumps(data, **kw):  # noqa
    ...
