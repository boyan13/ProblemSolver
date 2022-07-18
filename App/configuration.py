# +====================================================================================================================+
# Pythonic
from enum import Enum

# Internal
from GUI.Base.window import BaseWindow
# +====================================================================================================================+


STYLIZED_WINDOW: BaseWindow = None


def set_base_window_class(cls):
    global STYLIZED_WINDOW
    STYLIZED_WINDOW = cls


class AppStyle(Enum):
    Windows11_Dark = 1
