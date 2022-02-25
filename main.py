from core.actual_window import ActualWindow
from global_modules.macro_manager import load_macros
from core.macro_runner import MacroRunner
from global_modules.macro_manager import MacroManager
from global_modules.temp_manager import purge_temp
from core.tray import Tray

if __name__ == "__main__":
    purge_temp(True)

    macro_manager = MacroManager()
    load_macros(macro_manager)

    tray_thread = Tray(macro_manager)

    actual_window = ActualWindow(tray_thread)
    actual_window.setDaemon(True)

    macro_runner = MacroRunner(macro_manager, actual_window, tray_thread)
    macro_runner.setDaemon(True)

    actual_window.start()
    macro_runner.start()

    tray_thread.run_tray()  # Execute in main thread /!\

# TODO: readme
# TODO: Create macro module script
