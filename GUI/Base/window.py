# +====================================================================================================================+
# Pythonic
from typing import Union

# Libs
from PyQt5.QtWidgets import QMenuBar, QAction, QStatusBar

# Internal
from GUI.Components.widgets import StyledWidget, StyleEnabledMixin, StyledStackedWidget
# +====================================================================================================================+


class BaseTitleBar(StyledWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("WindowTitleBar")


class BaseStatusBar(StyleEnabledMixin, QStatusBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("WindowStatusBar")


class BaseMenuBar(StyleEnabledMixin, QMenuBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("WindowMenuBar")


class BaseView(StyledStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


class BaseWindow:

    VIEW_CLS = BaseView
    TITLEBAR_CLS = BaseTitleBar
    STATUSBAR_CLS = BaseStatusBar
    MENUBAR_CLS = BaseMenuBar

    def __init__(self, parent=None, also_do_setup=True, *args, **kwargs):

        self.title_bar = None
        self.status_bar = None
        self.menu_bar = None
        self.view = None

        super().__init__(parent)

        if also_do_setup:
            self._setup()

    def set_view(self, how: Union[int, str]):
        self.view.set_view(how)

    def new_action(self, menu, text):
        a = QAction(text, self)
        menu.addAction(a)

    # Title Bar

    def _build_title_bar(self, parent=None, *args, **kwargs):
        self.title_bar = self.TITLEBAR_CLS(parent=parent if parent is not None else self, *args, **kwargs)
        self._configure_title_bar()

    def _configure_title_bar(self):
        pass

    # Menu Bar

    def _build_menu_bar(self, parent=None, *args, **kwargs):
        self.menu_bar = self.MENUBAR_CLS(parent=parent if parent is not None else self, *args, **kwargs)
        self._configure_menu_bar()

    def _configure_menu_bar(self):
        pass

    # StatusBar

    def _build_status_bar(self, parent=None, *args, **kwargs):
        self.status_bar = self.STATUSBAR_CLS(parent=parent if parent is not None else self, *args, **kwargs)
        self._configure_status_bar()

    def _configure_status_bar(self):
        pass

    # View

    def _build_view(self, parent=None, *args, **kwargs):
        self.view = self.VIEW_CLS(parent=parent if parent is not None else self, *args, **kwargs)
        self._configure_view()

    def _configure_view(self):
        pass

    # Setup Procedure

    def _setup(self):
        self._build_title_bar()
        self._build_menu_bar()
        self._build_status_bar()
        self._build_view()

        self._create_layout()

    def _create_layout(self):
        raise NotImplementedError()
