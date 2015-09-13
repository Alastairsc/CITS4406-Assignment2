"""Creates an edited csv where errors has been replaced with default values"""

import sys
import os
import csv

from difflib import get_close_matches

#Config for default values of data types
def_int = 0
def_float = 0.0

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
            elif type == 'Boolean':
                self.bool_fix(col_num, row_num, value)
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
        """Function for fixing interger values.
            Changes to integer"""
        try:
            self.columns[col].values[row] = round(float(value)) #tries to cast
        except ValueError:
            print ()           #Do nothing
            
    def float_fix(self, col, row, value):
        """Function for fixing float values
            Changes to float"""
        try:
            self.columns[col].values[row] = float(value) #tries to cast
        except ValueError:
            print ()           #Do nothing
        
    def enum_fix(self, col, row, value):
        """Function for fixing Enumerated values.
            Changes value to closest enumerated value in the column"""
        most_common = self.columns[col].most_common
        items = []
        for i in most_common:
            items.append(i[0])
        self.columns[col].values[row] = get_close_matches(value[0], items, 2)[1]
       
    def bool_fix(self, col, row, value):
        """Function for fixing Boolean Values.
           Changes to closest boolean value """
        possible = {"true", "false"}
        self.columns[col].values[row] = get_close_matches(value, possible, 1)[0]
        
        
class Template(object):
    """Object storing user input that describes data given. Able to specify:
        Columns - state column number and data type
        Delimiter - state delimiter character (for comma use the word not ',')
        Start row - row of header (0 for no header)
        
        Columns and rows start at 1 not 0"""
        
    def __init__(self, filename):
        self.columns = {}
        self.delimiter = ''
        self.header_row = 0
        self.data_start = 1
       
        self.read(filename)
        
    def read(self, filename):
        with open(filename, newline='') as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                if len(row) > 1:
                    if row[0] == 'column':
                        self.columns[int(row[1])-1] = row[2] #column numbering starts at 1 instead of 0
                    elif row[0] == 'delimiter':
                        if(row[1] == 'comma'):
                            self.delimiter = ','
                        else:
                            self.delimiter = row[1]
                    elif row[0] == 'header':
                        self.header_row = int(row[1]) - 1
                        print("Set header: ", self.header_row)
                    elif row[0] == 'data_start':
                        self.data_start = int(row[1]) - 1
                        