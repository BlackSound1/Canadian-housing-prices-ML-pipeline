if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import see_redundant

@transformer
def transform(GDP_df, *args, **kwargs):
    # Keeping only data such that the NAICS data refers to all industries
    GDP_df = (
        GDP_df[GDP_df['North American Industry Classification System (NAICS)'] == 'All industries [T001]']
        .reset_index()
        .drop(columns=['index'])
        )

    # Check redundant columns
    # see_redundant(GDP_df)

    # Remove redundant columns
    GDP_df = GDP_df.drop(columns=['GEO', 'DGUID', 'North American Industry Classification System (NAICS)',
                                  'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID', 'STATUS', 'SYMBOL',
                                  'TERMINATED', 'DECIMALS', 'VECTOR', 'COORDINATE'])
    
    # Rename columns
    GDP_df = GDP_df.rename(columns={'VALUE': 'GDP (millions 2012 Constant Price)', 'REF_DATE' : 'Date'})

    # Since housing data is seasonally-adjusted, we keep only seasonally adjusted data at annual rates
    GDP_df = (
        GDP_df[GDP_df['Seasonal adjustment'] == 'Seasonally adjusted at annual rates']
        .reset_index()
        .drop(columns='index')
        )
    
    # Since there is no significant difference between 'Chained (2012) dollars' and '2012 constant prices',
    # we arbitrarily kept '2012 constant prices'
    GDP_df = GDP_df[GDP_df['Prices'] == '2012 constant prices'].reset_index().drop(columns='index')

    # Drop now-redundant columns
    GDP_df = GDP_df.drop(columns=['Seasonal adjustment', 'Prices'])

    # Keep only data between 2009 and 2019
    GDP_df = (
        GDP_df[
            (GDP_df['Date'].str[:4].astype(int) >= 2009) &
            (GDP_df['Date'].str[:4].astype(int) <= 2019)
            ]
        .reset_index()
        .drop(columns='index')
    )

    return GDP_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
