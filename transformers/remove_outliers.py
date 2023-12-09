if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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

    # Plot the column-wise histograms again, this time showing no outliers
    fig, axes = plt.subplots(nrows=8, ncols=4, figsize=(15, 5*8))
    fig.tight_layout(pad=3.0)

    for i, col in enumerate([col for col in merged_df_copy.columns if col != 'Date']):
        sns.boxplot(merged_df_copy[col], ax=axes[i // 4, i % 4])
        axes[i // 4, i % 4].set_title(col)

    plt.show()

    return merged_df_copy


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'