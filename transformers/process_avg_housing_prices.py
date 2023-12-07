if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


@transformer
def transform(average_housing_prices_df, *args, **kwargs):
    # Drop unneeded columns
    average_housing_prices_df = average_housing_prices_df.iloc[:, [0, 1]]

    return average_housing_prices_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
