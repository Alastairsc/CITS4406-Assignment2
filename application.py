__author__ = 'Liam'

import sys

from data import *
from report import *
#  from reader import Reader
#  from cleaner import Cleaner
#  from reporter import HTMLReport


def main():
    """
    Main execution body for the cleaning and sorting tool, it calls the
    required cleaning and analysis modules in their correct order.
    :return:
    """
    file = sys.argv[1]
    data = Data(file)
    data.clean()
    data.analyse()
    report = Report(data, file)
    report.html_report()

    #  csv_file = sys.argv[1]
    #  reader = Reader(csv_file)
    #  cleaner = Cleaner(reader.csv_data)

    #  analysers = [IntegerAnalyser(),NumericAnalyser(),StringAnalyser()]
    #  evaluator = Evaluator(cleaner.clean_data)
    #  analyser = Analyser(cleaner.clean_data)

    #  HTMLReport(csv_file, reader, cleaner)


if __name__ == '__main__':
    main()
