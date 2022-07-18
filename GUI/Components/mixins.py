# +====================================================================================================================+
# Libs
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLayout
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
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


class ExtendedQBoxAPIMixin:
    def __init__(self, parent=None, spacing=0, contents_margins=None):
        if parent is not None:
            super().__init__(parent)
        else:
            super().__init__()

        self.setSpacing(spacing)

        if contents_margins is None:
            self.setContentsMargins(0, 0, 0, 0)
        else:
            self.setContentsMargins(*contents_margins)

    def add(self, *args):
        for arg in args:

            # CASE (Spacing): Spacing
            if type(arg) is float:
                self.addSpacing(int(arg))

            # CASE (Stretch): Stretch
            elif type(arg) is int:
                self.addStretch(arg)

            # CASE (QWidget): Widget
            elif isinstance(arg, QWidget):
                self.addWidget(arg)

            # CASE (QLayout): Widget
            elif isinstance(arg, QLayout):
                self.addLayout(arg)

            # CASE (QWidget): Widget, Stretch, Alignment
            elif type(arg) is tuple and len(arg) == 3:
                widget, stretch, alignment = arg
                self.addWidget(widget, stretch, alignment=alignment)

            # CASE (QWidget): Widget, Alignment
            elif type(arg) is tuple and len(arg) == 2 and isinstance(arg[0], QWidget):
                widget, alignment = arg
                self.addWidget(widget, alignment=alignment)

            # CASE (QLayout): Layout, Stretch
            elif type(arg) is tuple and isinstance(arg[0], QLayout):
                layout, stretch = arg
                self.addLayout(layout, stretch)
