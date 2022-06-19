# ----------------------------------------------------------------------------------------------------------------------
import enum
import copy
import typing
from functools import cached_property
from types import SimpleNamespace

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy, QLineEdit, QFormLayout, QPushButton, QListWidget, \
    QListWidgetItem, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QGroupBox

from gui.Components.widgets import StyledWidget, StyleEnabledMixin
from gui.Components import utilities
# ----------------------------------------------------------------------------------------------------------------------


class FormColumn(StyledWidget):

    OBJECT_NAME_OF_FIELD_LABELS = 'FormFieldLabel'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.form_layout = QFormLayout(self)
        self.form_layout.setSpacing(15)

        self.to_harvest = []
        self.attributes = []

    def add_row(self, element, attribute_name_of_element: str, label: str = None, harvest=True):
        setattr(self, attribute_name_of_element, element)
        self.attributes.append(attribute_name_of_element)

        if harvest and element.harvestable:
            self.to_harvest.append(attribute_name_of_element)

        if label is not None:
            self.form_layout.addRow(label, element)
            the_label = self.form_layout.labelForField(element)
            the_label.setObjectName(self.OBJECT_NAME_OF_FIELD_LABELS)
        else:
            self.form_layout.addRow(element)
        a = 10

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}


class FormRow(StyledWidget):

    @property
    def to_harvest(self):
        to_harvest = []
        for form in self.columns:
            to_harvest += form.to_harvest
        return to_harvest

    @property
    def attributes(self):
        attributes = []
        for form in self.columns:
            attributes += form.attributes
        return attributes

    def __init__(self, parent=None, form_columns: typing.List[FormColumn] = None):
        super().__init__(parent)
        self.columns = form_columns

        self.hbox = utilities.nulled_layout(QHBoxLayout(self))
        for form in form_columns:
            form.setParent(self)
            form.form_layout.setAlignment(Qt.AlignTop)
            self.hbox.addWidget(form)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}

    def __getattr__(self, item):
        for form in self.columns:
            if item in form.attributes:
                return getattr(form, item)


class MasterForm(StyledWidget):

    @property
    def to_harvest(self):
        to_harvest = []
        for form in self.rows:
            to_harvest += form.to_harvest
        return to_harvest

    @property
    def attributes(self):
        attributes = []
        for form in self.columns:
            attributes += form.attributes
        return attributes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.rows = []

        self.vbox = utilities.nulled_layout(QVBoxLayout(self))
        self.vbox.addStretch(1)
        self.vbox.addStretch(2)

    def __getattr__(self, item):
        for form in self.rows:
            if item in form.attributes:
                return getattr(form, item)

    def add_form_row(self, form_row):
        form_row.setParent(self)
        self.rows.append(form_row)
        self.vbox.removeItem(self.vbox.itemAt(self.vbox.count()))
        self.vbox.addWidget(form_row)
        self.vbox.addStretch(2)

    def harvest(self):
        return {k: getattr(self, k).harvest() for k in self.to_harvest}


class FormElementMixin:

    _HARVESTABLE = True

    @cached_property
    def harvestable(self):
        """Whether this element contains data."""
        return self._HARVESTABLE

    def harvest(self):
        """Get the value (or values) of this element."""
        raise ValueError("This element does not hold harvestable data.")


# +--------------------+
# | Elements           |
# +--------------------+


class FormLineEdit(FormElementMixin, QLineEdit):

    _HARVESTABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

    def harvest(self):
        return self.text()


class FormRadioGroupBox(FormElementMixin, QGroupBox):

    _HARVESTABLE = True

    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.group = QButtonGroup()
        self.vbox = QVBoxLayout(self)

        for option in options:
            btn = FormRadioButton(self)
            btn.setText(option)
            self.group.addButton(btn)
            self.vbox.addWidget(btn)

    def harvest(self):
        try:
            text = self.group.checkedButton().text()
        except Exception:
            return None
        else:
            return text


class FormListWidget(FormElementMixin, QListWidget):

    _HARVESTABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def harvest(self):
        return [self.item(i) for i in range(self.count())]

    def keyPressEvent(self, event):

        # Delete selected row on user pressing 'Delete'.
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                row = self.row(item)
                self.takeItem(row)

        super().keyPressEvent(event)


