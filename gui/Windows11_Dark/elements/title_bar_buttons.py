# ----------------------------------------------------------------------------------------------------------------------
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton

from gui.widgets import MaterialIconButton
# ----------------------------------------------------------------------------------------------------------------------


class MinimizeButton(MaterialIconButton):
    ICON_CODE = '\ue931'
    ICON_SIZE = 18


class FullscreenButton(MaterialIconButton):
    ICON_CODE = '\ue3c6'
    ICON_SIZE = 15


class CloseButton(MaterialIconButton):
    ICON_CODE = '\ue5cd'
    ICON_SIZE = 18
