__author__ = 'Liam'
"""
Ref: http://www.dyinglovegrape.com/data_analysis/part1/1da3.php
http://stackoverflow.com/questions/2859674/converting-python-list-of-strings-to-their-type

    # def count empties emtpy
    count = 0
    for value in data:
        if len(value) == 0:
            count += 1
    if count / len(data) > 0.9:
        return True
    else:
        return False
"""

import csv
import ast
# from analyser import *
from collections import Counter
#  import unittest


def data_reader(csv_file):
    """
    Opens the CSV file, and collects the data as a list of lists. Cleans the
    headers from the data and then returns both as separate values.
    :param csv_file:
    :return:
    """
    read_data = csv.reader(open(csv_file, 'r'))
    data = []

    for row in read_data:
        data.append(row)

    header = data[0]
    data.pop(0)

    return header, data


def convert_empty_to_none(data):
    return [None if x == '' else x for x in data]


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


def main():
    """
    Main execution body for the cleaning and sorting tool, it calls the
    required cleaning and analysis modules in their correct order.
    :return:
    """
    header, data = data_reader('csv\oil_original.csv')
    clean_data = [convert_empty_to_none(i) for i in data]
    for i in range(len(header)):
        common_type = return_type(i, clean_data)
        print(common_type)
    pass


if __name__ == '__main__':
    main()
