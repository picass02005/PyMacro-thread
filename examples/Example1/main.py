from global_modules.get_config import get_config
from global_modules.macro_manager import MacroManager


class Example1:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here

        self.macro_manager.register(
            macro=self.example_1,                   # This is the main function of my macro
            keys="A.B+C",                           # This is the keystroke, it means "(A and B) or C"
            before=self.before_example_1,           # This function will be called before my maro
            after=self.after_example_1,             # This function will be called after my maro
            loop=False,                             # This macro won't loop
            window=get_config("Example1.windows")   # It will only work in the windows defined in the config
        )
        

    def before_example_1(self):
        print("Before example 1")

    def example_1(self):
        print("You pressed (A and B) or C while being inside of discord")

    def after_example_1(self):
        print("After example 1")


# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module(Example1)
