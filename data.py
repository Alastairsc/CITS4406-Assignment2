#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Reads CSV file for information, provides basic cleaning of data and then
runs analysis on said data.
"""

import csv
import os

try:
    from .analyser import *
    from .column import *
except SystemError:
    from analyser import *
    from column import *


num_headers = 1
re_separation = re.compile('[\|\\\;\s\t-]+')

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
        
        analysis -- Calls column analysis methods to run 'analysis' on all columns.
        
        find_errors -- Iterates through all columns in the Data object and calls these columns
        define_errors function.
        
        pre_analysis -- Iterates through a Data objects columns and first defines their least
        and most common elements, then if template is supplied, sets the type of the column to
        match the template, if not if column is not empty defines its type, and if it's a
        Identifier data type sets the columns size to me no more than data_size.
        
        gen_file -- Generates a csv file based on the data for after data has been corrected.
    
        get_row -- Returns the value of a given row in a list.
        
        change_row -- Edits a row of the data to a given value.
        
        getCellErrors -- Returns list of all cells containing invalid data, contains
        row number,. column number and its value.
        
        getRowErrors -- Returns a list of all row errors
        
        getColumns -- Returns a list of all columns
        
        get_column -- Returns a column of the Data given a column number.
        
        get_headers -- Returns the header row of the data.
    
        set_headers -- Given a map of column numbers to header names, maps the column headers
        to the correct value.
    
        clear_errors -- Clears Data.errors and Data.formatted_errors to allow find_errors()
        to be rerun.
    
        rebuild_raw_data -- Recreates raw_data from Data's columns and row.
        
        delete_invalid_row -- Deletes given invalid row at the index from the data.

        delete_column -- Deletes a given column

    Variables:
    
    	analysers -- Dictionary conataining types as keys and their respective
    	analysers as values (i.e. analysers['type'] == TypeAnalyser

        types -- Tuple containing all valid types as ordered pairs of form
        ('Type', 'Human readable type'). Used to map types on web site to their 
        correct progammatic name.

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
                
        template -- The template containing various settings.
        
        delimiter_type -- The delimiter used in the csv file (space, comma, tab, colon etc)
        
        header_row -- The row the headers (non-used data) is on.
        
        self.data_start -- The row the used data starts on.
        
        data_size -- The length all Identifier types Strings should be.
        
        ignore_empty -- A boolean stating whether empty columns should be skipped.
        
        std_devs_val -- The amount of standard deviations from the mean a value should be
        before it is counted as an error i.e. (mean +- std_devs_val * std_dev)
        
        range_list -- A list representing the minimum and maximum allowed values for any
        numeric data, outside of which it is an error. Formatted (min, max).
        
        set_ignore -- A set of integers representing columns to ignore empty values in.

        delete_set -- List of columns to be deleted

        deleted_col -- List of columns that have been deleted, for writing to template
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
            ('Numeric', 'Number'),
            ('Sci_Notation', 'Scientific notation'),
            ('String', 'String'),
            ('Time', 'Time'),
            ('Ignored', 'Ignored / not detected')
        )
    
    def __init__(self, *args, online=False):
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
        self.online = online
        
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
        self.delete_set = []
        self.deleted_col = []
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
            self.delete_set = self.template.delete_set
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
                    print("Delimiter Warning: could not determine delimiter, consider",
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
       #print('Raw data: ', sys.getsizeof(self.raw_data))

                
    def remove_invalid(self):
        """For each row in raw_data variable, checks row length and appends to 
        valid_rows variable if same length as headers, else appends to 
        invalid_rows variable. invalid_rows_indexes holds the amount of rows that have been
        skipped by the point the xth row has been accessed from valid_rows.
        """
        count = 0
        preamble = []
        self.invalid_rows.clear()
        self.invalid_rows_pos.clear()
        self.invalid_rows_indexes.clear()
        self.formatted_invalid_rows.clear()
        self.valid_rows.clear()
        self.invalid_rows_pos.clear()
        if self.data_start != 0:
            for row in range(0, self.data_start):
                preamble.append(self.raw_data.pop(0))
        preamble[self.header_row], empty_col = self.trim_header(preamble[self.header_row])
        row_length = len(preamble[self.header_row])
        for index, row in enumerate(self.raw_data):
            row = self.trim_row(row, empty_col)
            if len(row) != row_length:
                self.invalid_rows_indexes.append( index)
                self.formatted_invalid_rows.append(["%s: %d" % ("Line", index + 1)])
                self.invalid_rows.append(row)
                self.raw_data[index].clear()
                count += 1
            else:
                self.valid_rows.append(row)
                self.invalid_rows_pos.append(count)
                self.raw_data[index].clear()
        self.raw_data = preamble
        self.can_edit_rows = True

    def trim_header(self, row):
        """
        Trims empty cells from both ends of the header row
        :param row:
        :return trimmed header row and list of empty columns:
        """
        new_row = []
        empty_col = []
        for i, cell in enumerate(row):
            if cell != "":
                new_row.append(cell)
            else:
                empty_col.append(i)
        return new_row, empty_col

    def trim_row(self, row, empty_col):
        """
        Trims empty cells from row
        :param row:
        :return trimmed row:
        """
        new_row = []
        for i, cell in enumerate(row):
            if cell != "" or i not in empty_col:
                new_row.append(cell)
        return new_row

    def create_columns(self):
        """For each row in raw_data variable, assigns the first value to the 
        headers variable and creates a Column object with that header provided.
        Then removes header row from valid_rows. Then for each row in valid_rows,
        populates relevant column object with row data.
        """
        if self.columns:
            self.columns.clear()
        if self.header_row >=0:
            i = 1
            for value in self.raw_data[self.header_row]:
                tmp_list = []
                tmp_list.append(value)
                tmp_list.append(" (Column ")
                tmp_list.append(str(i))
                tmp_list.append(")")
                s = ''.join(tmp_list)
                i += 1
                self.columns.append(Column(self.online,header=s))
        length = len(self.valid_rows)
        for row_num in range(0, length):
            for index, value in enumerate(self.valid_rows[row_num]):
                self.columns[index].add_value(value)
            self.valid_rows[row_num].clear()
        self.valid_rows = []
        if self.delete_set:
            for colNo in self.delete_set:
                self.columns[colNo].delete_col()
                self.deleted_col.append(colNo)
            self.delete_set.clear() #only do once
        #self.invalid_rows = [] #dont for reversibility but uses more memory
        #self.invalid_rows_indexes = []
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
            if not column.empty and column.type in self.analysers:
                column.define_most_least_common()
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
             if not column.empty and not column.type == 'Ignored':
                column.define_errors(colNo, self.errors, self.formatted_errors, self.invalid_rows_pos, self.range_list, self.set_ignore, self.data_start)


    def pre_analysis(self):
        """First defines their least and most common elements, then if 
        template is supplied, sets the type of the column to match the template, if not if 
        column is not empty defines its type, and if it's a special data type sets the columns
        size to me no more than data_size.
        """             
        for colNo, column in enumerate(self.columns):
            column.define_most_least_common()
            if self.template != None and colNo in self.template.columns:
                column.set_type(self.template.columns[colNo])
                column.set_not_empty()
            else:
                column.define_type()
            if column.type == 'Identifier' and self.data_size != None and \
                colNo in self.data_size:
                column.set_Identifier_size(self.data_size[colNo])
            elif column.type == 'Integer' or column.type == 'Float' \
                        or column.type == 'Currency' or column.type == 'Sci_Notation' \
                        or column.type == 'Numeric':
                column.compatible = self.analysers[column.type].is_compatable(column.values)
            if self.ignore_empty:
                column.ignore_empty = True
        self.datatypes_are_defined = True

    def check_compatible(self):
        """Checks to see whether columns that are nummeric will be compatible with the numeric analyserss
        using the static analyser methods
        """
        for colNo, column in enumerate(self.columns):
            if column.type == 'Integer' or column.type == 'Float' \
                    or column.type == 'Currency' or column.type == 'Sci_Notation' \
                    or column.type == 'Numeric':
                column.compatible = self.analysers[column.type].is_compatable(column.values)
            else:
                column.compatible = True
        
    def get_row(self, row_num):
        """
        Returns the values of a row in list
        
           Keyword Arguments:
               
               row_num -- The row number to be fetched       
        """
        row = []
        for colNo, column in enumerate(self.columns):
            row.append(column.values[row_num])
        return row
        
    def change_row(self, row_num, new_values):
        """
        Edits a row of the data to a given value.
            Keyword Arguments:
                
                row_num - number of row being changed
                
                new_values - list of values row is to be changed to
        """
        for colNo, column in enumerate(self.columns):
            column.values[row_num] = new_values[colNo - 1]
        
    def gen_file(self, filePath=""):
        """
        Generates a csv file based on the data for after data has been corrected
        
            Keyword Arguments:
            
                filePath -- Name of file to be generated.   
        """
        fileLocation = os.path.join( filePath, os.path.splitext(self.filename)[0]) + "_corrected.csv"
        new_file = open(fileLocation, "w")
        #Write header rows
        for rowNo in range(0, self.data_start):
            row_len = len(self.raw_data[rowNo])
            for i, cell in enumerate(self.raw_data[rowNo]):
                if i not in self.deleted_col:
                    new_file.write(cell)
                    if(i == row_len - 1):
                        new_file.write("\n")
                    else:
                        new_file.write(",")
                elif(i == row_len - 1):
                    new_file.write("\n")
        num_rows = 0
        for col in self.columns:
            if not col.deleted: #get length of any column not deleted
                num_rows = len(col.values)
                break
        row_len = len(self.columns)
        for rowNo in range(0, num_rows):
            for colNo, column in enumerate(self.columns):
                if not column.deleted:
                    new_file.write(column.values[rowNo])
                    if(colNo == row_len - 1):
                        new_file.write("\n")
                    else:
                        new_file.write(",")
                elif(colNo == row_len - 1):
                    new_file.write("\n")
        new_file.close()
        return fileLocation
        
    def getCellErrors(self):
        """
            Returns list of all cells containing invalid data, contains
            row number,. column number and its value.
        """
        return self.errors
        
    def getRowErrors(self):
        """
            Returns a list of all row errors
        """
        return self.invalid_rows
        
    def getColumns(self):
        """
            Returns a list of all columns
        """
        return self.columns
        
    def get_column(self, colNo):
        """
            Returns a column of the data given a column number
        """
        return self.columns[colNo]
    
    def get_headers(self):
        """
            Returns the headers of data
        """
        return self.raw_data[self.header_row]
    
    def set_headers(self, header_map):
        """
            Sets headers of columns taking a dictionary 
            mapping column numbers to headers.
            
                Keyword Arguments:
                    header_map -- A map of column numbers to headers.
        """
        for colNo, header in header_map:
            self.raw_data[self.header_row][colNo] = header
    
    def clear_errors(self):
    	"""
    	    Wipes recorded errors to allow find_errors() to be rerun
    	"""
    	self.errors.clear()
    	self.formatted_errors.clear()
    	#self.invalid_rows = []              
        
    def rebuild_raw_data(self):
        """
            Re creates raw_data from Data's rows.
        """
        #if self.can_edit_rows == True:
        invalid_pos = 0
        valid_pos = 0
        total_rows = len(self.valid_rows) + len(self.invalid_rows)
        for i in range(0, total_rows):
            if self.valid_rows and invalid_pos == self.invalid_rows_pos[valid_pos]:
                self.raw_data.append(self.valid_rows.pop(0))
                valid_pos += 1
            elif self.invalid_rows:
                self.raw_data.append(self.invalid_rows.pop(0))
                invalid_pos += 1
        self.invalid_rows_pos.clear()
        self.invalid_rows_indexes.clear()
        self.formatted_invalid_rows.clear()
        self.can_edit_rows == False
        #else:
        #   raise RuntimeWarning('function Data.rebuild_raw_data() called after create_columns() or before remove_invalid()')
    
    def rebuild_rows(self):
        """
            Recreates raw data from the data's columns
        """
        total_rows = len(self.columns[0].values)
        for i in range(0, total_rows):
            row = []
            for col in self.columns:
                row.append(col.values[i])
            self.valid_rows.append(row)
        self.columns = []
        
    def delete_invalid_row(self, invalid_row_index):
        """
            Deletes given invalid row at the index from the data.
            
                Keyword Arguments:
                    
                    invalid_row_index -- Index of invalid row to be deleted.
        """
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

    def delete_column(self, colNo):
        self.deleted_col.append(colNo)
        self.columns[colNo].deleted = True
        self.columns[colNo].values = []

