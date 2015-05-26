__author__ = 'Liam'

from statistics import mean, mode, median_low, median, median_high

class Analyser(object):
    pass


class StringAnalyser(Analyser):
    def __init__(self, string_data):
        super().__init__()
        self.mode = mode(string_data)


class NumericalAnalyser(Analyser):
    def __init__(self, numerical_data):
        super().__init__()
        self.min = min(numerical_data)
        self.max = max(numerical_data)
        self.mode = mode(numerical_data)
        self.mean = mean(numerical_data)
        self.median_low = median_low(numerical_data)
        self.median = median(numerical_data)
        self.median_high = median_high(numerical_data)
