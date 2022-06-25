# +--------------------------------------------------------------------------------------------------------------------+
import enum
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from gui.Forms.form_factory_elements import FormLineEdit, FormRadioGroupBox, FormListWidget, FormTitle, FormButton
from gui.Forms.form_factory_forms import FormGroup, FormMatrix
# +--------------------------------------------------------------------------------------------------------------------+


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
        LineEdit = 2
        RadioGroup = 3
        ListWidget = 4
        Button = 5

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # Init
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def __init__(self, parent=None):

        self.construction_map = {
            self.ElementType.LineEdit: self._create_line_edit,
            self.ElementType.RadioGroup: self._create_radio_group,
            self.ElementType.ListWidget: self._create_list_widget,
            self.ElementType.Button: self._create_button,
        }

        self.parent = parent
        self.attributes = set()
        self.forms = []
        self.rows = []
        self.cols = []

    # +----------------------------------------------------------------------------------------------------------------+
    #
    #
    # API
    #
    #
    # +----------------------------------------------------------------------------------------------------------------+

    def init(self, row, col, title="", limit_width=True, limit_height=True) -> int:
        """Initialize a new subform."""

        form = FormGroup(self.parent, title, limit_width, limit_height)
        self.forms.append(form)
        self.rows.append(row)
        self.cols.append(col)

        return len(self.forms) - 1

    def add(self, which: int, element_type: ElementType, attr: str, label: str = None, harvest=True, **kwargs):
        """Add to a subform."""

        if attr in self.attributes:
            raise ValueError("Attribute name of element already exists :(")

        form = self.forms[which]
        elem = self.create_element(element_type, **kwargs)
        form.add_element(element=elem, attr=attr, label=label, harvest=harvest)

    def get(self):
        """Construct the final form and return it."""

        final = FormMatrix(self.parent)
        for row, col, form in zip(self.rows, self.cols, self.forms):
            final.add_form(row, col, form)
        return final

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
        element = FormTitle(self.parent)
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
