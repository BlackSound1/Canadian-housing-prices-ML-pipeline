if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import year_changer

@transformer
def transform(interest_rate_df, *args, **kwargs):
    # Keep only Bank Rate financial market rows
    interest_rate_df = interest_rate_df[interest_rate_df['Financial market statistics'] == 'Bank rate']

    # Drop NaN
    interest_rate_df = interest_rate_df.dropna().reset_index().drop(columns='index')
    
    # Remove unnecessary columns
    interest_rate_df = interest_rate_df.drop(columns=['Financial market statistics'])

    # Rename columns
    interest_rate_df = interest_rate_df.rename(columns={"VALUE": "interest rate", "REF_DATE" : "Date"})

    # Convert Date from YYYY-MM-DD format to YYYY-MM format
    interest_rate_df['Date'] = interest_rate_df['Date'].apply(year_changer)

    # Only keep data from 2009 to 2019
    interest_rate_df = (
        interest_rate_df[
            (interest_rate_df['Date'].str[:4].astype(int) >= 2009) &
            (interest_rate_df['Date'].str[:4].astype(int) <= 2019)
        ]
    )

    # Average the interest rates for each month
    interest_rate_df = interest_rate_df.groupby(['Date']).mean().reset_index()

    # Round the interest rates to 2 decimal places
    interest_rate_df['interest rate'] = interest_rate_df['interest rate'].apply(lambda x: round(x, 2))

    return interest_rate_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'