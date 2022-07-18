
# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QGridLayout, QSizePolicy

# Internal
from GUI.Base.window import BaseWindow
from GUI.Components.widgets import StyledWidget
from GUI.Forms.forms import *
from GUI.Utilities import pyqt_utilities as pyqt_utils
from GUI.Utilities import python_utilities as py_utils
from GUI.Components.layouts import ExtendedHBox, ExtendedVBox
from MCDM.AnalyticHierarchyProcess.model import *

# IMPORTANT
from App.configuration import STYLIZED_WINDOW


class AutoGridPos:

    def __init__(self, max_rows=None, max_cols=None):
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.gen = self.__next()
        self.__row_count = 0
        self.__col_count = 0
        self._populate_new_row = None

    def next_pos(self):
        return self.gen.__next__()

    def __next(self):

        while True:
            if self._populate_new_row:
                for j in range(self.__col_count):
                    yield self.__row_count - 1, j
            else:
                for i in range(self.__row_count):
                    yield i, self.__col_count - 1

            if self.max_rows is not None and self.__row_count == self.max_rows:
                self.__col_count += 1
                self._populate_new_row = False

            elif self.max_cols is not None and self.__col_count == self.max_cols:
                self.__row_count += 1
                self._populate_new_row = True

            elif self.__row_count == self.__col_count:
                self.__col_count += 1
                self._populate_new_row = False

            else:
                self.__row_count += 1
                self._populate_new_row = True


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


class Window(STYLIZED_WINDOW, StyledWidget):

    INITIAL_SIZE = (1150, 700)
    MINIMUM_SIZE = (700, 500)

    def __init__(self, parent=None):
        super().__init__(parent, also_do_setup=False)

        self.setMinimumSize(*self.MINIMUM_SIZE)
        self.resize(*self.INITIAL_SIZE)

        self.data_model = DataModel()
        self.backend = None

        self._setup()

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Menu Bar
    #
    # ------------------------------------------------------------------------------------------------------------------

    def _configure_menu_bar(self):
        self.file_menu = self.menu_bar.addMenu("&File")
        self.edit_menu = self.menu_bar.addMenu("&Edit")
        self.view_menu = self.menu_bar.addMenu("&View")
        self.help_menu = self.menu_bar.addMenu("&Help")

        self.new_action(self.file_menu, "&New")
        self.new_action(self.file_menu, "&Open")
        self.new_action(self.file_menu, "&Save")
        self.new_action(self.file_menu, "&Exit")
        self.new_action(self.edit_menu, "&Copy")
        self.new_action(self.edit_menu, "&Paste")
        self.new_action(self.edit_menu, "&Cut")
        self.new_action(self.view_menu, "&Reset window size")
        self.new_action(self.help_menu, "&About")
        self.new_action(self.help_menu, "&Shortcuts")

        self.view_menu.actions()[0].triggered.connect(self.menu__view__reset_window_size)

    #
    # Callbacks
    #

    def menu__view__reset_window_size(self):
        self.resize(*self.INITIAL_SIZE)

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Views
    #
    # ------------------------------------------------------------------------------------------------------------------

    #
    # Configs
    #

    def _configure_view(self):
        
        # Criteria/Alternatives data collection form
        self.gather_form = InputForm()
        self.gather_form.setObjectName('WindowView')
        self.view.add_view(key='gather_form', view=pyqt_utils.wrap_in_scroll_area(self.gather_form, parent=self))

        # Value setting form
        self.values_form = ValuesForm(self.data_model)
        self.values_form.setObjectName('WindowView')
        self.view.add_view(key='values_form', view=pyqt_utils.wrap_in_scroll_area(self.values_form, parent=self))

        # Weights form
        self.weights_form = WeightsForm(self.data_model)
        self.weights_form.setObjectName('WindowView')
        self.view.add_view(key='weights_form', view=pyqt_utils.wrap_in_scroll_area(self.weights_form, parent=self))

        # Rankings form
        self.rankings_form = RankingForm(self.data_model)
        self.rankings_form.setObjectName('WindowView')
        self.view.add_view(key='rankings_form', view=pyqt_utils.wrap_in_scroll_area(self.rankings_form, parent=self))

        # Preps
        self.set_prep('values_form', self._prep_values_form)
        self.set_prep('weights_form', self._prep_weights_form)
        self.set_prep('rankings_form', self._prep_rankings_form)

        # Navigation
        self.set_next('gather_form', 'values_form')
        self.set_next('values_form', 'weights_form')
        self.set_next('weights_form', 'rankings_form')

        # Set the initial view
        self.view.set_view('gather_form')

    #
    # Preps
    #

    def _prep_values_form(self, form):
        current_form = self.view.get_view().widget()
        form = form.widget()
        
        if current_form is self.view.get_view('gather_form').widget():
            data = current_form.harvest()
            self.data_model.reset()

            for criterion_item in data['Criteria']['criteria_list']:

                name_ = criterion_item.data.text
                type_ = criterion_item.data.type
                goal_ = criterion_item.data.goal
                self.data_model.add_criterion(name_, type_, goal_)

            for alternative_item in data['Alternatives']['alternatives_list']:

                name_ = alternative_item.data.text
                self.data_model.add_alternative(name_)

            if len(self.data_model.criteria) == 0 or len(self.data_model.alternatives) == 0:
                return False

            form.reset()
            return True

        elif current_form is self.view.get_view('weights_form').widget():
            return True

        return False

    def _prep_weights_form(self, form):
        current_form = self.get_current().widget()
        form = form.widget()

        if current_form is self.view.get_view('values_form').widget():
            # Init backend at this point
            self.backend = AHPModel(self.data_model)
            data = current_form.harvest()

            for criterion in data.keys():
                for alternative, value in data[criterion].items():
                    if value is None or value == "":
                        return False
                    elif self.data_model.criteria[criterion].data_type is DataType.Qualitative:
                        self.data_model.set_value(criterion, alternative, value.value)
                    else:
                        self.data_model.set_value(criterion, alternative, float(value))

            form.reset()
            return True

        elif current_form is self.view.get_view('rankings_form').widget():
            return True

        return False

    def _prep_rankings_form(self, form):
        current_form = self.get_current().widget()
        form = form.widget()

        if current_form is not self.view.get_view('weights_form').widget():
            return False

        data = current_form.harvest()['Compare']
        for pair, weight in data.items():
            criteria1, criteria2 = pair.split('_____')
            self.backend.set_weight(criteria1, criteria2, weight)

        form.reset(self.backend)
        return True


