__author__ = 'Liam'


class Cleaner(object):
    def __init__(self, csv_data):
        self.clean_data = []
        self.invalid_length_rows = self.remove_invalid_rows(csv_data)
        self.remove_misc_values()

        #  self.clean_data = self.convert_empty_to_none(self.original_data)

    def remove_invalid_rows(self, csv_data):
        """
        This method flags rows that hold more columns than the headers, which
        likely means the data is garbled/out of order anyway. It returns
        the flagged rows, while correct rows are appended to the Cleaner
        object's clean_data array.
        :param csv_data:
        :return:
        """
        invalid_rows = []
        for i in csv_data[1]:
            if len(csv_data[0]) == len(i):
                self.clean_data.append(i)
            else:
                invalid_rows.append(i)
        return invalid_rows

    def remove_misc_values(self):
        """
        Replaces identified values of unclear meaning or inexact value
        , i.e., '-', '<1', with an agreed value.
        :return:
        """
        for i in range(len(self.clean_data)):
            for j in range(len(self.clean_data[i])):
                if self.clean_data[i][j] == '-':
                    self.clean_data[i][j] = ''
                elif '<' in self.clean_data[i][j]:
                    self.clean_data[i][j] = ''
