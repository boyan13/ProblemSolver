# +====================================================================================================================+
# Pythonic
from itertools import combinations
from functools import cached_property

# Libs
import pandas as pd

# Internal
from MCDM.AnalyticHierarchyProcess.enums import *
from MCDM.AnalyticHierarchyProcess.criteria import AHPCriteria
from GUI.Utilities import pandas_utilities as pandas_utils
from GUI.Utilities import python_utilities as py_utils
# +====================================================================================================================+


class AHPException(Exception):
    pass


class AHPDataFrameModel:
    """A structure that holds a dataframe and some intermediary results. This just establishes some API for the way
    we store additional data associated with the data frame, like results of row/column operations."""

    def __init__(
            self,
            name: str,
            values: dict = None,
            data_frame: pd.DataFrame = None,
            row_results: dict = None,
            col_results: dict = None
    ):
        self.__name = name  # Name, mostly useful for printing
        self.data_frame = data_frame  # The data frame itself
        self.values = values if values is not None else {}  # Some values we associate with this dataframe

        # These are important results, but we do not want to append them directly as rows/cols of the dataframe,
        # so we store them 'externally' instead.

        self.row_results = row_results if row_results is not None else {}  # Row results (for example each column's sum)
        self.col_results = col_results if col_results is not None else {}  # Column results (for example each row's sum)

    @property
    def name(self):
        return self.__name


