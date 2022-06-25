
# ----------------------------------------------------------------------------------------------------------------------
import typing
from typing import Union

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QSizeGrip, QWidget

from gui.Components import base_window
from gui.Components.utilities import nulled_layout
from gui.Components.mixins import RoundEdgesMixin
from gui.Components.widgets import StyledWidget, MaterialIconButton, StyledStackedWidget

from gui.Forms import forms

from gui.Windows11_Dark import constants as const
from gui.Windows11_Dark.stylesheet import Windows11_Dark_stylesheet
from gui.Windows11_Dark.Elements.title_bar_buttons import MinimizeButton, FullscreenButton, CloseButton

# ----------------------------------------------------------------------------------------------------------------------


class View(base_window.BaseView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContentsMargins(10, 10, 10, 10)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


class TitleBar(base_window.BaseTitleBar):
    class MinimizeButton(MaterialIconButton):
        ICON_CODE = '\ue931'
        ICON_SIZE = 18

    class FullscreenButton(MaterialIconButton):
        ICON_CODE = '\ue3c6'
        ICON_SIZE = 15

    class CloseButton(MaterialIconButton):
        ICON_CODE = '\ue5cd'
        ICON_SIZE = 18

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setFixedHeight(self.parent().TITLE_BAR_HEIGHT)

        self.minimize_btn = MinimizeButton(self)
        self.fullscreen_btn = FullscreenButton(self)
        self.close_btn = CloseButton(self)

        self.buttons = [self.minimize_btn, self.fullscreen_btn, self.close_btn]

        self.minimize_btn.clicked.connect(parent.showMinimized)
        self.fullscreen_btn.clicked.connect(
            lambda: parent.showNormal() if parent.isMaximized() else parent.showMaximized()
        )
        self.close_btn.clicked.connect(parent.closeEvent)

        self.vbox = nulled_layout(QVBoxLayout(self))
        self.hbox = nulled_layout(QHBoxLayout())
        self.hbox.addWidget(QtWidgets.QLabel("Problem Solver", parent=self))
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.minimize_btn)
        self.hbox.addSpacing(3)
        self.hbox.addWidget(self.fullscreen_btn)
        self.hbox.addWidget(self.close_btn)
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)

        self.last_cursor_position = None
        # If this value is None, then mouseMoveEvent is invalid, and we do not attempt to move the widget.
        # This is needed because if you start dragging from within a child widget like the Minimize Button,
        # and continue onto the TitleBar itself, then the mousePressEvent would have been triggered for the child,
        # and we would not have a valid last_cursor_position once we actually trigger the TitleBar's moveEvent.
        # This way we only allow moveEvent if we have initially clicked onto the TitleBar, thus setting a valid
        # cursor starting position.

    def mousePressEvent(self, event):
        self.last_cursor_position = event.globalPos()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.last_cursor_position = None

    def mouseMoveEvent(self, event):
        if self.last_cursor_position is None:
            return

        delta = QtCore.QPoint(event.globalPos() - self.last_cursor_position)
        self.parent().move(self.parent().x() + delta.x(), self.parent().y() + delta.y())
        self.last_cursor_position = event.globalPos()
        super().mouseMoveEvent(event)


class StatusBar(base_window.BaseStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.setFixedHeight(self.parent().STATUS_BAR_HEIGHT)
        self.setSizeGripEnabled(True)  # ON by default according to the docs, but I'll still be explicit about it


class StylizedBaseWindow(RoundEdgesMixin, base_window.BaseWindow, StyledWidget):

    TITLEBAR_CLS = TitleBar
    STATUSBAR_CLS = StatusBar
    VIEW_CLS = View

    BORDER_COLOR = const.COLOR__WINDOW_OUTLINE
    BACKGROUND_COLOR = const.COLOR__HARD
    BORDER_WIDTH = 1
    BORDER_RADIUS = const.DIMENSION__WINDOW_BORDER_RADIUS
    TITLE_BAR_HEIGHT = const.DIMENSION__TITLE_BAR_HEIGHT
    STATUS_BAR_HEIGHT = const.DIMENSION__STATUS_BAR_HEIGHT

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Init
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setStyleSheet(Windows11_Dark_stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH)

        self.last_cursor_position = None

    # Title Bar

    def _build_title_bar(self, parent=None, *args, **kwargs):
        super()._build_title_bar(parent=self)

    def _configure_title_bar(self):
        pass

    # Status Bar

    def _build_status_bar(self, parent=None, *args, **kwargs):
        super()._build_status_bar(parent=self, *args, **kwargs)

    def _configure_status_bar(self):
        pass

    # Menu Bar

    def _build_menu_bar(self, parent=None, *args, **kwargs):
        super()._build_menu_bar(parent=self, *args, **kwargs)

    def _configure_menu_bar(self):
        pass

    # View

    def _build_view(self, parent=None, *args, **kwargs):
        super()._build_view(parent=self)

    def _configure_view(self):
        pass

    # Layout

    def _create_layout(self):

        self.title_bar_hbox = QHBoxLayout()
        self.title_bar_hbox.addSpacing(self.BORDER_RADIUS)
        self.title_bar_hbox.addWidget(self.title_bar)

        self.status_bar_hbox = QHBoxLayout()
        self.status_bar_hbox.addSpacing(self.BORDER_RADIUS // 3)
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

