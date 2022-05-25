# ----------------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
# ----------------------------------------------------------------------------------------------------------------------


class StyleEnabledWidget(QWidget):
    def __init__(self, parent=None, object_name=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)
        if object_name is not None:
            self.setObjectName(object_name)
