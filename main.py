#
# # coding: utf-8
# import sys
# from PyQt5.Qt import Qt
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QCursor
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#
#         # Window size
#         self.WIDTH = 300
#         self.HEIGHT = 300
#         self.resize(self.WIDTH, self.HEIGHT)
#
#         # Widget
#         self.centralwidget = QWidget(self)
#         self.centralwidget.resize(self.WIDTH, self.HEIGHT)
#
#         # Menu
#         self.setContextMenuPolicy(Qt.CustomContextMenu)
#         self.customContextMenuRequested.connect(self.right_menu)
#
#         # Initial
#         self.setWindowFlag(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.setWindowOpacity(0.6)
#
#         radius = 150
#         self.centralwidget.setStyleSheet(
#             """
#             background:rgb(255, 255, 255);
#             border-top-left-radius: 0 px;
#             border-bottom-left-radius:{0}px;
#             border-top-right-radius: 0 px;
#             border-bottom-right-radius:{0}px;
#             """.format(radius)
#         )
#
#     def right_menu(self, pos):
#         menu = QMenu()
#
#         # Add menu options
#         exit_option = menu.addAction('Exit')
#
#         # Menu option events
#         exit_option.triggered.connect(lambda: exit())
#
#         # Position
#         menu.exec_(self.mapToGlobal(pos))
#
#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.moveFlag = True
#             self.movePosition = event.globalPos() - self.pos()
#             self.setCursor(QCursor(Qt.OpenHandCursor))
#             event.accept()
#
#     def mouseMoveEvent(self, event):
#         if Qt.LeftButton and self.moveFlag:
#             self.move(event.globalPos() - self.movePosition)
#             event.accept()
#
#     def mouseReleaseEvent(self, QMouseEvent):
#         self.moveFlag = False
#         self.setCursor(Qt.CrossCursor)
#
#
# if __name__ == '__main__':
#     app = QApplication([])
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())


# ----------------------------------------------------------------------------------------------------------------------
import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication

import gui
from gui.style import AppStyle
from gui import Windows11_Dark

from app import configuration
from gui.Windows11_Dark.window import StylizedBaseWindow as BaseWindow__Windows11_Dark
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app_style = AppStyle.Windows11_Dark

    if app_style is AppStyle.Windows11_Dark:
        configuration.set_base_window_class(BaseWindow__Windows11_Dark)
    else:
        raise ValueError("Invalid app style.")

    application = QApplication(sys.argv)
    QtCore.QDir('resources')
    QtGui.QFontDatabase.addApplicationFont('resources/MaterialIcons-Regular.ttf')
    from app.window import Window
    window = Window()
    window.show()
    sys.exit(application.exec_())
