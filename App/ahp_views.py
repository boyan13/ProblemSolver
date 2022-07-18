# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QSizePolicy, QGridLayout

# App
from App.ahp_forms import WeightsFormBoxes, RankingsFormBoxes

# Internal
from GUI.Components.layouts import ExtendedHBox, ExtendedVBox
from GUI.Forms.elements import *
from GUI.Forms.widgets import *
from MCDM.Data.model import DataModel
# +====================================================================================================================+


class WeightsForm(FormView):

    def __init__(self, data_model: DataModel):
        super().__init__(back_btn=CheckButton("Back"), proceed_btn=CheckButton("Proceed"))
        self.data_model = data_model
        self.setMinimumWidth(1000)

    def reset(self):
        if self.layout() is not None:
            pyqt_utils.purge_layout(self.layout())

        vbox = ExtendedVBox(self, spacing=15)
        form_hbox = ExtendedHBox()
        form_vbox = ExtendedVBox()
        form_grid = pyqt_utils.null_layout(QGridLayout())
        form_grid.setSpacing(10)
        nav_hbox = ExtendedHBox()

        vbox.add(1, form_hbox, 1, nav_hbox, 10.0)
        form_hbox.add(1, form_vbox, 1)
        form_vbox.add(form_grid)
        nav_hbox.add(3, self.back_btn, 1, self.proceed_btn, 3)

        boxes = WeightsFormBoxes(self.data_model).form_groups
        self.boxes = boxes
        box = boxes[0]

        if len(box.elements_attributes) == 0:
            box.setMinimumWidth(500)

        form_grid.addWidget(box, 0, 0)

        self.setMinimumWidth(500)

class RankingForm(FormView):

    def __init__(self, data_model: DataModel):
        super().__init__(back_btn=CheckButton("Back"))
        self.data_model = data_model

    def reset(self, backend):
        if self.layout() is not None:
            pyqt_utils.purge_layout(self.layout())

        vbox = ExtendedVBox(self, spacing=15)
        form_hbox = ExtendedHBox()
        form_vbox = ExtendedVBox()
        form_grid = pyqt_utils.null_layout(QGridLayout())
        form_grid.setSpacing(10)
        nav_hbox = ExtendedHBox()

        vbox.add(1, form_hbox, 1, nav_hbox, 10.0)
        form_hbox.add(1, form_vbox, 1)
        form_vbox.add(form_grid)
        nav_hbox.add(3, self.back_btn, 1, float(self.back_btn.sizeHint().width()), 3)

        boxes = RankingsFormBoxes(self.data_model, backend).form_groups
        self.boxes = boxes
        for box in boxes:
            box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        form_grid.addWidget(boxes[0], 0, 0)

        self.setMinimumWidth(500)
