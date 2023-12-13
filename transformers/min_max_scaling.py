if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


def min_max(col: pd.Series) -> pd.Series:
    """
    Perform min-max scaling on a column of a DataFrame

    :param col: The column to perform min-max scaling on
    :return: The pd.Series of the updated column data
    """

    # Get the minimum and maximum values for the column
    min_ = col.min()
    max_ = col.max()

    # Create a list of values to create the new pd.Series from
    vals = []

    # For each of the values in the column, compute the min-max scaled new value and add it to the
    # list of values to create the pd.Series with
    for v in col.values:
        new_v = (v - min_) / (max_ - min_)
        vals.append(new_v)

    # Create the new pd.Series based on this new data
    series = pd.Series(data=vals, dtype=float, name=col.name)

    return series


@transformer
def transform(merged_df_copy, *args, **kwargs):
    cols_to_ignore = ['Date', 'GDP (millions 2012 Constant Price)', 'Average price', 'One storey price', 'Two storey price',
                      'Townhouse price', 'Apartment price', 'Number of families', 'Number of immigrants', 'Population']
    
    # For each of the columns, min_max scale their values
    for c in [i for i in merged_df_copy.columns if i not in cols_to_ignore]:
        merged_df_copy[c] = min_max(merged_df_copy[c])

    return merged_df_copy


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'