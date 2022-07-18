# +====================================================================================================================+
# Pythonic
import types
from typing import Union

# Libs
from PyQt5.QtWidgets import QWidget, QMenuBar, QAction, QStatusBar, QPushButton, QScrollArea
from PyQt5.QtCore import pyqtSignal, QObject

# Internal
from GUI.Components.widgets import StyledWidget, StyleEnabledMixin, StyledStackedWidget
# +====================================================================================================================+


class BaseTitleBar(StyledWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("WindowTitleBar")

        self.minimize_btn: QPushButton = None
        self.fullscreen_btn: QPushButton = None
        self.close_btn: QPushButton = None

        self.buttons = [self.minimize_btn, self.fullscreen_btn, self.close_btn]


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
        self.names = {}

    def keys(self):
        return list(self.views.keys())

    def add_view(self, key: str, view) -> int:
        self.views[key] = view
        self.names[view] = key
        return self.addWidget(view)

    def get_view(self, how: Union[int, str] = None):
        if how is None:
            return self.currentWidget()
        elif type(how) is str:
            return self.views[how]
        else:
            return self.widget(how)

    def set_view(self, how: Union[int, str]):
        if type(how) is str:
            self.setCurrentWidget(self.views[how])
        else:
            self.setCurrentIndex(self.indexOf(how))


class BaseWindow:

    VIEW_CLS = BaseView
    TITLEBAR_CLS = BaseTitleBar
    STATUSBAR_CLS = BaseStatusBar
    MENUBAR_CLS = BaseMenuBar

    def __init__(self, parent=None, also_do_setup=True, *args, **kwargs):

        self.title_bar: BaseWindow.TITLEBAR_CLS = None
        self.status_bar: BaseWindow.STATUSBAR_CLS = None
        self.menu_bar: BaseWindow.MENUBAR_CLS = None
        self.view: BaseWindow.VIEW_CLS = None

        # Form flow mapping
        self._view_next_mappings = {}
        self._view_prev_mappings = {}

        # Optionally maps views to methods that are called before they are set (view prep methods).
        self.on_view_arrive = {}
        # Optionally maps views to a methods that handle post-view logic before another view is set (on proceed).
        self.on_view_proceed = {}

        super().__init__(parent)

        if also_do_setup:
            self._setup()

    def set_view(self, how: Union[int, str, QWidget]):
        current_view = self.get_current(return_key=True)
        next_view = self.get_key(how, as_str=True)

        ok = True

        if current_view in self.on_view_proceed:
            ok &= self.on_view_proceed[current_view]()

        if next_view in self.on_view_arrive:
            ok &= self.on_view_arrive[next_view]()

        if ok:
            self.view.set_view(how)

    def new_action(self, menu, text):
        a = QAction(text, self)
        menu.addAction(a)

    def get_key(self, view: Union[str, int, QWidget], as_int=False, as_str=False, as_widget=False):
        int_, str_, wgt_ = None, None, None

        if type(view) is int:
            int_ = view
        elif type(view) is str:
            str_ = view
        elif isinstance(view, QWidget):
            wdg_ = view

        if as_int:
            if int_ is not None:
                pass
            elif str_ is not None:
                int_ = self.view.indexOf(self.view.views[str_])
            elif wgt_ is not None:
                int_ = self.view.indexOf(wgt_)

        if as_str:
            if str_ is not None:
                pass
            elif int_ is not None:
                str_ = self.view.names[self.view.widget(int_)]
            elif wgt_ is not None:
                str_ = self.view.names[wgt_]

        if as_widget:
            if wgt_ is not None:
                pass
            elif int_ is not None:
                wgt_ = self.view.widget(int_)
            elif str_ is not None:
                wgt_ = self.view.views[str_]

        result = []

        if as_int:
            result.append(int_)
        if as_str:
            result.append(str_)
        if as_widget:
            result.append(wgt_)

        if len(result) == 0:
            return None
        if len(result) == 1:
            return result[0]
        else:
            return result

    def set_prep(self, view: str, method: Union[types.FunctionType, types.LambdaType]):
        self.on_view_arrive[view] = lambda: method(self.view.get_view(view))

    def set_post(self, view: str, method: Union[types.FunctionType, types.LambdaType]):
        self.on_view_proceed[view] = lambda: method(self.view.get_view(view))

    def set_next(self, view: str, view_to_follow: str, link_both_ways=True):
        view1 = self.view.get_view(view)

        if isinstance(view1, QScrollArea):
            view1 = view1.widget()

        try:
            if view1.proceed_btn is not None:
                view1.proceed_btn.disconnect()
        except TypeError:
            pass

        view1.proceed_btn.clicked.connect(lambda btn_value: self.set_view(view_to_follow))
        self._view_next_mappings[view] = view_to_follow

        if link_both_ways:
            self.set_prev(view_to_follow, view)

    def set_prev(self, view: str, previous_view: str):
        view1 = self.view.get_view(view)

        if isinstance(view1, QScrollArea):
            view1 = view1.widget()

        try:
            if view1.back_btn is not None:
                view1.back_btn.disconnect()
        except TypeError:
            pass

        view1.back_btn.clicked.connect(lambda btn_value: self.set_view(previous_view))
        self._view_prev_mappings[view] = previous_view

    def get_current(self, return_key=False):
        current_view = self.view.names[self.view.currentWidget()]
        if return_key:
            return current_view
        else:
            return self.view.views[current_view]

    def get_next(self, view: str = None, return_key=False):
        if view is None:
            view = self.view.names[self.view.currentWidget()]

        next_view = self._view_next_mappings[view]

        if return_key:
            return next_view
        else:
            return self.view.views[next_view]

    def get_prev(self, view: str = None, return_key=False):
        if view is None:
            view = self.view.names[self.view.currentWidget()]

        prev_view = self._view_prev_mappings[view]
        if return_key:
            return prev_view
        else:
            return self.view.views[prev_view]

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
