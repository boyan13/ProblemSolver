# ----------------------------------------------------------------------------------------------------------------------
import typing

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QSizeGrip

from app.stylesheet import Windows11_Dark_stylesheet
from gui.widgets import StyleEnabledWidget
# ----------------------------------------------------------------------------------------------------------------------


class Window(StyleEnabledWidget):

    BORDER_RADIUS = 10
    BORDER_WIDTH = 1
    BORDER_COLOR = '#454545'
    BACKGROUND_COLOR = '#21201f'
    TITLE_BAR_HEIGHT = 34
    STATUS_BAR_HEIGHT = 30

    class TitleBar(StyleEnabledWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.setFixedHeight(self.parent().TITLE_BAR_HEIGHT)

        def mousePressEvent(self, event):
            self.last_cursor_position = event.globalPos()
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            delta = QtCore.QPoint(event.globalPos() - self.last_cursor_position)
            self.parent().move(self.parent().x() + delta.x(), self.parent().y() + delta.y())
            self.last_cursor_position = event.globalPos()
            super().mouseMoveEvent(event)

    class StatusBar(StyleEnabledWidget):
        def __init__(self, parent=None, sizegrip: QSizeGrip = None):
            super().__init__(parent)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.setFixedHeight(self.parent().STATUS_BAR_HEIGHT)

            if sizegrip is not None:
                sizegrip_vbox = QVBoxLayout()
                sizegrip_vbox.addStretch(1)
                sizegrip_vbox.addWidget(sizegrip, 0)

            self.hbox = QHBoxLayout(self)
            self.hbox.setSpacing(0)
            self.hbox.setContentsMargins(0, 0, 0, 0)
            self.hbox.addStretch(1)
            if sizegrip is not None:
                self.hbox.addLayout(sizegrip_vbox)

    class View(StyleEnabledWidget):
        pass

    def __init__(self, parent=None, dimensions: typing.Tuple[int, int] = (600, 400)):
        super().__init__(parent)
        self.setStyleSheet(Windows11_Dark_stylesheet)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        self.dimensions = dimensions
        self.resize(*dimensions)
        self.setMinimumSize(300, 150)
        self.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH)
        self.last_cursor_position = None

        self._setup_view()

    # Setups

    def _setup_view(self):

        def _build_title_bar():
            self.title_bar = Window.TitleBar(self)

        def _build_menu_bar():
            def new_action(menu, text):
                a = QtWidgets.QAction(text, self)
                menu.addAction(a)

            self.menu_bar = QtWidgets.QMenuBar(self)

            self.file_menu = self.menu_bar.addMenu("&File")
            self.edit_menu = self.menu_bar.addMenu("&Edit")
            self.view_menu = self.menu_bar.addMenu("&View")
            self.help_menu = self.menu_bar.addMenu("&Help")

            new_action(self.file_menu, "&New")
            new_action(self.file_menu, "&Open")
            new_action(self.file_menu, "&Save")
            new_action(self.file_menu, "&Exit")

            new_action(self.edit_menu, "&Copy")
            new_action(self.edit_menu, "&Paste")
            new_action(self.edit_menu, "&Cut")

            new_action(self.view_menu, "&Reset window size")

            new_action(self.help_menu, "&About")
            new_action(self.help_menu, "&Shortcuts")

            self.view_menu.actions()[0].triggered.connect(self.view__reset_window_size)

        def _build_view():
            self.view = Window.View(parent=self)
            self.view.setContentsMargins(10, 10, 10, 10)
            self.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        def _build_status_bar():
            self.size_grip = QtWidgets.QSizeGrip(self)
            self.status_bar = Window.StatusBar(self, sizegrip=self.size_grip)
            self.size_grip.show()

        _build_title_bar()
        _build_menu_bar()
        _build_view()
        _build_status_bar()

        self.title_bar_hbox = QHBoxLayout()
        self.title_bar_hbox.addSpacing(self.BORDER_RADIUS)
        self.title_bar_hbox.addWidget(self.title_bar)
        self.title_bar_hbox.addSpacing(self.BORDER_RADIUS)

        self.status_bar_hbox = QHBoxLayout()
        self.status_bar_hbox.addSpacing(self.BORDER_RADIUS)
        self.status_bar_hbox.addWidget(self.status_bar)
        self.status_bar_hbox.addSpacing(self.BORDER_RADIUS // 3)

        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setSpacing(0)
        self.vbox.addLayout(self.title_bar_hbox)
        self.vbox.addWidget(self.menu_bar)
        self.vbox.addWidget(self.view)
        self.vbox.addLayout(self.status_bar_hbox)
        self.vbox.addSpacing(self.BORDER_RADIUS // 3)

    # Paint Event

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        qp.setPen(QtGui.QColor(self.BORDER_COLOR))
        qp.pen().setWidth(self.BORDER_WIDTH)
        qp.setBrush(QtGui.QColor(self.BACKGROUND_COLOR))
        qp.drawRoundedRect(0, 0, self.size().width(), self.size().height(), self.BORDER_RADIUS, self.BORDER_RADIUS)
        qp.end()

    # Callback handlers

    def view__reset_window_size(self):
        self.resize(*self.dimensions)
