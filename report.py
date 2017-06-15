"""Generate reports based on data provided via a Data object.

Classes:
    Report -- Contains methods to generate and output appropriate HTML for the report.
    
"""
try:
	from .template import *
except:
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

        date_analysis -- Return date based statistics on input.
        
        time_anaysis -- Return time based statistics on input.
        
        day_analysis -- Return day based statistics on input.
        
        hyper_analysis -- Return hyperlink based analyis on input.
        
        list_creator -- Provided a list, returns an unordered html list of values in the list.
        
    Static Methods:
        list_creator -- Provided a list, returns an unordered html list of values in the list.
        
        row_creator -- Provided a list, returns a HTML row of values in the list.
        
        initial_show_items -- Returns the number of items to show initially for each type in the 
        report before hiding them under a 'show more' button.
    
    Variables:
        GRAPH_LIMIT -- How many rows before the graphs will stop displaying every value, but just show a summary

        data -- Reference to Data object, the output from analysis of file_name.
        
        file_name -- Reference to a CSV file containing the data being worked on.

        chart_data -- A String of data that is formatted correctly to be input to a graph API.
    """


    def __init__(self, data, offline=True):
        """Initialise the Report object and assign local variables.
        
        Keyword arguments:
        data -- The processed CSV data object.
        
        file -- The filename of the report.
        """
        self.GRAPH_LIMIT = 10000
        self.data = data
        self.file_name = data.filename
        self.chart_data = ''
        self.offline = offline
        self.types = {
            'Boolean': 'Boolean',
            'Char': 'Character',
            'Currency': 'Currency',
            'Date': 'Date',
            'Datetime': 'Date Time',
            'Day': 'Day of the Week',
            'Email': 'Email Address',
            'Enum': 'Enumerable Set',
            'Float': 'Decimals only',
            'Hyperlink': 'Hyperlink',
            'Identifier': 'Identification code',
            'Integer': 'Integers only',
            'Numeric': 'Number',
            'Sci_Notation': 'Scientific notation',
            'String': 'String',
            'Time': 'Time',
            'Ignored': 'Ignored / not detected'
        }
    
    @staticmethod
    def initial_show_items():
        """Return the number of items to show initially, where clicking 'show more' will expand."""
        return 4

    @staticmethod
    def item_limit():
        """Return the maximum number of items to display if 'show more' is disabled (offline)"""
        return 30

    def empty_columns(self):
        """Return a list of empty columns in the data object."""
        return [column.header for column in self.data.columns if column.empty]
    
    def html_report(self, previous_url=""):
        """Write a HTML file based on analysis of CSV file by calling the various
        type analyses. Returns a string of html.
        """
        if self.offline:
            self.chart_data = '[];'
        html = base_template.format(
            filename = path.split(self.file_name)[1],
            len_invalid_rows=len(self.data.formatted_invalid_rows),
            invalid_rows=self.list_creator(self.data.formatted_invalid_rows), 
            empty_columns=self.list_creator(self.empty_columns()),
            len_empty_columns=len(self.empty_columns()),
            error_columns=self.list_creator(self.data.formatted_errors),
            len_error_columns=len(self.data.errors),
            len_columns=len(self.data.columns[0].values),
            delimiter_type = self.data.delimiter_type,
            num_columns=len(self.data.columns),
            column_details=self.make_header_details(self.data.columns),
            numerical_analysis=self.numerical_analysis(),
            string_analysis=self.string_analysis(),
            identifier_analysis=self.identifier_analysis(),
            enum_analysis=self.enum_analysis(),
            email_analysis=self.email_analysis(),
            currency_analysis =self.currency_analysis(),
            boolean_analysis = self.boolean_analysis(),
            datetime_analysis = self.datetime_analysis(),
            date_analysis = self.date_analysis(),
            time_analysis = self.time_analysis(),
            char_analysis = self.char_analysis(),
            day_analysis = self.day_analysis(),
            hyper_analysis = self.hyper_analysis(),
            previous = previous_url,
            chart_data = self.chart_data
            )
        # gen report for debugging
        return str(html) 


    def list_creator(self, list_items, height=500):
        """Return provided list as an unordered HTML list.
        
        Keyword arguments:
        list_items -- List of items to be turned into HTML.
        """
        itemCount = 0
        if len(list_items) < Report.item_limit():
            html_list = '<ul>'
            if list_items:
                for item in list_items:
                    if not self.offline and itemCount > Report.initial_show_items():
                      html_list += '<li class="hidden">' + str(item) + '</li>'
                    else:
                      html_list += '<li>' + str(item) + '</li>'
            else:
                html_list += '<li>' + 'Empty' + '</li>'
            if not self.offline and itemCount > Report.initial_show_items()+1:
              html_list += "<li class='showMore'>Show More</li>"
            html_list += '</ul>'
        else:
            html_list = '<div style="height: ' + str(height) + '; width: 100%;overflow:auto;"><ul>'
            for item in list_items:
                  html_list += '<li>' + str(item) + '</li>'
            html_list += '</ul></div>'
        if itemCount > Report.item_limit():
            msg = "<p>Only displaying the first " + str(Report.item_limit()) + \
                  " errors. Consider suppressing anomalies using a template.</p>"
            html_list = msg + html_list
        return html_list


    def row_creator(self, row_items, rowNumber = 0, type = 'none', hide = False):
        """Return provided list as HTML rows.
        
        Arguments:
        row_items -- List of items to be turned into HTML.
        """
        html_row=""
        if not self.offline and rowNumber>Report.initial_show_items():
            if rowNumber == Report.initial_show_items()+1:
                html_row = '<tr><td colspan="100%" class="info showMoreTable">Show More</td></tr>'
            html_row += '<tr class="hidden">'
        else:
            html_row += '<tr>'
        for item in row_items:
            if isinstance(item, list) and len(item) > 10:
                html_row += '<td width="10%"><div style="height: 200px;overflow:auto;"><ul style="list-style-type:none; padding-left:0;">'
                for x in item:
                    html_row += '<li>' + str(x) + '</li>'
                html_row += '</ul></div></td>'
            else:
                html_row += '<td>' + str(item) + '</td>'
        #Chart
        if not hide and not self.offline:
            html_row += '<td><a onclick="showChart(\''+type+'\','+str(rowNumber)+',this)" href="#col_analysis">Show Data</a></td>'
        else:
            # html_row += '<td>&nbsp</td>'
            pass
        html_row += '</tr>'
        return html_row
        
    def numerical_analysis(self):
        """Return HTML string of numerical analysis on columns of type Float or 
        Integer in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var numbData = [ "
        for column in self.data.columns:
            if column.type == 'Float' or column.type == 'Integer'\
            or column.type == 'Sci_Notation' or column.type == 'Numeric':
                most_common = column.most_common[:5]
                least_common = column.least_common[:5]
                for i in range(0,len(most_common)):
                    try:
                        tup1 = most_common[i]
                        tup1 = (self.str_to_num(tup1[0]), tup1[1])
                        most_common[i] = (round(tup1[0], 4),tup1[1])
                    except TypeError:
                        pass #non numeric
                    try:
                        tup1 = least_common[i]
                        tup1 = (self.str_to_num(tup1[0]), tup1[1])
                        least_common[i] = (round(tup1[0], 4), tup1[1])
                    except TypeError:
                        pass #non numeric
                header = column.header.rsplit(' ', 2)
                math_stats = [self.shorten(header[0],15) + "<br>" + header[1] + " " + header[2] + "<br>" + self.types[column.type]]
                math_stats.append(self.list_stack(most_common))
                math_stats.append(self.list_stack(least_common))
                math_stats.append(column.analysis.unique)
                math_stats.append("Min: " + str(column.analysis.min) + "<br>Max: " + str(column.analysis.max))
                math_stats.append("Average:<br>" + str(column.analysis.mean) + "<br>Standard Deviation:<br>" +
                                  str(column.analysis.stdev))
                math_stats.append("Lower: " + str(column.analysis.quartile_low) + "<br>Median: " + str(column.analysis.median) +
                                  "<br>Upper: " + str(column.analysis.quartile_up))
                math_stats.append(column.analysis.stDevOutliers)
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                    values = column.values
                    if len(values)>self.GRAPH_LIMIT:
                        values = values[:self.GRAPH_LIMIT]
                    for valueRowNo, value in enumerate(values):
                        try:
                            self.chart_data = ''.join([self.chart_data,"['Row ",str(valueRowNo),"',",str(value),"],"])
                        except:
                            pass
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data, "],"])

                rowNo+=1;
                rows += self.row_creator(math_stats,rowNo,'N')
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows
        
    def string_analysis(self):
        """Return HTML string of string analysis on columns of type string 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var stringData = [ "
        for column in self.data.columns:
            if column.type == 'String':           
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'S')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data , "[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data, "],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows
        
    def enum_analysis(self):
        """Return HTML string of enumeration analysis on columns of type Enum 
        in the data object by accessing the various class variables of the
        columns.
        """
        rowNo = 0;
        rows = ''
        self.chart_data += "var enumData = [ "
        for column in self.data.columns:
            if column.type == 'Enum':
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo += 1;
                rows += self.row_creator(row, rowNo, 'E')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                    for col in column.most_common:
                      self.chart_data = ''.join([self.chart_data , "[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data, "],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows
        
    def email_analysis(self):
        """Return HTML string of email analysis on columns of type email
        in the data objectby accessing the various class variables of the
        columns.
        """      
        rowNo = 0;
        rows = ''
        self.chart_data += "var emailData = [ "
        for column in self.data.columns:
            if column.type == 'Email':
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'Em')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data , "[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data, "],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows
        
    def boolean_analysis(self):
        """Return HTML string of boolean analysis on columns of type boolean
        in the data objectby accessing the various class variables of the
        columns.
        """      
        rowNo = 0;
        rows = ''
        self.chart_data += "var boolData = [ "
        for column in self.data.columns:
            if column.type == 'Boolean':
                row = [column.header,
                       column.analysis.mode,
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique,
                       column.total_true,
                       column.total_false,
                       column.total_yes,
                       column.total_no,
                       column.total_true + column.total_false + column.total_yes + column.total_no]
                rowNo += 1;
                rows += self.row_creator(row, rowNo, 'B')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                    for col in column.most_common:
                      self.chart_data = ''.join([self.chart_data, "[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data, "],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows
        
    def currency_analysis(self):
        """Return HTML string of numerical analysis on columns of type Currency
        in the data object by accessing the various class variables of the
        columns.
        """
        rowNo = 0;
        rows = ''
        self.chart_data += "var currencyData = [ "
        for column in self.data.columns:
            if column.type == 'Currency':
                row = [column.header,
                       column.analysis.min,
                       column.analysis.max,
                       column.analysis.mode,
                       column.analysis.mean,
                       column.analysis.quartile_low,
                       column.analysis.median,
                       column.analysis.quartile_up,
                       column.analysis.stdev,
                       column.analysis.stDevOutliers,
                       column.most_common[:5],
                       column.least_common[:5],
                       column.analysis.unique]
                rowNo += 1;
                rows += self.row_creator(row, rowNo, 'C')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data, "["])
                    self.chart_data = ''.join([self.chart_data , "['Row ','Value'],"])
                    valueRowNo = 0
                    values = column.values
                    if len(values)>self.GRAPH_LIMIT:
                        for value in values[:self.GRAPH_LIMIT]:
                            try:
                                x = float(value)
                                valueRowNo+=1
                                self.chart_data = ''.join([self.chart_data,"['Row ",str(valueRowNo),"',",str(value),"],"])
                            except:
                                pass
                    else:
                        for value in values:
                            try:
                                x = float(value)
                                valueRowNo+=1
                                self.chart_data = ''.join([self.chart_data,"['Row ",str(valueRowNo),"',",str(value),"],"])
                                #self.chart_data += "['Row "+str(valueRowNo)+"',"+str(value)+"],"
                            except:
                                pass
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data , "],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def date_analysis(self):
        """Return HTML string of date analysis on columns of type date 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var dateData = [ "
        for column in self.data.columns:
            if column.type == 'Date':           
                row = [column.header,
                       column.analysis.mode,
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique,
                       column.analysis.dateDF,
                       column.analysis.dateMM,
                       column.analysis.dateJA,
                       column.analysis.dateSN]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'D')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data,"["])
                    self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data,"[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data,"],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def time_analysis(self):
        """Return HTML string of time analysis on columns of type time 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var timeData = [ "
        for column in self.data.columns:
            if column.type == 'Time':           
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique,
                       column.analysis.hourCS[:5],
                       column.analysis.hourCS[-5:]]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'T')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data,"["])
                    self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data,"[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data,"],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def char_analysis(self):
        """Return HTML string of char analysis on columns of type char 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var charData = [ "
        for column in self.data.columns:
            if column.type == 'Char':           
                row = [column.header,
                       column.analysis.mode,
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                self.chart_data = ''.join([self.chart_data,"["])
                self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                for col in column.most_common[:10]:
                  self.chart_data = ''.join([self.chart_data,"[",str(col).replace("(","").replace(")",""),"],"])
                self.chart_data = self.chart_data[:-1]
                self.chart_data = ''.join([self.chart_data,"],"])
                rows += self.row_creator(row,rowNo,'Ch')
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def day_analysis(self):
        """Return HTML string of day analysis on columns of type day 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var dayData = [ "
        for column in self.data.columns:
            if column.type == 'Day':           
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'Dy')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data,"["])
                    self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data,"[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data,"],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def hyper_analysis(self):
        """Return HTML string of hyperlink analysis on columns of type hyper 
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        self.chart_data += "var hyperData = [ "
        for column in self.data.columns:
            if column.type == 'Hyperlink':           
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'H')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data,"["])
                    self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data,"[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data,"],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def identifier_analysis(self):
        """Return HTML string of identifier analysis on columns of type identifier
        in the data objectby accessing the various class variables of the
        columns by accessing the various class variables of the
        columns.
        """
        rowNo = 0;
        rows = ''
        self.chart_data += "var identData = [ "
        for column in self.data.columns:
            if column.type == 'Identifier':           
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo+=1;
                rows += self.row_creator(row, rowNo, 'I')
                if not self.offline:
                    self.chart_data = ''.join([self.chart_data,"["])
                    self.chart_data = ''.join([self.chart_data,"['Row ','Value'],"])
                    for col in column.most_common[:10]:
                      self.chart_data = ''.join([self.chart_data, "[",str(col).replace("(","").replace(")",""),"],"])
                    self.chart_data = self.chart_data[:-1]
                    self.chart_data = ''.join([self.chart_data,"],"])
        self.chart_data = self.chart_data[:-1]
        self.chart_data += "];"
        return rows

    def datetime_analysis(self):
        """Return HTML string of date analysis on columns of type date
        in the data object by accessing the various class variables of the
        columns.
        """
        rows = ''
        rowNo = 0;
        #self.chart_data += "var dateData = [ "
        for column in self.data.columns:
            if column.type == 'Datetime':
                row = [column.header,
                       self.flag_errors(column.analysis.mode),
                       self.flag_errors(column.most_common[:5]),
                       self.flag_errors(column.least_common[:5]),
                       column.analysis.unique]
                rowNo += 1;
                #self.chart_data = ''.join([self.chart_data, "["])
                #self.chart_data = ''.join([self.chart_data, "['Row ','Value'],"])
                #for col in column.most_common[:10]:
                #    self.chart_data = ''.join([self.chart_data, "[", str(col).replace("(", "").replace(")", ""), "],"])
                #self.chart_data = self.chart_data[:-1]
                #self.chart_data = ''.join([self.chart_data, "],"])
                rows += self.row_creator(row, rowNo, 'D', hide=True)
        #self.chart_data = self.chart_data[:-1]
        #self.chart_data += "];"
        return rows

    def gen_html(self, html):
        """Generates html report for the file"""
        filename = path.splitext(self.file_name)[0] + "_report.html"
        html_file = open(filename, "w")
        html_file.write(html)
        html_file.close()
        return filename

    def str_to_num(self, value):
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass #non numeric

    def make_header_details(self, columns):
        """
            Generates list explaining details about all columns in the data
            :param columns to process:
            :return html ready scrollable list of colummn details:
        """
        column_details = []
        for col in columns:
            column_details.append(str(col.header + " - " + self.types[col.type]))
        return self.list_creator(column_details, height=375)

    def shorten(self,string, n):
        """
        Breaks very long strings into stacked html lines separating at known word separators.
        This includes spaces, dashes or underscores
        :param string to be broken:
        :param n approximate length to cut lines:
        :return html ready line:
        """
        if ' ' in string:
            separator = ' '
        elif '-' in string:
            separator = '-'
        elif '_' in string:
            separator = '_'
        else:
            return string
        sentence = string.split(separator)
        result = ""
        line = sentence[0]
        for i, word in enumerate(sentence[1:]):
            if len(line) + len(word) > n:
                result += line + "<br>"
                line = separator + word
            else:
                line += separator + word
            if i == len(sentence) - 2:
                result += line
        return result

    def list_stack(self, list):
        """
        Separates list items and puts them in their own html line. Also flags empty cells and NA cells in red font.
        :return html ready stacked list:
        """
        result = ""
        list = self.flag_errors(list)
        for i, item in enumerate(list):
            if i == len(list) - 1:
                result += str(item)
            else:
                result += str(item) + "<br>"
        return result

    def flag_errors(self, list_in):
        not_list = False
        if not isinstance(list_in, list):
            list_in = [(list_in, 0)]
            not_list = True
        for i, item in enumerate(list_in):
            if item[0] == '' or item[0] == "":
                list_in[i] = ('<font color="red"><EMPTY></font>', item[1])
            elif str(item[0]).lower().strip() == "na" or str(item[0]).lower() == "n/a":
                list_in[i] = ('<font color="red">' + item[0] + '</font>', item[1])
        if not_list:
            return list_in[0][0]
        return list_in