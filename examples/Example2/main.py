from global_modules.macro_manager import MacroManager


class Example2:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here

        # Those macros work everywhere
        self.macro_manager.register(macro=self.A, keys="A", loop=False)
        self.macro_manager.register(
            macro=self.B,
            keys="B",
            before=self.before_B,
            after=self.after_B,
            loop=True  # This macro will loop
        )

        self.macro_manager.disable_for_window("discord")  # No macros will works in discord

    def A(self):
        print("A macro")

    def B(self):
        print("B macro")

    def before_B(self):
        print("Before B")

    def after_B(self):
        print("After B")


# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module(Example2)
