if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import numpy as np


@transformer
def transform(merged_df_copy, *args, **kwargs):
    
    # From the above charts, we see that these columns possess outliers
    outlier_columns = [
        'Real GDP Growth',
        'Emp. Growth',
        'GDP Inflation',
        'US Real GDP Growth',
        'US CPI Inflation',
        'CPI_COMMON',
        'CPI_MEDIAN',
        'STATIC_TOTALCPICHANGE',
    ]

    # Go through each of these columns, and squash their outlying values to the 25th 
    # or 75th percentile, as necessary. For instance, if an outlier is below the 25th percentile,
    # set it to exactly the 25th percentile
    for col in outlier_columns:
        percentiles = merged_df_copy[col].quantile([0.25, 0.75]).values
        merged_df_copy[col] = np.clip(merged_df_copy[col], percentiles[0], percentiles[1])

    return merged_df_copy


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'