from global_modules.macro_manager import MacroManager


class Test:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here
        self.macro_manager.register(self.a, "F13")

    def a(self):
        pass


# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module(Test)
