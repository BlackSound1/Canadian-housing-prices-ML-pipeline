from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import glob

def merge_econ_inidicators(econ_files: list) -> pd.DataFrame:
    COLUMN_LIST = ['Year', 'Real GDP Growth', 'Unemp. Rate', 'Emp. Growth',
       'CPI Inflation', 'Core Inflation (CPIX)', 'GDP Inflation',
       '3 Month T-Bill', '10 Year  Bnchmk. Govt. Bond Rate',
       'Exchange Rate         (U.S.$)', 'US Real GDP Growth',
       'U.S. 90-day T-bill', "US Gov't Bond Rate (10 years)",
       'US CPI Inflation', 'US GDP Inflation', 'Oil Price   WTI   $US/Barrel',
       'Gas Price  Henry Hub   $US/mmbtu']

    # Create a dummy DataFrame to concat onto
    new_df = pd.DataFrame(columns=COLUMN_LIST)

    # Loop through each file
    for file in econ_files:

        # Read the DataFrame
        df = pd.read_csv(file)

        # Get the 0th row
        df = df.iloc[[0]]

        # Concat this row to the new df
        new_df = pd.concat([new_df, df])

    new_df = new_df.sort_values('Year').reset_index().drop(columns='index')

    return new_df

@data_loader
def load_data_from_file(*args, **kwargs):
    econ_files = glob.glob(f"{kwargs['FILES_LOCATION']}/econ_indicators/*.csv")

    df = merge_econ_inidicators(econ_files)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
