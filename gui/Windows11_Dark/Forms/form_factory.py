# ----------------------------------------------------------------------------------------------------------------------
import enum

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel, QSizePolicy, QWidget, QLineEdit, QFormLayout, QPushButton, QListWidget, \
    QListWidgetItem, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup

from gui.Windows11_Dark.Components.widgets import StyledWidget, StyleEnabledMixin
# ----------------------------------------------------------------------------------------------------------------------

class FormFactoryForm(StyledWidget):
    """Subform used by Form Factory when building complex forms. Form elements must inherit and implement FormFactoryElementInterface"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.form_layout = QFormLayout(self)
        self.to_harvest = []

    def harvest(self):
        """Harvest the form's data. Recursively call harvest() on its elements and store the results in a dict."""

        data = {}
        for attr in self.to_harvest:
            data[attr] = getattr(self, attr).harvest()
        return data

# +--------------------+
# | Harvestable        |
# +--------------------+

class FormFactoryElementInterface:

    def harvest(self):
        """Harvest the elements's data."""

        # Form's data harvest will fail if you do not implement this.
        raise NotImplementedError()

class FormLineEdit(FormFactoryElementInterface, QLineEdit):

    def harvest(self):
        return self.text()


class FormRadioGroup(FormFactoryElementInterface, QButtonGroup):

    def harvest(self):
        return self.checkedButton().text()


class FormListWidget(FormFactoryElementInterface, QListWidget):

    def harvest(self):
        return [self.item(i).text() for i in range(self.count())]

    def keyPressEvent(self, event):

        # Delete selected row on user pressing 'Delete'.
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                row = self.row(item)
                self.takeItem(row)

        super().keyPressEvent(event)

class FormRadioButton(QRadioButton):
    pass


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

# +--------------------+
# | Non-Harvestable    |
# +--------------------+

class FormLabel(StyleEnabledMixin, QLabel):
    pass


class FormFakeLabel(QLabel):
    pass


class FormButton(QPushButton):
    pass

# +--------------------+
# | Factory            |
# +--------------------+

class FormFactory:

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

        self.hbox = QHBoxLayout()

        for i in range(self.columns):
            self.column_forms.append(FormFactoryForm(parent))
            self.hbox.addWidget(self.column_forms[i])

    def add(self, column: int, element: ElementType, name, label: str = None, harvest=True, **kwargs):
        if 0 > column or column > self.columns:
            raise ValueError("Column must be between 0 and {}".format(self.columns))

        form = self.column_forms[column]
        form_element = self.create_element(element, **kwargs)

        self.attributes.append((name, form_element))
        if not isinstance(form_element, FormFactoryElementInterface):
            harvest = False

        if label is not None:
            form.form_layout.addRow(label, form_element)
        else:
            form.form_layout.addRow(form_element)

        if harvest:
            self.to_harvest.append(name)

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
    # >
    # >

    def _create_label(self, text: str = None):
        element = FormLabel(self.parent)
        if text is not None:
            element.setText(text)
        return element

    def _create_line_edit(self):
        element = FormLineEdit(self.parent)
        return element

    def _create_radio_group(self, buttons_texts: list):
        element = QButtonGroup(self.parent)
        for text in buttons_texts:
            button = FormRadioButton(self.parent)
            button.setText(text)
            element.addButton(button)
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
        entire_form = StyledWidget(self.parent)

        for attr, value in self.attributes:
            setattr(entire_form, attr, value)
        setattr(entire_form, 'harvest', lambda self=entire_form, to_harvest=self.to_harvest: {k: getattr(self, k).harvest() for k in to_harvest})

        for form in self.column_forms:
            form.form_layout.setAlignment(Qt.AlignTop)
            form.setParent(entire_form)
        entire_form.setLayout(self.hbox)

        return entire_form