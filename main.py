# ----------------------------------------------------------------------------------------------------------------------
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from gui.Windows11_Dark import window
# ----------------------------------------------------------------------------------------------------------------------


class DemoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 300)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    QtCore.QDir('resources')
    QtGui.QFontDatabase.addApplicationFont('resources/MaterialIcons-Regular.ttf')
    app = window.Window()
    app.show()
    sys.exit(application.exec_())
