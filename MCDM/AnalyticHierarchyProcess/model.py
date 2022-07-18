# +====================================================================================================================+
# Pythonic
import typing

# Libs
import pandas as pd

# Internal
from GUI.Utilities import pandas_utilities as pandas_utils
from MCDM.AnalyticHierarchyProcess.backends import AHPProcessor
from MCDM.AnalyticHierarchyProcess.enums import Important
from MCDM.Data.model import DataModel
# +====================================================================================================================+


class AHPModel:

    """
    Analytic Hierarchy Process model.

    3-level version:

                                      +------+
                                      | Goal |                                    LEVEL 0 (GOAL)
                                      +------+
                                         |
                                         |
                               +---------+----------+
                               |                    |
                               |                    |
                         +------------+      +------------+
                         | Criteria 1 |      | Criteria 1 |                        LEVEL 1 (CRITERIA)
                         +------------+      +------------+
                               |                   |
                               |                   |
                     +---------|---------+---------+----------+
                     |         |         |                    |
                     |         |         |                    |
                +--------------+------+--------------------+  |
                |    |                |  |                 |  |
                |    |                |  |                 |  |
        +---------------+       +---------------+       +---------------+
        | Alternative 1 |       | Alternative 1 |       | Alternative 1 |          LEVEL 2 (ALTERNATIVES)
        +---------------+       +---------------+       +---------------+

    """

    def __init__(self, data_model: DataModel, backend: typing.Union[type(AHPProcessor)] = AHPProcessor):

        self.data_model = data_model
        self.backend_class = backend
        self.importance_matrix = pd.DataFrame()

        self.logging = False
        self.consistency_threshold = 0.2

        for criteria in self.data_model.criteria:
            pandas_utils.add_col(self.importance_matrix, criteria, unfilled=Important.Equally)
            pandas_utils.add_col(self.importance_matrix, criteria, unfilled=Important.Equally)
            self.importance_matrix.at[criteria, criteria] = Important.Equally

    def set_logging(self, on_off: bool):
        self.logging = on_off

    def set_consistency_threshold(self, value: float):
        self.consistency_threshold = value

    def set_weight(self, criteria: str, other_criteria: str, value: int):
        """Set an importance weight between two criteria."""

        if criteria == other_criteria:
            raise ValueError("Cannot weight a criteria against itself.")
        if value not in Important.range():
            raise ValueError(f"{value} not in range {Important.range()}.")

        self.importance_matrix.loc[criteria, other_criteria] = Important(value)
        self.importance_matrix.loc[other_criteria, criteria] = Important(-value)

    def __repr__(self):
        return "\n" + self.data_model.goal + "\n" + self.importance_matrix.__repr__()

    def process(self):
        if self.logging:
            print(f'\n\n\n=======================================================')
            print(f'Backend: {self.backend_class.__name__}.')
            print(f'Begin processing...')
            print(f'=======================================================')

        processor = self.backend_class(self.data_model, self.importance_matrix, self.consistency_threshold)
        return processor.process(log=self.logging)
