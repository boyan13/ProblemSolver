# +====================================================================================================================+
# Internal
from MCDM.AnalyticHierarchyProcess.enums import *
# +====================================================================================================================+


class Criteria:

    @property
    def name(self):
        return self.__name

    @property
    def data_type(self):
        return self.__data_type

    @property
    def goal(self):
        return self.__goal

    def __init__(self, name: str, data_type: DataType, goal: DataGoal):
        self.__name = name
        self.__data_type = data_type
        self.__goal = goal

    def __hash__(self):
        return hash(self.__name)


class AHPCriteria(Criteria):
    def __init__(self, position: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
