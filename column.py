#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Stores values of columns of the data, checks for errors in column.

Global Variables:
    threshold -- A float representing a percentage of which a columns values must be of a type
    before the column is declared to be of that type i.e. if 95% of the columns values are
    integers it will be of type Integer. Can be set via template, default 0.9 (90%).

    enum_threshold -- An integer representing the amount of times which a value in an Enumerable
    type column must appear for it to not be taken as an error. Can be set via template, default
    1.

    invalid_values -- Values which are pre-agreed not to appear in valid data and should be
    stripped. Currently not used.

    re_float -- Regular expression for float type.

    re_int -- Regular expression for integer type.

    re_email -- Regular expression for email type.

    re_currency -- Regular expression for currency type. Currently only supports ($,€,£) symbols.

    re_boolean -- Regular expression for boolean type.

    re_sci_notation -- Regular expression for scientific notation type.

    re_separation -- Regular expression for the different types of delimiters in files.

    re_date -- Regular expression for date type.

    re_time -- Regular expression for time type.

    re_char -- Regular expression for character type.

    re_day -- Regular expression for day type.

    re_hyper -- Regular expression for hyperlink type.

"""
import re
from collections import Counter
from email.utils import parseaddr


threshold = 0.9
enum_threshold = 1

#  Config
invalid_values = ['-', '*', '_', '$']
re_float = re.compile('^-?\d*?\.\d+$')
re_int = re.compile('^\s*-?\d+$')
re_email = re.compile('@')
re_currency = re.compile('^\(?(\s*((-?(\$|€|£))|((\$|€|£)-?))(\d*\.\d*|\.\d*|\d*))\)?')
re_boolean = re.compile('^\s*T$|^\s*F$|^\s*True$|^\s*False$|^\s*Y$|^\s*N$|^\s*Yes$|^\s*No$', re.I)
re_sci_notation= re.compile('\s*[\+-]?(\d+(\.\d+)?|\d*\.\d+)([eE][+\-]?\d+)?')

re_date = re.compile('^((31(\/|-)(0?[13578]|1[02]))(\/|-)|((29|30)(\/|-)(0?[1,3-9]|1[0-2])(\/|-)))((1[6-9]|[2-9]\d)?\d{2})$|^(29(\/|-)0?2(\/|-)(((1[6-9]|[2-9]\d)?(0[48]|[2468][048]|[13579][26])|((16|[2468][048]|[3579][26])00))))$|^(0?[1-9]|1\d|2[0-8])(\/|-)((0?[1-9])|(1[0-2]))(\/|-)((1[6-9]|[2-9]\d)?\d{2})$')
re_time = re.compile('(^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$)|(^(1[012]|0?[1-9]):[0-5][0-9](\ )?(?i)(am|pm)$)')
re_char = re.compile('^\D$')
re_day = re.compile('^(?i)(monday|tuesday|wednesday|thursday|friday|saturday|sunday)$')
re_hyper = re.compile('^(?i)(https?:\/\/).+$')

class Column(object):
    """Object to hold data from each column within the provided CSV file.

    Methods:
        change_misc_values -- Removes misc/unclear values from column values. Used in
        Data.clean() but this function is unused.

        drop_greater_than -- Removes '<', '>' from column values. Defined but unused.

        define_most_least_common -- Sets object variable to hold 15 most common values
        and least common values for that column.

        define_type -- Sets object variable to type (e.g., String) according
        to column values.

        define_errors -- Defines a list that contains the row and column of possibly
        incorrect values.

        check_empty -- Checks whether a provided cell in a column is empty or not.

        set_type -- Sets type of column for use with templates

        set_size -- Sets the size of the data for use when checking for errors, for use with
        the 'Identifier' data type.

        set_empty -- Sets a columns empty attribute to True.

        set_not_empty -- Sets a columns empty attribute to False.

        is_Empty -- Returns whether or not a columns empty attribute is True or False.

        set_Identifier_size -- Sets the size of the data for identifier type.

        updateCell -- Changes the value of a given cell with one provided.


    Variables:
        most_common -- List with the <= 15 most common results within the column values.

        least_common -- List with the <= 15 least common results within the column values.

        empty -- Boolean value of whether the column holds values or not.

        header -- String containing column header/title.

        type -- The type of data in column, e.g., String, Float, Integer,
        Enumerated, represented as a String.

        values -- List of CSV values for the column.

        analysis -- Analysis object associated with this column.

        unique -- Integer representing the amount of unique values in this column.

        total_true -- The amount of 'true' booleans in this column.

        total_false -- The amount of 'false' booleans in this column.

        total_yes -- The amount of 'yes' booleans in this column.

        total_no -- The amount of 'no' booleans in this column.

        data_size -- The length which all correct strings in this column should be.

        ignore_empty -- A boolean representing whether empty cells in this column should
        be ignored.

    """

    def __init__(self, header=''):
        self.compatible = True
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
        self.deleted = False

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
        self.most_common.clear()
        self.least_common.clear()
        self.unique = self.uniqueCount(self.values)
        temp_list = Counter(self.values).most_common()
        for i, e in list(enumerate(temp_list)):
            if i < 15:
                self.most_common.append(e)
        for i, e in reversed(list(enumerate(temp_list))):
            if i < 15:
                self.least_common.append(e)
        if not self.most_common \
                or (self.most_common[0][0] == "" and self.most_common[0][1] / len(self.values) >= threshold):
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
                    sci_not_count += 1
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
                # These are also chars
                if temp_value == 'T' or temp_value == 'F' or temp_value == 'Y' or temp_value == 'N':
                    char_count += 1
            elif re_sci_notation.fullmatch(value):
                sci_not_count += 1
            elif re_date.search(value):
                date_count += 1
            elif re_time.search(value):
                time_count += 1
            elif re_char.search(value):
                char_count += 1
            elif re_day.search(value):
                day_count += 1
            elif re_hyper.search(value):
                hyper_count += 1
        num_values = len(self.values)
        if self.empty:
            self.type = 'Ignored'
        elif float_count / len(self.values) >= threshold:
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

    def define_errors(self, columnNumber, errors, formatted_errors, invalid_rows_pos, range_list2, set_to_ignore,
                      data_start):
        """Define all the rows/columns with invalid values and append to errors, and
        formatted_errors once formatted properly.

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

            range_list2 -- A list with two values (min, max) respectively, if supplied in a
            template all values numeric values must fall between these two values or are an
            error.

            set_to_ignore -- A set containing integers representing columns set to ignore
            empty values in.

            data_start -- Integer representing the row actual data (not headers) starts on.
        """
        tup = ()
        # Column previously set to ignore, pass
        if self.type == 'Ignored':
            pass
        # What follows is each individual type with their error checking
        elif self.type == 'Float':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_float.match(value):
                    reason = 'not a decimal number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

                elif len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Integer':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_int.match(value):
                    reason = 'not an integer'
                    if not invalid_rows_pos:
                        print('Invalid Rows Empty')
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

                if len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Numeric':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_int.match(value) and not re_float.match(value) and not re_sci_notation.match(
                        value) and not value == '0':
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                try:
                    if float(value) < -6.00E+58 or 6.00E+58 < float(value):
                        reason = 'too large or too small'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        self.updateCell(x, '')
                except:
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

                if len(range_list2) > 0:
                    if float(value) < range_list2[0] or float(value) > range_list2[1]:
                        reason = 'out of template range'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Email':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_email.search(value):
                    if parseaddr(value)[1] == '':
                        reason = 'not an email'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Boolean':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_boolean.match(value):
                    reason = 'not a recognised yes/no type'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Currency':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_currency.match(value):
                    reason = 'not a recognised currency'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))


        elif self.type == 'String':
            for x, value in enumerate(self.values):
                self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                 data_start)

        elif self.type == 'Enum':
            self.define_most_least_common()
            for x, value in enumerate(self.least_common):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif self.least_common[x][1] <= 1:
                    freq = 0
                    for index, cell in enumerate(self.values):
                        if cell == value[0]:
                            reason = 'Low frequency of enum value: (%s)' % self.least_common[x][1]
                            tup = (index + invalid_rows_pos[index] + data_start, columnNumber, value[0], reason, index)
                            errors.append(tup)
                            formatted_errors.append(
                                "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                            freq += 1

        elif self.type == 'Sci_Notation':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_sci_notation.match(value):
                    reason = 'not scientific notation'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                try:
                    if float(value) < -6.00E+76 or 6.00E+76 < float(value):
                        reason = 'too large or too small'
                        tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                        errors.append(tup)
                        formatted_errors.append(
                            "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
                        self.updateCell(x, '')
                except:
                    reason = 'not a number'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Identifier':
            if self.data_size != -1:
                size = self.data_size
            else:
                size = len(self.values[0])
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif len(value) != int(size):
                    reason = 'Identifier has length ' + str(len(value)) + ' instead of ' + size
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))
        elif self.type == 'Date':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_date.match(value):
                    reason = 'not a recognised date'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Time':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_time.match(value):
                    reason = 'not a recognised time'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Char':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_char.match(value):
                    reason = 'not a recognised character'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Day':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_day.match(value):
                    reason = 'not a recognised day'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

        elif self.type == 'Hyperlink':
            for x, value in enumerate(self.values):
                if self.check_empty(x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                                    data_start):
                    continue
                elif not re_hyper.match(value):
                    reason = 'not a recognised hyperlink'
                    tup = (x + invalid_rows_pos[x] + data_start, columnNumber, value, reason, x)
                    errors.append(tup)
                    formatted_errors.append(
                        "Row: %d Column: %d Value: %s - %s" % (tup[0] + 1, tup[1] + 1, tup[2], reason))

    def check_empty(self, x, value, columnNumber, errors, formatted_errors, invalid_rows_pos, set_to_ignore,
                    data_start):
        """Checks an individual cell of a column to see if it is empty. If it is set to ignore
        empty cells for this column returns True. If it is not set to ignore, return True and add
        cell to the list of errors. If it is not empty, return False.

        Keyword arguments:
            x -- Integer postion of cell in column.

            value -- value in cell.

            columnNumber -- Number of column that cell is in.

            errors -- List of errors. Numbered from 0. Contains row number (formatted for data
            with incorrect columns removed), column number, cell value, reason for error (empty
            cell) and row number (formatted for data with incorrect columns still present).

            formatted_errors -- List of formatted errors, a human readable version of errors.
            Contains a string listing the row and column in human readable form of the empty cell
            and it's reason for being an error (empty cell).

            invalid_rows_pos -- An array containing a number matching the amount of invalid
            rows that have been removed from analysis by the time that row is accessed. i.e.
            invalid_rows_pos[1] = 2 says that by the time values[1] is evaluated two rows have
            been removed from analysis.

            set_to_ignore -- A set containing integers representing columns set to ignore
            empty values in.

            data_start -- Integer representing the row actual data (not headers) starts on.
        """

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

    def set_Identifier_size(self, size=-1):
        """Sets the size of the data for identifier type"""
        if size == -1:
            self.data_size = len(self.values[0])
        else:
            self.data_size = size
        return self.data_size

    def updateCell(self, pos, new_value):
        """Changes the value of a cell given

            Keyword Arguments:

                pos -- position of cell in column to change

                new_value -- value to set cell too
        """

        self.values[pos] = new_value