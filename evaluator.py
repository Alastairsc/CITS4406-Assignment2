__author__ = 'Liam'
"""
Module implements all evaluation methods
"""

import ast
from collections import Counter

#  pattern = re.compile("d")
#  pattern.search("dog")


def return_type(i, data):
    """
    Iterates over the data in the column provided as i to return the most
    common type in that column.

    :param i: The position of the header iterable.
    :param data: The data to iterate over to find the column values.
    :return:
    """
    cnt = Counter()
    values = []
    for j in range(len(data)):
        values.append(data[j][i])
    for data_type in [evaluate_type(value) for value in values]:
        cnt[data_type] += 1
    return str(cnt.most_common()[0][0])


def evaluate_type(val):
    """
    Interprets strings passed and attempts to return their correct type. E.g.,
    val = '1' should return as "<class 'int'>".
    :param val:
    :return:
    """
    try:
        val = ast.literal_eval(val)
    except ValueError:
        pass
    except SyntaxError:
        #  Without this, will fail on values with mixed type, e.g., '793B'
        pass
    return type(val)
