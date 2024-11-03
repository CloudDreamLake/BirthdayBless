import os.path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget

from ._DeskTopEmbedded import Ui_Form


class EmbeddedDesktop(QWidget,  Ui_Form):
    def __init__(self, change_signal: pyqtSignal, embedded_dll, parent=None):
        super(EmbeddedDesktop, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        change_signal.connect(self.change)
        self.embedded_dll = embedded_dll

    def change(self, img_path):
        print(os.path.abspath(img_path))
        pixmap = QPixmap(os.path.abspath(img_path))
        pixmap = pixmap.scaled(self.avatar.width(), self.avatar.height(), Qt.AspectRatioMode.KeepAspectRatio)

        print(pixmap)
        print(self.avatar)
        self.avatar.setPixmap(pixmap)

        self.close()
        self.show()
        self.embedded_dll.Load2Desktop(int(self.winId()))

