import inspect
from typing import Union, Callable, List

from global_modules import logs


def reload_all():
    logs.info("CORE", "Function reload_all isn't implemented")


class MacroManager:
    def __init__(self):
        self.loaded = {}

    def load_module(self, module) -> None:
        """
        :param module: The module class
        :return: None
        """

        if not inspect.isclass(module):
            raise TypeError(f"Module {module} isn't a class, please check than you submitted a class in all your module"
                            f"s' startup functions")

        self.loaded.update({
            module.__name__: {
                'class': module(self),
                'callbacks': []
            }
        })

        self.loaded[module.__name__]['class'].after_init()

    def register(
            self,
            function: Callable,
            keys: str,
            before: Callable = None,
            after: Callable = None,
            loop: bool = False,
            window: Union[None, List[str]] = None
    ):
        for i in [function, before, after]:
            if not ((not inspect.isfunction(i) and i == function) or (not inspect.isfunction(i) or i is None)):
                logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: Given function, before or after "
                                           f"isn't a function object (or none for before and after)")
                return None

        try:
            class_name = function.__qualname__.split(".")[-2]

        except IndexError:
            logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: cannot find parent class' name")
            return None

        if window is not None and type(window) != list:
            logs.error("MacroManager", f"Cannot load macro with {keys=} {window=}: window not valid (must be None or a "
                                       f"list)")
            return None

        self.loaded[class_name]['callbacks'].append({
            'function': function,
            'before': before,
            'after': after,
            'keys': keys,
            'loop': loop,
            'window': window
        })

        print(self.loaded)

    def disable_for_window(self):
        pass  # Todo
