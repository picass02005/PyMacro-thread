# PyMacro

---

## Features

---

- Macro handler fully threaded
- Can create macros that loop until you press the hook a 2nd time
- Can create hooks with multiple keys by using `.` (and) and `+` (or)
- Optimized for ram and CPU usage (nota: ensure you have a timeout with loop macros to avoid CPU usage)

## Requirements

---

- Python 3.8 or above
- For linux only: xdotool (can be installed with apt, pacman, dnf, ...)
- Does not actually work on macOS (feel free to make a pull request)

## Installing

---

You need to be in an empty folder with a shell opened with this directory in current working directory

### On linux:

```bash
git clone https://github.com/picass02005/PyMacro-thread.git
# If it doesn't work, download it from github directly by following the link

python3 -m pip install virtualenv # Can be avoided if you already have virtualenv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
mkdir macros
```

### On windows:

```bash
git clone https://github.com/picass02005/PyMacro-thread.git
# If it doesn't work, download it from github directly by following the link

python -m pip install virtualenv # Can be avoided if you already have virtualenv
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt
mkdir macros
```

Next, you need a script to launch it.

### Linux

Use a service to run it at startup.

- Your working directory need to be the PyMacro's folder

- On some environments, the process must run with another user than root (or the tray menu won't appear). If it's your case, specify in your service the user

If you want help, RTFM ([everything you need to know is here](https://wiki.archlinux.org/title/systemd#Writing_unit_files))

### Windows

Create a file named `run_pymacro.bat` and copy and paste the following:

```bash
cd c:\path\to\PyMacro # Change it to the path of the root of your PyMacro install
CALL venv\Scripts\activate.bat
start pythonw run.py
```

**Change the path in the cd** to your PyMacro's folder

Put this script in `%AppData%\Microsoft\Windows\Start Menu\Programs\Startup`

## Code your macro

---

If you run `create_macro_module.py`, it will create a module under `./macros/name` (name is asked by the script)

A module is composed by the following tree:

```
[directory] name
├── [file] main.py
├── [file] config.json
└── [directory] modules
```

You can put everything you need to run `main.py` under `./modules`

If you go in main.py, you'll see there is some imports and the beginning of a class:
```python
from global_modules.get_config import get_config
from global_modules.macro_manager import MacroManager


class Name:
    def __init__(self, macro_manager: MacroManager):  # Do not change args, will be invoked by MacroManager
        self.macro_manager = macro_manager

    def after_init(self):  # Do not change function name or args, will be invoked by MacroManager
        # Put all register or disabler in here
        
        pass

        # See end of the readme for detailed doc about registering macros and disabling them for a window those functions

    #  NOTA: don't make functions static (@staticmethod or moving them outside the class except if it's in a module)

# Do not change the following lines

def startup(macro_manager: MacroManager):
    macro_manager.load_module(Name)
```

Those are the main modules for users.

- get_config
> This adds a function, `get_config()` which allow you to read json configs easily.
> ```python
> temp_dir_folder = get_config("default.temp_dir")  # This will return the temp_dir field in the config.json at the root of the project
> example_config = get_config("test.config")  # This will return the config field in the config.json of the test module
> ```

- MacroManager

> This class add two main functions, `MacroManager.register()` and `MacroManager.disable_for_window()`
> - MacroManager.register()
> > This function is used to register a macro. It has 6 arguments:
> > - macro: function
> > > The macro's function (cf. the main function)
> > - keys: string
> > > The key(s) you need to pull to trigger the macro (`.` means "and" and `+` means "or"; or have the priority over the and, e. `ctrl.a+b` means "ctrl and a or b")
> > - before: function (optional)
> > > The function which will be executed before the loop if it's set to true, else before the macro
> > - after: function (optional)
> > > Same as before but after macro or loop
> > - loop: boolean (optional)
> > > A bool indicating if the given macro must be run while you don't press another time the keys
> > - window: List[string] (optional)
> > > A list of string which correspond of the window's names where this macro is active. If it's set to None, this will work unless another macro is set on the same hook, or you disable macro on a specific window
>
> - MacroManager.disable_for_window()
> > This one is used to disable every macro on a specific window. It has 1 argument:
> > - window: string
> > > The window where you want to disable macros

## Temp files

--- 

You have temp_manager.py in global_modules to create temp files / temp folders.

Usage:
```python
from global_modules import temp_manager

temp_dir_path = temp_manager.create_random_dir(base_name="test", time_= 10)  # This will create a temp dir which name begin with "test" and which will last for 10 minutes after last edit in it
temp_file_path = temp_manager.create_random_file(base_name="test", extension="txt", time_=10)  # This will create a temp txt file which name begin with "test" and which last for 10 minutes after last edit

# If you set time_ to 0, file won't be deleted until you reboot PyMacro
```

## Example macro

---

To create example macros, you can run `create_example_macros.py` (it will create 2 example folders under `./macros`)

## Support me

---

Feel free to support me on my [PayPal](https://paypal.me/picasso2005), it really helps me a lot
