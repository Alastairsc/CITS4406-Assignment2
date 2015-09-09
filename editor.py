"""Creates an edited csv where errors has been replaced with default values"""

import sys
import os


class Editor(object):
    """Corrects errors before writing to new file"""
    
    def __init__(self, data):
        self.columns = data.columns
        self.errors = data.formatted_errors
        self.raw_data = data.raw_data
        
    def correctErrors(self):
        """Corrects the errors for given data"""
        
        for row, col, value in enumerate(self.errors):
            type = self.columns[col].type
            if type == 'Integer':
                try:
                    value = int(value)
                except ValueError:
                    value = 0
            elif type == 'Float':
                try:
                    value = float(value)
                except ValueError:
                    value = 0
            #TODO add the rest of the types
                
    def make_corrected(self, filename):
        """Creates a corrected Csv file"""
        fp = open(os.path.splitext(filename)[0] + "_corrected.csv", 'w')
        for row in self.raw_data:
            for cell in row:
                fp.write(str(cell) + ',')
            fp.write("\n")
        fp.close()
            
        