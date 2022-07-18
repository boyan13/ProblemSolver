# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QFormLayout, QWidget

# Internal
from GUI.Forms.elements import *
# +====================================================================================================================+


class FormLayout(QFormLayout):
    OBJECT_NAME_FOR_LABELS = 'FormLabel'
    OBJECT_NAME_FOR_LABELS_MUTED = 'FormLabelMuted'

    def addRow(self, label: typing.Union[QWidget, str] = None, field: QWidget = None, label_muted=False) -> None:
        if label is not None:
            super().addRow(label, field)
            if type(label) is str:
                if label_muted:
                    self.labelForField(field).setObjectName(self.OBJECT_NAME_FOR_LABELS_MUTED)
                else:
                    self.labelForField(field).setObjectName(self.OBJECT_NAME_FOR_LABELS)
        else:
            super().addRow(field)
