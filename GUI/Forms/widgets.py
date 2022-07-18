# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QGroupBox

# Internal libs
from GUI.Components.widgets import StyledWidget
from GUI.Forms.mixins import FormBoxMixin
# +====================================================================================================================+


class FormBox(FormBoxMixin, QGroupBox):
    pass


class FormView(StyledWidget):
    def __init__(self, boxes: list = None, proceed_btn=None, back_btn=None, parent=None):
        super().__init__(parent)
        self.setContentsMargins(15, 15, 15, 15)
        self.boxes = boxes if boxes is not None else []

        self.proceed_btn = proceed_btn
        if proceed_btn is not None:
            proceed_btn.setParent(self)

        self.back_btn = back_btn
        if back_btn is not None:
            back_btn.setParent(self)

    def harvest(self):
        data = {}

        for box in self.boxes:
            data[box.title()] = box.harvest()

        return data
