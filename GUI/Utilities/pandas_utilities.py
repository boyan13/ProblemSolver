# +====================================================================================================================+
# Pythonic
import copy
from contextlib import contextmanager

# Libs
import pandas as pd
# +====================================================================================================================+


@contextmanager
def no_truncating():
    """Prevent pandas printing from truncating the output if it is too large, by temporarily disabling some
    restrictions."""

    max_rows = pd.get_option('display.max_rows')
    max_cols = pd.get_option('display.max_columns')
    width = pd.get_option('display.width')

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    try:
        yield

    finally:
        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', max_cols)
        pd.set_option('display.width', width)


def add_row(df, name, values=None):
    """Add a new row to the DataFrame's index and rename it."""

    df.loc[len(df.index)] = values
    df.rename({len(df.index) - 1: name}, axis='index', inplace=True)


def add_col(df, name, values=None, unfilled=None):
    """Add a column to the DataFrame. If the values are less than the index length, fill the unfilled fields with
    whatever is passed to 'fill_with'."""

    v = copy.copy(values)
    unfilled_count = len(df.index) - len(v)
    v += [unfilled] * unfilled_count
    df[name] = v
