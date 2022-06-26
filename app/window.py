# +--------------------------------------------------------------------------------------------------------------------+
from gui.Components.base_window import BaseWindow
from gui.Components.widgets import StyledWidget
from gui.Forms.forms import *

# BASE_WINDOW must be set by the application before attempting to instance a Window()
from app.configuration import STYLIZED_WINDOW
# +--------------------------------------------------------------------------------------------------------------------+


def CombinedForm__Criteria__Alternatives():
    return FormMatrix.combine(MCDMForm_Criteria(), MCDMForm_Alternatives())


class Window(STYLIZED_WINDOW, BaseWindow, StyledWidget):

    def __init__(self, parent=None):
        super().__init__(parent, also_do_setup=False)

        self.dimensions = (900, 700)
        self.setMinimumSize(900, 700)
        self.resize(*self.dimensions)

        self._setup()

    # Menu Bar

    def _configure_menu_bar(self):
        self.file_menu = self.menu_bar.addMenu("&File")
        self.edit_menu = self.menu_bar.addMenu("&Edit")
        self.view_menu = self.menu_bar.addMenu("&View")
        self.help_menu = self.menu_bar.addMenu("&Help")

        self.new_action(self.file_menu, "&New")
        self.new_action(self.file_menu, "&Open")
        self.new_action(self.file_menu, "&Save")
        self.new_action(self.file_menu, "&Exit")
        self.new_action(self.edit_menu, "&Copy")
        self.new_action(self.edit_menu, "&Paste")
        self.new_action(self.edit_menu, "&Cut")
        self.new_action(self.view_menu, "&Reset window size")
        self.new_action(self.help_menu, "&About")
        self.new_action(self.help_menu, "&Shortcuts")

        self.view_menu.actions()[0].triggered.connect(self.menu__view__reset_window_size)

    # View

    def _configure_view(self):
        self.view.add_view(key='criteria_and_alternatives', view=CombinedForm__Criteria__Alternatives())
        self.view.set_view('criteria_and_alternatives')

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    # Callback handlers
    #
    #
    # ------------------------------------------------------------------------------------------------------------------

    def menu__view__reset_window_size(self):
        self.resize(*self.dimensions)
