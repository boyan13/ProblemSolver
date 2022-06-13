# +--------------------------------------------------------------------------------------------------------------------+
import enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QLineEdit, QFormLayout, QPushButton, QListView, QVBoxLayout,\
    QHBoxLayout, QListWidgetItem

from gui.Windows11_Dark.Forms.form_factory import FormFactory
# +--------------------------------------------------------------------------------------------------------------------+


E = FormFactory.ElementType  # shortcut for the enum

# +----------------------------------------+
# | Multicriterial Analysis Forms          |
# +----------------------------------------+

def MA_CriteriaDataForm(parent=None):
    factory = FormFactory(parent)
    factory.add(0, E.Label, name="criteria_heading", text="Multicriterial Analysis")
    factory.add(0, E.LineEdit, name="criteria_input", label="Criteria: ", harvest=False)
    factory.add(1, E.ListWidget, name="criteria_list", max_height=300)
    factory.add(0, E.Button, name="TEST_BTN", text="TEST_BTN")
    factory.add(1, E.FakeLabel, name="fake")

    form = factory.get_form()

    def add_criteria(form):
        form.criteria_list.addItem(form.criteria_input.harvest())
        form.criteria_input.setText("")

    form.criteria_input.returnPressed.connect(lambda f=form: add_criteria(f))
    form.TEST_BTN.pressed.connect(lambda: print(form.harvest()))

    return form
