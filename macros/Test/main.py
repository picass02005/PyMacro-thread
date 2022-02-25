import time

from global_modules.macro_manager import MacroManager


class Test:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here
        self.macro_manager.register(self.macro, "F13", before=self.before, after=self.after, loop=True)
        self.macro_manager.disable_for_window("opera")

    #  NOTA: don't make functions static, or it breaks register

    def macro(self):
        print("macro")
        time.sleep(1)

    def before(self):
        print("before")
        time.sleep(1)

    def after(self):
        print("after")
        time.sleep(1)


# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module(Test)
