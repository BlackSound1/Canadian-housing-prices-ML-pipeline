if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from utilities import see_redundant, diff_cal, value_adder, month_adder

@transformer
def transform(populations_df, *args, **kwargs):
    # Keep only rows where GEO=Canada and Sex=Both sexes and Age group=All ages
    populations_df = (
        populations_df[
            (populations_df['GEO'] == 'Canada') &
            (populations_df['Sex'] == 'Both sexes') &
            (populations_df['Age group'] == 'All ages')
            ]
        .reset_index()
        .drop(columns='index')
    )

    # Check redundant columns
    # print("Redundant columns:")
    # see_redundant(populations_df)
    # print()

    # Remove redundant columns
    populations_df = populations_df.drop(columns=['GEO', 'DGUID', 'Sex', 'Age group', 'UOM', 'UOM_ID', 
                                                  'SCALAR_FACTOR', 'SCALAR_ID', 'VECTOR', 'COORDINATE',
                                                  'STATUS', 'SYMBOL', 'TERMINATED', 'DECIMALS'])

    # Remove unnecessary years. Keep from 2008 to allow for filling in synthetic data for months
    populations_df = (
        populations_df[
            (populations_df['REF_DATE'].astype(int) >= 2008) &
            (populations_df['REF_DATE'].astype(int) <= 2019)
            ]
        .reset_index()
        .drop(columns='index')
    )

    # Rename colunms
    populations_df = populations_df.rename(columns= {'REF_DATE' : 'Date', "VALUE": "Population"})

    # Get list of differences between entries in the "Population" column for generating synthetic data
    diff_list = diff_cal(populations_df['Population'])

    # Smooth out data in "Population" column to get synthetic monthly data
    populations_df['Population'] = populations_df['Population'].apply(value_adder, diff_list=diff_list)

    # Remove last row
    populations_df = populations_df.drop(index=11)

    # Transform Dates from YYYY format to YYYY-MM format
    populations_df['Date'] = populations_df['Date'].apply(month_adder, add_1=True)

    # Explode the "Date" and "Population" list-columns into individual rows
    populations_df = populations_df.explode(['Date', 'Population']).reset_index().drop(columns='index')

    populations_df['Population'] = populations_df['Population'].astype(int)

    return populations_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'