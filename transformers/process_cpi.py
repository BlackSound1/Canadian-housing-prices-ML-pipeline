if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import year_changer

@transformer
def transform(CPI_df, *args, **kwargs):
    
    # Change Date format from YYYY-MM-DD to YYYY-MM
    CPI_df['date'] = CPI_df['date'].apply(year_changer)

    # Take only dates between 2009 and 2019
    CPI_df['date'] = CPI_df['date'].astype(str)
    CPI_df = CPI_df[(CPI_df['date'].str[0:4].astype(int) >= 2009) &
                    (CPI_df['date'].str[0:4].astype(int) <= 2019)].reset_index().drop(columns='index')
    
    # Rename columns
    CPI_df = CPI_df.rename(columns={'date' : 'Date'})

    return CPI_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
