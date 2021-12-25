import importlib
import sys
import time

import psutil
from threading import Thread

from core.tray import Tray
from global_modules import logs
from global_modules.get_config import get_config


class ActualWindow(Thread):
    def __init__(self, tray_thread: Tray):
        Thread.__init__(self)
        self.__init_platform_specific()

        self._tray = tray_thread
        self.actual_window = None

    def __init_platform_specific(self):
        if sys.platform == "win32":
            self._ctypes = __import__("ctypes")
            self._wintypes = importlib.import_module("ctypes.wintypes")

        if sys.platform == "linux" or sys.platform == "linux2":
            self._subprocess = __import__("subprocess")

            proc = self._subprocess.Popen(["/bin/bash", "-c", "which xdotool"], stdout=self._subprocess.PIPE,
                                          stderr=self._subprocess.PIPE)
            stdout_, stderr_ = proc.communicate()

            if stderr_:
                logs.error("get_window", f"Cannot find xdotool. Please install it with apt / pacman / dnf / ... "
                                         f"(bash error: {stderr_.decode()[:-1]})")
                exit(1)

            else:
                self._path = stdout_.decode()[:-1]
                logs.info("get_window", f"xdotool found under {self._path}")

    def run(self):
        while True:
            time.sleep(get_config("global.window_detection_timeout"))
            if self._tray.enabled:
                self.actual_window = self.__get_actual_window()

    def __get_actual_window(self):
        if sys.platform == "win32":
            user32 = self._ctypes.windll.user32

            h_wnd = user32.GetForegroundWindow()
            pid = eval("self._wintypes.DWORD()")
            user32.GetWindowThreadProcessId(h_wnd, self._ctypes.byref(pid))

            return psutil.Process(pid=pid.value).name().replace(".exe", "")

        else:
            process = self._subprocess.Popen([self._path, "getactivewindow", "getwindowpid"],
                                             stdout=self._subprocess.PIPE,
                                             stderr=self._subprocess.PIPE)
            stdout, stderr = process.communicate()

            if stderr:
                logs.error("get_window", f"Active window pid not found: (${self._path} getactivewindow getwindowpid) >&"
                                         f" {stderr.decode()[:-1]}")

                return None

            else:
                pid = int(stdout.decode()[:-1])
                return psutil.Process(pid=pid).exe()
