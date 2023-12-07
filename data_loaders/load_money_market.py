from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@data_loader
def load_data_from_file(*args, **kwargs):
    filepath = f"{kwargs['FILES_LOCATION']}/money_market.csv"

    df = pd.read_csv(filepath)

    # Get unique values for Financial market statistics
    print('Unique values for "Financial market statistics":')
    display(df['Financial market statistics'].unique())

    print()

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
