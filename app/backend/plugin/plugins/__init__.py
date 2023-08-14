import os
from typing import List

from ..type import Plugin


_PLUGINS: List[Plugin] = []
_plugin_dir = os.path.dirname(__file__)
modules = [os.path.splitext(_file)[0] for _file in os.listdir(_plugin_dir) if not _file.startswith('__')]
for mod in modules:
    exec('from .{} import {}; _PLUGINS.append({}())'.format(mod, mod, mod))


def get_plugin(name: str) -> Plugin:
    return next(filter(lambda p: p.name == name, _PLUGINS), None)


def get_plugins() -> List[Plugin]:
    return _PLUGINS
