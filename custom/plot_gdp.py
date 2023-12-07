if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import matplotlib.pyplot as plt
import seaborn as sns

def _plot_series(series, series_name, series_index=0):
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = series['Date']
  ys = series['GDP (millions 2012 Constant Price)']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])


@custom
def transform_custom(GDP_df, *args, **kwargs):
    fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
    df_sorted = GDP_df.sort_values('Date', ascending=True)
    _plot_series(df_sorted, '')
    sns.despine(fig=fig, ax=ax)
    plt.xticks([])
    plt.xlabel('Date (2009 - 2019)')
    _ = plt.ylabel('GDP (millions 2012 Constant Price)')

    return None
