if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import see_redundant

@transformer
def transform(new_housing_df, *args, **kwargs):
    # Keep only Canada-wide data
    new_housing_df = new_housing_df[new_housing_df['GEO'] == 'Canada'].reset_index().drop(columns='index')

    # Keep only Total price indexes
    new_housing_df = (
        new_housing_df[new_housing_df['New housing price indexes'] == 'Total (house and land)']
        .reset_index()
        .drop(columns='index')
    )

    # Check unnecesary columns
    # print("Redundant columns:")
    # see_redundant(new_housing_df)

    # Drop unnecessary columns
    new_housing_df = (
        new_housing_df
        .drop(columns=['DGUID', 'UOM', 'UOM_ID', 'VECTOR', 'SCALAR_FACTOR', 'SCALAR_ID', 'COORDINATE',
                       'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS', 'GEO', 'New housing price indexes'])
        .reset_index()
        .drop(columns='index')
    )

    # Rename columns
    new_housing_df = new_housing_df.rename(columns= {'REF_DATE' : 'Date', "VALUE": "Housing index"})

    # Keep only data between 2009 and 2019
    new_housing_df = (
        new_housing_df[
            (new_housing_df['Date'].str[:4].astype(int) >= 2009) &
            (new_housing_df['Date'].str[:4].astype(int) <= 2019)
        ]
        .reset_index()
        .drop(columns='index')
    )

    return new_housing_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'