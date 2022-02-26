import importlib
import inspect
import os
from typing import Union, Callable, List

from global_modules import logs


class MacroManager:
    def __init__(self):
        self._loaded = {}
        self._window_disabled = []

    def load_module(self, module) -> None:
        """
        :param module: The module class
        :return: None
        """

        if not inspect.isclass(module):
            raise TypeError(f"Module {module} isn't a class, please check than you submitted a class in all your module"
                            f"s' startup functions")

        self._loaded.update({
            module.__name__: {
                'class': module(self),
                'callbacks': []
            }
        })

        self._loaded[module.__name__]['class'].after_init()

    def reload_all(self):
        logs.info("CORE", "Reloading all macro")

        for i in self._loaded.copy().keys():
            logs.info("CORE", f"Macro {i} unloaded")
            self._loaded.pop(i)

        self.load_macros()

    def register(
            self,
            macro: Callable,
            keys: str,
            before: Callable = None,
            after: Callable = None,
            loop: bool = False,
            window: Union[None, List[str]] = None
    ) -> None:
        """
        :param macro: The macro's function (cf. the main function)
        :param keys: The key(s) you need to pull to trigger the macro ("." means "and" and "+" means "or"; or have the
        priority over the and, e. "ctrl.a+b" means "ctrl and a or b")
        :param before: The function which will be executed before the loop if it's set to true, else before the macro
        :param after: Same as before but after macro or loop
        :param loop: A bool indicating if the given macro must be run while you don't press another time the keys
        :param window: A list of string which correspond of the window's names where this macro is active. If it's set
        to None, this will work unless another macro is set on the same hook, or you disable macro on a specific window
        :return: None
        """

        for i in [macro, before, after]:
            if not ((not inspect.isfunction(i) and i == macro) or (not inspect.isfunction(i) or i is None)):
                logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: Given macro, before or after "
                                           f"isn't a function object (or none for before and after)")
                return None

        try:
            class_name = macro.__qualname__.split(".")[-2]

        except IndexError:
            logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: cannot find parent class' name")
            return None

        if window is not None and type(window) != list:
            logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: window not valid (must be None or a "
                                       f"list)")
            return None

        self._loaded[class_name]['callbacks'].append({
            'macro': macro,
            'before': before,
            'after': after,
            'keys': keys,
            'loop': loop,
            'window': window
        })

        logs.info("MacroManager", f"Macro on {keys=} {window=} successfully registered")

    def disable_for_window(self, window: str) -> None:
        """
        :param window: The window where you want to disable macros
        :return: None
        """

        self._window_disabled.append(window.lower())

        logs.info("MacroManager", f"Macros on {window=} successfully disabled")

    def get_loaded_for_window(self, window_name: str):
        if window_name is None:
            return {}

        window_name = window_name.lower()

        if len(list(filter(lambda x: x in window_name, self._window_disabled))) != 0:
            return {}

        else:
            ret = {}
            for value in self._loaded.values():
                for callback in value['callbacks']:
                    if callback['window'] is None and callback['keys'].lower() not in ret.keys():
                        ret.update({callback['keys'].lower(): {
                            'macro': callback['macro'],
                            'before': callback['before'],
                            'after': callback['after'],
                            'loop': callback['loop']
                        }})

                    elif window_name in callback['window']:
                        ret.update({callback['keys'].lower(): {
                            'macro': callback['macro'],
                            'before': callback['before'],
                            'after': callback['after'],
                            'loop': callback['loop']
                        }})

            return ret

    def load_macros(self) -> None:
        """
        :param self: Macro manager object inherited from main thread
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
                    mo = importlib.import_module(f'macros.{macro}.main')
                    importlib.reload(mo)
                    exec("mo.startup(ma)", {'ma': self, 'mo': mo})
                    logs.info("MacroLoader", f"Macro {macro} successfully loaded")

                except Exception as err:
                    logs.error("MacroLoader", f"Macro {macro} can't be loaded: {type(err)} {err}")
