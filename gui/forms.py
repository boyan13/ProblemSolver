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
# ----------------------------------------------------------------------------------------------------------------------


# class MainForm(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAttribute(Qt.WA_StyledBackground)
#
#         vbox = QVBoxLayout(self)
#
#         alternatives_form = AlternativesForm(self)
#         # criteria_form = CriteriaForm(self)
#
#         vbox.addWidget(alternatives_form)
#
#
# class AlternativesForm(QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAttribute(Qt.WA_StyledBackground)
#         form_layout = QFormLayout()
#         self.setLayout(form_layout)
#         self._setup_view()
#
#     def _setup_view(self):
#         form: QFormLayout = self.layout()
#
#         self.heading = QLabel("Alternatives")
#         self.input_field = QLineEdit(self)
#         self.alternatives = QListView(self)
#
#         form.addRow(self.heading)
#         form.addRow("Add:", self.input_field)
#         form.addRow("Alternatives:", self.alternatives)
