#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reads CSV file for information, provides basic cleaning of data and then
runs analysis on said data."""

import sys
import os

"""sysPathStr = "%s%s" % (os.path.dirname(os.path.realpath(__file__)), "/lib/python3.4/site-packages")
#print (sysPathStr)
sys.path.append(sysPathStr)
for pth in sys.path:
    print (pth)"""

import csv
import re
from collections import Counter
try:
	from .analyser import *
except SystemError:
	from analyser import *

#  Config
invalid_values = ['-', '*', '_', '$']
re_float = re.compile('^-?\d*?\.\d+$')
re_int = re.compile('^\s*[1-9]\d*$')
re_email = re.compile('@')
re_currency = re.compile('(^\s*((-?(\$|€|£))|((\$|€|£)-?))(\d*\.\d*|\.\d*|\d*))')
re_boolean = re.compile('^\s*T$|^\s*F$|^\s*True$|^\s*False$|^\s*Y$|^\s*N$|^\s*Yes$|^\s*No$', re.I)
re_sci_notation= re.compile('\s*[\+-]?(\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?')
#[\+-]?((\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?)
#[\+-]?\d+(\.\d+)?[eE]\d
re_separation = re.compile('[\s,;]+')
re_date = re.compile('^(?:(?:31(\/)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$')
re_time = re.compile('(^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|(^(1[012]|0?[1-9]):[0-5][0-9](\ )?(?i)(am|pm)$)')
re_char = re.compile('^\D$')
re_day = re.compile('^(?i)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$')
re_hyper = re.compile('^(?i)(https?:\/\/).+$')

    
class Column(object):
    """Object to hold data from each column within the provided CSV file.
    
    Methods:
        change_misc_values -- Removes misc/unclear values from column values.
        
        drop_greater_than -- Removes '<', '>' from column values.
        
        define_most_least_common -- Sets object variable to hold 15 most common values
        and least common values for that column.
        
        define_type -- Sets object variable to type (e.g., String) according
        to column values.
        
        define_errors -- Defines a list that contains the row and column of possibly
        incorrect values.
    
    Variables:
        most_common -- <= 15 most common results within the column values.
        
        least_common -- <= 15 least common results within the column values.
        
        empty -- Boolean value of whether the column holds values or not.
        
        header -- Column header/title.
        
        type -- The type of data in column, e.g., String, Float, Integer,
        Enumerated.
        
        values -- List of CSV values for the column.
        
        analysis -- Analysis object associated with this column.

    """
    def __init__(self, header=''):
        self.most_common = []
        self.least_common = []
        self.empty = False
        self.header = header
        self.type = ''
        self.values = []
        self.analysis = None
        self.total_true = 0
        self.total_false = 0
        self.total_yes = 0
        self.total_no = 0
        self.data_size = -1
        self.ignore_empty = False
        #  Todo: Does initialising as None even make sense?

    def change_misc_values(self):
        """
        Replaces identified values of unclear meaning or inexact value, i.e., 
        '-', with an agreed value.
        """
        for index, value in enumerate(self.values):
            if value in invalid_values:
                self.values[index] = ''
                
    def drop_greater_than(self):
        pass
        #  Todo: Implement method to handle (strip?) '<', '>'.
        
        

    def define_most_least_common(self):
        """Set 15 most common results to class variable, and set object variable 
        empty if appropriate.
        """
        temp_list = Counter(self.values).most_common()
        for i, e in list(enumerate(temp_list)):
            if i < 15:
                self.most_common.append(e)
        for i, e in reversed(list(enumerate(temp_list))):
            if i < 15:
                self.least_common.append(e)
       # print("Column: ", self.values)
      #  print("Most Common: ", self.most_common)
        if self.most_common[0][0] == '' \
                and self.most_common[0][1] / len(self.values) >= threshold:
            self.empty = True

    def define_type(self):
        """Run column data against regex filters and assign object variable type
        as appropriate.
        """
        float_count = 0
        int_count = 0
        email_count = 0
        currency_count = 0
        boolean_count = 0
        sci_not_count = 0
        date_count = 0
        time_count = 0
        char_count = 0
        day_count = 0
        hyper_count = 0
        
        #  Todo: Define date type.

        for x, value in enumerate(self.values):
          #  print("Values: " , value)
            if re_float.match(value):
               # print(value)
                float_count += 1
            elif re_int.match(value):
               # print(value)
                int_count += 1
                value = value.strip()
            elif re_email.search(value):
              #  print(value)
                if parseaddr(value)[1] != '':
              #      print(parseaddr(value)[1])
          #          print("Email match")
                    email_count += 1
            elif re_currency.search(value):
              #  print(value)
             #   print ("Group")
               # print (re_currency.search(value).group())
                currency_count += 1
            elif re_boolean.search(value):
              #  print(value)
                boolean_count += 1
                #print(value)
                temp_value = str(value.upper())
              #  print(temp_value)
                if temp_value == ' TRUE' or temp_value == ' T' or temp_value == 'TRUE' or temp_value == 'T':
                    self.total_true += 1
                if temp_value == ' FALSE' or temp_value == ' F' or temp_value == 'FALSE' or temp_value == 'F':
                    self.total_false += 1
                if temp_value == ' YES' or temp_value == ' Y' or temp_value == 'YES' or temp_value == 'Y':
                    self.total_yes += 1
                if temp_value == ' NO' or temp_value == ' N' or temp_value == 'NO' or temp_value == 'N':
                    self.total_no += 1
            elif re_sci_notation.fullmatch(value):
                #print("Sci not match:", value)
                sci_not_count += 1
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
        num_values = len(self.values)
        if float_count / len(self.values) >= threshold:
            self.type = 'Float'
        elif int_count / len(self.values) >= threshold:
            self.type = 'Integer'
        elif float_count / num_values >= threshold:
            self.type = 'Float'
        elif (float_count + int_count) / num_values >= threshold:
            self.type = 'Numeric'
        elif email_count / num_values >= threshold:
        #    print('Email type')
            self.type = 'Email'
        elif currency_count / num_values >= threshold:
      #     print('Currency type')
            self.type = 'Currency'
        elif boolean_count / num_values >= threshold:
       #     print('Boolean type')
            self.type = 'Boolean'
        elif sci_not_count / num_values >= threshold:
            self.type = 'Sci_Notation'
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
        elif len(self.most_common) < 10:
            self.type = 'Enum'
        else:
            self.type = 'String'

    def define_errors(self, columnNumber, errors, formatted_errors, invalid_rows_pos):
        """Define all the rows/columns with invalid values and append to errors, and
        formatted_errors once formatted properly. invalid_rows_pos holds the amount of
        rows that have been skipped by the time the current row x is being considered.
        
        Keyword arguments:
            columnNumber -- The number of the current column being iterated over, numbered
            from 0.
            
            errors -- A list of errors to be edited of the form (row number, column number,
            error value) which is numbered from 0.
            
            formatted_errors -- A list of errors to be edited of the form (row number, column
            number, error value) which is numbered from 1.
            
            invalid_rows_pos -- An array containing a number matching the amount of invalid
            rows that have been removed from analysis by the time that row is accessed. i.e.
            invalid_rows_pos[1] = 2 says that by the time values[1] is evaluated two rows have
            been removed from analysis.
        """
        tup = ()        
        if self.type == 'Float':
            for x, value in enumerate(self.values):           
                if not re_float.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Integer':
            for x, value in enumerate(self.values):
                if not re_int.match(value) and not value == '0':
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Numeric':
            for x, value in enumerate(self.values):
                if value == '' and self.ignore_empty:
                    continue
                if not re_int.match(value) and not re_float.match(value) and not value == '0':
                    print("Value: ", value)
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - not a number" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Email':
            for x, value in enumerate(self.values):
                if re_email.search(value):
                    if parseaddr(value)[1] == '':
                        tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Boolean':
            for x, value in enumerate(self.values):
                if not re_boolean.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Currency':
           # print('Currency errors')
            for x, value in enumerate(self.values):
                if not re_currency.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
                else:
                    self.values[x] = re.sub('(\$)|(€)|(£)', '', value)
        elif self.type == 'String':
            for x, value in enumerate(self.values):
                if (value == '' or value == ' ') and self.ignore_empty:
                    continue
                if value == '' or value == ' ':
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Enum':
            for x, value in enumerate(self.least_common):  
                if self.least_common[x][1] <= enum_threshold:
                    i = 0 
                    freq = 0
                    for cell in self.values:
                        if cell == value[0]:
                            tup = (i + 1 + invalid_rows_pos[x], columnNumber + 1, value[0])
                            errors.append(tup)
                            formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
                            freq += 1
                        i+=1
                    if freq == 0:
                         raise Exception('Least common value not found')
        elif self.type == 'Sci_Notation':
            for x, value in enumerate(self.values):
                if not re_sci_notation.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Identifier':
            if self.data_size != -1:
                size = self.data_size
            else:
                size = len(self.values[0])
            for x, value in enumerate(self.values):
                if len(value) != size:
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Date':
            for x, value in enumerate(self.values):           
                if not re_date.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))

        elif self.type == 'Time':
            for x, value in enumerate(self.values):           
                if not re_time.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))

        elif self.type == 'Char':
            for x, value in enumerate(self.values):           
                if not re_char.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))

        elif self.type == 'Day':
            for x, value in enumerate(self.values):           
                if not re_day.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))

        elif self.type == 'Hyperlink':
            for x, value in enumerate(self.values):           
                if not re_float.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
                
       # print("Errors: ", errors)

    def set_type(self, type):
        """Sets type of column for use with templates"""
        self.type = type

    def set_size(self, size):
        """Sets the size of the data for use when checking for errors.
            For use with the 'Identifier' data type"""
        self.data_size = size
    
    def set_empty(self):
        """Set Column to be empty"""
        self.empty = True
    
    def set_not_empty(self):
        """Set Column to be not empty"""
        self.empty = False
    
    def is_Empty(self):
        """Whether or not column is empty"""
        return self.empty == True
        
        
class Data(object):
    """Main store for CSV data, reading the data from the CSV file and then 
    assigning out to relevant variables.
    
    Methods:
        read -- Reads the CSV file and outputs to raw_data variable.
        
        remove_invalid -- Reads from raw_data variable and assigns rows to 
        valid_rows or invalid_rows according to their length.
        
        create_columns -- Creates column object according to valid_rows, assigning
        column header and column values.
        
        clean -- Calls column cleaning methods to run 'cleaning' on all columns.
        
        analyse -- Calls column analysis methods to run 'analysis' on all columns.
    
    Variables:
        columns -- List of column objects.
        
        headers -- List of column headers.
        
        invalid_rows -- List of invalid rows (i.e., more or less columns than
        number of headers).
        
        formatted_errors -- List of errors in file, each error contains: row, column 
        and value of the error.
        
        raw_data -- List of raw CSV data as rows.
        
        valid_rows -- List of valid rows (i.e., same number of columns as headers).
        
        errors -- List of rows and columns of possibly incorrect values.
    """
    def __init__(self, *args):
        """Can take up to two arguments, 
            first argument -- filename
            second argument -- template"""
        
        self.filename = args[0]
        self.columns = []
        self.invalid_rows = []
        self.invalid_rows_pos = []
        self.errors = []     
        self.formatted_errors = []
        self.raw_data = []
        self.valid_rows = []
        self.analysers = {'String': StringAnalyser, 'Integer': NumericalAnalyser,
                     'Float': NumericalAnalyser, 'Enum': EnumAnalyser, 
                     'Email': EmailAnalyser, 'Currency': CurrencyAnalyser,
                     'Boolean': BooleanAnalyser, 'Sci_Notation': SciNotationAnalyser,
                     'Identifier': IdentifierAnalyser, 'Date': DateAnalyser,
                     'Time': TimeAnalyser, 'Char': CharAnalyser,
                     'Day': DayAnalyser, 'Hyperlink': HyperAnalyser, 
                     'Numeric': NumericalAnalyser}
        
        #Template settings
        self.template = None
        self.delimiter = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        self.ignore_empty = False
       # print(len(args))
        if len(args) > 1:  
            self.template = args[1]
            self.delimiter = self.template.delimiter
            self.header_row = self.template.header_row
            self.data_start = self.template.data_start
            self.data_size = self.template.data_size
            self.ignore_empty = self.template.ignore_empty
        #Process data
        self.read(self.filename)
        self.remove_invalid()
        self.create_columns()
        

    def read(self, csv_file):
        """Opens and reads the CSV file, line by line, to raw_data variable.
        
        Keyword arguments:
            csv_file -- The filename of the file to be opened.
        """
        #f = csv.reader(open(csv_file))
        #for row in f:
        #    self.raw_data.append(row)
        #separation of comma, semicolon, dash, tab delimited csv files
        if self.delimiter == '':
          #  print("Here")
            with open(csv_file, newline='') as csvfile:
                    try:
                        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters='space,;-\|\t\\')
                        csvfile.seek(0)
                        f = csv.reader(csvfile, dialect)
                    except:
                        print("Delimiter Warning: could not determine delimiter, consider",\
                        "specifying using template. Continuing using comma")
                        csvfile.seek(0)
                        f = csv.reader(csvfile, delimiter=',')
                    for row in f:
                        #print(row)
                        self.raw_data.append(row)
        else:
            #template specified delimiter
            with open(csv_file, newline='') as csvfile:
                f = csv.reader(csvfile, delimiter=self.delimiter)
                for row in f:
                   self.raw_data.append(row)

    def remove_invalid(self):
        """For each row in raw_data variable, checks row length and appends to 
        valid_rows variable if same length as headers, else appends to 
        invalid_rows variable. invalid_rows_pos holds the amount of rows that have been
        skipped by the point the xth row has been accessed from valid_rows.
        """
        count = 0
        preamble = []
        if self.data_start != 0:
            for row in range(0, self.data_start):
                preamble.append(self.raw_data[row])
        row_length = len(self.raw_data[self.header_row])
        for index, row in enumerate(self.raw_data):
            if len(row) != row_length:
                self.invalid_rows.append(["%s: %d" % ("Line", index + 1)])
                self.raw_data[index] = []
                #print(self.invalid_rows)
                count = count + 1
            else:
                self.valid_rows.append(row)
                self.invalid_rows_pos.append(count)
                self.raw_data[index] = []
        self.raw_data = preamble
    #    print("Invalid row pos: ", self.invalid_rows_pos)

    def create_columns(self):
        """For each row in raw_data variable, assigns the first value to the 
        headers variable and creates a Column object with that header provided.
        Then removes header row from valid_rows. Then for each row in valid_rows,
        populates relevant column object with row data.
        """
        if self.header_row >=0:
            for value in self.raw_data[self.header_row]:
                self.columns.append(Column(header=value))
            self.valid_rows.pop(self.header_row)            
       # for vrows in self.valid_rows:
        #    print(vrows)
        length = len(self.valid_rows)
        for row_num in range(self.data_start - 1, length):
            for index, value in enumerate(self.valid_rows[row_num]):
                self.columns[index].values.append(value)
            self.valid_rows[row_num] = []
        self.valid_rows = []
        

    def clean(self):
        """Calls cleaning methods on all columns.
        """
        for column in self.columns:
            column.change_misc_values()
            column.drop_greater_than()

    def analysis(self):
        """Iterates through each column and analyses the columns values using the
        columns type analyser.
        """
        for colNo, column in enumerate(self.columns):
             if not column.empty:
                if column.type in self.analysers:
                    #print("col type: ", column.type)
                    column.analysis = self.analysers[column.type](column.values)  
            
    def find_errors(self):
        """Iterates through each column and finds any errors according to pre-determined
        conditions.
        """
        for colNo, column in enumerate(self.columns):
             if not column.empty:
                column.define_errors(colNo, self.errors, self.formatted_errors, self.invalid_rows_pos)

    def pre_analysis(self):
        """First defines their least and most common elements, then if 
        template is supplied, sets the type of the column to match the template, if not if 
        column is not empty defines its type, and if it's a special data type sets the columns
        size to me no more than data_size.
        """
        
        for colNo, column in enumerate(self.columns):
           # print("Col: ",colNo)
            column.define_most_least_common()
            if not column.empty:
                if self.template != None and colNo in self.template.columns:
                    column.set_type(self.template.columns[colNo])
                else:
                    column.define_type()
                if column.type == 'Identifier' and self.data_size != None and \
                    colNo in self.data_size:
                    column.set_Identifier_size(self.data_size[colNo])
                if self.ignore_empty:
                    column.ignore_empty = True
                    
    def get_row(self, row_num):
        """Returns the values of a row in list"""
        row = []
        for colNo, column in enumerate(self.columns):
            row.append(column.values[row_num])
        return row
        
    def change_row(self, row_num, new_values):
        """Edits a row of the data given:
            row_num - number of row being changed
            new_values - list of values row is to be changed to"""
        for colNo, column in enumerate(self.columns):
            column.values[row_num] = new_values[colNo - 1]
        
    def gen_file(self):
        """Generates a csv file based on the data for after
        data has been corrected"""
        new_file = open(os.path.splitext(self.filename)[0] + "_corrected.csv", "w")
        #Write header rows
        for rowNo in range(0, self.data_start):
            row_len = len(self.raw_data[rowNo])
            for i, cell in enumerate(self.raw_data[rowNo]):
                new_file.write(cell)
                if(i == row_len - 1):
                    new_file.write("\n")
                else:
                    new_file.write(",")
        num_rows = len(self.columns[0].values)
        row_len = len(self.columns)
        for rowNo in range(0, num_rows):
            for colNo, column in enumerate(self.columns):
                new_file.write(column.values[rowNo])
                if(colNo == row_len - 1):
                    new_file.write("\n")
                else:
                    new_file.write(",")
                    
    def get_column(self, colNo):
        """Returns a column of the data given a column number"""
        return self.columns[colNo]
    
    def get_headers(self):
        """Returns the headers of data"""
        return self.raw_data[self.header_row]
    
    def set_headers(self, header_map):
        """Sets headers of columns taking a dictionary 
        mapping column numbers to headers"""
        for colNo, header in header_map:
            self.raw_data[self.header_row][colNo] = header
