# +====================================================================================================================+
# Internal
from GUI.Components.widgets import StyledWidget
from GUI.Forms.elements import *
from MCDM.Data.enums import DataType
from MCDM.AnalyticHierarchyProcess.model import *

# App
from App.data_views import *
from App.ahp_views import *

# IMPORTANT
from App.configuration import STYLIZED_WINDOW
# +====================================================================================================================+


class Window(STYLIZED_WINDOW, StyledWidget):

    INITIAL_SIZE = (1150, 700)
    MINIMUM_SIZE = (700, 500)

    def __init__(self, parent=None):
        super().__init__(parent, also_do_setup=False)

        self.setMinimumSize(*self.MINIMUM_SIZE)
        self.resize(*self.INITIAL_SIZE)

        self.data_model = DataModel()
        self.backend = None

        self.logs_on = False
        self.permanent_message = LabelMuted(text='Logs: OFF')

        self._setup()

        self.status_bar.addPermanentWidget(self.permanent_message)  # For now this will suffice.

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

        self.new_action(self.file_menu, "&New", self.menu__file__new)
        # self.new_action(self.file_menu, "&Open")
        # self.new_action(self.file_menu, "&Save")
        self.new_action(self.file_menu, "&Exit", self.menu__file__exit)
        self.new_action(self.edit_menu, "&Toggle logs", self.menu__edit__toggle_logs)
        # self.new_action(self.edit_menu, "&Paste")
        # self.new_action(self.edit_menu, "&Cut")
        self.new_action(self.view_menu, "&Reset window size", self.menu__view__reset_window_size)
        # self.new_action(self.help_menu, "&About")
        # self.new_action(self.help_menu, "&Shortcuts")

    #
    # Callbacks
    #

    def menu__file__new(self):
        self.data_model.reset()
        self.backend = None
        self.view.get_view('gather_form').widget().reset()
        self.set_view('gather_form')

    def menu__file__exit(self):
        self.close()

    def menu__edit__toggle_logs(self):
        self.logs_on = not self.logs_on

        if self.backend is not None:
            self.backend.set_logging(self.logs_on)

        if self.logs_on:
            self.permanent_message.setText('Logs: ON')
        else:
            self.permanent_message.setText('Logs OFF')

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
            self.backend.set_logging(self.logs_on)

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


