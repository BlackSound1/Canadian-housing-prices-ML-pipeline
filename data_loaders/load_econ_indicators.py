from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd


@data_loader
def load_data(*args, **kwargs):
    COLUMN_LIST = ['Year', 'Real GDP Growth', 'Unemp. Rate', 'Emp. Growth',
       'CPI Inflation', 'Core Inflation (CPIX)', 'GDP Inflation',
       '3 Month T-Bill', '10 Year  Bnchmk. Govt. Bond Rate',
       'Exchange Rate         (U.S.$)', 'US Real GDP Growth',
       'U.S. 90-day T-bill', "US Gov't Bond Rate (10 years)",
       'US CPI Inflation', 'US GDP Inflation', 'Oil Price   WTI   $US/Barrel',
       'Gas Price  Henry Hub   $US/mmbtu']

    # Create a dummy DataFrame to concat onto
    new_df = pd.DataFrame(columns=COLUMN_LIST)

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'comp333-data'
    
    object_keys = [
        'COMP333_Project_Data/econ_indicators/DEC_2009.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2010.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2011.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2012.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2013.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2014.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2015.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2016.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2017.csv',
        'COMP333_Project_Data/econ_indicators/DEC_2018.csv',
        'COMP333_Project_Data/econ_indicators/SEP_2019.csv',
        ]

    for key in object_keys:
        df = (
            GoogleCloudStorage
            .with_config(ConfigFileLoader(config_path, config_profile))
            .load(bucket_name, key)
        )

        # Get the 0th row
        df = df.iloc[[0]]

        # Concat this row to the new df
        new_df = pd.concat([new_df, df])

    new_df = new_df.sort_values('Year').reset_index().drop(columns='index')

    return new_df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
