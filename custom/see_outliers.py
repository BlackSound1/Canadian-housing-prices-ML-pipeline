if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import seaborn as sns
import matplotlib.pyplot as plt


@custom
def transform_custom(merged_df_copy, *args, **kwargs):
    # Plot histograms for all columns, to see outliers
    fig, axes = plt.subplots(nrows=8, ncols=4, figsize=(15, 5*8))
    fig.tight_layout(pad=3.0)

    for i, col in enumerate([col for col in merged_df_copy.columns if col != 'Date']):
        sns.boxplot(merged_df_copy[col], ax=axes[i // 4, i % 4])
        axes[i // 4, i % 4].set_title(col)

    return None
