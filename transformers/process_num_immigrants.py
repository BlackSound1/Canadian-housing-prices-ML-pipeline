if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import year_changer, month_adder

@transformer
def transform(number_of_immigrants_df, *args, **kwargs):
    # Rename columns
    number_of_immigrants_df = number_of_immigrants_df.rename(columns={'number': 'Number of immigrants', 'year': 'Date'})

    # Changing the year from YYYY - YYYY format to YYYY format
    number_of_immigrants_df['Date'] = number_of_immigrants_df['Date'].apply(year_changer, num=4)

    # Keep only 2009 - 2019 data
    number_of_immigrants_df['Date'] = number_of_immigrants_df['Date'].astype(str).astype(int)
    number_of_immigrants_df = (
        number_of_immigrants_df[
            (number_of_immigrants_df['Date'] >= 2009) &
            (number_of_immigrants_df['Date'] <= 2019)
        ]
        .reset_index()
        .drop(columns='index')
    )

    # Add months to each year
    number_of_immigrants_df['Date'] = number_of_immigrants_df['Date'].apply(month_adder)

    def immigrants_changer(val: int) -> list:
        """
        Let there be an equal number of immigrants for each month of the year

        :param val: The number of immigrants for a year
        :return: A list of integers, each the orignal number of immigrants divided by 12
        """
        new_val = int((val / 12))
        ls = [new_val] * 12
        return ls

    # Let there be an equal number of new immigrants for each month of the year
    number_of_immigrants_df['Number of immigrants'] = number_of_immigrants_df['Number of immigrants'].apply(immigrants_changer)

    # Explode the list-columns into individual rows
    number_of_immigrants_df = number_of_immigrants_df.explode(['Date', 'Number of immigrants']).reset_index().drop(columns='index')

    return number_of_immigrants_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'