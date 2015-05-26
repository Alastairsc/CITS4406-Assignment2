__author__ = 'Liam'

import csv


class Reader(object):
    def __init__(self, csv_data):
        self.header, self.data = self.data_reader(csv_data)

    @staticmethod
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
