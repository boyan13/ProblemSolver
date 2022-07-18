# +====================================================================================================================+
# Pythonic
import typing
from collections import OrderedDict
from itertools import combinations

# Internal
from MCDM.Data.alternative import Alternative
from MCDM.Data.criteria import Criteria
from MCDM.Data.enums import DataType, DataGoal, QualitativeValue
# +====================================================================================================================+


class DataModel:
    def __init__(self, goal: str = ""):

        self.goal = goal
        self.criteria = OrderedDict()
        self.alternatives = OrderedDict()
        self.alternatives_values = {}

    def set_goal(self, goal: str):
        self.goal = goal

    def get_minimum_pairs(self, of_criteria=True):
        """Get all pairs of criteria."""
        if of_criteria:
            return list(combinations(list(self.criteria.keys()), 2))
        else:
            return list(combinations(list(self.alternatives.keys()), 2))

    def reset(self):
        self.criteria = OrderedDict()
        self.alternatives = OrderedDict()
        self.alternatives_values = {}

    def add_criterion(self, name: str, data_type: str, goal: str):
        """Add a criterion."""

        name_ = name
        data_type_ = DataType.from_string(data_type)
        goal_ = DataGoal.from_string(goal)

        if data_type_ is None or goal_ is None:
            raise TypeError('Failed to cast to a proper data type or goal.')

        criteria = Criteria(name_, data_type_, goal_)
        self.criteria[criteria.name] = criteria
        self.alternatives_values[criteria.name] = {}

    def add_alternative(self, name: str):
        self.alternatives[name] = Alternative(name=name, criteria=list(self.criteria))

    def set_value(self, criterion: str, alternative: str, value: typing.Union[float, int, QualitativeValue]):

        if self.criteria[criterion].data_type is DataType.Qualitative and type(value) is not QualitativeValue:
            try:
                value = QualitativeValue(value)
            except Exception as exc:
                raise TypeError(f"Bad value type for qualitative data.")
        if self.criteria[criterion].data_type is DataType.Quantitative and type(value) not in {int, float}:
            raise TypeError(f"Bad value type for quantitative data.")

        self.alternatives_values[criterion][alternative] = value

    def get_value(self, criterion: str, alternative: str, numeric=True):

        value = self.alternatives_values[criterion][alternative]
        if numeric and self.criteria[criterion].data_type is DataType.Qualitative:
            value = value.value
        return value
