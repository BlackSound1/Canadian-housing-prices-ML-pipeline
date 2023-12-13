if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


def decimal_scaling(data: list) -> list:
    """
    Perform decimal scaling normalization on a given list of data.

    The list of data represents all the values for an attribute A,
    perhaps the list of all values in a column of a DataFrame.

    Get the maximum absolute value of the given data. Then figure out the smallest possible J value such that
    `(max_abs_val /  10^J) < 1`.

    :param data: The list of existing data
    :return: The new list of normalized data
    """

    def infinite_nums():
        """
        Generator to keep giving numbers from 0 to infinity.

        Shouldn't need infinite tries to get a good J value, but you might need many tries for astronomical numbers, perhaps.

        :return: The next highest number
        """
        num = 0
        while True:
            yield num
            num += 1

    # Get the maximum value for the given data
    max_abs_A = max(set(abs(v) for v in data))

    # To find the J value, start at 0...
    J = 0

    # Start counting infinite numbers from 0
    for i in infinite_nums():
        # Test if the current number meets the criteria
        if max_abs_A / 10**i < 1:
            # If so, that's the J value. Quit counting to infinity
            J = i
            break

    # Create a list of new data containing normalized old data. New data will be old data divided by 10^J
    new_data = [(v / (10**J)) for v in data]

    return new_data


@transformer
def transform(merged_df_copy, *args, **kwargs):
    cols_to_use = ['GDP (millions 2012 Constant Price)', 'Average price', 'One storey price', 'Two storey price',
                   'Townhouse price', 'Apartment price', 'Number of families', 'Number of immigrants', 'Population']
    
    # For each of the above columns, decimal scale their values
    for c in cols_to_use:
        merged_df_copy[c] = decimal_scaling(list(merged_df_copy[c].values))

    return merged_df_copy


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'