# ----------------------------------------------------------------------------------------------------------------------
import enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QLineEdit, QFormLayout, QPushButton, QListView, \
    QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup

from gui.Windows11_Dark.Components.widgets import StyleEnabledWidget
# ----------------------------------------------------------------------------------------------------------------------


class FormFactory:

    class ElementType(enum.Enum):
        Label = 1
        LineEdit = 2
        RadioGroup = 3
        ListView = 4

    class Form(StyleEnabledWidget):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
            self.form_layout = QFormLayout(self)
            self.to_harvest = []

        def harvest(self):
            data = {}
            for attr in self.to_harvest:
                data[attr] = getattr(self, attr).harvest()
            return data

    class FormLabel(QLabel):
        pass

    class FormLineEdit(QLineEdit):
        def harvest(self):
            return self.text()

    class FormRadioButton(QRadioButton):
        pass

    class FormRadioGroup(QButtonGroup):
        def harvest(self):
            return self.checkedButton().text()

    class FormListView(QListView):
        def harvest(self):
            items = []
            model = self.model()
            if model is not None:
                for row in range(model.rowCount()):
                    index = model.index(row, 1)
                    item = model.data(index, Qt.DisplayRole)
                    items.add(item)
            return items

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # Init
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def __init__(self, parent=None, columns=2):

        self.parent = parent
        self.columns = columns
        self.column_forms = []

        self.attributes = []
        self.to_harvest = []

        self.hbox = QHBoxLayout()

        for i in range(self.columns):
            self.column_forms.append(self.Form(parent))
            self.hbox.addWidget(self.column_forms[i])

    def add(self, column: int, element: ElementType, name, label: str = None, harvest=True, **kwargs):
        if 0 > column or column > self.columns:
            raise ValueError("Column must be between 0 and {}".format(self.columns))

        form = self.column_forms[column]
        form_element = self.create_element(element, **kwargs)

        self.attributes.append((name, form_element))
        if isinstance(form_element, FormFactory.FormLabel):
            harvest = False

        if label is not None:
            form.form_layout.addRow(label, form_element)
        else:
            form.form_layout.addRow(form_element)

        if harvest:
            self.to_harvest.append(name)

    def create_element(self, element: ElementType, **kwargs):

        if element == self.ElementType.Label:
            return self._create_label(**kwargs)

        elif element == self.ElementType.LineEdit:
            return self._create_line_edit()

        elif element == self.ElementType.RadioGroup:
            return self._create_radio_group()

        elif element == self.ElementType.ListView:
            return self._create_list_view()

    def _create_label(self, text: str = None):
        element = self.FormLabel(self.parent)
        if text is not None:
            element.setText(text)
        return element

    def _create_line_edit(self):
        element = self.FormLineEdit(self.parent)
        return element

    def _create_radio_group(self, buttons_texts: list):
        element = QButtonGroup(self.parent)
        for text in buttons_texts:
            button = self.FormRadioButton(self.parent)
            button.setText(text)
            element.addButton(button)
        return element

    def _create_list_view(self):
        element = self.FormListView(self.parent)
        return element

    def get_form(self):
        entire_form = StyleEnabledWidget(self.parent)

        for attr, value in self.attributes:
            setattr(entire_form, attr, value)
        setattr(entire_form, 'harvest', lambda self=entire_form, to_harvest=self.to_harvest: {k: getattr(self, k).harvest() for k in to_harvest})

        for form in self.column_forms:
            form.setParent(entire_form)
        entire_form.setLayout(self.hbox)

        return entire_form