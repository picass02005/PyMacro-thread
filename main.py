from core.load_macros import load_macros
from global_modules.macro_manager import MacroManager
from global_modules.temp_manager import purge_temp
from core.tray import Tray

if __name__ == "__main__":
    purge_temp(True)

    macro_manager = MacroManager()
    load_macros(macro_manager)

    tray_thread = Tray()  # Execute in main thread /!\
    tray_thread.run_tray()
