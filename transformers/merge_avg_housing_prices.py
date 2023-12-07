if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(average_housing_prices_df, average_housing_prices_type_df, *args, **kwargs):
    # Merge the DataFrames
    average_housing_df = pd.merge(average_housing_prices_df, average_housing_prices_type_df, on='Date')

    return average_housing_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'