if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import date_numeric

@transformer
def transform(merged_df, *args, **kwargs):

    # Convert all Date values to numeric format
    merged_df['Date'] = merged_df['Date'].apply(date_numeric)
    
    # Force certain data types
    merged_df = merged_df.astype({'GDP Inflation': float, 'Oil Price   WTI   $US/Barrel': float, 'Number of immigrants': int})

    # Reorder columns
    merged_df = merged_df[['Date', 'Real GDP Growth', 'Unemp. Rate', 'Emp. Growth',
                'CPI Inflation', 'Core Inflation (CPIX)', 'GDP Inflation',
                '10 Year  Bnchmk. Govt. Bond Rate', 'Exchange Rate         (U.S.$)',
                'US Real GDP Growth', "US Gov't Bond Rate (10 years)",
                'US CPI Inflation', 'US GDP Inflation', 'Oil Price   WTI   $US/Barrel',
                'Gas Price  Henry Hub   $US/mmbtu', 'ATOM_V41693242', 'CPIW',
                'CPI_COMMON', 'CPI_MEDIAN', 'CPI_TRIM', 'STATIC_CPIXFET',
                'STATIC_TOTALCPICHANGE', 'GDP (millions 2012 Constant Price)',
                'One storey price', 'Two storey price', 'Townhouse price',
                'Apartment price', 'interest rate', 'Housing index',
                'Number of families', 'Number of immigrants', 'Population', 'Average price']]

    return merged_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'