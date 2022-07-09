# +====================================================================================================================+
# Pythonic
import sys

# Libs
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication

# Internal
from App.configuration import AppStyle
from App import configuration
from GUI.Look.Windows11_Dark.window import StylizedBaseWindow as BaseWindow__Windows11_Dark
# +====================================================================================================================+


if __name__ == '__main__':
    app_style = AppStyle.Windows11_Dark

    if app_style is AppStyle.Windows11_Dark:
        configuration.set_base_window_class(BaseWindow__Windows11_Dark)
    else:
        raise ValueError("Invalid App style.")

    application = QApplication(sys.argv)
    QtCore.QDir('resources')
    QtGui.QFontDatabase.addApplicationFont('resources/MaterialIcons-Regular.ttf')
    from App.window import Window
    window = Window()
    window.show()
    sys.exit(application.exec_())
