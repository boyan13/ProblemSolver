# ----------------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QWidget, QPushButton
# ----------------------------------------------------------------------------------------------------------------------


class StyleEnabledWidget(QWidget):
    def __init__(self, *args, object_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        if object_name is not None:
            self.setObjectName(object_name)


class RoundEdgesMixin:

    # These need to be set or the widget would crash when it tries to paint itself.
    BACKGROUND_COLOR = None
    BORDER_COLOR = None
    BORDER_WIDTH = None
    BORDER_RADIUS = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)
        qp.setPen(QtGui.QColor(self.BORDER_COLOR))
        pen = qp.pen()
        pen.setWidth(self.BORDER_WIDTH)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(self.BACKGROUND_COLOR))
        qp.drawRoundedRect(0, 0, self.width(), self.height(), self.BORDER_RADIUS, self.BORDER_RADIUS)
        qp.end()


class MaterialIconButton(QPushButton):
    ICON_CODE = None
    ICON_SIZE = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText(self.ICON_CODE)
        font: QFont = self.font()
        font.setPixelSize(self.ICON_SIZE)
        self.setFont(font)
