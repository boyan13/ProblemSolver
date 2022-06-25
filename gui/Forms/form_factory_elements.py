# ----------------------------------------------------------------------------------------------------------------------

from types import SimpleNamespace

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QGroupBox, QButtonGroup, QVBoxLayout, QListWidget, \
                            QListWidgetItem, QRadioButton, QLabel, QPushButton

from gui.Components.widgets import StyleEnabledMixin
from gui.Forms.form_factory_interfaces import FormElementMixin
from gui.Components import utilities as u
# ----------------------------------------------------------------------------------------------------------------------


class FormLineEdit(FormElementMixin, QLineEdit):

    _HARVESTABLE = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def harvest(self):
        return self.text()


class FormRadioGroupBox(FormElementMixin, QGroupBox):

    _HARVESTABLE = True

    def __init__(self, options, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.group = QButtonGroup()
        self.vbox = u.nulled_layout(QVBoxLayout(self))

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
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(super().sizeHint().width(), self.maximumHeight())

    def harvest(self):
        return [self.item(i) for i in range(self.count())]

    def keyPressEvent(self, event):

        # Delete selected row on user pressing 'Delete'.
        if event.key() == Qt.Key_Delete:
            for item in self.selectedItems():
                row = self.row(item)
                self.takeItem(row)

        super().keyPressEvent(event)


class FormListWidgetItem(QListWidgetItem):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


class FormTitle(FormElementMixin, StyleEnabledMixin, QLabel):

    _HARVESTABLE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


class FormButton(FormElementMixin, StyleEnabledMixin, QPushButton):

    _HARVESTABLE = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)


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
