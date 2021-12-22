import importlib

from global_modules import logs
from global_modules.macro_manager import MacroManager

logs.info("load_macro", "Function not implemented")

# TODO
"""
macros
| Test
| | test.py
| | config.json
| | Modules
| | | some modules
"""


def load_macros(macro_manager: MacroManager):
    module = importlib.import_module('macros.test')
    exec("module.startup(manager)", {'manager': macro_manager, 'module': module})
