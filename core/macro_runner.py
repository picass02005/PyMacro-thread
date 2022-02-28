import time
from threading import Thread
from typing import Union

from pynput.keyboard import Key, KeyCode, Listener

from core.actual_window import ActualWindow
from core.tray import Tray
from global_modules import logs
from global_modules.macro_manager import MacroManager


class MacroRunner(Thread):
    def __init__(self, macro_manager: MacroManager, actual_window: ActualWindow, tray: Tray):
        Thread.__init__(self)

        self.__macro_manager = macro_manager
        self.__actual_window = actual_window
        self.__tray = tray

        self.__actual_window.callback_window_change = self.end_all_loop
        self.__tray.callback_disable = self.end_all_loop

        self.__running = {}

        self.__pressed = []

    def run(self):
        listener = Listener(on_press=self.__key_press_callback, on_release=self.__key_release_callback)
        listener.start()

    def __key_press_callback(self, key: Union[Key, KeyCode]):
        if not self.__is_key_pressed(self.__get_key_name(key)):
            self.__pressed.append(self.__get_key_name(key))

        if not self.__tray.enabled:
            return

        key_universal = None

        if isinstance(key, Key):
            key_universal = key.name

        elif isinstance(key, KeyCode):
            if key.char is None:
                return

            else:
                key_universal = key.char

        actual_loaded = self.__macro_manager.get_loaded_for_window(self.__actual_window.actual_window)

        if key_universal not in str(actual_loaded.keys()):
            return

        for macro_key in actual_loaded.keys():
            if self.__is_dict_key_pressed(macro_key):
                macro = actual_loaded[macro_key]

                time.sleep(0.2)  # To avoid triggering two times a macro

                if macro["loop"]:
                    if macro_key not in self.__running.keys():
                        self.__running.update({macro_key: {'macro': macro, 'thread': self.__macro_run_thread(macro)}})
                        self.__running[macro_key]['thread'].start()

                    else:
                        logs.info("MacroRunner", f"Terminating macro on {macro_key} due to user input")
                        self.__running[macro_key]['thread'].terminate()
                        self.__running[macro_key]['thread'].join()

                        if self.__running[macro_key]['macro']['after']:
                            after = self.__running[macro_key]['macro']['after']
                            logs.info("keyboard_handler", f"After {str(after).split(' ')[2]} started")
                            thread = Thread(target=after, daemon=True)
                            thread.start()

                        self.__running.pop(macro_key)

                else:
                    def wrapper():
                        thread_ = self.__macro_run_thread(macro)
                        thread_.start()
                        thread_.join()

                        if macro['after']:
                            logs.info("keyboard_handler", f"After {str(macro['after']).split(' ')[2]} started")
                            macro['after']()

                    thread = Thread(target=wrapper, daemon=True)
                    thread.start()

    def __key_release_callback(self, key: Union[Key, KeyCode]):
        if self.__is_key_pressed(self.__get_key_name(key)):
            self.__pressed.remove(self.__get_key_name(key))

    def __is_key_pressed(self, key: str) -> bool:
        return key in self.__pressed

    @staticmethod
    def __get_key_name(key: Union[Key, KeyCode]) -> str:
        if isinstance(key, Key):
            return key.name

        elif isinstance(key, KeyCode):
            if key.char is not None:
                return key.char

            else:
                return str(key.vk)

    def __is_dict_key_pressed(self, dict_key: str) -> bool:
        sub_keys = dict_key.split("+")

        for i in sub_keys:
            call = True
            for j in i.split("."):
                if not self.__is_key_pressed(j):
                    call = False

            if call:
                return True

        return False

    class __macro_run_thread(Thread):
        def __init__(self, macro=dict):
            Thread.__init__(self)
            self.setDaemon(True)

            self.macro = macro

            self.is_running = True

        def run(self):
            macro_func = self.macro['macro']
            before = self.macro['before']

            if before:
                logs.info("keyboard_handler", f"Before {str(before).split(' ')[2]} running")
                before()

            logs.info("keyboard_handler", f"Macro {str(macro_func).split(' ')[2]} started")

            if self.macro['loop']:
                while self.is_running:
                    macro_func()

            else:
                macro_func()

        def terminate(self):
            self.is_running = False

    def end_all_loop(self):
        for i in self.__running.copy().keys():
            logs.info("MacroRunner", f"Terminating macro {i} due to window change or disabling")
            self.__running[i]['thread'].terminate()
            self.__running[i]['thread'].join()

            if self.__running[i]['macro']['after']:
                after = self.__running[i]['macro']['after']
                logs.info("keyboard_handler", f"After {str(after).split(' ')[2]} started")
                thread = Thread(target=after, daemon=True)
                thread.start()

            self.__running.pop(i)
