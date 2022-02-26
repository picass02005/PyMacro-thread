import string
import os
import time


def check_name(name_) -> bool:
    if name_ is None:
        return False

    for i in name_.lower():
        if not (i in string.ascii_lowercase or i in string.digits):
            return False

        return True


name = None
while not check_name(name):
    name = input("Type the name of your module (be sure to use only digits and ascii letters):\n>>> ")

if not os.path.isdir("macros"):
    os.mkdir("macros")

if os.path.exists(f"macros/{name.capitalize()}"):
    os.chdir(f"macros/{name.capitalize()}")
    print(f"This macro already exists under \"{os.getcwd()}\"")
    exit(1)

os.mkdir(f"macros/{name.capitalize()}")
os.chdir(f"macros/{name.capitalize()}")

os.mkdir("Modules")

with open("config.json", "w") as f:
    f.write("{}")

with open("main.py", "w") as f:
    f.write(
        f"""from global_modules.get_config import get_config
from global_modules.macro_manager import MacroManager


class {name.capitalize()}:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here
        
        pass

        # See end of the readme for detailed doc about registering macros and disabling them for a window those
        # functions

    #  NOTA: don't make functions static (@staticmethod or moving them outside the class except if it's in a module)


# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module({name.capitalize()})
        """
    )

print(f"Macro module under \"{os.getcwd()}\" successfully created")
