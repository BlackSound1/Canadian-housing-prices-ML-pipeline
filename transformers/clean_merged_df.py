if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
from datetime import datetime as dt

@transformer
def transform(merged_df, *args, **kwargs):

    def date_numeric(val):
        """
        Convert a given date string to numeric form

        :param val: The Date value to convert
        """
        d = dt.strptime(val, '%Y-%m').toordinal()
        return d

    # Convert all Date values to numeric format
    merged_df['Date'] = merged_df['Date'].apply(date_numeric)
    
    # Force certain data types
    merged_df = merged_df.astype({'GDP Inflation': float, 'Oil Price   WTI   $US/Barrel': float, 'Number of immigrants': int})

    return merged_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'