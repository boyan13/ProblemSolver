# +====================================================================================================================+
# Pythonic
import math

# Internal
from GUI.Utilities import pandas_utilities as pandas_utils
from GUI.Utilities import python_utilities as py_utils
from MCDM.AnalyticHierarchyProcess.exceptions import AHPException
from MCDM.Data.enums import DataGoal
from MCDM.Data.model import DataModel
from MCDM.Data.types import *
# +====================================================================================================================+


class AHPProcessor:
    def __init__(self, data_mode: DataModel, importance_matrix: pd.DataFrame, consistency_threshold=0.1):

        if not len(data_mode.criteria) < self.criteria_limit:
            raise AHPException(f"The AHP model works with up to {self.criteria_limit} criteria.")

        self.data_model = data_mode
        self.importance_matrix = importance_matrix

        self.consistency_threshold = consistency_threshold

        self.storage = {
            'criteria': {
                'matrices': {'pairwise': None, 'normalized': None},
                'vectors': {'sum': None, 'priority': None},
                'values': {'lambda_max': None, 'ci': None, 'cr': None, 'cr': None}
            },
            'alternatives': {
                criteria: {
                    'matrices': {'pairwise': None, 'normalized': None},
                    'vectors': {'sum': None, 'priority': None},
                    'values': {'lambda_max': None, 'ci': None, 'cr': None, 'cr': None}
                } for criteria in self.data_model.criteria}
        }

    def get_criteria_matrices_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['criteria']['matrices'][k] for k in keys]}

    def get_criteria_vectors_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['criteria']['vectors'][k] for k in keys]}

    def get_criteria_values_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['criteria']['values'][k] for k in keys]}

    def get_alternatives_matrices_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['alternatives']['matrices'][k] for k in keys]}

    def get_alternatives_vectors_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['alternatives']['vectors'][k] for k in keys]}

    def get_alternatives_values_as_dict(self, *keys):
        return {k: v for k, v in [self.storage['alternatives']['values'][k] for k in keys]}

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Properties
    #
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def criteria_limit(self):
        return len(self.saaty_random_index_table())

    @staticmethod
    def saaty_random_index_table():
        """The table of random consistency indices for each reciprocal (pairwise) matrix size."""
        return {
            1: 0,          2: 0,          3: 0.52,          4: 0.89,          5: 1.11,
            6: 1.25,       7: 1.35,       8: 1.40,          9: 1.45,         10: 1.49,
            11: 1.51,     12: 1.54,      13: 1.56,         14: 1.57,         15: 1.58
        }

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Processing
    #
    # ------------------------------------------------------------------------------------------------------------------

    def _build_alternatives_pairwise_matrix_from_values(self, criteria: str):
        df = pd.DataFrame()

        alternative_pairs = self.data_model.get_minimum_pairs(of_criteria=False)

        for alternative in self.data_model.alternatives:
            pandas_utils.add_col(df, alternative)
            pandas_utils.add_row(df, alternative)
            df.at[alternative, alternative] = 1.0

        for alternative1, alternative2 in alternative_pairs:
            value1 = self.data_model.get_value(criteria, alternative1)
            value2 = self.data_model.get_value(criteria, alternative2)

            value1 = 0.00000001 if value1 == 0 else value1
            value2 = 0.00000001 if value2 == 0 else value2

            df.at[alternative1, alternative2] = value1 / value2
            df.at[alternative2, alternative1] = value2 / value1

        return Pd_DataFrameMatrix('Pairwise matrix', df)

    def process(self, log=False):

        # Will eventually replace floats with something more precise.

        # Shortcuts

        cmat = self.storage['criteria']['matrices']
        cvec = self.storage['criteria']['vectors']
        cval = self.storage['criteria']['values']

        # ----------------------------------------------------------------------------------------------------
        # Log the initial state
        if log:
            self._log(Pd_DataFrameMatrix('Importance matrix', self.importance_matrix))
        # ----------------------------------------------------------------------------------------------------

        # Parse the Importance matrix into the decimal Pairwise Criteria matrix.
        cmat['pairwise'] = self.compute__parse_importance_matrix(self.importance_matrix)

        # ----------------------------------------------------------------------------------------------------
        # Log the pairwise matrix
        if log:
            self._log(cmat['pairwise'])
        # ----------------------------------------------------------------------------------------------------

        # Normalize the pairwise criteria matrix.
        cmat['normalized'], cvec['sum'] = self.compute__normalized_pairwise_matrix(cmat['pairwise'])

        # ----------------------------------------------------------------------------------------------------
        # Log the normalized pairwise matrix with the column sums
        if log:
            self._log(cmat['normalized'], extra_rows=py_utils.get_multiple(cvec, 'sum'))
        # ----------------------------------------------------------------------------------------------------

        # Compute the priority vector
        cvec['priority'] = self.compute__priority_vector(cmat['normalized'])

        # ----------------------------------------------------------------------------------------------------
        # Log the pairwise matrix with the priority vector
        if log:
            self._log(cmat['pairwise'], extra_cols=py_utils.get_multiple(cvec, 'priority'))
        # ----------------------------------------------------------------------------------------------------

        # If criterion A is preferred over criterion B (A > B), and criterion B is preferred over criterion C
        # (B > C), then by the transitive property we should conclude that criterion A is preferred over criterion C
        # (A > C). If this is not actually the case, then the weights of the criteria are set inconsistently.
        #
        # In order to detect inconsistencies in the judgement of criteria, we will calculate Saaty's Consistency
        # Ratio: CR = CI / RI, where CI is Saaty's Consistency Index and RI is Saaty's Random Consistency Index.

        cval['lambda_max'] = self.compute__eigen_value(cmat['pairwise'], cvec['priority'])

        # ----------------------------------------------------------------------------------------------------
        # Log the eigenvalue lambda_max
        if log:
            self._log(caption='Eigen value', extra_values=py_utils.get_multiple(cval, 'lambda_max'))
        # ----------------------------------------------------------------------------------------------------

        # Check if consistency is below the 10% threshold set by Saaty. To do that we need to compute Saaty's
        # consistency ratio CR = CI / RI, where CI is the consistency index and RI is the random consistency index.
        # The consistency index is obtained from Saaty's formula: CI = (lambda_max - n) / (n - 1), where lambda_max
        # is the principal eigen value and n is the dimension of the reciprocal matrix.

        cval['ci'], cval['ri'], cval['cr'] = self.compute__consistency_data(
            cval['lambda_max'], len(self.data_model.criteria)
        )

        # ----------------------------------------------------------------------------------------------------
        # Log the consistency values
        if log:
            self._log(
                caption='Consistency data', extra_values=py_utils.get_multiple(cval, 'lambda_max', 'ci', 'ri', 'cr'))
        # ----------------------------------------------------------------------------------------------------

        if not cval['cr'].value < self.consistency_threshold:
            raise AHPException(
                "Pairwise matrix is not consistent. CR={0} ({0:.0%})".format(cval['cr'].value) +
                ", which violates the maximum threshold of {0:.0%}.".format(self.consistency_threshold)
            )

        #
        # Alternatives
        #

        # This part is not ideal, I should refactor.

        alternatives_matrix = pd.DataFrame()
        best_values = {c: None for c in self.data_model.criteria}

        # Build alternatives matrix and find the best value among each criterion
        for criterion in self.data_model.criteria:
            pandas_utils.add_col(alternatives_matrix, criterion)  # Add criterion as column
            criterion_goal = self.data_model.criteria[criterion].goal  # Get the goal (min/max) for the criterion

            for alternative in self.data_model.alternatives:
                pandas_utils.add_row(alternatives_matrix, alternative)  # Add alternative as row

                # Get the value of the alternative for the criterion
                value = self.data_model.get_value(criterion, alternative)

                # Search for best value among alternatives (largest if maximizing, smallest is minimizing)
                if best_values[criterion] is None:
                    best_values[criterion] = value
                elif criterion_goal is DataGoal.Maximize and best_values[criterion] < value:
                    best_values[criterion] = value
                elif criterion_goal is DataGoal.Minimize and best_values[criterion] > value:
                    best_values[criterion] = value

        # Normalize alternatives matrix
        for criterion in self.data_model.criteria:
            best = best_values[criterion]
            for alternative in self.data_model.alternatives:

                value = self.data_model.get_value(criterion, alternative)

                if self.data_model.criteria[criterion].goal is DataGoal.Minimize:
                    normalized_value = best / value
                else:
                    normalized_value = value / best

                alternatives_matrix.at[alternative, criterion] = normalized_value

        # The alternatives and their ranks
        rankings = {}

        # map each criterion to its weight
        weights = {c: w for c, w in zip(self.data_model.criteria, cvec['priority'].value)}

        # Perform ranking
        for alternative in alternatives_matrix.index:
            alternative_ranking = 0

            for criterion in alternatives_matrix.columns:
                alternative_ranking += alternatives_matrix.at[alternative, criterion] * weights[criterion]

            rankings[alternative] = alternative_ranking

        # ----------------------------------------------------------------------------------------------------
        if log:
            self._log(Pd_DataFrameMatrix('Alternatives normalized matrix', alternatives_matrix), caption='Ranking',
                      extra_rows=py_utils.get_multiple(cvec, 'priority'),
                      extra_values=[Python_NumericValue('Ranking: ' + k, v) for k, v in rankings.items()])
        # ----------------------------------------------------------------------------------------------------

        return rankings

        # for criteria in self.data_model.criteria:
        #
        #     # Shortcuts
        #     amat = self.storage['alternatives'][criteria]['matrices']
        #     avec = self.storage['alternatives'][criteria]['vectors']
        #     aval = self.storage['alternatives'][criteria]['values']
        #
        #     amat['pairwise'] = self._build_alternatives_pairwise_matrix_from_values(criteria)
        #     amat['normalized'], avec['sum'] = self.compute__normalized_pairwise_matrix(amat['pairwise'])
        #     avec['priority'] = self.compute__priority_vector(amat['normalized'])
        #     aval['lambda_max'] = self.compute__eigen_value(amat['pairwise'], avec['priority'])
        #     aval['ci'], aval['ri'], aval['cr'] = self.compute__consistency_data(
        #         aval['lambda_max'], len(self.data_model.alternatives)
        #     )
        #
        #     # ----------------------------------------------------------------------------------------------------
        #     if log:
        #         self._log(amat['pairwise'], comment=criteria,
        #                   extra_cols=py_utils.get_multiple(avec, 'priority'),
        #                   extra_values=py_utils.get_multiple(aval, 'lambda_max', 'ci', 'ri', 'cr'))
        #     # ----------------------------------------------------------------------------------------------------
        #
        # eigenvalue_matrix = pd.DataFrame()
        #
        # for criteria in self.importance_matrix.index:
        #     pandas_utils.add_col(eigenvalue_matrix, criteria)
        #
        # for alternative in self.data_model.alternatives.values():
        #     pandas_utils.add_row(eigenvalue_matrix, alternative.name)
        #
        # for criteria in self.importance_matrix.index:
        #     priority_vector = self.storage['alternatives'][criteria]['vectors']['priority']
        #     pandas_utils.add_col(eigenvalue_matrix, criteria, priority_vector.value)
        #
        # # ----------------------------------------------------------------------------------------------------
        # if log:
        #     self._log(Pd_DataFrameMatrix('Eigenvalue matrix', eigenvalue_matrix),
        #               extra_rows=py_utils.get_multiple(cvec, 'priority'))
        # # ----------------------------------------------------------------------------------------------------
        #
        # ranking = {}
        #
        # for alternative in self.data_model.alternatives.values():
        #     row = eigenvalue_matrix.loc[alternative.name]
        #     ranking[alternative.name] = 0
        #
        #     for criterion, weight in zip(self.importance_matrix.index, cvec['priority'].value):
        #         value = row[criterion]
        #         weighted = value * weight
        #
        #         if self.data_model.criteria[criterion].goal is DataGoal.Maximize:
        #             ranking[alternative.name] += weighted
        #         else:
        #             ranking[alternative.name] -= weighted
        #
        # # ----------------------------------------------------------------------------------------------------
        # if log:
        #     to_log = [Python_NumericValue(name, float(score)) for name, score in ranking.items()]
        #     self._log(caption='Ranking', extra_values=to_log)
        # # ----------------------------------------------------------------------------------------------------
        #
        # return ranking

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Static Computational Blocks
    #
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def compute__parse_importance_matrix(importance_matrix: pd.DataFrame):
        df = pd.DataFrame.copy(importance_matrix)
        for row in df.index:
            for col in df.columns:
                df.loc[row, col] = df.loc[row, col].numeric

        return Pd_DataFrameMatrix('Pairwise matrix', df)

    @staticmethod
    def compute__normalized_pairwise_matrix(pairwise_matrix: Pd_DataFrameMatrix):
        df = pd.DataFrame.copy(pairwise_matrix.value)

        columns_summed = [sum(df[col]) for col in df.index]

        for row in df.index:
            for j, col in enumerate(df.columns):
                df.loc[row, col] /= columns_summed[j]

        return Pd_DataFrameMatrix('Normalized pairwise matrix', df), Python_ListVector('Sum', columns_summed)

    @staticmethod
    def compute__priority_vector(normalized_pairwise_matrix: Pd_DataFrameMatrix):
        """Obtain the normalized principal eigenvector (priority vector) of a pairwise matrix by averaging across each
        row."""

        df = pd.DataFrame.copy(normalized_pairwise_matrix.value)

        priority_vector = []
        for row in df.index:
            row_sum = sum([df.loc[row, col] for col in df.columns])
            priority_vector.append(row_sum / len(df.index))

        return Python_ListVector('Priority', priority_vector)

    @staticmethod
    def compute__eigen_value(pairwise_matrix: Pd_DataFrameMatrix, priority_vector: Python_ListVector):
        """
            There are different ways to compute the principal eigenvalue for a given pairwise matrix. We are computing
            it using the direct formula:

                            sum (WEIGHTED_PRIORITY_VECTOR / PRIORITY_VECTOR)
            lambda_max =    ------------------------------------------------   ,      where
                                    PAIRWISE_MATRIX_DIMENSION

            * WEIGHTED_PRIORITY_VECTOR = PAIRWISE_MATRIX * PRIORITY_VECTOR
        """

        df = pd.DataFrame.copy(pairwise_matrix.value)
        priorities = priority_vector.value

        #
        # Part 1: Calculate the weighted priority vector
        #

        weighted_priority_vector = []

        for row in df.index:  # for each row
            weighted_row_elements = []  # weight and gather the row elements here

            for j, col in enumerate(df.columns):  # for each column
                priority = priorities[j]  # get the priority for that column
                node = df.loc[row, col]  # get the row element
                df.at[
                    row, col] = node * priority  # multiply the element by the priority and set the node's new value
                weighted_row_elements.append(df.at[row, col])  # store the result for later summation

            summed = sum(weighted_row_elements)  # sum the weighted row elements

            # Corner case weirdness because I'm using floats.
            # The idea is if I get 3.9999999... turn it into 4, or I get negative consistency indices down the road.
            if summed + 0.000000001 >= math.ceil(summed):
                summed = math.ceil(summed)

            weighted_priority_vector.append(summed)  # finally, store the sum

        #
        # Part 2: Calculate the principal eigen value lambda_max
        #

        sums_over_priorities = [s / p for s, p in zip(weighted_priority_vector, priorities)]
        eigen_value = sum(sums_over_priorities) / len(df.index)

        return Python_NumericValue('Lambda Max', eigen_value)

    @staticmethod
    def compute__consistency_data(lambda_max: Python_NumericValue, pairwise_matrix_dimension: int):
        lmax = lambda_max.value
        n = pairwise_matrix_dimension
        if n != 1:
            ci = (lmax - n) / (n - 1)
        else:
            ci = 0
        ri = AHPProcessor.saaty_random_index_table()[n]
        cr = ci / ri if ri > 0 else 0

        CI = Python_NumericValue('Consistency Index (CI)', ci)
        RI = Python_NumericValue('Random Consistency Index (RI)', ri)
        CR = Python_NumericValue('Consistency Ratio (CR)', cr)

        return CI, RI, CR

    # ------------------------------------------------------------------------------------------------------------------
    #
    # Logging
    #
    # ------------------------------------------------------------------------------------------------------------------

    def _log(
            self,
            data_frame: TitledResult = None,  # The data frame that will be printed.
            comment: str = None,  # Add clarification or something noteworthy.
            caption: str = None,  # Information about what we are logging / showing.

            # Extra rows to be added to the data frame before it is printed.
            extra_rows: typing.Union[typing.List[Python_NumericValue], typing.Tuple[Python_NumericValue]] = None,

            # Extra columns to be added to the data frame before it is printed.
            extra_cols: typing.Union[typing.List[Python_ListVector], typing.Tuple[Python_ListVector]] = None,

            # Key-value pairs to also be logged.
            extra_values: typing.Union[typing.List[Python_NumericValue], typing.Tuple[Python_NumericValue]] = None
    ):

        df = pd.DataFrame.copy(data_frame.value) if data_frame is not None else None

        if extra_rows is not None:
            for row in extra_rows:
                pandas_utils.add_row(df, row.name, row.value)

        if extra_cols is not None:
            for col in extra_cols:
                pandas_utils.add_col(df, col.name, col.value)

        margin = '\n\n\n'
        func = py_utils.current_function(go_back=2) + "()"
        func += f" [{data_frame.name}]" if data_frame is not None else ""
        comment = f'({comment})' if comment is not None else None
        caption = f'Caption: {caption}' if caption is not None else None

        print(margin)
        print(func)
        print(comment) if comment is not None else None
        print(caption) if caption is not None else None
        print()
        print(df) if df is not None else None
        print() if df is not None else None
        if extra_values is not None:
            print("{0:30} {1:10} {2}".format('KEYS', ' ', 'VALUES'))
            for result in extra_values:
                if type(result.value) not in {int, float, str, list, dict, tuple}:
                    v = type(result.value)
                else:
                    v = result.value
                print("{0:30} {1:10} {2}".format(result.name, '-', v))
        print(margin)
