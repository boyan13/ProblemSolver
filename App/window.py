
# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QGridLayout, QSizePolicy

# Internal
from GUI.Base.window import BaseWindow
from GUI.Components.widgets import StyledWidget
from GUI.Forms.forms import *
from GUI.Utilities import pyqt_utilities as pyqt_utils

# IMPORTANT
from App.configuration import STYLIZED_WINDOW
# +====================================================================================================================+


def InputForm():

    #
    # Gather UI elements
    #

    # Gather the various form boxes for the complete form.
    box1, box2 = CriteriaFormBoxes().form_groups
    box3, box4 = AlternativesFormBoxes().form_groups

    # Create a proceed button.
    proceed_btn = CheckButton('Proceed')

    # Configure the form boxes.
    boxes = [box1, box2, box3, box4]
    for box in boxes:
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #
    # Create the view
    #

    # Create the view
    view = StyledWidget()

    # Configure the view
    view.setContentsMargins(15, 15, 15, 15)

    # Set ui elements to the view
    view.criteria_boxes = [box1, box2]
    view.alternatives_boxes = [box3, box4]
    view.proceed_btn = proceed_btn

    #
    # Configure the layout for the view
    #

    view.hbox = pyqt_utils.null_layout(QHBoxLayout(view))
    view.hbox.addStretch(1)
    vbox = pyqt_utils.null_layout(QVBoxLayout())
    vbox.setSpacing(15)
    view.hbox.addLayout(vbox)
    view.hbox.addStretch(4)

    grid = pyqt_utils.null_layout(QGridLayout())
    grid.setSpacing(10)
    grid.addWidget(box1, 0, 0)
    grid.addWidget(box2, 0, 1)
    grid.addWidget(box3, 1, 0)
    grid.addWidget(box4, 1, 1)
    vbox.addLayout(grid)

    bot_hbox = pyqt_utils.null_layout(QHBoxLayout())
    bot_hbox.addStretch(2)
    bot_hbox.addWidget(proceed_btn)
    bot_hbox.addStretch(1)
    vbox.addLayout(bot_hbox)

    view.setMinimumWidth(962)
    return view


class Window(STYLIZED_WINDOW, BaseWindow, StyledWidget):

    INITIAL_SIZE = (1200, 800)
    MINIMUM_SIZE = (800, 600)

    def __init__(self, parent=None):
        super().__init__(parent, also_do_setup=False)

        self.setMinimumSize(*self.MINIMUM_SIZE)
        self.resize(*self.INITIAL_SIZE)

        self._setup()

    #
    # Setups
    #

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

    def _configure_view(self):
        gather_form_view = InputForm()
        gather_form_view.setObjectName('WindowView')
        self.view.add_view(key='gather_form', view=pyqt_utils.wrap_in_scroll_area(gather_form_view, parent=self))
        self.view.set_view('gather_form')

    #
    # Callback handlers
    #

    def menu__view__reset_window_size(self):
        self.resize(*self.INITIAL_SIZE)
