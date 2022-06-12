
# ----------------------------------------------------------------------------------------------------------------------
import typing
from typing import Union

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout, QSizeGrip, QWidget

from gui.utilities import nulled_layout
from gui.Windows11_Dark.stylesheet import Windows11_Dark_stylesheet
from gui.Windows11_Dark.Components.mixins import RoundEdgesMixin
from gui.Windows11_Dark.Components.widgets import StyleEnabledWidget, MaterialIconButton, StyleEnabledStackedWidget
from gui.Windows11_Dark.Elements.forms import MulticriterialAnalysisForm
from gui.Windows11_Dark.Elements.title_bar_buttons import MinimizeButton, FullscreenButton, CloseButton
# ----------------------------------------------------------------------------------------------------------------------


class Window(RoundEdgesMixin, StyleEnabledWidget):

    BORDER_COLOR = '#606060'  # '#454545'
    BACKGROUND_COLOR = '#202020'
    BORDER_WIDTH = 1
    BORDER_RADIUS = 11
    TITLE_BAR_HEIGHT = 32
    STATUS_BAR_HEIGHT = 30

    class TitleBar(StyleEnabledWidget):

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

    class View(StyleEnabledStackedWidget):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setContentsMargins(10, 10, 10, 10)
            self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

            self.views = {}

        def keys(self):
            return list(self.views.keys())

        def add_view(self, key: str, view) -> int:
            self.views[key] = view
            return self.addWidget(view)

        def set_view(self, how):
            if type(how) is str:
                self.setCurrentWidget(self.views[how])
            else:
                self.setCurrentIndex(self.indexOf(how))

        def harvest_view(self):
            pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Init
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, parent=None, dimensions: typing.Tuple[int, int] = (700, 800)):
        super().__init__(parent)

        self.setStyleSheet(Windows11_Dark_stylesheet)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.dimensions = dimensions
        self.resize(*dimensions)

        self.setMinimumSize(300, 150)
        self.setContentsMargins(self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH, self.BORDER_WIDTH)

        self.last_cursor_position = None

        self._setup()

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Setups
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def _setup(self):

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

            self.view_menu.actions()[0].triggered.connect(self.menu__view__reset_window_size)

        def _build_status_bar():
            self.size_grip = QtWidgets.QSizeGrip(self)
            self.status_bar = Window.StatusBar(self, sizegrip=self.size_grip)
            self.size_grip.show()

        def _build_view():
            self.view = Window.View(parent=self)
            self.view.add_view(key='ma_form', view=MulticriterialAnalysisForm(self))
            self.view.set_view('ma_form')
        # >
        # >
        # >

        _build_title_bar()
        _build_menu_bar()
        _build_status_bar()
        _build_view()

        self.title_bar_hbox = QHBoxLayout()
        self.title_bar_hbox.addSpacing(self.BORDER_RADIUS)
        self.title_bar_hbox.addWidget(self.title_bar)

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

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Callback handlers
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def menu__view__reset_window_size(self):
        self.resize(*self.dimensions)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Controls
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def show_view(self, which: Union[str, QWidget]):
        self.view.set_view(which)
