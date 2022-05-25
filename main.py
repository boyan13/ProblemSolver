# ----------------------------------------------------------------------------------------------------------------------
import sys
from PyQt5.QtWidgets import QApplication
from app.window import Windows11_Dark
# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = Windows11_Dark.Window()
    window.show()
    sys.exit(application.exec_())
