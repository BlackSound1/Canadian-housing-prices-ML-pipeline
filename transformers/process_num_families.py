if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import diff_cal, value_adder, month_adder

@transformer
def transform(number_of_families_df, *args, **kwargs):
    # Rename columns
    number_of_families_df = (
        number_of_families_df.rename(columns= {'year' : 'Date', 'number (in millions)': 'Number of families'})
    )

    # Make "Number of families" be in the millions

    number_of_families_df['Number of families'] = number_of_families_df['Number of families'].apply(lambda x: int(x * 1_000_000))

    # Keep only data between 2009 and 2019
    number_of_families_df['Date'] = number_of_families_df['Date'].astype(str).astype(int)
    number_of_families_df = (
        number_of_families_df[
            (number_of_families_df['Date'] >= 2008) &
            (number_of_families_df['Date'] <= 2019)
        ]
        .reset_index()
        .drop(columns='index')
    )

    # Find differences between the values in the "Number of families" column 
    diff_list = diff_cal(number_of_families_df['Number of families'])

    # Create a list in the "Number of families" column with smoothed out values between the previous value
    # and the next value, using the diff_list. Creates smooth monthly data for each year
    number_of_families_df['Number of families'] = number_of_families_df['Number of families'].apply(value_adder, diff_list=diff_list)

    # Drop the last row
    number_of_families_df = number_of_families_df.drop(index=11)

    # Add 1 to each year as compensation, to keep year range between 2009 and 2019
    number_of_families_df['Date'] = number_of_families_df['Date'].apply(month_adder, add_1=True)

    # Explode both the list-columns into individual rows
    number_of_families_df = number_of_families_df.explode(['Date', 'Number of families']).reset_index().drop(columns='index')

    # Make the "Number of families" column int
    number_of_families_df['Number of families'] = number_of_families_df['Number of families'].astype(int)

    return number_of_families_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'