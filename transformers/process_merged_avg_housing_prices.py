if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import year_changer

@transformer
def transform(average_housing_df, *args, **kwargs):
    # Rename columns
    average_housing_df = average_housing_df.rename(columns={'  Average*': 'Average price', "One_storey": "One storey price",
                                                            "Two_storey": "Two storey price", 'Townhouse': "Townhouse price",
                                                            "Apartment_unit": "Apartment price"})
    
    # Round decimal places
    def average_rounder(val):
        return round(val, 2)

    average_housing_df['Average price'] = average_housing_df['Average price'].astype(float)
    average_housing_df['Average price'] = average_housing_df['Average price'].apply(average_rounder)

    # Change the Date format from YYYY-MM-DD to YYYY-MM
    average_housing_df['Date'] = average_housing_df['Date'].astype(str)
    average_housing_df['Date'] = average_housing_df['Date'].apply(year_changer)

    # Only take data from years 2009 to 2019
    average_housing_df = (
        average_housing_df[
            (average_housing_df['Date'].str[:4].astype(int) >= 2009) &
            (average_housing_df['Date'].str[:4].astype(int) <= 2019)
        ]
    )
    
    return average_housing_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'