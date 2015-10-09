"""Creates an edited csv where errors has been replaced with default values.
        Not used in final program"""

import sys
import os
import csv

from difflib import get_close_matches

#Config for default values of data types
def_int = 0
def_float = 0.0

class Editor(object):
    """Corrects errors before writing to new file
        Depricated
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
        

"""Unused type code"""
#re_date = re.compile('^(?:(?:31(\/)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
#re_time = re.compile('(^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|(^(1[012]|0?[1-9]):[0-5][0-9](\ )?(?i)(am|pm)$)')
#re_char = re.compile('^\D$')
#re_day = re.compile('^(?i)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$')
#re_hyper = re.compile('^(?i)(https?:\/\/).+$')
       date_count = 0
        time_count = 0
        char_count = 0
        day_count = 0
        hyper_count = 0

            elif re_date.search(value) :
                date_count += 1
            elif re_time.search(value) :
                time_count += 1
            elif re_char.search(value) :
                char_count += 1
            elif re_day.search(value) :
                day_count += 1
            elif re_hyper.search(value) :
                hyper_count +=1
                
                
        elif date_count / len(self.values) >= threshold:
            self.type = 'Date'
        elif time_count / len(self.values) >= threshold:
            self.type = 'Time'
        elif char_count / len(self.values) >= threshold:
            self.type = 'Char'
        elif day_count / len(self.values) >= threshold:
            self.type = 'Day'
        elif hyper_count / len(self.values) >= threshold:
            self.type = 'Hyperlink'