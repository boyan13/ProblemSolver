# ----------------------------------------------------------------------------------------------------------------------
import enum
import copy

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QLabel, QSizePolicy, QLineEdit, QFormLayout, QPushButton, QListWidget, \
    QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup

from gui.Components.widgets import StyledWidget, StyleEnabledMixin
from gui.Components import utilities
# ----------------------------------------------------------------------------------------------------------------------


class FormFactoryForm(StyledWidget):
    """Subform used by Form Factory when building complex forms. Form elements must inherit and implement
    FormFactoryElementInterface"""

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


class FormFactoryStretcher(StyledWidget):
    """When the actual column forms are expanded to the maximum, we want this stretcher to start taking up any
    additional horizontal spacing. This has a purely visual purpose."""
    pass


# +--------------------+
# | Harvestable        |
# +--------------------+


class FormFactoryElementInterface:

    def harvest(self):
        """Harvest the elements's data."""
        # Form's data harvest will fail if you do not implement this.
        raise NotImplementedError()


class FormLineEdit(FormFactoryElementInterface, QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

    def harvest(self):
        return self.text()


class FormRadioGroup(FormFactoryElementInterface, QButtonGroup):

    def harvest(self):
        return self.checkedButton().text()


class FormListWidget(FormFactoryElementInterface, QListWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)


class FormFakeLabel(QLabel):
    pass


class FormButton(StyleEnabledMixin, QPushButton):
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

        # We store the __attr__ strings of all form elements. We need this when we later construct the master form.
        self.attributes = []

        # This determines which form elements will be added for harvesting to the master form's harvest method.
        self.to_harvest = []

        self.vbox = utilities.nulled_layout(QVBoxLayout())
        self.hbox = utilities.nulled_layout(QHBoxLayout())

        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(2)

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
            the_label = form.form_layout.itemAt(form.form_layout.rowCount() - 1).widget()
            the_label.setObjectName(self.FIELD_LABEL_OBJ_NAME)
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

        # This will be the combination of all subforms into a master form.
        master_form = StyledWidget(self.parent, object_name="Form")

        # Set all form elements as attributes of the master form
        for attr, value in self.attributes:
            setattr(master_form, attr, value)

        # Set a copy of the to_harvest list on the master form. This allows you to later change which elements should be
        # harvested if you want to, since the harvest() method created below uses this attribute to decide which
        # elements to query for their data.
        setattr(master_form, 'to_harvest', copy.deepcopy(self.to_harvest))

        # Automatically construct a method that harvests the master form's elements and returns a data dict.
        setattr(master_form, 'harvest', lambda self_=master_form: {k: getattr(self_, k).harvest() for k in self_.to_harvest})

        for form in self.column_forms:
            form.form_layout.setAlignment(Qt.AlignTop)
            form.setParent(master_form)
        master_form.setLayout(self.vbox)

        return master_form