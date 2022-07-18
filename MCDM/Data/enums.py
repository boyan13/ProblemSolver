# +====================================================================================================================+
# Pythonic
from enum import Enum
# +====================================================================================================================+


class DataType(Enum):

    @classmethod
    def from_string(cls, value: str):
        for e in cls:
            if e.name == value:
                return e

    Quantitative = 1
    Qualitative = 2


class DataGoal(Enum):

    @classmethod
    def from_string(cls, value: str):
        for e in cls:
            if e.name == value:
                return e

    Minimize = 1
    Maximize = 2


class QualitativeValue(Enum):
    ExceptionallyBad = 1
    ExtremelyBad = 2
    VeryBad = 3
    Bad = 4
    Average = 5
    Good = 6
    VeryGood = 7
    ExtremelyGood = 8
    ExceptionallyGood = 9