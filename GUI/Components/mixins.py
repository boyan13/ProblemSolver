# +====================================================================================================================+
# Libs
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter
# +====================================================================================================================+


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
        qp.setRenderHint(QPainter.HighQualityAntialiasing, True)
        qp.setPen(QtGui.QColor(self.BORDER_COLOR))
        pen = qp.pen()
        pen.setWidth(self.BORDER_WIDTH)
        qp.setPen(pen)
        qp.setBrush(QtGui.QColor(self.BACKGROUND_COLOR))
        qp.drawRoundedRect(0, 0, self.width(), self.height(), self.BORDER_RADIUS, self.BORDER_RADIUS)
        qp.end()
