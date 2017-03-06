"""Class for reading templates to pass on information about how
to process the data for the data class"""     

import csv

class Template(object):
    """Object storing user input that describes data given. Able to specify:
    
            Class Variables:
                columns -- state column number and data type.
            
                delimiter_type -- state delimiter character (for comma and space use the word not 
                ',' or ' ').
            
                header_row -- row of header (0 for no header).
            
                data_start -- row that data starts on
            
                data_size -- Length that all strings of identifer type must be.
            
                ignore_empty -- Boolean representing whether to ignore empty cells or not.
            
                threshold_val -- minimum proportion of column that has the correct data type
            
                enum_threshold_val -- Minimum amount of times an enumerated value must appear
                in a column to not be an error.
            
                std_devs -- How many standard deviations away from the mean numeric values are
                allowed to be.
            
                range_vals -- A list of two items [min, max] representing the minimum and maximum
                values numeric values can take.
            
                ignore_set -- A set listing all the columns that empty cells are to be ignored in.
        
            Columns and rows start at 1 not 0
        
            Class Methods:
                read -- Reads the template csv file and inputs data into corresponding variables
                if it's found in the file.
        """
        
    def __init__(self, filename):
        self.columns = {}
        self.delimiter_type = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        self.ignore_empty = False
        self.threshold_val = 0.90
        self.enum_threshold_val = 1
        self.std_devs = 3
        self.range_vals = []
        self.ignore_set = set()
        self.delete_set = []

        self.read(filename)
        
    def read(self, filename):
        """Reads template file, assumes correct formatting, if user editing
        is permitted will need to be improved with more checks.
        
            Keyword Arguments:
                filename -- filename of csv template file to be read for options.
        
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
                        if(row[1].lower() == 'comma') or (row[1] == ','):
                            self.delimiter_type = ','
                        elif(row[1].lower() == 'semicolon') or (row[1] == ';'):
                            self.delimiter_type = ';'
                        elif(row[1].lower() == 'space') or (row[1] == '\\s'):
                            self.delimiter_type = 'Space'
                        elif(row[1].lower() == 'dash') or (row[1] == '-'):
                            self.delimiter_type = '-'
                        elif(row[1].lower() == 'backslash') or (row[1] == '\\'):
                            self.delimiter_type = '\\'
                        elif(row[1].lower() == 'pipe') or (row[1] == '|'):
                            self.delimiter_type = '|'
                        elif(row[1].lower() == 'tab') or (row[1] == '\\t'):
                            self.delimiter_type = 'Tab'
                        else:
                            self.delimiter = row[1]
                    elif row[0].lower() == 'header':
                        self.header_row = int(row[1]) - 1
                    elif row[0].lower() == 'data_start':
                        self.data_start = int(row[1]) - 1
                    elif row[0].lower() == 'ignore_empty':
                        if row[1] == 'all':
                            self.ignore_empty = True
                    elif row[0].lower() == 'threshold_val':
                        self.threshold_val = float(row[1])
                    elif row[0].lower() == 'enum_threshold_val':
                        self.enum_threshold_val = int(row[1])    
                    elif row[0].lower() == 'std_dev': 
                        self.std_devs = float(row[1])
                    elif row[0].lower() == 'range':
                        self.range_vals.append(float(row[1]))
                        self.range_vals.append(float(row[2]))
                    elif row[0].lower() == 'ignore_empty_column':
                        for x, value in enumerate(row):
                            if x != 0:
                                self.ignore_set.add(int(value) - 1)
                    elif row[0].lower() == 'delete_col':
                        for col in row[1:]:
                            self.delete_set.append(int(col))
                    else:
                        print("Not an option: ", row)
