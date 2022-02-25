import os
import subprocess
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from global_modules import logs
from global_modules.macro_manager import reload_all


class Tray:
    def __init__(self):
        self.__app = QApplication([])

        self.__app.setQuitOnLastWindowClosed(False)
        self.__parent = QWidget()
        self.__icon = QIcon("core/tray_images/tray_enabled.png")

        self.tray = QSystemTrayIcon(self.__icon, self.__parent)
        self.tray.setToolTip("PyMacro")

        self.enabled = True

        self.__build_menu(enabled=True)

        self.tray.setVisible(True)

        self.callback_disable = None

    def __build_menu(self, enabled: bool = True):
        menu = QMenu(self.__parent)

        item = QAction(self.__parent)
        item.setText("PyMacro - By picasso2005")
        item.setEnabled(False)
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setSeparator(True)
        menu.addAction(item)

        if enabled:
            item = QAction(self.__parent)
            item.setText("Disable")
            item.triggered.connect(lambda: self.__toggle_enabled())

        else:
            item = QAction(self.__parent)
            item.setText("Enable")
            item.triggered.connect(lambda: self.__toggle_enabled())

        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("TODO Reload registered macros")
        item.triggered.connect(lambda: reload_all())
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setSeparator(True)
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Open macros folder")
        item.triggered.connect(lambda: self.__open_folder())
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Open logs")
        item.triggered.connect(lambda: self.__open_logs())
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setSeparator(True)
        menu.addAction(item)

        item = QAction(self.__parent)
        item.setText("Exit")
        item.triggered.connect(lambda: self.__exit())
        menu.addAction(item)

        self.tray.setContextMenu(menu)

    def run_tray(self):
        logs.info("CORE", "Tray started")
        self.__app.exec()

    def __toggle_enabled(self):
        if self.enabled:
            self.enabled = False
            self.tray.setIcon(QIcon("core/tray_images/tray_disabled.png"))
            self.__build_menu(enabled=False)

            logs.info("tray", "Macros disabled")

            if self.callback_disable is not None:
                self.callback_disable()

        else:
            self.enabled = True
            self.tray.setIcon(QIcon("core/tray_images/tray_enabled.png"))
            self.__build_menu(enabled=True)

            logs.info("tray", "Macros enabled")

    @staticmethod
    def __open_logs():
        if sys.platform == "win32":
            subprocess.Popen(f"\"{os.getcwd()}\\{logs.LOG_PATH}\"", shell=True)

        elif sys.platform == "linux" or sys.platform == "linux2":
            subprocess.Popen(f"xdg-open \"{os.getcwd()}/{logs.LOG_PATH}\"", shell=True)

    @staticmethod
    def __open_folder():
        if sys.platform == "win32":
            subprocess.Popen(f"explorer \"{os.getcwd()}\\macros\"", shell=True)

        elif sys.platform == "linux" or sys.platform == "linux2":
            subprocess.Popen(f"xdg-open \"{os.getcwd()}/macros\"", shell=True)

    def __exit(self):
        self.__app.exit(0)

        logs.info("tray", "Exiting app")
        exit(0)
