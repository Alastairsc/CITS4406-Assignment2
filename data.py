__author__ = 'Liam'

import csv
import re
from collections import Counter
from statistics import mean, mode, median_low, median, median_high, \
    StatisticsError


#  Config
threshold = 0.9
invalid_values = ['-', '*', '_']
re_float = re.compile('^\d+\.?\d*$')
re_int = re.compile('^[1-9]\d*$')


class Analyser(object):
    def __init__(self, values):
        try:
            self.mode = mode(values)
        except StatisticsError:
            self.mode = 'N/A'


class StringAnalyser(Analyser):
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some string exclusive statistics.


class EnumAnalyser(Analyser):
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some enum exclusive statistics.


class NumericalAnalyser(Analyser):
    def __init__(self, values):
        values = [float(i) for i in values]
        super().__init__(values)
        self.min = min(values)
        self.max = max(values)
        self.mean = mean(values)
        self.median_low = median_low(values)
        self.median = median(values)
        self.median_high = median_high(values)


class Column(object):
    def __init__(self, header=''):
        self.most_common = []
        self.empty = False
        self.header = header
        #  self.invalid = False
        self.type = ''
        self.values = []
        self.analysis = None
        #  Todo: Does initialising as None even make sense?

    def change_misc_values(self):
        """
        Replaces identified values of unclear meaning or inexact value
        , i.e., '-', with an agreed value.
        :return:
        """
        for index, value in enumerate(self.values):
            if value in invalid_values:
                self.values[index] = ''
                
    def drop_greater_than(self):
        pass

    def define_most_common(self):
        self.most_common = Counter(self.values).most_common(15)
        if self.most_common[0][0] == '' \
                and self.most_common[0][1] / len(self.values) >= threshold:
            self.empty = True

    def define_type(self):
        float_count = 0
        int_count = 0
        boolean = ['true', 'false']
        #  Todo: Define date type.

        for value in self.values:
            if re_float.match(value):
                float_count += 1
                if re_int.match(value):
                    int_count += 1
            if float_count / len(self.values) >= threshold:
                if float_count == int_count:
                    self.type = 'Integer'
                else:
                    self.type = 'Float'
                    #  Todo: Whole number '0' being interpreted as Float.
                    #  Todo: Need to read value e.g. '030203898', as String. Perhaps trigger on '0' not immediately followed by '.'?
            elif len(self.most_common) <= 2:
                if self.most_common[0][0].lower() in boolean:
                    self.type = 'Bool'
            elif len(self.most_common) < 10:
                self.type = 'Enum'
            else:
                self.type = 'String'
                #  Todo: Refuses to assign values as 'String' even when forced?


class Data(object):
    def __init__(self, csv_file):
        self.columns = []
        self.headers = []
        self.invalid_rows = []
        self.raw_data = []
        self.valid_rows = []

        self.read(csv_file)
        self.remove_invalid()
        self.create_columns()

    def read(self, csv_file):
        f = csv.reader(open(csv_file))
        for row in f:
            self.raw_data.append(row)

    def remove_invalid(self):
        for row in self.raw_data:
            if len(row) != len(self.raw_data[0]):
                self.invalid_rows.append(row)
            else:
                self.valid_rows.append(row)

    def create_columns(self):
        for value in self.raw_data[0]:
            self.columns.append(Column(header=value))
            self.headers.append(value)
        self.valid_rows.pop(0)

        for row in self.valid_rows:
            for index, value in enumerate(row):
                self.columns[index].values.append(value)

    def clean(self):
        for column in self.columns:
            column.change_misc_values()
            column.drop_greater_than()

    def analyse(self):
        analysers = {'String': StringAnalyser, 'Integer': NumericalAnalyser,
                     'Float': NumericalAnalyser, 'Enum': EnumAnalyser}
        for column in self.columns:
            column.define_most_common()
            if not column.empty:
                column.define_type()
                if column.type in analysers:
                    column.analysis = analysers[column.type](column.values)
