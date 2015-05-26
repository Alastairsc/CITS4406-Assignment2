__author__ = 'Liam'


class Cleaner(object):
    def __init__(self, csv_data):
        self.original_data = csv_data
        self.clean_data = self.convert_empty_to_none(self.original_data)

    @staticmethod
    def convert_empty_to_none(unclean_data):
        return [None if x == '' else x for x in unclean_data]
