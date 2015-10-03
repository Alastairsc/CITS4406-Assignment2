"""Class for reading templates to pass on information about how
to process the data for the data class"""     

import sys
import os
import csv
import re 

re_int = re.compile('^\s*[1-9]\d*$')

class Template(object):
    """Object storing user input that describes data given. Able to specify:
            Columns - state column number and data type.
            
            Delimiter - state delimiter character (for comma and space use the word not ',' or ' ').
            
            Header row - row of header (0 for no header).
            
            Start row - row that data starts on
            
            Threshold value - minimum proportion of column that has the correct data type
            
        
        Columns and rows start at 1 not 0"""
        
    def __init__(self, filename):
        self.columns = {}
        self.delimiter = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        self.ignore_empty = False
        self.threshold_val = 0.90
        self.enum_threshold_val = 1
        self.std_devs = 3
        self.range_vals = []
        self.ignore_set = set()
        
        self.read(filename)
        
    def read(self, filename):
        """Reads template file, assumes correct formatting, if user editing
        is permitted will need to be improved with more checks
        
        See documentation"""
        with open(filename, newline='') as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                if len(row) > 1:
                    if row[0].lower() == 'column':
                        self.columns[int(row[1])-1] = row[2] #column numbering starts at 1 instead of 0
                        if len(row) > 3 and row[2] == 'Identifier' and row[3].lower() == 'size':
                            self.data_size[int(row[1])-1] = int(row[4])
                    elif row[0].lower() == 'delimiter':
                        if(row[1] == 'comma'):
                            self.delimiter = ','
                            #TODO add space
                        else:
                            self.delimiter = row[1]
                    elif row[0].lower() == 'header':
                        self.header_row = int(row[1]) - 1
                        print("Set header: ", self.header_row)
                    elif row[0].lower() == 'data_start':
                        self.data_start = int(row[1]) - 1
                    elif row[0].lower() == 'ignore_empty':
                        if row[1] == 'all':
                            self.ignore_empty = True
                    elif row[0].lower() == 'threshold_val':
                        self.threshold_val = float(row[1])
                    elif row[0].lower() == 'enum_threshold_val':
                        self.enum_threshold_val = int(row[1])    
                    elif row[0].lower() == 'std_devs': 
                        self.std_devs = float(row[1])
                    elif row[0].lower() == 'range':
                        self.range_vals.append(float(row[1]))
                        self.range_vals.append(float(row[2]))
                        print (self.range_vals)
                    elif row[0].lower() == 'ignore_empty_column':
                        for x, value in enumerate(row):
                            if value != 'ignore_empty_column':
                                self.ignore_set.add(int(value))
                                print(self.ignore_set)  
