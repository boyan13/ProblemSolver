# +====================================================================================================================+
# Pythonic
from types import SimpleNamespace
from typing import Dict, List, Tuple, Union, Any

# Libs
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLineEdit, QGroupBox, QButtonGroup, QVBoxLayout, QListWidget, QListWidgetItem, \
                            QRadioButton, QLabel, QPushButton, QComboBox, QWidget, QLayout, QLayoutItem

# Internal
from GUI.Components.widgets import StyleEnabledMixin
from GUI.Forms.mixins import *
from GUI.Utilities import pyqt_utilities as pyqt_utils
# +====================================================================================================================+


class SizeHintAutomationMixin:

    def __init__(self, *args, **kwargs):
        self.__size_hint_w = None
        self.__size_hint_h = None
        self.__size_hint_w_min = None
        self.__size_hint_h_min = None
        super().__init__(*args, **kwargs)

    def set_size_hints(
            self,
            size: str,  # Small, Medium, Big, Large, Infinite
            standard_hint_width=True,  # Whether to set this size for the sizeHint().width()
            standard_hint_height=False,  # Whether to set this size for the sizeHint().height()
            minimum_hint_width=True,  # Whether to set this size for the minimumSizeHint().width()
            minimum_hint_height=False  # Whether to set this size for the minimumSizeHint().height()
    ):
        if standard_hint_width:
            self.__size_hint_w = self.size_hint_value('width', size, minimum_hint=False)
        if standard_hint_height:
            self.__size_hint_h = self.size_hint_value('height', size, minimum_hint=False)
        if minimum_hint_width:
            self.__size_hint_w_min = self.size_hint_value('width', size, minimum_hint=True)
        if minimum_hint_height:
            self.__size_hint_h_min = self.size_hint_value('height', size, minimum_hint=True)

    def sizeHint(self) -> QtCore.QSize:
        sh = super().sizeHint()
        w = sh.width() if self.__size_hint_w is None else self.__size_hint_w
        h = sh.height() if self.__size_hint_h is None else self.__size_hint_h
        return QSize(w, h)

    def minimumSizeHint(self) -> QtCore.QSize:
        sh = super().minimumSizeHint()
        w = sh.width() if self.__size_hint_w_min is None else self.__size_hint_w_min
        h = sh.height() if self.__size_hint_h_min is None else self.__size_hint_h_min
        return QSize(w, h)

    @staticmethod
    def size_hint_value(dimension: str, size: str, minimum_hint=False):
        if dimension == 'width':

            if size == 'small':
                return 50 if minimum_hint else 120

            elif size == 'medium':
                return 100 if minimum_hint else 240

            elif size == 'big':
                return 150 if minimum_hint else 360

            elif size == 'bigger':
                return 200 if minimum_hint else 480

            elif size == 'large':
                return 250 if minimum_hint else 600

            elif size == 'larger':
                return 300 if minimum_hint else 720

            elif size == 'infinite':
                return 99999

        elif dimension == 'height':

            if size == 'infinite':
                return 99999
            else:
                return int(SizeHintAutomationMixin.size_hint_value('width', size, minimum_hint) // 2.5)


class LineEdit(FormBoxHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QLineEdit):

    def __init__(self, numeric_only=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_hints('small')

        if numeric_only:
            self.setValidator(QtGui.QDoubleValidator())

    def harvest(self):
        return self.text()


class ComboBox(FormBoxHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QComboBox):

    def __init__(self, choices: Dict[str, Any], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.value_for_index = {}

        for choice, value in choices.items():
            self.addItem(choice)
            index = self.findText(choice)
            self.value_for_index[index] = value

    def harvest(self):
        return self.value_for_index[self.currentIndex()]


class RadioButton(FormBoxNonHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QRadioButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_hints('small')


class ColumnRadioGroup(FormBoxHarvestableElementMixin, StyleEnabledMixin, QGroupBox):
    def __init__(self, texts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = QButtonGroup()
        self.vbox = pyqt_utils.null_layout(QVBoxLayout(self))
        for text in texts:
            b = RadioButton(parent=self)
            b.setText(text)
            self.group.addButton(b)
            self.vbox.addWidget(b)

    def harvest(self):
        try:
            text = self.group.checkedButton().text()
        except Exception:
            return None
        else:
            return text


class GridRadioGroup(FormBoxHarvestableElementMixin, StyleEnabledMixin, QGroupBox):
    def __init__(self, texts, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = QButtonGroup()

        self.grid = pyqt_utils.null_layout(QtWidgets.QGridLayout(self))
        self.__i = 0
        self.__j = 0

        for text in texts:
            b = RadioButton(parent=self)
            b.setText(text)
            self.group.addButton(b)

        for button in self.group.buttons():
            self.__add(button)

    def __add(self, button):
        self.grid.addWidget(self.__i, self.__j, button)

        i, j = self.__i, self.__j
        r, c = self.grid.rowCount(), self.grid.columnCount()

        if i == j == r - 1 == c - 1:
            self.__i = 0
            self.__j = c

        elif i < j - 1:
            self.__i += 1

        elif i == j - 1:
            self.__i = j
            self.__j = 0

        elif i > j:
            self.__j += 1

        else:
            raise RuntimeError("It should not be possible to get here.")

    def harvest(self):
        try:
            text = self.group.checkedButton().text()
        except Exception:
            return None
        else:
            return text


class ListWidget(FormBoxHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QListWidget):

    def __init__(self, read_only=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_hints('bigger', standard_hint_height=True, minimum_hint_height=True)
        self._read_only = read_only

    def set_read_only(self, value: bool):
        self._read_only = value

    def harvest(self):
        return [self.item(i) for i in range(self.count())]

    def keyPressEvent(self, event):
        # Delete selected row on user pressing 'Delete'.
        if event.key() == Qt.Key_Delete and not self._read_only:
            for item in self.selectedItems():
                row = self.row(item)
                self.takeItem(row)

        super().keyPressEvent(event)


class ListWidgetItem(QListWidgetItem):
    def __init__(self, text, **kwargs):
        super().__init__(text, type=1000)

        # This is probably not the best approach, but it's quick and easy to work with for now.
        self.data = SimpleNamespace()
        self.data.text = text
        for k, v in kwargs.items():
            setattr(self.data, k, v)

    def __repr__(self):
        return self.data.text


class Label(FormBoxNonHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class LabelMuted(FormBoxNonHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CheckButton(FormBoxNonHarvestableElementMixin, SizeHintAutomationMixin, StyleEnabledMixin, QPushButton):
    def __init__(self, text="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_hints('small')
        self.setText(text)


# class FormListView(QListView):
#     def harvest(self):
#         items = []
#         model = self.model()
#         if model is not None:
#             for row in range(model.rowCount()):
#                 index = model.index(row, 1)
#                 item = model.data(index, Qt.DisplayRole)
#                 items.add(item)
#         return items
