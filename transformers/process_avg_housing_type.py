if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(average_housing_prices_type_df, *args, **kwargs):

    # Remove unneeded columns
    average_housing_prices_type_df = average_housing_prices_type_df.drop(columns=['Composite'])

    return average_housing_prices_type_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'