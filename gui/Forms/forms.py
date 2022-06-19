# +--------------------------------------------------------------------------------------------------------------------+
from types import SimpleNamespace
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem
from gui.Forms.form_factory import FormFactory, FormListWidgetItem
# +--------------------------------------------------------------------------------------------------------------------+


E = FormFactory.ElementType  # shortcut for the enum


def MCDMForm_Criteria(parent=None):
    factory = FormFactory(parent)
    factory.add(0, E.Label, name='title', text='Criteria')
    factory.add(0, E.LineEdit, name='input_name', label='Criteria: ', harvest=False)
    factory.add(
        0, E.RadioGroup, name='input_type', label='Criteria Type', harvest=False,
        options=('Quantitative', 'Qualitative'), default=0
    )
    factory.add(
        0, E.RadioGroup, name='input_goal', label='Min / Max', harvest=False,
        options=('Minimize', 'Maximize'), default=0
    )
    factory.add(0, E.Button, name='TEST_BTN', text='TEST_BTN')

    factory.add(1, E.Label, name='criteria_list_title', text='Criteria set')
    factory.add(1, E.ListWidget, name='criteria_list', max_height=300)
    factory.add(1, E.FakeLabel, name='fake')

    form = factory.get_form()

    form.input_name.setPlaceholderText('Add criteria')

    def add_criteria(form):
        text = form.input_name.harvest()
        if text != "":
            criteria_type = form.input_type.harvest()
            criteria_goal = form.input_goal.harvest()
            if criteria_type is None or criteria_goal is None:
                return
            item = FormListWidgetItem(text, type=criteria_type, goal=criteria_goal)
            item.setText(text + f" ({criteria_type})")
            form.criteria_list.addItem(item)
        form.input_name.setText("")

    form.input_name.returnPressed.connect(lambda f=form: add_criteria(f))
    form.TEST_BTN.pressed.connect(lambda: print(form.harvest()))

    return form


def MCDMForm_Alternatives(parent=None):
    factory = FormFactory(parent)
    factory.add(0, E.Label, name='title', text='Alternatives')
    factory.add(0, E.LineEdit, name='input_name', label='Alternative: ', harvest=False)
    factory.add(0, E.Button, name='TEST_BTN', text='TEST_BTN')

    factory.add(1, E.Label, name='alternatives_list_title', text='Alternatives set')
    factory.add(1, E.ListWidget, name='alternatives_list', max_height=300)
    factory.add(1, E.FakeLabel, name='fake')

    form = factory.get_form()

    form.input_name.setPlaceholderText('Add alternative')

    def add_alternative(form):
        text = form.input_name.harvest()
        if text != "":
            item = FormListWidgetItem(text)
            form.alternatives_list.addItem(item)
        form.input_name.setText("")

    form.input_name.returnPressed.connect(lambda f=form: add_alternative(f))
    form.TEST_BTN.pressed.connect(lambda: print(form.harvest()))

    return form