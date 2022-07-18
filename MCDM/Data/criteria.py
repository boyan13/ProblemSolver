# +====================================================================================================================+
# Internal
from MCDM.Data.enums import DataType, DataGoal
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
        if type(data_type) is not DataType or type(goal) is not DataGoal:
            raise TypeError()

        self.__name = name
        self.__data_type = data_type
        self.__goal = goal

    def __hash__(self):
        return hash(self.__name)


class AHPCriteria(Criteria):
    def __init__(self, position: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.position = position
