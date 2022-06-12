# +--------------------------------------------------------------------------------------------------------------------+
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

from gui.Windows11_Dark.Factories.form_factory import FormFactory
# +--------------------------------------------------------------------------------------------------------------------+


E = FormFactory.ElementType  # shortcut for the enum


def MulticriterialAnalysisForm(parent=None):
    factory = FormFactory(parent)
    factory.add(0, E.Label, name="criteria_heading", text="Multicriterial Analysis")
    factory.add(0, E.LineEdit, name="criteria_input", label="Criteria: ", harvest=False)
    factory.add(1, E.ListView, name="criteria_list")

    form = factory.get_form()
    return form
