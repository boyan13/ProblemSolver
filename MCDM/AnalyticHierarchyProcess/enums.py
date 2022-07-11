# +====================================================================================================================+
# Pythonic
from typing import Any
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
    Neutral = 5
    Good = 6
    VeryGood = 7
    ExtremelyGood = 8
    ExceptionallyGood = 9


class Important(Enum):

    Extremely = 9
    BetweenVeryStronglyAndExtremely = 8
    VeryStrongly = 7
    BetweenStronglyAndVeryStrongly = 6
    Strongly = 5
    BetweenModeratelyAndStrongly = 4
    Moderately = 3
    BetweenEquallyAndModerately = 2

    Equally = 1  # You can also pass '-1' and it will work due to the overridden _missing_() method.

    BetweenEquallyAndModeratelyNot = -2
    ModeratelyNot = -3
    BetweenModeratelyAndStronglyNot = -4
    StronglyNot = -5
    BetweenStronglyAndVeryStronglyNot = -6
    VeryStronglyNot = -7
    BetweenVeryStronglyAndExtremelyNot = -8
    ExtremelyNot = -9

    def __str__(self):
        if self.value > 0:
            return str(self.value)
        else:
            return str(f"1/{abs(self.value)}")

    @property
    def numeric(self):
        if self.value >= 0:
            return float(self.value)
        else:
            return 1 / abs(float(self.value))

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if type(value) is int and value == -1:  # treat '-1' as '1'
            return Important.Equally
        else:
            return super()._missing_(value)

    @classmethod
    def range(cls):
        values = [e.value for e in cls]
        return range(min(values), max(values) + 1)
