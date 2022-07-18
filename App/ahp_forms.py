# +====================================================================================================================+
# Pythonic

# Internal
from GUI.Components.layouts import ExtendedHBox, ExtendedVBox
from GUI.Forms.elements import *
from GUI.Forms.layouts import FormLayout
from GUI.Forms.widgets import *
from MCDM.AnalyticHierarchyProcess.enums import Important
from MCDM.AnalyticHierarchyProcess.exceptions import AHPException
from MCDM.Data.model import DataModel
# +====================================================================================================================+


class WeightsFormBoxes:

    def __init__(self, data_model: DataModel):
        self.form_groups: List[FormBox] = []
        self._setup_view(data_model)

    def _setup_view(self, data_model: DataModel):

        box = FormBox(title='Compare')
        self.form_groups.append(box)

        hbox = ExtendedHBox(box, spacing=15)
        vbox = ExtendedVBox(spacing=15)
        lay = FormLayout()
        lay.setSpacing(10)
        hbox.add(15.0, 1, vbox, 1, 15.0)
        vbox.add(15.0, 1, lay, 1, 15.0)

        choices = {}
        for e in Important:
            choice = "(" + str(e) + ") " + e.name
            choices[choice] = e.value

        pairs = data_model.get_minimum_pairs()
        for pair in pairs:
            text1 = LabelMuted(text="Importance of ")
            text1.set_size_hints('')
            criteria1 = Label(text=pair[0])
            text2 = LabelMuted(text=" over ")
            criteria2 = Label(text=pair[1])

            importance = ComboBox(choices=choices)
            importance.setCurrentIndex(8)

            hbox = ExtendedHBox()
            hbox.add(text1, criteria1, text2, criteria2, 1, importance)
            lay.addRow(field=hbox)
            box.set_as_pairs((criteria1.text() + '_____' + criteria2.text(), importance))
class RankingsFormBoxes:

    def __init__(self, data_model: DataModel, backend):
        self.form_groups: List[FormBox] = []
        self._setup_view(data_model, backend)

    def _setup_view(self, data_model: DataModel, backend):

        box = FormBox(title='Ranking')
        self.form_groups.append(box)

        hbox = ExtendedHBox(box, spacing=15)
        vbox = ExtendedVBox(spacing=15)
        lay = FormLayout()
        lay.setSpacing(10)
        hbox.add(15.0, 1, vbox, 1, 15.0)
        vbox.add(15.0, 1, lay, 1, 15.0)

        try:
            ranking = backend.process()
        except AHPException as exc:
            problem = Label(text=exc.text)
            problem.setWordWrap(True)
            box.setTitle("Error")
            lay.addRow(label="A problem occurred:", field=problem, label_muted=True)
            box.set(problem=problem)
            return

        ranking_chart = ListWidget(read_only=True)
        lay.addRow(field=ranking_chart)

        reverse_map = {}
        values = []

        for alternative, rank in ranking.items():
            if rank not in reverse_map.keys():
                reverse_map[rank] = []
            reverse_map[rank].append(alternative)
            values.append(rank)

        values.sort(reverse=True)

        for value in values:
            alternative = reverse_map[value].pop(0)
            text = f"({str(value)})  {alternative}"
            item = ListWidgetItem(text)
            ranking_chart.addItem(item)

        box.set(scores=ranking_chart)
