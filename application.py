__author__ = 'Liam'
"""
Ref: http://www.dyinglovegrape.com/data_analysis/part1/1da3.php
http://stackoverflow.com/questions/2859674/converting-python-list-of-strings-to-their-type
https://docs.python.org/3.4/library/statistics.html

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

import configparser
import sys

from reader import Reader
from cleaner import Cleaner
from evaluator import Evaluator
from analyser import Analyser
from reporter import HTMLReport


def list_creator(list_items):
    html = '<ul>'
    for i in list_items:
        html += '<li>' + str(i) + '</li>'
    html += '</ul>'
    return html


def main():
    """
    Main execution body for the cleaning and sorting tool, it calls the
    required cleaning and analysis modules in their correct order.
    :return:
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    csv_file = sys.argv[1]

    reader = Reader(csv_file)
    cleaner = Cleaner(reader.csv_data)
    evaluator = Evaluator(reader.header, cleaner.clean_data)
    analyser = Analyser()
    HTMLReport(csv_file, cleaner, analyser)
    a = 'apple'

    """clean_data = [convert_empty_to_none(i) for i in data]
    cleaned_data = [Cleaner.convert_empty_to_none(i) for i in data]
    for i in range(len(header)):
        common_type = return_type(i, clean_data)
        print(common_type)
    pass"""

if __name__ == '__main__':
    main()
