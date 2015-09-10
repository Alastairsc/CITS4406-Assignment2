"""Creates an edited csv where errors has been replaced with default values"""

import sys
import os

from difflib import get_close_matches

#Config for default values of data types
def_int = 0
def_float = 0.0
def_str = " "
def_email = "default@home.com"
def_boolean = False
def_date = "0/0/0"
def_time = 00.00
def_char = ' '
def_hyperlink = " "
def_currency = 0
def_dow = " "
def_coords = 0

class Editor(object):
    """Corrects errors before writing to new file
    """
    
    def __init__(self, data):
        self.columns = data.columns
        self.errors = data.errors
        
    def correctErrors(self):
        """Corrects the errors for given data"""
        for i, (row, col, value) in enumerate(self.errors):
            col_num = col - 1
            row_num = row - 1
            type = self.columns[col_num].type
     
            if type == 'Integer':
                self.int_fix(col_num, row_num, value)
            elif type == 'Float':
                self.float_fix(col_num, row_num, value)
            elif type == 'Enum':
                self.enum_fix(col_num, row_num, value)
            elif type == 'String':
                self.string_fix(col_num, row_num, value)
            #TODO add the rest of the types
                
    def make_corrected(self, filename):
        """Creates a corrected Csv file"""
        self.correctErrors()
        fp = open(os.path.splitext(filename)[0] + "_corrected.csv", 'w')
        size = len(self.columns[0].values)
        for col in self.columns:
            fp.write(str(col.header) + ",") 
            #Write header to file
        fp.write("\n")
        for row in range(0, size):
            for col in self.columns:
                fp.write(str(col.values[row]) + ',')
            fp.write("\n")
        fp.close()
    
    def int_fix(self, col, row, value):
        """Function for fixing interger values"""
        try:
            self.columns[col].values[row] = round(float(value)) #tries to cast
        except ValueError:
            self.columns[col].values[row] = def_int #default value
            
    def float_fix(self, col, row, value):
        """Function for fixing float values"""
        try:
            self.columns[col].values[row] = float(value) #tries to cast
        except ValueError:
            self.columns[col].values[row] = def_float #default value
        
    def enum_fix(self, col, row, value):
        """Function for fixing Enumerated values"""
        most_common = self.columns[col].most_common
        items = []
        for i in most_common:
            items.append(i[0])
        self.columns[col].values[row] = get_close_matches(value[0], items, 2)[1]
       
    #def string_fix(self, col, row, value):
    
        #TODO add fix