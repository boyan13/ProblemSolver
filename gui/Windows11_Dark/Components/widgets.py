# ----------------------------------------------------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedWidget
# ----------------------------------------------------------------------------------------------------------------------

class StyleEnabledMixin:
    """Enable styling for widgets. Expects QWidget as base class."""
    def __init__(self, parent, object_name=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        if object_name is not None:
            self.setObjectName(object_name)


class StyledWidget(StyleEnabledMixin, QWidget):
    pass


class StyledStackedWidget(StyleEnabledMixin, QStackedWidget):
    pass


class MaterialIconButton(QPushButton):
    ICON_CODE = None
    ICON_SIZE = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText(self.ICON_CODE)
        font: QFont = self.font()
        font.setPixelSize(self.ICON_SIZE)
        self.setFont(font)
