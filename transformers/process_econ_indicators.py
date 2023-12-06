if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

from utilities import month_adder

@transformer
def transform(econ_indicators, *args, **kwargs):
    # Remove data that occurs every 3 months and that we don't think is useful
    econ_indicators = econ_indicators.drop(columns=['3 Month T-Bill','U.S. 90-day T-bill'])

    # Rename columns
    econ_indicators = econ_indicators.rename(columns= {'Year' : 'Date'})

    # Convert YYYY Date format to [YYYY-MM]
    econ_indicators['Date'] = econ_indicators['Date'].apply(month_adder)

    # Explode the lists of Dates in YYYY-MM format to individual rows
    econ_indicators = econ_indicators.explode(['Date']).reset_index().drop(columns='index')

    return econ_indicators


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
