import pandas as pd
from datetime import datetime as dt


def see_redundant(df: pd.DataFrame) -> None:
    """
    Check how many unique values are in each column. If there's only 1 value in a column, it's probably redundant

    :param df: The DataFrame to check redundant columns of
    """

    for col in df.columns:
        print(f"{[col]}: {list(df[col].unique())}")


def value_adder(val, diff_list) -> list:
    """
    Takes the difference between 2 years' data values and returns a list of smoothed data points between them

    :param val: The first value to start with
    :param diff_list: The list of differences

    :return: The list if values to fill-in with
    """

    # Create initial list, starting with the initial value
    ls = [val]

    # Get the next item in the dict that is 'unused'
    try:
        diff_orig = diff_list[0]
    except Exception:
        diff_orig = 0

    # Go through number 1 to 11
    for i in range(1, 12):
        diff = diff_orig / 12  # Set the difference to be 1/12 the original
        diff *= i  # Multiply it by the current number
        new_val = val  # Set a temp variable to be the original value, so the original doesn't explode
        new_val += diff  # Add the diff to the new value
        ls.append(round(new_val, 2))  # Add this result to the list to return

    # Remove the first element from the diff_list
    if len(diff_list) != 0:
        del diff_list[0]

    return ls


def month_adder(val, add_1=False) -> list:
    """
    Takes a given year and splits it into 12 months in YYYY-MM format

    :param val: The given year
    :param add_1: Whether to add 1 to the month

    :return: The list of YYYY-MM entries
    """

    if add_1:
        ls = [f"{val + 1}-{i:02}" for i in range(1, 13)]
    else:
        ls = [f"{val}-{i:02}" for i in range(1, 13)]

    return ls


def diff_cal(col: pd.Series) -> list:
    """
    Finds the list of differences between each values in a DataFrames given column

    :param col: The column to find differences between

    :return: The list of differences between the elements of the column
    """

    diff_list = []

    for i in range(len(col) - 1):
        this = col[i]  # Get this row value
        that = col[i + 1]  # Get the next row value
        diff = that - this  # Find the difference
        diff_list.append(diff)  # Add it to the list of differences

    return diff_list


def year_changer(val, num=7):
    """
    Takes dates in YYY-MM-DD format and transforms them to YYYY-MM format

    :param val: The year to transform
    :param num: How many characters to keep
    :return: The transformed date value
    """

    val = val[:num]
    return val


def date_numeric(val):
    """
    Convert a given date string to numeric form

    :param val: The Date value to convert
    """
    d = dt.strptime(val, '%Y-%m').toordinal()
    return d
