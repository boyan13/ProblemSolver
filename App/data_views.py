# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QSizePolicy, QGridLayout

# App
from App.data_forms import CriteriaFormBoxes, AlternativesFormBoxes, ValuesFormBoxes

# Internal
from GUI.Components.layouts import ExtendedHBox, ExtendedVBox
from GUI.Forms.elements import *
from GUI.Forms.widgets import *
from GUI.Utilities.pyqt_utilities import AutoGridPos
from MCDM.Data.model import DataModel
# +====================================================================================================================+


class InputForm(FormView):

    def __init__(self):
        super().__init__(proceed_btn=CheckButton('Proceed'))

        # Gather the various form boxes for the complete form.
        box1, box2 = CriteriaFormBoxes().form_groups
        box3, box4 = AlternativesFormBoxes().form_groups
        self.boxes = boxes = [box1, box2, box3, box4]

        # Configure the form boxes.
        for box in boxes:
            box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Create layouts
        vbox = ExtendedVBox(self, spacing=15)
        form_hbox = ExtendedHBox()
        form_vbox = ExtendedVBox()
        form_grid = pyqt_utils.null_layout(QGridLayout())
        form_grid.setSpacing(10)
        nav_hbox = ExtendedHBox()

        # Configure main vbox
        vbox.add(1, form_hbox, 1, nav_hbox, 10.0)

        # Configure forms hbox
        form_hbox.add(1, form_vbox, 1)

        # Configure forms vbox
        form_vbox.add(form_grid)

        # Configure forms grid
        form_grid.addWidget(box1, 0, 0)
        form_grid.addWidget(box2, 0, 1)
        form_grid.addWidget(box3, 1, 0)
        form_grid.addWidget(box4, 1, 1)

        # Configure nav buttons hbox
        nav_hbox.add(3, float(self.proceed_btn.sizeHint().width()), 1, self.proceed_btn, 3)

        self.setMinimumWidth(986)

    def reset(self):
        box1, box2, box3, box4 = self.boxes
        box1.criteria_name.setText("")
        box1.criteria_type.group.buttons()[box1.criteria_type.initial].setChecked(True)
        box1.criteria_goal.group.buttons()[box1.criteria_goal.initial].setChecked(True)
        box2.criteria_list.clear()
        box3.alternative_name.setText("")
        box4.alternatives_list.clear()


class ValuesForm(FormView):

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

        boxes = ValuesFormBoxes(self.data_model).form_groups
        self.boxes = boxes

        auto_grid_pos = AutoGridPos(max_cols=3)

        for i, box in enumerate(boxes):
            box.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            box.setMinimumWidth(300)

            i, j = auto_grid_pos.next_pos()
            form_grid.addWidget(box, i, j)

        cols = 3 if len(self.boxes) >= 5 else 2 if len(self.boxes) >= 2 else 1
        min_w = cols * 300 + cols * 15
        self.setMinimumWidth(min_w)
