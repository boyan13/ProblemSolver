# +====================================================================================================================+
# Pythonic
import typing

# Internal
from MCDM.Data.enums import DataType, DataGoal, QualitativeValue
from MCDM.Data.criteria import Criteria
# +====================================================================================================================+


class Alternative:

    @property
    def name(self):
        return self.__name

    @property
    def criteria_names(self):
        return [c.name for c in self._criteria.values()]

    def __init__(self, name: str, criteria: typing.List[Criteria]):
        self.__name = name
        self._criteria = criteria
        self._values = {}

    def get_numeric(self, item):
        if self._criteria[item].data_type is DataType.Qualitative:
            return self._values[item].value
        else:
            return self._values[item]

    def __getitem__(self, item):
        return self._values[item]

    def __setitem__(self, key, value):

        if key not in self.criteria_names:
            raise KeyError('Attempting to set the value of an unknown criterion.')
        if self._criteria[key].data_type is DataType.Qualitative and type(value) is not QualitativeValue:
            raise TypeError(f"Bad value type for qualitative data.")
        if self._criteria[key].data_type is DataType.Quantitative and type(value) not in {int, float}:
            raise TypeError(f"Bad value type for quantitative data.")

        self._values[key] = value

    def __hash__(self):
        return hash(self.__name)


class AHPAlternative(Alternative):
    def __init__(self, position: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
