from typing import List

from PyQt6 import QtCore
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QAbstractItemView, QTableWidget, QHeaderView

from src import PersonManager
from ._MainWindow import Ui_MainWindow
from .DeskTopEmbedded import EmbeddedDesktop


class MainWindow(QMainWindow, Ui_MainWindow):
    change_signal = pyqtSignal(str)

    def __init__(self, data_list: PersonManager, embedded_dll, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.is_embedded = False
        self.embedded_dll = embedded_dll
        self.embedded_ui = EmbeddedDesktop(self.change_signal, embedded_dll)

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(len(data_list.persons))
        i = 0
        for person in data_list.persons:
            item1 = QTableWidgetItem(person.name)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2 = QTableWidgetItem(person.img_path)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableWidget.setItem(i, 0, item1)
            self.tableWidget.setItem(i, 1, item2)
            i += 1

        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableWidget.selectRow(0)
        self.tableWidget.setStyleSheet("selection-background-color: lightblue;")

        self.prev.clicked.connect(self.prev_button_clicked_slot)
        self.nxt.clicked.connect(self.nxt_button_clicked_slot)
        self.flush.clicked.connect(self.flush_button_clicked_slot)
        self.embedded.clicked.connect(self.embedded_button_clicked_slot)

    def prev_button_clicked_slot(self):
        selectRow = self.tableWidget.currentRow()
        print(f'click prev {selectRow}')
        selectRow -= 1
        if selectRow < 0:
            selectRow = self.tableWidget.rowCount() - 1
        self.tableWidget.selectRow(selectRow)

        self.flush_button_clicked_slot()

    def nxt_button_clicked_slot(self):
        selectRow = self.tableWidget.currentRow()
        print(f'click nxt {selectRow}')
        self.tableWidget.selectRow((selectRow + 1) % self.tableWidget.rowCount())

        self.flush_button_clicked_slot()

    def flush_button_clicked_slot(self):
        selectRow = self.tableWidget.currentRow()
        self.change_signal.emit(self.tableWidget.item(selectRow, 1).text())

    def embedded_button_clicked_slot(self):
        _translate = QtCore.QCoreApplication.translate
        if self.is_embedded:
            self.embedded.setText(_translate("MainWindow", "嵌入"))
            self.embedded_ui.close()
        else:
            screen = QGuiApplication.primaryScreen().geometry()  # 获取屏幕类并调用
            self.embedded.setText(_translate("MainWindow", "取消"))
            print(f'screen size {screen.size()}')
            self.embedded_ui.setGeometry(0, 0, screen.width(), screen.height())
            self.embedded_ui.show()
            self.embedded_dll.Load2Desktop(int(self.embedded_ui.winId()))

            self.flush_button_clicked_slot()

        self.is_embedded = not self.is_embedded
