"""Generate reports based on data provided via a Data object.

Classes:
Report -- Contains methods to generate and output appropriate HTML for the report.
"""
try:
	from .template import *
except SystemError:
	from template import *

from os import path

class Report(object):
    """The main report object.
    
    Methods:
        __init__ -- Initialise the object and create required local variables.
    
        empty_columns -- Return empty columns in the data object.
    
        html_report -- Create HTML report and output to file.
    
        list_creator -- Helper method to generate a HTML list from provided input.
    
        row_creator -- Helper method to generate HTML rows from provided input.
    
        numerical_analysis -- Return numerical based statistics on input.
    
        string_analysis -- Return string based statistics on input.
    
        enum_analysis -- Return enumeration based statistics on input.
    
        bool_analysis -- Return boolean based statistics on input.
    
        email_analysis -- Return email based statistics on input.
    
    Variables:
        data -- Reference to Data object.
        
        file -- Reference to CSV file.
    """
    def __init__(self, data, file):
        """Initialise the Report object and assign local variables.
        
        Keyword arguments:
        data -- The processed CSV data object.
        
        file -- The filename of the report.
        """
        self.data = data
        self.file_name = file
    
    def empty_columns(self):
        """Return a list of empty rows in the data object."""
        return [column.header for column in self.data.columns if column.empty]
    
    def html_report(self):
        """Write a HTML file based on analysis of CSV file by calling the various
        type analyses.
            Returns string of html report
        """
        html = base_template.format(
            header= path.basename(self.file_name), 
            len_invalid_rows=len(self.data.invalid_rows),
            invalid_rows=self.list_creator(self.data.invalid_rows), 
            empty_columns=self.list_creator(self.empty_columns()),
            len_empty_columns=len(self.empty_columns()),
            error_columns=self.list_creator(self.data.formatted_errors),
            len_error_columns=len(self.data.errors),
            len_columns=len(self.data.valid_rows),
            numerical_analysis=self.numerical_analysis(),
            string_analysis=self.string_analysis(),
            identifier_analysis=self.identifier_analysis(),
            enum_analysis=self.enum_analysis(),
            email_analysis=self.email_analysis(),
            currency_analysis =self.currency_analysis(),
            boolean_analysis = self.boolean_analysis()
            )
        self.gen_html(html)
        #gen report for debugging
        return str(html) 

    @staticmethod
    def list_creator(list_items):
        """Return provided list as an unordered HTML list.
        
        Keyword arguments:
        list_items -- List of items to be turned into HTML.
        """
        html_list = '<ul>'
        if list_items:
            for item in list_items:
                html_list += '<li>' + str(item) + '</li>'
        else:
            html_list += '<li>' + 'Empty' + '</li>'
        html_list += '</ul>'
        return html_list

    @staticmethod
    def row_creator(row_items):
        """Return provided list as HTML rows.
        
        Arguments:
        row_items -- List of items to be turned into HTML.
        """
        html_row = '<tr>'
        for item in row_items:
            html_row += '<td>' + str(item) + '</td>'
        html_row += '</tr>'
        return html_row
        
    def numerical_analysis(self):
        """Return HTML string of numerical analysis on columns of type Float or 
        Integer in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Float' or column.type == 'Integer'\
            or column.type == 'Sci_Notation':
               # print(column.header)
                math_stats= [column.analysis.min,
                       column.analysis.max,
                       column.analysis.mode,
                       column.analysis.mean,
                       column.analysis.median_low,
                       column.analysis.median,
                       column.analysis.median_high,
                       column.analysis.normDist,
                       column.analysis.stdev,
                       column.analysis.stDevOutliers,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                row = [column.header]
                for stats in math_stats:
                    if not stats == 'N/A':
                        row.append(stats)
                    else:
                        row.append(stats)
                        #causes problems if some columns have different stats to others of
                        #same type
                rows += self.row_creator(row)
        return rows
        
    def string_analysis(self):
        """Return HTML string of string analysis on columns of type string 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'String':           
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                rows += self.row_creator(row)
        return rows
        
    def enum_analysis(self):
        """Return HTML string of enumeration analysis on columns of type Enum 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Enum':
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                rows += self.row_creator(row)
        return rows
        
        
    def email_analysis(self):
        """Return HTML string of email analysis on columns of type email
        in the data objectby accessing the various class variables of the
        columns.
        """      
        rows = ''
        for column in self.data.columns:
            if column.type == 'Email':
                row = [column.header,
                        column.analysis.mode,
                        column.most_common[:5],
                        column.least_common[:5],
                       column.analysis.unique]
                rows += self.row_creator(row)
        return rows
        
    def boolean_analysis(self):
        """Return HTML string of boolean analysis on columns of type boolean
        in the data objectby accessing the various class variables of the
        columns.
        """      
        rows = ''
        for column in self.data.columns:
            if column.type == 'Boolean':
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique,
                       column.total_true,
                       column.total_false,
                       column.total_yes,
                       column.total_no,
                       column.total_true + column.total_false + column.total_yes + column.total_no]
                rows += self.row_creator(row)
        return rows
        
    def currency_analysis(self):
        """Return HTML string of numerical analysis on columns of type Currency
         in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Currency':
                print(column.header)
                row = [column.header,
                       column.analysis.min,
                       column.analysis.max,
                       column.analysis.mode,
                       column.analysis.mean,
                       column.analysis.median_low,
                       column.analysis.median,
                       column.analysis.median_high,
                       column.analysis.normDist,
                       column.analysis.stdev,
                       column.analysis.stDevOutliers,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                rows += self.row_creator(row)
        return rows

    def identifier_analysis(self):
        """Return HTML string of identifier analysis on columns of type identifier
        in the data objectby accessing the various class variables of the
        columns by accessing the various class variables of the
        columns.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Identifier':           
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                rows += self.row_creator(row)
        return rows
        
    def gen_html(self, html):
        """Generates html report for the file"""
        html_file = open("{}_report.html".format(self.file_name), "w")
        html_file.write(html)
        html_file.close()
