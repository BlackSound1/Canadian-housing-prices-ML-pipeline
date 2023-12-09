if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


@transformer
def transform(merged_df, *args, **kwargs):
    
    # Make a copy of the merged DataFrame
    merged_df_copy = merged_df.copy()

    # Plot histograms for all columns, to see outliers
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