class AHPModel:

    """Analytic Hierarchy Process model."""

    def __init__(self, goal: str):
        self.goal = goal
        self.criteria = {}
        self.data_frame = pd.DataFrame()

        self._max_criteria = len(self.saaty_random_index_table)

    #
    # Properties
    #

    @cached_property
    def saaty_random_index_table(self):

        """The table of random consistency indices for each reciprocal (pairwise) matrix size."""

        return {
            1: 0,
            2: 0,
            3: 0.52,
            4: 0.89,
            5: 1.11,
            6: 1.25,
            7: 1.35,
            8: 1.40,
            9: 1.45,
            10: 1.49,
            11: 1.51,
            12: 1.54,
            13: 1.56,
            14: 1.57,
            15: 1.58
        }

    #
    #
    #
    # Logging
    #
    #
    #

    def _log_processing(self, dfm: AHPDataFrameModel, header="", use_this_df_instead: pd.DataFrame = None):

        df_ = pd.DataFrame.copy(dfm.data_frame if use_this_df_instead is None else use_this_df_instead)

        for row_name, row in dfm.row_results.items():
            pandas_utils.add_row(df_, row_name, row)

        for col_name, col in dfm.col_results.items():
            pandas_utils.add_col(df_, col_name, col)

        data_frame_info = f"(DataFrame - {dfm.name})"
        data_frame_info += "[Overridden]" if use_this_df_instead is not None else ""
        data_frame_info += '\n'

        print('\n\n\n')
        print(header)
        print(data_frame_info)
        print(df_)
        print()
        if len(dfm.values) > 0:
            print("{0:30} {1:10} {2}".format('KEYS', ' ', 'VALUES'))
            for k, v in dfm.values.items():
                if type(v) not in {int, float, str, list, dict, tuple}:
                    v = type(v)
                print("{0:30} {1:10} {2}".format(k, '-', v))
        print('\n\n\n')

    #
    #
    #
    # Python Dunders
    #
    #
    #

    def __repr__(self):

        return "\n" + self.goal + "\n\n" + self.data_frame.__repr__()

    #
    #
    #
    # API - Getting
    #
    #
    #

    def goal(self, name: str):
        return self.criteria[name].goal

    def data_type(self, name: str):
        return self.criteria[name].data_type

    def position(self, name: str):
        return self.criteria[name].position

    def get_criteria_names(self):
        return list(self.criteria.keys())

    def get_pairwise(self):
        """Get all criteria pairs."""
        pairwise_combinations = list(combinations(self.get_criteria_names(), 2))
        return pairwise_combinations

    #
    #
    #
    # API - Logic
    #
    #
    #

    def add_criteria(self, name: str, data_type: str, goal: str):

        if len(self.criteria) == self._max_criteria:
            raise AHPException(f"The AHP model works with up to {self._max_criteria} criteria.")

        position_ = len(self.criteria)
        name_ = name
        data_type_ = DataType.from_string(data_type)
        goal_ = DataGoal.from_string(goal)

        criteria = AHPCriteria(position_, name_, data_type_, goal_)
        self.criteria[criteria.name] = criteria

        # Add criteria column
        self.data_frame[criteria.name] = Important.Equally
        # Add criteria row
        self.data_frame.loc[len(self.data_frame.index)] = Important.Equally
        # Change the row name to the criteria name instead of the default indexing number
        self.data_frame.rename({len(self.data_frame.index) - 1: criteria.name}, axis='index', inplace=True)

    def set_weight(self, criteria: str, other_criteria: str, value: int):
        """Set pairwise comparison weight between two criteria."""
        if criteria == other_criteria:
            raise ValueError("Cannot weight a criteria against itself.")
        if value not in Important.range():
            raise ValueError(f"{value} not in range {Important.range()}.")

        self.data_frame.loc[criteria][other_criteria] = Important(value)
        self.data_frame.loc[other_criteria][criteria] = Important(-value)

    #
    #
    #
    # API - Execute
    #
    #
    #

    def process(self, log=False):

        # Dev note: Using pandas DataFrame instead of numpy ndarrays is definitely not the most optimal way to
        # implement this, especially considering that DataFrames are not meant to be used as matrices. However,
        # DataFrame makes it easy to visualize and neatly document the process. In the future I can implement
        # additional backends to process this more efficiently.

        # Since this process is quite complex, I've split the procedure into multiple inner functions prefixed by
        # '_processing'. This makes it easier to read (allows for more extensive documentation and declarative-style
        # coding), log (we can access the function's name to log the current step instead of hard-coding strings)
        # and debug (the stack trace would print the inner function in which a problem has occurred, which carries
        # semantic meaning).

        # >
        # >
        # >

        def _process_get_pairwise_matrix():
            # Parse all enum weights into their respective numeric values.

            for row in self.criteria:
                for col in self.criteria:
                    df.loc[row][col] = df.loc[row][col].numeric

            pairwise.data_frame = pd.DataFrame.copy(df)
            self._log_processing(pairwise, py_utils.current_function()) if log else None

        # >
        # >
        # >

        def _process_sum_columns():
            # Sum each column. We do this in order to later normalize the nodes.

            pairwise.row_results['Sum'] = [sum(df[col]) for col in self.criteria]  # Sum each column
            self._log_processing(pairwise, py_utils.current_function()) if log else None

        # >
        # >
        # >

        def _process_normalize_pairwise_matrix():
            # Divide each element by its column's sum, in order to normalize the pairwise matrix.

            for row in self.criteria:
                for i, col in enumerate(self.criteria):
                    df.loc[row][col] /= pairwise.row_results['Sum'][i]

            normalized_pairwise.data_frame = pd.DataFrame.copy(df)
            self._log_processing(normalized_pairwise, py_utils.current_function()) if log else None

        # >
        # >
        # >

        def _process_compute_priority_vector():
            # Obtain the normalized principal eigenvector (priority vector) by averaging across each row.

            priorities = []
            for row in self.criteria:
                summed = sum([df.loc[row][col] for col in self.criteria])
                priorities.append(summed / len(self.criteria))

            normalized_pairwise.col_results['Priority'] = priorities
            self._log_processing(normalized_pairwise, py_utils.current_function()) if log else None

        # >
        # >
        # >

        def _process_compute_principal_eigen_value():
            """If criterion A is preferred over criterion B (A > B), and criterion B is preferred over criterion C
            (B > C), then by the transitive property we should conclude that criterion A is preferred over criterion C
            (A > C). If this is not actually the case, then the weights of the criteria are set inconsistently.
            
            In order to detect inconsistencies in the judgement of criteria, we will calculate Saaty's Consistency
            Ratio: CR = CI / RI, where CI is Saaty's Consistency Index and RI is Saaty's Random Consistency Index.

            Using the principal eigen (priority) vector, we find the principal eigen value lambda_max, which is needed
            to compute the consistency index.

            lambda_max = sum ( (PAIRWISE_MATRIX * PRIORITY_VECTOR) / WEIGHTED_SUM_VECTOR ) / PAIRWISE_MATRIX_SIZE
            """

            df = pd.DataFrame.copy(pairwise.data_frame)

            priorities = normalized_pairwise.col_results['Priority']

            for j, col in enumerate(self.criteria):
                priority = priorities[j]
                for row in self.criteria:
                    node = df.loc[row].at[col]
                    df.at[row, col] = node * priority

            sums = []

            for row in self.criteria:
                sums.append(sum([df.at[row, col] for col in self.criteria]))
            pairwise.col_results['Weighted Sum'] = sums

            eigen_value = sum( [sm / pr for sm, pr in zip(sums, priorities)] ) / len(self.criteria)
            values['eigen_value'] = eigen_value

            self._log_processing(pairwise, py_utils.current_function(), df) if log else None

        # >
        # >
        # >

        def _process_compute_consistency_index():
            """The consistency index is obtained by Saaty's formula: CI = (lambda_max - n) / (n - 1), where lambda_max
            is the principal eigen value and n is the dimension of the reciprocal matrix."""

            lambda_max = values['eigen_value']
            n = len(self.criteria)
            ci = (lambda_max - n) / (n - 1)
            values['CI'] = ci

            self._log_processing(pairwise, py_utils.current_function(), df) if log else None

        # >
        # >
        # >

        def _process_compute_consistency_ratio():
            """The consistency ratio is obtained by the formula CR = CI / RI."""

            ci = values['CI']
            ri = self.saaty_random_index_table[len(self.criteria)]
            cr = ci / ri
            values['CR'] = cr

            self._log_processing(pairwise, py_utils.current_function(), df) if log else None

        # >
        # >
        # >

        def _process_check_consistency():
            """Check if consistency is below the 10% threshold set by Saaty."""

            cr = values['CR']
            if not cr < 0.10:
                raise AHPException(
                    "Judgement matrix is not consistent. Calculated {0:.0%}".format(cr) +
                    " consistency ratio (must be < 10%)."
                )

        # >
        # >
        # >
        # >
        # >
        # >

        with pandas_utils.no_truncating():

            # Preparation

            df = pd.DataFrame.copy(self.data_frame)
            values = {}

            pairwise = AHPDataFrameModel('Pairwise matrix', values)
            normalized_pairwise = AHPDataFrameModel('Normalized pairwise matrix', values)
            
            # Procedure

            self._log_processing(pairwise, py_utils.current_function(), df) if log else None
            
            _process_get_pairwise_matrix()
            _process_sum_columns()
            _process_normalize_pairwise_matrix()
            _process_compute_priority_vector()
            _process_compute_principal_eigen_value()
            _process_compute_consistency_index()
            _process_compute_consistency_ratio()
            _process_check_consistency()
