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
from statistics import mean, mode, median_low, median, median_high, stdev, \
    StatisticsError, Decimal
from scipy.stats import mstats
from numpy import array
from email.utils import parseaddr



#  Config
threshold = 0.9
enum_threshold = 1
standardDeviations = 3
invalid_values = ['-', '*', '_', '$']
re_float = re.compile('^-?\d*?\.\d+$')
re_int = re.compile('^\s*[1-9]\d*$')
re_email = re.compile('@')
re_currency = re.compile('(^\s*((-?(\$|€|£))|((\$|€|£)-?))(\d*\.\d*|\.\d*|\d*))')
re_boolean = re.compile('^\s*T$|^\s*F$|^\s*True$|^\s*False$|^\s*Y$|^\s*N$|^\s*Yes$|^\s*No$', re.I)
re_sci_notation= re.compile('-?(\d+(\.\d*)?|\d*\.\d+)([eE][+\-]?\d+)?')
"""^\s*\$d*\."""
re_separation = re.compile('[\s,;]+')

class Analyser(object):
    """Base analysis class object. Initiate the object, and assigns the 
    statistical mode, if any.
    
    Class variables:
    mode -- Returns the mode of the column analysed.
    
    Child Classes and associated variables:
    StringAnalyser -- String column analysis.
    EmailAnalyser -- Email column analysis.
    EnumAnalyser -- Enumerated column analysis.
    NumericalAnalyser -- String/Float column analysis.
        min -- Minimum value in column values.
        max -- Maximum value in column values.
        mean -- Mean value in column values.
        median_low -- Low median for column values.
        median -- Median value for column values.
        median_high -- High median for column values.
        normDist -- String Yes/No if columns value is normally distributed.
        stdev -- Standard deviation for column values, N/A if not normally distributed to
                    to within 95.5% confidence.
        stDevOutliers -- List of values outside a certain number of standard deviations
                        from the mean.
    CurrencyAnalyser -- Child class of NumericalAnalyser
    BooleanAnalyser -- Boolean column analysis
    """
    def __init__(self, values):
        try:
            self.mode = mode(values)
        except StatisticsError:
         #   print(values)
            print("Statistics error")
            self.mode = 'N/A'

class EmailAnalyser(Analyser):
    "Run email analysis"
    def __init__(self, values):
        super().__init__(values)
        print(self.mode)
        # TODO Something actually useful for emails.
        
class NumericalAnalyser(Analyser):
    """Runs numeric analysis."""
    def __init__(self, values): 
        new_values = []
        for i in values:
            if i != '':
                new_values.append(eval(i))
        values = new_values
       # values = [eval(i) for i in values]
        super().__init__(values)
        self.stDevOutliers = []
        self.pval = mstats.normaltest(array(values))[1]
        self.min = min(values)
        self.max = max(values)
        self.mean = Decimal(mean(values)).quantize(Decimal('.00000'))
        self.median_low = median_low(values)
        self.median = median(values)
        self.median_high = median_high(values)
        self.stdev = Decimal(stdev(values)).quantize(Decimal('.00'))
        self.normDist = 'No'
        if(self.pval < 0.055):
            self.normDist = 'Yes'
        if self.normDist != 'No':
            for value in values:
                if value < (self.mean - standardDeviations * self.stdev) or \
                value > (self.mean + standardDeviations * self.stdev):                
                    self.stDevOutliers.append(value)
        
class CurrencyAnalyser(NumericalAnalyser):
    "Run currency analysis, calls NumericalAnalyser as a superclass"
    def __init__(self, values):
        """for x, value in enumerate(self.values):
            try:
                value[x] = eval(self.values[x])
            except SyntaxError:"""
        super().__init__(values)

class StringAnalyser(Analyser):
    """Run string analysis."""
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some string exclusive statistics.


class EnumAnalyser(Analyser):
    """Run enumeration analysis."""
    def __init__(self, values):
        super().__init__(values)
        #  TODO Implement some enum exclusive statistics.
                             
