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
from analyser import *

#  Config
invalid_values = ['-', '*', '_', '$']
re_float = re.compile('^-?\d*?\.\d+$')
re_int = re.compile('^\s*[1-9]\d*$')
re_email = re.compile('@')
re_currency = re.compile('(^\s*((-?(\$|€|£))|((\$|€|£)-?))(\d*\.\d*|\.\d*|\d*))')
re_boolean = re.compile('^\s*T$|^\s*F$|^\s*True$|^\s*False$|^\s*Y$|^\s*N$|^\s*Yes$|^\s*No$', re.I)
re_sci_notation= re.compile('[\+-]?(\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?')
#[\+-]?((\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?)
#[\+-]?\d+(\.\d+)?[eE]\d
re_separation = re.compile('[\s,;]+')

    
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

        #  Todo: Define date type.

        for x, value in enumerate(self.values):
        #    print(value)
            if re_float.match(value):
                float_count += 1
            elif re_int.match(value):
                int_count += 1
                value = value.strip()
            elif re_email.search(value):
                if parseaddr(value)[1] != '':
                    print(parseaddr(value)[1])
          #          print("Email match")
                    email_count += 1
            elif re_currency.search(value):
                print ("Group")
                print (re_currency.search(value).group())
                currency_count += 1
            elif re_boolean.search(value):
                boolean_count += 1
                temp_value = str(value.upper())
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
        if float_count / len(self.values) >= threshold:
            self.type = 'Float'
        elif int_count / len(self.values) >= threshold:
            self.type = 'Integer'
        elif email_count / len(self.values) >= threshold:
        #    print('Email type')
            self.type = 'Email'
        elif currency_count / len(self.values) >= threshold:
      #     print('Currency type')
            self.type = 'Currency'
        elif boolean_count / len(self.values) >= threshold:
       #     print('Boolean type')
            self.type = 'Boolean'
        elif sci_not_count / len(self.values) >= threshold:
            self.type = 'Sci_Notation'
        elif len(self.most_common) < 10:
            self.type = 'Enum'
        else:
            self.type = 'String'

    def define_errors(self, columnNumber, errors, formatted_errors, invalid_rows_pos):
        """Define all the rows/columns with invalid values and append to errors, and
        formatted_errors once formatted properly. invalid_rows_pos holds the amount of
        rows that have been skipped by the time the current row x is being considered."""
        tup = ()        
        if self.type == 'Float':
            for x, value in enumerate(self.values):           
                if not re_float.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
        elif self.type == 'Integer':
            for x, value in enumerate(self.values):
                if not re_int.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
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
            print('Currency errors')
            for x, value in enumerate(self.values):
                if not re_currency.match(value):
                    tup = (x + 1 + invalid_rows_pos[x], columnNumber + 1, value)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s" % (tup[0] + 1, tup[1], tup[2]))
                else:
                    self.values[x] = re.sub('(\$)|(€)|(£)', '', value)
        elif self.type == 'String':
            for x, value in enumerate(self.values):
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
       # print("Errors: ", errors)

    def set_type(self, type):
        """Sets type of column for use with tempaltes"""
        self.type = type

    def set_size(self, size):
        """Sets the size of the data for use when checking for errors.
            For use with the 'Identifier' data type"""
        self.data_size = size
        
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

        self.columns = []
     #   self.headers = []
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
                     'Identifier': IdentifierAnalyser}
        
        #Template settings
        self.template = None
        self.delimiter = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        if len(args) > 1:  
            self.template = args[1]
            self.delimiter = self.template.delimiter
            self.header_row = self.template.header_row
            self.data_start = self.template.data_start
            self.data_size = self.template.data_size
        #Process data
        self.read(args[0])
        self.remove_invalid()
        self.create_columns()
        

    def read(self, csv_file):
        """Opens and reads the CSV file, line by line, to raw_data variable."""
        #f = csv.reader(open(csv_file))
        #for row in f:
        #    self.raw_data.append(row)
        #separation of comma, semicolon, dash, tab delimited csv files
        if self.template == None:
            print("Here")
            with open(csv_file, newline='') as csvfile:
                    try:
                        dialect = csv.Sniffer().sniff(csvfile.read(), delimiters=',;-\t')
                    except:
                        print("Delimiter Error: could not determine delimiter, consider",\
                        "specifying using template")
                        exit(0)
                    csvfile.seek(0)
                    f = csv.reader(csvfile, dialect)
                    for row in f:
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
        for index, row in enumerate(self.raw_data):
            if len(row) != len(self.raw_data[0]):
                self.invalid_rows.append(["%s: %d" % ("Line", index + 1)])
           #     print(self.invalid_rows)
                count = count + 1
            else:
                self.valid_rows.append(row)
                self.invalid_rows_pos.append(count)
    #    print("Invalid row pos: ", self.invalid_rows_pos)

    def create_columns(self):
        """For each row in raw_data variable, assigns the first value to the 
        headers variable and creates a Column object with that header provided.
        Then removes header row from valid_rows. (Todo: Maybe can read straight 
        from valid rows? Why/Why not?). Then for each row in valid_rows,
        populates relevant column object with row data.
        """
        if self.header_row >=0:
            for value in self.raw_data[self.header_row]:
                self.columns.append(Column(header=value))
              #  self.headers.append(value)
            self.valid_rows.pop(self.header_row)            

        length = len(self.valid_rows)
        for row_num in range(self.data_start, length):
            for index, value in enumerate(self.valid_rows[row_num]):
                self.columns[index].values.append(value)

    def clean(self):
        """Calls cleaning methods on all columns."""
        for column in self.columns:
            column.change_misc_values()
            column.drop_greater_than()

    def analysis(self):
        for colNo, column in enumerate(self.columns):
             if not column.empty:
                if column.type in self.analysers:
                    column.analysis = self.analysers[column.type](column.values)  
            
    def find_errors(self):
        for colNo, column in enumerate(self.columns):
             if not column.empty:
                column.define_errors(colNo, self.errors, self.formatted_errors, self.invalid_rows_pos)

    def pre_analysis(self):
        """Calls analysis methods on all columns, checking if they are empty
        first. First defines their least and most common elements, then if 
        column is not empty defines its type, any outliers and finally checks
        for any errors.
        """
        
        for colNo, column in enumerate(self.columns):
            column.define_most_least_common()
            if not column.empty:
                if self.template != None and colNo in self.template.columns:
                    column.set_type(self.template.columns[colNo])
                else:
                    column.define_type()
                if column.type == 'Identifier' and self.data_size != None and \
                    colNo in self.data_size:
                    column.set_size(self.data_size[colNo])                     
