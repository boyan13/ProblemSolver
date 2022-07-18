# +====================================================================================================================+
# Pythonic
from enum import Enum
from typing import Any
# +====================================================================================================================+


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
