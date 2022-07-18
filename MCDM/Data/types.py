# +====================================================================================================================+
# Pythonic
import typing

# Libs
import pandas as pd
# +====================================================================================================================+


class TitledResult:

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Pd_DataFrameMatrix(TitledResult):

    def __init__(self, name: str, value: pd.DataFrame):
        super().__init__(name, value)


class Python_ListVector(TitledResult):

    def __init__(self, name: str, value: typing.Union[list, tuple]):
        super().__init__(name, value)


class Python_NumericValue(TitledResult):

    def __init__(self, name: str, value: typing.Union[float, int]):
        super().__init__(name, value)
