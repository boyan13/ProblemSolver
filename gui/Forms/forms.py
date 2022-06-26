# +--------------------------------------------------------------------------------------------------------------------+
import typing
from typing import Union, List, Tuple
from types import SimpleNamespace
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem
from gui.Forms.form_factory import FormFactory
from gui.Forms.form_factory_elements import FormListWidgetItem
from gui.Forms.form_factory_forms import FormMatrix
# +--------------------------------------------------------------------------------------------------------------------+


E = FormFactory.ElementType  # shortcut for the enum


def MCDMForm_Criteria(parent=None):
    factory = FormFactory(parent)

    input_form = factory.init(0, 0, "Criteria", limit_height=False)
    list_form = factory.init(0, 1, "Criteria set")

    factory.add(
        input_form,
        E.LineEdit,
        attr='input_name',
        label='Criteria: ',
        harvest=False
    )
    factory.add(
        input_form,
        E.RadioGroup,
        attr='input_type',
        label='Criteria type:',
        harvest=False,
        options=('Quantitative', 'Qualitative'),
        default=0
    )
    factory.add(
        input_form,
        E.RadioGroup,
        attr='input_goal',
        label='Min / Max:',
        harvest=False,
        options=('Minimize', 'Maximize'),
        default=0
    )
    factory.add(
        input_form,
        E.Button,
        attr='TEST_BTN',
        label=" ",
        text='TEST_BTN'
    )
    factory.add(
        list_form,
        E.ListWidget,
        attr='criteria_list',
        max_height=300
    )

    form = factory.get()

    def add_criteria(form):
        text = form.input_name.harvest()
        if text != "":
            criteria_type = form.input_type.harvest()
            criteria_goal = form.input_goal.harvest()
            if criteria_type is None or criteria_goal is None:
                return
            item = FormListWidgetItem(text, type=criteria_type, goal=criteria_goal)
            item.setText(text + f" ({criteria_type}) ({criteria_goal})")
            form.criteria_list.addItem(item)
        form.input_name.setText("")

    def test_harvest(form):
        print(form.harvest())

    form.input_name.setPlaceholderText('Add criteria')
    form.input_name.returnPressed.connect(lambda f=form: add_criteria(f))
    form.TEST_BTN.pressed.connect(lambda f=form: test_harvest(f))

    return form


def MCDMForm_Alternatives(parent=None) -> FormMatrix:
    factory = FormFactory(parent)

    input_form = factory.init(0, 0, "Alternatives", limit_height=False)
    list_form = factory.init(0, 1, "Alternatives set")

    factory.add(
        input_form,
        E.LineEdit,
        attr='input_name',
        label='Alternative: ',
        harvest=False
    )
    factory.add(
        input_form,
        E.Button,
        attr='TEST_BTN',
        label=" ",
        text='TEST_BTN'
    )

    factory.add(
        list_form,
        E.ListWidget,
        attr='alternatives_list',
        max_height=300
    )

    form = factory.get()

    def add_alternative(form):
        text = form.input_name.harvest()
        if text != "":
            item = FormListWidgetItem(text)
            form.alternatives_list.addItem(item)
        form.input_name.setText("")

    def test_harvest(form):
        print(form.harvest())

    form.input_name.setPlaceholderText('Add alternative')
    form.input_name.returnPressed.connect(lambda f=form: add_alternative(f))
    form.TEST_BTN.pressed.connect(lambda f=form: test_harvest(f))

    return form


def TEST(parent=None) -> FormMatrix:

    factory = FormFactory(parent)
    form1 = factory.init(0, 0, "Critera")
    form2 = factory.init(0, 1, "Alternatives")

    factory.add(
        form1,
        E.LineEdit,
        attr='input_name',
        label='Criteria: ',
        harvest=False
    )
    factory.add(
        form1,
        E.RadioGroup,
        attr='input_type',
        label='Criteria type:',
        harvest=False,
        options=('Quantitative', 'Qualitative'),
        default=0
    )
    factory.add(
        form1,
        E.RadioGroup,
        attr='input_goal',
        label='Min / Max:',
        harvest=False,
        options=('Minimize', 'Maximize'),
        default=0
    )
    factory.add(
        form1,
        E.Button,
        attr='TEST_BTN',
        label=" ",
        text='TEST_BTN'
    )

    factory.add(
        form2,
        E.LineEdit,
        attr='input_name',
        label='Alternative: ',
        harvest=False
    )
    factory.add(
        form2,
        E.Button,
        attr='TEST_BTN',
        label=" ",
        text='TEST_BTN'
    )

    form = factory.get()
    return form
