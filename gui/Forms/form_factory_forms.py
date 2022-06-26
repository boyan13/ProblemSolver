# ----------------------------------------------------------------------------------------------------------------------
import typing
from functools import cached_property

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QGroupBox, QFormLayout, QVBoxLayout, QHBoxLayout, QGridLayout

from gui.Components import utilities
from gui.Components.widgets import StyledWidget
from gui.Forms.form_factory_interfaces import FormMixin, FormManagerMixin
from gui.Forms.form_factory_elements import *
# ----------------------------------------------------------------------------------------------------------------------


class FormVSpacer(StyledWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)


class FormGroup(FormMixin, QGroupBox):

    OBJECT_NAME_OF_FIELD_LABELS = 'FormLabel'
    resized = QtCore.pyqtSignal(QtGui.QResizeEvent)

    def __init__(self, parent=None, title: str = "", limit_width=True, limit_height=True):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setTitle(title)
        self.form_layout = QFormLayout(self)
        self.form_layout.setSpacing(10)

        self.vspacer = None

        self._should_limit_width = limit_width
        self._should_limit_height = limit_height

        self.max_width_set = False
        self.max_height_set = False

    def limit_width(self, value: bool):
        if value is True:
            if self._should_limit_width is not value:
                self.max_width_set = False
                self._should_limit_width = True
                self.resize(self.sizeHint())
        else:
            if self._should_limit_width is value:
                self.max_width_set = False
                self._should_limit_width = False
                self.resize(self.sizeHint())

    def limit_height(self, value: bool):
        if value is True:
            if self._should_limit_height is not value:
                self.max_height_set = False
                self._should_limit_height = True
                self.resize(self.sizeHint())
        else:
            if self._should_limit_height is value:
                self.max_height_set = False
                self._should_limit_height = False
                self.resize(self.sizeHint())

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.resize(self.sizeHint())

    def update_max_dimensions(self):

        # We have already set the size limits.
        if self.max_width_set and self.max_height_set:
            return

        # We do not want to restrict our size.
        if not self._should_limit_width and not self._should_limit_height:
            return

        all_are_at_max_width = []
        all_are_at_pref_height = []

        check_width = True and self._should_limit_width
        check_height = True and self._should_limit_height

        for attr in self.attributes:
            element: QtWidgets.QWidget = getattr(self, attr)

            if check_width:
                if element.width() == element.maximumWidth():
                    all_are_at_max_width.append(True)
                else:
                    check_width = False

            if check_height:
                if element.height() == element.sizeHint().height():
                    all_are_at_pref_height.append(True)
                else:
                    check_height = False

            if check_width is check_height is False:
                return

        if all_are_at_max_width:
            self.setMaximumWidth(self.width())
            self.max_width_set = True

        if all_are_at_pref_height and self.vspacer.height() < 1:
            self.setMaximumHeight(self.height())
            self.max_height_set = True

    def add_element(self, element, attr: str, label: str = None, harvest=True):

        setattr(self, attr, element)
        self.attributes.append(attr)

        self.form_layout.removeItem(self.form_layout.itemAt(self.form_layout.rowCount()))

        if harvest and element.harvestable:
            self.to_harvest.append(attr)

        if label is not None:
            self.form_layout.addRow(label, element)
            the_label = self.form_layout.labelForField(element)
            the_label.setObjectName(self.OBJECT_NAME_OF_FIELD_LABELS)
        else:
            self.form_layout.addRow(element)

        self.vspacer = FormVSpacer(self)
        self.form_layout.addWidget(self.vspacer)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.update_max_dimensions()
        self.resized.emit(a0)
        super().resizeEvent(a0)


class FormMatrix(FormManagerMixin, StyledWidget):

    @classmethod
    def combine(cls, form1, form2, direction: str = 'below'):

        combined = cls()

        if direction == 'below':
            rows = {}
            first_form = False

            for form in [form1, form2]:
                first_form = not first_form
                for subform in form.subforms:
                    row, col, row_span, col_span = form.grid.getItemPosition(form.grid.indexOf(subform))
                    if not first_form:
                        if row not in rows:
                            rows[row] = combined.grid.rowCount() + row
                        row = rows[row]
                    combined.add_form(row, col, form)
        else:
            raise ValueError("Invalid direction")

        return combined

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.grid = utilities.nulled_layout(QGridLayout(self))
        self.grid.setSpacing(15)

    def add_form(self, row, col, form: FormGroup) -> int:
        self.grid.addWidget(form, row, col)
        self.subforms.append(form)
        return self.grid.indexOf(form)


