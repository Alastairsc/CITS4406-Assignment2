__author__ = 'Liam'
"""
Module implements all evaluation methods
"""

#  pattern = re.compile("d")
#  pattern.search("dog")
#  config['DEFAULT']['Compression']


class Evaluator(object):
    def __init__(self, header, clean_data):
        self.types = ['String', 'Number', 'Enumerated']
        self.identified_data = self.identify_type(header, clean_data)

        #  self.common_types = Counter(clean_data).most_common(5)
        #  self.type_identifier(clean_data)

    @staticmethod
    def identify_type(header, clean_data):
        data = []
        """
        for i in range(len(header)):
            for j in range(len(clean_data)):
                print(clean_data[j][i])
        """

        for i in range(len(header)):
            column = []
            for j in range(len(clean_data)):
                column.append(clean_data[j][i])
            print(column)

        return column
