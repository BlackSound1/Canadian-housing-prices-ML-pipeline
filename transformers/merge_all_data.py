if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from functools import reduce

@transformer
def transform(populations_df, econ_indicators, number_of_families_df, new_housing_df,
              interest_rate_df, CPI_df, GDP_df, number_of_immigrants_df, average_housing_df, 
              *args, **kwargs):

    # Accumulate all DataFrames into 1 list
    df_list = [econ_indicators, CPI_df, GDP_df, average_housing_df, interest_rate_df, new_housing_df,
               number_of_families_df, number_of_immigrants_df, populations_df]

    # Force all Date columns to be strings, in case they aren't
    econ_indicators['Date'] = econ_indicators['Date'].astype(str)
    CPI_df['Date'] = CPI_df['Date'].astype(str)
    GDP_df['Date'] = GDP_df['Date'].astype(str)
    average_housing_df['Date'] = average_housing_df['Date'].astype(str)
    interest_rate_df['Date'] = interest_rate_df['Date'].astype(str)
    new_housing_df['Date'] = new_housing_df['Date'].astype(str)
    number_of_families_df['Date'] = number_of_families_df['Date'].astype(str)
    number_of_immigrants_df['Date'] = number_of_immigrants_df['Date'].astype(str)
    populations_df['Date'] = populations_df['Date'].astype(str)

    # Merge all DataFrames
    merged_df = reduce(lambda left, right: pd.merge(left,right,on=['Date'], how='outer'), df_list)

    return merged_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'