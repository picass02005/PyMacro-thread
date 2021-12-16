from global_modules.temp_manager import purge_temp
from core.tray import Tray

if __name__ == "__main__":
    purge_temp(True)

    tray_thread = Tray()  # Execute in main thread /!\
    tray_thread.run_tray()
