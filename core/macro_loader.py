import importlib
import os

from global_modules import logs
from global_modules.macro_manager import MacroManager


def load_macros(macro_manager: MacroManager) -> None:
    """
    :param macro_manager: Macro manager object inherited from main thread
    :return: None
    """

    for macro in os.listdir("macros"):
        is_valid = True

        if os.path.isdir(f"macros/{macro}") and macro != "__pycache__":
            for i in ["main.py", "config.json"]:
                if not os.path.isfile(f"macros/{macro}/{i}"):
                    logs.warn("MacroLoader", f"Macro referred at macros/{macro} isn't valid (missing {i})")
                    is_valid = False

        elif os.path.isfile(f"macros/{macro}"):
            logs.warn("MacrosLoader", f"Macro referred at macros/{macro} isn't a valid macro")
            is_valid = False

        else:
            is_valid = False

        if is_valid:
            try:
                logs.info("MacroLoader", f"Loading macro {macro}...")
                exec("mo.startup(ma)", {'ma': macro_manager, 'mo': importlib.import_module(f'macros.{macro}.main')})
                logs.info("MacroLoader", f"Macro {macro} successfully loaded")

            except Exception as err:
                logs.error("MacroLoader", f"Macro {macro} can't be loaded: {type(err)} {err}")
