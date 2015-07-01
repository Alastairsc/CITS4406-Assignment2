"""Generate reports based on data provided via a Data object.

Classes:
Report -- Contains methods to generate and output appropriate HTML for the 
report.
"""

from template import *


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
    
    Variables:
    data -- Reference to Data object.
    file -- Reference to CSV file.
    """
    def __init__(self, data, file):
        """Initialise the Report object and assign local variables.
        
        Arguments:
        data -- The processed CSV data object.
        file -- The filename of the report.
        """
        self.data = data
        self.file_name = file
    
    def empty_columns(self):
        """Return a list of empty rows in the data object."""
        return [column.header for column in self.data.columns if column.empty]
    
    def html_report(self):
        """Write a HTML file based on analysis of CSV file."""
        html = base_template.format(
            header=self.file_name, 
            len_invalid_rows=len(self.data.invalid_rows),
            invalid_rows=self.list_creator(self.data.invalid_rows), 
            empty_columns=self.list_creator(self.empty_columns()),
            len_empty_columns=len(self.empty_columns()),
            len_columns=len(self.data.valid_rows),
            numerical_analysis=self.numerical_analysis(),
            string_analysis=self.string_analysis(),
            enum_analysis=self.enum_analysis()
            )
        html_file = open("{}_report.html".format(self.file_name), "w")
        html_file.write(html)
        html_file.close()

    @staticmethod
    def list_creator(list_items):
        """Return provided list as an unordered HTML list.
        
        Arguments:
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
        Integer in the data object.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Float' or column.type == 'Integer':
                row = [column.header,
                       column.analysis.min,
                       column.analysis.max,
                       column.analysis.mode,
                       column.analysis.mean,
                       column.analysis.median_low,
                       column.analysis.median,
                       column.analysis.median_high,
                       column.most_common[:5]]
                rows += self.row_creator(row)
        return rows
        
    def string_analysis(self):
        """Return HTML string of string analysis on columns of type string 
        in the data object.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'String':
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5]]
                rows += self.row_creator(row)
        return rows
        
    def enum_analysis(self):
        """Return HTML string of enumeration analysis on columns of type Enum 
        in the data object.
        """
        rows = ''
        for column in self.data.columns:
            if column.type == 'Enum':
                row = [column.header,
                       column.analysis.mode,
                       column.most_common[:5]]
                rows += self.row_creator(row)
        return rows
        
    def bool_analysis(self):
        pass
        # Todo: Implement boolean analysis.
