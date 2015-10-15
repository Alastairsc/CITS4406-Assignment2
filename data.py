#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Reads CSV file for information, provides basic cleaning of data and then
runs analysis on said data."""

import sys
import os
import csv
import re
from collections import Counter
try:
	from .analyser import *
except SystemError:
	from analyser import *

threshold = 0.9
enum_threshold = 1
num_headers = 1

#  Config
invalid_values = ['-', '*', '_', '$']
re_float = re.compile('^-?\d*?\.\d+$')
re_int = re.compile('^\s*-?\d+$')
re_email = re.compile('@')
re_currency = re.compile('^(\s*((-?(\$|€|£))|((\$|€|£)-?))(\d*\.\d*|\.\d*|\d*))')
re_boolean = re.compile('^\s*T$|^\s*F$|^\s*True$|^\s*False$|^\s*Y$|^\s*N$|^\s*Yes$|^\s*No$', re.I)
re_sci_notation= re.compile('\s*[\+-]?(\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?')
re_separation = re.compile('[\|\\\;\s\t-]+')
re_date = re.compile('^((31(\/|-)(0?[13578]|1[02]))(\/|-)|((29|30)(\/|-)(0?[1,3-9]|1[0-2])(\/|-)))((1[6-9]|[2-9]\d)?\d{2})$|^(29(\/|-)0?2(\/|-)(((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))))$|^(0?[1-9]|1\d|2[0-8])(\/|-)((0?[1-9])|(1[0-2]))(\/|-)((1[6-9]|[2-9]\d)?\d{2})$')
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
        self.unique = -1
        self.total_true = 0
        self.total_false = 0
        self.total_yes = 0
        self.total_no = 0
        self.data_size = -1
        self.ignore_empty = False


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
        
    def uniqueCount(self, values):
        """Return the amount of unique values in the values list.
        
        Keyword arguments:
            values -- A list of values.
        """
        valSet = set()
        for vals in values:
            valSet.add(vals)
        return len(valSet) 

    def define_most_least_common(self):
        """Set 15 most common results to class variable, and set object variable 
        empty if appropriate.
        """
        self.unique = self.uniqueCount(self.values)
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
        if self.unique == len(self.values) or self.unique == 1:
            self.least_common = []
            self.most_common = []
        

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
        
        for x, value in enumerate(self.values):
            if re_float.match(value):                
                if abs(float(value)) < 0.000001:
                    sci_not_count +=1
                else:
                    float_count += 1
            elif re_int.match(value) or value == '0':
                if abs(int(value)) > 1000000:
                    sci_not_count += 1
                else:
                    int_count += 1
                    value = value.strip()
            elif re_email.search(value):
                if parseaddr(value)[1] != '':
                    email_count += 1
            elif re_currency.search(value):
                self.values[x].replace('"', '')
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
                #These are also chars
                if temp_value == 'T' or temp_value == 'F' or temp_value == 'Y' or temp_value == 'N':
                    char_count +=1
            elif re_sci_notation.fullmatch(value):
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
        elif sci_not_count / num_values >= threshold:
            self.type = 'Sci_Notation'
        elif (float_count + int_count + sci_not_count) / num_values >= threshold:
            self.type = 'Numeric'
        elif email_count / num_values >= threshold:
            self.type = 'Email'
        elif currency_count / num_values >= threshold:
            self.type = 'Currency'
        elif boolean_count / num_values >= threshold:
            self.type = 'Boolean'
        elif date_count / num_values >= threshold:
            self.type = 'Date'
        elif time_count / num_values >= threshold:
            self.type = 'Time'
        elif char_count / num_values >= threshold:
            self.type = 'Char'
        elif day_count / num_values >= threshold:
            self.type = 'Day'
        elif hyper_count / num_values >= threshold:
            self.type = 'Hyperlink'
        elif len(self.most_common) < 10 and len(self.most_common) != 0:
            self.type = 'Enum'
        else:
            self.type = 'String'


    def define_errors(self, columnNumber, errors, formatted_errors, invalid_rows_pos, range_list2, set_to_ignore, data_start):
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
        if self.type == 'Ignore':
            pass  
        elif self.type == 'Float':
            for x, value in enumerate(self.values): 
                if (value == "" and self.ignore_empty) or (len(value) == 0 and columnNumber in set_to_ignore):
                    continue          
                if not re_float.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a decimal number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
                elif len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
        elif self.type == 'Integer':
            for x, value in enumerate(self.values):
                if (value == "" and self.ignore_empty) or (len(value) == 0 and columnNumber in set_to_ignore):
                    continue
                if not re_int.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not an integer'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

                if len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
        elif self.type == 'Numeric':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue
                if not re_int.match(value) and not re_float.match(value) and not re_sci_notation.match(value) and not value == '0'\
                and not  self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                try:
                    if float(value) < -6.00E+58 or 6.00E+58 < float(value):
                        reason = 'too large or too small'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        self.updateCell(x, '')
                except:
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
                if len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        
        elif self.type == 'Email':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue
                if not re_email.search(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    if parseaddr(value)[1] == '':
                        reason = 'not an email'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        
        elif self.type == 'Boolean':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and ColumnNumber in set_to_ignore):
                    continue
                if not re_boolean.match(value) and not  self.check_empty(x, value, columnNumber,\
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised yes/no type'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
        elif self.type == 'Currency':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue
                if not re_currency.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised currency'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))                  

                    
        elif self.type == 'String':
            for x, value in enumerate(self.values):
                self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore)
                    
        elif self.type == 'Enum':
            for x, value in enumerate(self.least_common):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue  
                if self.least_common[x][1] <= 1 and not  self.check_empty(x, value, columnNumber,\
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    i = 0 
                    freq = 0
                    for cell in self.values:
                        if cell == value[0]:
                            reason = 'Low frequency of enum value: (%s)' % self.least_common[x][1]
                            tup = (x + invalid_rows_pos[x] + self.data_start, columnNumber, value[0], reason)
                            errors.append(tup)
                            formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                            freq += 1
                        i+=1
                    if freq == 0:
                         raise Exception('Least common value not found')
                         
        elif self.type == 'Sci_Notation':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue
                if not re_sci_notation.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not scientific notation'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                try:
                    if float(value) < -6.00E+76 or 6.00E+76 < float(value):
                        reason = 'too large or too small'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        self.updateCell(x, '')
                except:
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                    
        elif self.type == 'Identifier':
            if self.data_size != -1:
                size = self.data_size
            else:
                size = len(self.values[0])
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue
                if len(value) != size and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'too long or too short'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
        elif self.type == 'Date':
            for x, value in enumerate(self.values):       
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue    
                if not re_date.match(value) and not  self.check_empty(x, value, columnNumber,\
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised date'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Time':
            for x, value in enumerate(self.values):
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue           
                if not re_time.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised time'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Char':
            for x, value in enumerate(self.values):    
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue       
                if not re_char.match(value) and not  self.check_empty(x, value, columnNumber, \
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised character'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Day':
            for x, value in enumerate(self.values):           
                if not re_day.match(value) and not  self.check_empty(x, value, columnNumber,\
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised day'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Hyperlink':
            for x, value in enumerate(self.values):     
                if (value == '' and self.ignore_empty) or (value == '' and columnNumber in set_to_ignore):
                    continue      
                if not re_hyper.match(value) and not  self.check_empty(x, value, columnNumber,\
                errors, formatted_errors, invalid_rows_pos, set_to_ignore):
                    reason = 'not a recognised hyperlink'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append("Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

    def check_empty(self, x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore):
        """Checks whether the value in a cell is empty
        Keyword arguments:
            x -- postion of cell in column
            
            value -- value in cell"""
        if ((value == '' or value == ' ') and self.ignore_empty) or \
            ((value == '' or value == ' ') and columnNumber in set_to_ignore):
            return True
        elif value == '' or value == ' ':
            reason = 'empty cell'
            tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
            errors.append(tup)
            formatted_errors.append("Row: %d Column: %d  - %s" % (tup[0] + 1, tup[1] + 1, reason))
            return True
        else:
            return False
            
    def set_type(self, type):
        """Sets type of column for use with templates"""
        self.type = type

    def set_size(self, size):
        """Sets the size of the data for use when checking for errors.
            For use with the 'Identifier' data type
            
            size -- length of identifier"""
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
        
    def set_Identifier_size(self, size):
        """Sets the size of the data for identifier type"""
        self.data_size = size
    
    def updateCell(self, pos, new_value):
        """Changes the value of a cell given
        
            pos -- position of cell in column to change
            
            new_value -- value to set cell too"""
        self.values[pos] = new_value
    
        
class Data(object):
    """Main store for CSV data, reading the data from the CSV file and then 
    assigning out to relevant variables.
    
    Global variables:
        threshold -- The percentage threshold which the column must have of a type before
        it is declared that type.
        
        enum_threshold -- The integer threshold which if the count of occurence of a value is
        less than the value is declared an error.
    
    Methods:
        read -- Reads the CSV file and outputs to raw_data variable.
        
        remove_invalid -- Reads from raw_data variable and assigns rows to 
        valid_rows or invalid_rows according to their length.
        
        create_columns -- Creates column object according to valid_rows, assigning
        column header and column values.
        
        clean -- Calls column cleaning methods to run 'cleaning' on all columns.
        
        analysis -- Calls column analysis methods to run 'analysis' on all columns.
    
    Variables:
    
    	analysers -- Dictionary conataining types as keys and their respective
	analysers as values (i.e. analysers['type'] == TypeAnalyser
	
	types -- Tuple containing all valid types as ordered pairs of form 
	('Type', 'Human readable type'). Used to map types on web site
	to their correct progammatic name.
	
    	Filename -- String of path to file containing data
    	
        columns -- List of column objects.
        
        invalid_rows -- List of invalid rows (i.e., more or less columns than
        number of headers). Copied from raw_data
        
        invalid_rows_indexes -- List of indexes corresponding to invalid rows.

        formatted_invalid_rows -- List of invalid rows for report.
        
        invalid_rows_pos -- List of the amount of invalid rows in the raw data prior
        to each valid row (i.e. the nth element contains number of invalid rows
        prior to the nth valid row)
        
        errors -- list of errors in file; errors[n][0] is row of error, errors[n][1]
        is column of error, errors[n][2] is the value of in that location, 
        errors[n][3] is the reason for the error & error[4] is the index for the
        value in columns[n1].values.
        
        formatted_errors -- List of errors in file, each error contains: row, column 
        and value of the error.
        
        raw_data -- List of raw CSV data as rows. After remove_invalid() has run
        this only contains rows from the CSV file prior to the start of the data.
        
        valid_rows -- List of valid rows (i.e., same number of columns as headers).
        
        can_edit_rows -- is a boolean value true after remove_invalid() and before
        create_columns() have been run only. It defines whether rebuild_raw_data()
        and delete_invalid_row() may be called.
        
        data_in_columns -- is a boolean true after create_columns() is completed,
        it defines whether the Data object is in a form gen_file() expects.
        
        datatypes_are_defined -- is a boolean true after pre_analysis() has been
        run and each column's type is defined. It defines whether export_datatypes()
        may be run.
        
    """
    analysers = {
        'String': StringAnalyser,
        'Integer': NumericalAnalyser,
        'Float': NumericalAnalyser,
        'Enum': EnumAnalyser, 
        'Email': EmailAnalyser,
        'Currency': CurrencyAnalyser,
        'Boolean': BooleanAnalyser,
        'Sci_Notation': SciNotationAnalyser,
        'Identifier': IdentifierAnalyser,
        'Date': DateAnalyser,
        'Time': TimeAnalyser,
        'Char': CharAnalyser,
        'Day': DayAnalyser,
        'Hyperlink': HyperAnalyser, 
        'Numeric': NumericalAnalyser
        }
    types = (
            ('Boolean', 'Boolean'),
            ('Char', 'Character'),
            ('Currency', 'Currency'),
            ('Date', 'Date'),
            ('Day', 'Day of the Week'),
            ('Email', 'Email Address'),
            ('Enum', 'Enumerable Set'),
            ('Float', 'Decimals only'),
            ('Hyperlink', 'Hyperlink'),
            ('Identifier', 'Identification code'),
            ('Integer', 'Integers only'),
            ('Numeric', 'Real numbers'),
            ('Sci_Notation', 'Scientific notation'),
            ('String', 'String'),
            ('Time', 'Time'),
            ('Ignored', 'Ignored / not detected')
        )
    
    def __init__(self, *args):
        """Can take up to two arguments, 
            first argument -- filename
            second argument -- template"""

        self.filename = args[0]
        self.columns = []
        self.invalid_rows = []
        self.invalid_rows_indexes = []
        self.formatted_invalid_rows = []
        self.invalid_rows_pos = []
        self.errors = []     
        self.formatted_errors = []
        self.raw_data = []
        self.can_edit_rows = False
        self.data_in_columns = False
        self.datatypes_are_defined = False
        self.valid_rows = []

        
        #Template settings
        self.template = None
        self.delimiter_type = ''
        self.header_row = 0
        self.data_start = 1
        self.data_size = {}
        self.ignore_empty = False
        self.std_devs_val = 3
        self.range_list = []
        self.set_ignore = set()
        if len(args) > 1:  
            self.template = args[1]
            self.delimiter_type = self.template.delimiter_type
            self.header_row = self.template.header_row
            self.data_start = self.template.data_start
            self.data_size = self.template.data_size
            self.ignore_empty = self.template.ignore_empty
            threshold = self.template.threshold_val
            enum_threshold = self.template.enum_threshold_val
            self.std_devs_val = self.template.std_devs
            self.range_list = self.template.range_vals
            self.set_ignore = self.template.ignore_set
        #Process data
        self.read(self.filename)
        

    def read(self, csv_file):
        """Opens and reads the CSV file, line by line, to raw_data variable.
        
        Keyword arguments:
            csv_file -- The filename of the file to be opened.
        """
        #f = csv.reader(open(csv_file))
        #for row in f:
        #    self.raw_data.append(row)
        #separation of comma, semicolon, dash, tab delimited csv files
        if self.delimiter_type == '':
            with open(csv_file,'rU', newline='', encoding='ISO-8859-1') as csvfile:
                try:
                    #dialect = csv.Sniffer().sniff(csvfile.read(), delimiters='space,;-\|\t\\')
                    #csvfile.seek(0)
                    #f = csv.reader(csvfile, dialect)
                    #NEW SPLIT DELIMITER
                    f = csv.reader(csvfile)
                    for line in f:
                        n_col = len(line)
                        if n_col == 1:
                            result = re.split(re_separation, line[0])
                            self.raw_data.append(result)
                            delimiter_search = re.search(re_separation, line[0]).group(0)   #NEW
                            if delimiter_search == ' ':
                                self.delimiter_type = 'Space'
                            elif delimiter_search == '\t':
                                self.delimiter_type = 'Tab'
                            else:
                                self.delimiter_type = delimiter_search   #NEW
                        else:
                            self.raw_data.append(line)
                            self.delimiter_type = ','   #NEW

                except:
                    print("Delimiter Warning: could not determine delimiter, consider",\
                    "specifying using template. Continuing using comma")
                    csvfile.seek(0)
                    f = csv.reader(csvfile, delimiter=',')
                    self.delimiter_type = ','
                    for row in f:                          
                        self.raw_data.append(row)
        else:
            #template specified delimiter
            with open(csv_file, 'rU', encoding='ISO-8859-1') as csvfile:
                f = csv.reader( csvfile, delimiter=self.delimiter_type)
                for row in f:
                    self.raw_data.append(row)
                
    def remove_invalid(self):
        """For each row in raw_data variable, checks row length and appends to 
        valid_rows variable if same length as headers, else appends to 
        invalid_rows variable. invalid_rows_indexes holds the amount of rows that have been
        skipped by the point the xth row has been accessed from valid_rows.
        """
        count = 0
        preamble = []
        if self.data_start != 0:
            for row in range(0, self.data_start):
                preamble.append(self.raw_data.pop(0))
        row_length = len(preamble[self.header_row])
        for index, row in enumerate(self.raw_data):
            if len(row) != row_length:
                self.invalid_rows_indexes.append( index)
                self.formatted_invalid_rows.append(["%s: %d" % ("Line", index + 1)])
                self.invalid_rows.append(row)
                self.raw_data[index] = []
                count = count + 1
            else:
                self.valid_rows.append(row)
                self.invalid_rows_pos.append(count)
                self.raw_data[index] = []
        self.raw_data = preamble
        self.can_edit_rows = True

    def create_columns(self):
        """For each row in raw_data variable, assigns the first value to the 
        headers variable and creates a Column object with that header provided.
        Then removes header row from valid_rows. Then for each row in valid_rows,
        populates relevant column object with row data.
        """
        if self.header_row >=0:
            i = 1
            for value in self.raw_data[self.header_row]:
                tmp_list = []
                tmp_list.append(value)
                tmp_list.append(" (column ")
                tmp_list.append(str(i))
                tmp_list.append(")")
                s = ''.join(tmp_list)
                i = i + 1
                self.columns.append(Column(header=s))
        length = len(self.valid_rows)
        for row_num in range(0, length):
            for index, value in enumerate(self.valid_rows[row_num]):
                self.columns[index].values.append(value)
            self.valid_rows[row_num] = []
        self.valid_rows = []
        self.invalid_rows = []
        self.invalid_rows_indexes = []
        self.can_edit_rows = False
        self.data_in_columns = True
        
        
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
                    if( column.type == 'Integer' or column.type == 'Float' \
                        or column.type == 'Currency' or column.type == 'Sci_Notation' \
                        or column.type == 'Numeric'):
                        column.analysis = self.analysers[column.type](column.values, self.std_devs_val)  
                    else:
                        column.analysis = self.analysers[column.type](column.values)
        
    def find_errors(self):
        """Iterates through each column and finds any errors according to pre-determined
        conditions.
        """
        for colNo, column in enumerate(self.columns):
             if not column.empty:
                column.define_errors(colNo, self.errors, self.formatted_errors, self.invalid_rows_pos, self.range_list, self.set_ignore, self.data_start)
        
    def pre_analysis(self):
        """First defines their least and most common elements, then if 
        template is supplied, sets the type of the column to match the template, if not if 
        column is not empty defines its type, and if it's a special data type sets the columns
        size to me no more than data_size.
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
                    column.set_Identifier_size(self.data_size[colNo])
                if self.ignore_empty:
                    column.ignore_empty = True
        self.datatypes_are_defined = True
        
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
        
    def gen_file(self, filePath=""):
        """Generates a csv file based on the data for after
        data has been corrected"""
        fileLocation = os.path.join( filePath, os.path.splitext(self.filename)[0]) + "_corrected.csv"
        new_file = open(fileLocation, "w")
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
        new_file.close()
        return fileLocation
        
    def getCellErrors(self):
        """Returns list of all cells containing invalid data, contains
            row number,. column number and its value."""
        return self.errors
        
    def getRowErrors(self):
        """Returns a list of all row errors"""
        return self.invalid_rows
        
    def getColumns(self):
        """Returns a list of all columns"""
        return self.columns
        
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
    
    def clear_errors(self):
    	"""Wipes recorded errors to allow find_errors() to be rerun"""
    	self.errors = []
    	self.formatted_errors = []
    	#self.invalid_rows = []              
        
    def rebuild_raw_data(self):
        if self.can_edit_rows == True:
            invalid_pos = 0
            valid_pos = 0
            total_rows = len(self.valid_rows) + len(self.invalid_rows)
            for i in range(0, total_rows):
                if invalid_pos == self.invalid_rows_pos[valid_pos]:
                    self.raw_data.append(self.valid_rows.pop(0))
                    valid_pos += 1
                else:
                    self.raw_data.append(self.invalid_rows.pop(0))
                    invalid_pos += 1
            self.invalid_rows_pos = []
            self.invalid_rows_indexes = []
            self.formatted_invalid_rows = []
            self.can_edit_rows == False
        else:
            raise RuntimeWarning('function Data.rebuild_raw_data() called after create_columns() or before remove_invalid()')

    def delete_invalid_row(self, invalid_row_index):
        if self.can_edit_rows == True:
            row_index = self.invalid_rows_indexes[invalid_row_index]
            next_valid = row_index - invalid_row_index #Index of first valid row after removed invalid row in invalid_rows_pos
            for i in range(next_valid,len(self.invalid_rows_pos)):
                self.invalid_rows_pos[i] = self.invalid_rows_pos[i] - 1

            self.invalid_rows_indexes.pop(invalid_row_index)
            self.formatted_invalid_rows.pop(invalid_row_index)
            self.invalid_rows.pop(invalid_row_index)
        else:
            raise RuntimeWarning('function Data.rebuild_raw_data() called after create_columns() or before remove_invalid()')


