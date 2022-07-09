# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QFormLayout, QSizePolicy

# Internal
from GUI.Utilities import pyqt_utilities as pyqt_utils
from GUI.Forms.elements import *
# +====================================================================================================================+


class FormLayout(QFormLayout):
    OBJECT_NAME_FOR_LABELS = 'FormLabel'

    def addRow(self, label: typing.Union[QWidget, str] = None, field: QWidget = None) -> None:
        if label is not None:
            super().addRow(label, field)
            if type(label) is str:
                self.labelForField(field).setObjectName(self.OBJECT_NAME_FOR_LABELS)
        else:
            super().addRow(field)


class FormBox(FormBoxMixin, QGroupBox):
    pass


class FormGroupsNamespace(SimpleNamespace):

    def __setattr__(self, key, value):
        if not isinstance(value, FormBox):
            raise TypeError(f"You may only add {FormBox.__name__} instances.")
        super().__setattr__(key, value)

    def __getattribute__(self, item) -> FormBox:
        return super().__getattribute__(item)

    def __iter__(self):
        return iter([getattr(self, a) for a in self.__dict__.keys()])

    def __len__(self):
        return len(self.__dict__.keys())


class CriteriaFormBoxes:

    def __init__(self):
        self.form_groups = []
        self._setup_widgets()
        self._setup_layout()

    # Event handles

    @staticmethod
    def add_criteria_to_list(box1_, box2_):

        text = box1_.criteria_name.harvest()
        box1_.criteria_name.setText("")
        c_type = box1_.criteria_type.harvest()
        c_goal = box1_.criteria_goal.harvest()

        if text == "" or c_type is None or c_goal is None:
            return

        item = ListWidgetItem(text, type=c_type, goal=c_goal)
        item.setText(text + f" ({c_type}) ({c_goal})")
        box2_.criteria_list.addItem(item)

    @staticmethod
    def del_criteria_from_list(box2_):

        for item in box2_.criteria_list.selectedItems():
            row = box2_.criteria_list.row(item)
            box2_.criteria_list.takeItem(row)

    # Setups

    def _setup_widgets(self):

        # Create boxes

        box1 = self.box1 = FormBox("Add Criteria")
        box2 = self.box2 = FormBox("Criteria")
        box1.setMaximumHeight(800)
        box2.setMaximumHeight(800)
        self.form_groups = [box1, box2]

        # Create elements

        criteria_name = LineEdit(is_harvestable=False)
        criteria_add = CheckButton(text="ADD")
        criteria_del = CheckButton(text="DELETE")
        criteria_type = ColumnRadioGroup(texts=["Quantitative", "Qualitative"], is_harvestable=False)
        criteria_goal = ColumnRadioGroup(texts=["Minimize", "Maximize"], is_harvestable=False)
        criteria_list = ListWidget()

        # Assign to boxes

        self.box1.set(
            criteria_name=criteria_name,
            criteria_add=criteria_add,
            criteria_del=criteria_del,
            criteria_type=criteria_type,
            criteria_goal=criteria_goal
        )
        self.box2.set(
            criteria_list=criteria_list
        )

        # Configure

        criteria_name.setPlaceholderText("Name")
        criteria_type.group.buttons()[0].setChecked(True)
        criteria_goal.group.buttons()[0].setChecked(True)

        # Connect

        criteria_name.returnPressed.connect(
            lambda box1_=box1, box2_=box2: self.__class__.add_criteria_to_list(box1_, box2_)
        )
        criteria_add.clicked.connect(
            lambda checked, box1_=box1, box2_=box2: self.__class__.add_criteria_to_list(box1_, box2_)
        )
        criteria_del.clicked.connect(
            lambda checked, box2_=box2: self.__class__.del_criteria_from_list(box2_)
        )

    def _setup_layout(self):

        box1, box2 = self.form_groups

        def _setup_box1_layout():

            lay = FormLayout(box1)

            # Layout

            lay.setSpacing(10)
            lay.addRow("Criteria name:", box1.criteria_name)
            lay.addRow("Type:", box1.criteria_type)

            hbox = pyqt_utils.null_layout(QHBoxLayout())
            hbox.addWidget(box1.criteria_add)
            hbox.addSpacing(10)
            hbox.addWidget(box1.criteria_del)

            vbox = pyqt_utils.null_layout(QVBoxLayout())
            vbox.addWidget(box1.criteria_goal)
            vbox.addSpacing(10)
            vbox.addLayout(hbox)

            lay.addRow("Goal:", vbox)

        def _setup_box2_layout():

            lay = FormLayout(box2)

            # Size Policies

            box2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            box2.criteria_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Layout

            lay.setSpacing(10)
            lay.addRow(box2.criteria_list)

        _setup_box1_layout()
        _setup_box2_layout()


class AlternativesFormBoxes:

    def __init__(self):
        self.form_groups = []
        self._setup_widgets()
        self._setup_layout()

    # Event handles

    @staticmethod
    def add_alternative_to_list(box1_, box2_):

        text = box1_.alternative_name.harvest()
        box1_.alternative_name.setText("")

        if text == "":
            return

        item = ListWidgetItem(text)
        item.setText(text)
        box2_.alternatives_list.addItem(item)

    @staticmethod
    def del_criteria_from_list(box2_):

        for item in box2_.alternatives_list.selectedItems():
            row = box2_.alternatives_list.row(item)
            box2_.alternatives_list.takeItem(row)

    # Setups

    def _setup_widgets(self):

        # Create boxes

        box1 = self.box1 = FormBox("Add Alternative")
        box2 = self.box2 = FormBox("Alternatives")
        box1.setMaximumHeight(800)
        box2.setMaximumHeight(800)
        self.form_groups = [box1, box2]

        # Create elements

        alternative_name = LineEdit(is_harvestable=False)
        alternative_add = CheckButton(text="ADD")
        alternative_del = CheckButton(text="DELETE")
        alternatives_list = ListWidget()

        # Assign to boxes

        self.box1.set(
            alternative_name=alternative_name,
            alternative_add=alternative_add,
            alternative_del=alternative_del
        )
        self.box2.set(
            alternatives_list=alternatives_list
        )

        # Configure

        alternative_name.setPlaceholderText("Name")

        # Connect

        alternative_name.returnPressed.connect(
            lambda box1_=box1, box2_=box2: self.__class__.add_alternative_to_list(box1_, box2_)
        )
        alternative_add.clicked.connect(
            lambda checked, box1_=box1, box2_=box2: self.__class__.add_alternative_to_list(box1_, box2_)
        )
        alternative_del.clicked.connect(
            lambda checked, box2_=box2: self.__class__.del_criteria_from_list(box2_)
        )

    def _setup_layout(self):

        box1, box2 = self.form_groups

        def _setup_box1_layout():

            lay = FormLayout(box1)

            # Layout

            lay.setSpacing(10)

            hbox = pyqt_utils.null_layout(QHBoxLayout())
            hbox.addWidget(box1.alternative_add)
            hbox.addSpacing(10)
            hbox.addWidget(box1.alternative_del)

            vbox = pyqt_utils.null_layout(QVBoxLayout())
            vbox.addWidget(box1.alternative_name)
            vbox.addSpacing(10)
            vbox.addLayout(hbox)

            lay.addRow("Alternative name:", vbox)

        def _setup_box2_layout():

            lay = FormLayout(box2)

            # Size Policies

            box2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            box2.alternatives_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Layout

            lay.setSpacing(10)
            lay.addRow(box2.alternatives_list)

        _setup_box1_layout()
        _setup_box2_layout()
