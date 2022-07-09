
# +====================================================================================================================+
# Pythonic
from enum import Enum
# +====================================================================================================================+


STYLIZED_WINDOW = None


def set_base_window_class(cls):
    global STYLIZED_WINDOW
    STYLIZED_WINDOW = cls


class AppStyle(Enum):
    Windows11_Dark = 1