class FormListWidgetItem(FormElementMixin, QListWidgetItem):
    def __init__(self, text, **kwargs):
        super().__init__(text, type=1000)

        # This is probably not the best approach, but it's quick and easy to work with for now.
        self.data = SimpleNamespace()
        self.data.text = text
        for k, v in kwargs.items():
            setattr(self.data, k, v)

    def __repr__(self):
        return self.data.text


class FormRadioButton(FormElementMixin, QRadioButton):

    _HARVESTABLE = False


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


class FormLabel(FormElementMixin, StyleEnabledMixin, QLabel):

    _HARVESTABLE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)


class FormFakeLabel(FormElementMixin, QLabel):

    _HARVESTABLE = False


class FormButton(FormElementMixin, StyleEnabledMixin, QPushButton):

    _HARVESTABLE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)


# +--------------------+
# | Factory            |
# +--------------------+


class FormFactory:

    """Builds complex forms through a simple API. The number of columns passed to the __init__ is the number of
    subforms that make up the entire form. Each subform takes up a column and all subforms (or just forms) are placed
    in a row next to each other. When populating them you just have to specify the target column (form) and the row.
    The ElementType enum provides an API for the types of elements that can be added to the form. The get_form() will
    return a single widget that combines all forms, and its harvest() method will collect the data of all form elements
    that are harvestable and return a dict with field names (or attribute names) as keys. By default, all form elements
    that contain data are harvestable, but you may specify some that should not be included in the harvest. Since you
    specify all element attribute names, you can directly access form elements using those names and connect signals
    and slots on the returned form to configure additional logic."""

    FIELD_LABEL_OBJ_NAME = "FormFieldLabel"

    class ElementType(enum.Enum):
        Label = 1
        LineEdit = 2
        RadioGroup = 3
        ListWidget = 4
        Button = 5
        FakeLabel = 6

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # Init
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def __init__(self, parent=None, columns=2):

        self.construction_map = {
            self.ElementType.Label: self._create_label,
            self.ElementType.LineEdit: self._create_line_edit,
            self.ElementType.RadioGroup: self._create_radio_group,
            self.ElementType.ListWidget: self._create_list_widget,
            self.ElementType.Button: self._create_button,
            self.ElementType.FakeLabel: self._create_fake_label
        }

        self.parent = parent
        self.columns = columns

        self.column_forms = []
        self.attributes = []
        self.to_harvest = []

        for i in range(self.columns):
            self.column_forms.append(FormColumn(parent))

    def add(self, column: int, element_type: ElementType, name: str, label: str = None, harvest=True, **kwargs):

        if 0 > column or column > self.columns:
            raise ValueError("Column must be between 0 and {}".format(self.columns))

        if name in self.attributes:
            raise ValueError("Element name already used.")

        form = self.column_forms[column]
        elem = self.create_element(element_type, **kwargs)
        form.add_row(elem, name, label, harvest)

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # Element Creation
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def create_element(self, element: ElementType, **kwargs):
        return self.construction_map[element](**kwargs)

    # >

    def _create_label(self, text: str = None):
        element = FormLabel(self.parent)
        if text is not None:
            element.setText(text)
        return element

    def _create_line_edit(self):
        element = FormLineEdit(self.parent)
        return element

    def _create_radio_group(self, options: list, default: int = None):
        element = FormRadioGroupBox(parent=self.parent, options=options)
        if default is not None:
            element.group.buttons()[default].setChecked(True)
        return element

    def _create_list_widget(self, max_height=None):
        element = FormListWidget(self.parent)
        if max_height is not None:
            element.setMaximumHeight(max_height)
        return element

    def _create_button(self, text=None):
        element = FormButton(self.parent)
        if text is not None:
            element.setText(text)
        return element

    def _create_fake_label(self):
        element = FormFakeLabel(self.parent)
        return element

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # API
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def get_form(self):
        """Construct the final form and return it."""
        form_row = FormRow(None, self.column_forms)
        master_form = MasterForm(self.parent)
        master_form.add_form_row(form_row)
        return master_form
