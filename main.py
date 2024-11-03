# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from UI.MainWindow import MainWindow
from src import PersonManager

from ctypes import cdll

embedded_window_dll = cdll.LoadLibrary('./Load2Desktop.dll')

if __name__ == "__main__":
    pm = PersonManager().load_persons_from_directory('assets/avatars')
    app = QApplication(sys.argv)
    my_win = MainWindow(pm, embedded_window_dll)
    my_win.show()
    sys.exit(app.exec())
