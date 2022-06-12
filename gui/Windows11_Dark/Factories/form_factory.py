# ----------------------------------------------------------------------------------------------------------------------
import enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListView
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout

from gui.Windows11_Dark.Components.widgets import StyleEnabledWidget
# ----------------------------------------------------------------------------------------------------------------------


class FormFactory:

    COLUMNS = 2

    # >
    # >
    # >

    class ElementType(enum.Enum):
        Label = 1
        LineEdit = 2
        Button = 3
        ListView = 4

    class Form(StyleEnabledWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.form_layout = QFormLayout(self)

    # >
    # >
    # >

    def __init__(self, parent=None):

        self.parent = parent
        self.column_forms = []
        self.hbox = QHBoxLayout()

        for i in range(self.COLUMNS):
            self.column_forms.append(self.Form(parent))
            self.hbox.addWidget(self.column_forms[i])

    def add(self, column: int, element: ElementType, label: str = None, text: str = ""):
        if 0 > column or column > self.COLUMNS:
            raise ValueError("Column must be between 0 and {}".format(self.COLUMNS))
        if label is not None:
            self.column_forms[column].form_layout.addRow(label, self.create_element(element, text))
        else:
            self.column_forms[column].form_layout.addRow(self.create_element(element, text))

    def create_element(self, element: ElementType, text: str = ""):
        if element == self.ElementType.Label:
            e = QLabel(self.parent)
            e.setText(text)
            return e
        elif element == self.ElementType.LineEdit:
            e = QLineEdit(self.parent)
            return e
        elif element == self.ElementType.Button:
            e = QPushButton(self.parent)
            e.setText(text)
            return e
        elif element == self.ElementType.ListView:
            e = QListView(self.parent)
            return e

    def get_form(self):
        form = QWidget(self.parent)
        form.setLayout(self.hbox)
        return form