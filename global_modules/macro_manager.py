import inspect
from typing import Union, Callable, List

from global_modules import logs


def reload_all():
    logs.info("CORE", "Function reload_all isn't implemented")


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