class BooleanAnalyser(Analyser):
    "Run email analysis"
    def __init__(self, values):
        super().__init__(values)

class Sci_NotationAnalyser(NumericalAnalyser):
    """Run Scientific notation analysis."""
    def __init__(self, values):
        super().__init__(values)

class Column(object):
    """Object to hold data from each column within the provided CSV file.
    
    Methods:
    change_misc_values -- Removes misc/unclear values from column 
        values.
    drop_greater_than -- Removes '<', '>' from column values.
    define_most_common -- Sets object variable to hold 15 most common values
        for that column.
    define_type -- Sets object variable to type (e.g., String) according
        to column values.
    define_least_common -- Sets object variable to hold 15 least common values 
        for that column.
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
        
        

    def define_most_common(self):
        """Set 15 most common results to class variable, and set object variable 
        empty if appropriate.
        """
        self.most_common = Counter(self.values).most_common(15)
        if self.most_common[0][0] == '' \
                and self.most_common[0][1] / len(self.values) >= threshold:
            self.empty = True
            
    def define_least_common(self):
        """Set 15 least common results to class variable, and set object variable
        empty if appropriate.
        """
        commonList = Counter(self.values).most_common()
        for i, e in reversed(list(enumerate(commonList))):
            if i < 15:
                self.least_common.append(e)
        if self.least_common[0][0] == '' \
            and self.least_common[0][1] / len(self.values) >= threshold:
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
             #   print('Boolean match')
            elif re_sci_notation.fullmatch(value):
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
       # print("Errors: ", errors)


        
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
        and value of the error
    raw_data -- List of raw CSV data as rows.
    valid_rows -- List of valid rows (i.e., same number of columns as headers).
    errors -- List of rows and columns of possibly incorrect values.
    """
    def __init__(self, csv_file):
        self.columns = []
        self.headers = []
        self.invalid_rows = []
        self.invalid_rows_pos = []
        self.errors = []     
        self.formatted_errors = []
        self.raw_data = []
        self.valid_rows = []
        self.read(csv_file)
        self.remove_invalid()
        self.create_columns()

    def read(self, csv_file):
        """Opens and reads the CSV file, line by line, to raw_data variable."""
        #f = csv.reader(open(csv_file))
        #for row in f:
        #    self.raw_data.append(row)

        #SEPARATION
        """When data in csv files are in one column separated by comma, semicolon, or space, they are
        separated accordingly"""
        #new_csv = open(csv_file)
        f = csv.reader(open(csv_file))
        #for row in f:
        for line in f:
            n_col = len(line)
            #print(n_col)
            if n_col == 1:
                result = re.split(re_separation, line[0])
                self.raw_data.append(result)
                #print(self.raw_data)
            else:
                self.raw_data.append(line)
                #print(self.raw_data)

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
        for value in self.raw_data[0]:
            self.columns.append(Column(header=value))
            self.headers.append(value)
        self.valid_rows.pop(0)

        for row in self.valid_rows:
            for index, value in enumerate(row):
                self.columns[index].values.append(value)

    def clean(self):
        """Calls cleaning methods on all columns."""
        for column in self.columns:
            column.change_misc_values()
            column.drop_greater_than()

    def analyse(self):
        """Calls analysis methods on all columns, checking if they are empty
        first. First defines their least and most common elements, then if 
        column is not empty defines its type, any outliers and finally checks
        for any errors.
        """
        analysers = {'String': StringAnalyser, 'Integer': NumericalAnalyser,
                     'Float': NumericalAnalyser, 'Enum': EnumAnalyser, 
                     'Email': EmailAnalyser, 'Currency': CurrencyAnalyser,
                     'Boolean': BooleanAnalyser, 'Sci_Notation': Sci_NotationAnalyser}
        for colNo, column in enumerate(self.columns):
            column.define_most_common()
            column.define_least_common()
            if not column.empty:
                column.define_type()
                column.define_errors(colNo, self.errors, self.formatted_errors, self.invalid_rows_pos)
                if column.type in analysers:
                    column.analysis = analysers[column.type](column.values)       
