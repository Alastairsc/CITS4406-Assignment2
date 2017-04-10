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
        #gen report for debugging
        return str(html) 


    def list_creator(self, list_items):
        """Return provided list as an unordered HTML list.
        
        Keyword arguments:
        list_items -- List of items to be turned into HTML.
        """
        itemCount = 0
        if len(list_items) < Report.item_limit():
            html_list = '<ul>'
            if list_items:
                for item in list_items:
                    if not self.offline and itemCount>Report.initial_show_items():
                      html_list += '<li class="hidden">' + str(item) + '</li>'
                    else:
                      html_list += '<li>' + str(item) + '</li>'
            else:
                html_list += '<li>' + 'Empty' + '</li>'
            if not self.offline and itemCount>Report.initial_show_items()+1:
              html_list += "<li class='showMore'>Show More</li>"
            html_list += '</ul>'
        else:
            html_list='<div style="height: 500; width: 100%;overflow:auto;"><ul>'
            for item in list_items:
                  html_list += '<li>' + str(item) + '</li>'
            html_list += '</ul></div>'
        if itemCount > Report.item_limit():
            msg = "<p>Only displaying the first " + str(Report.item_limit()) + " errors. Consider supressing anomalies using a template.</p>"
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
            html_row += '<td>&nbsp</td>'
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
                math_stats= [column.analysis.min,
                       column.analysis.max,
                       column.analysis.mean,
                       column.analysis.quartile_low,
                       column.analysis.median,
                       column.analysis.quartile_up,
                       column.analysis.stdev,
                       column.analysis.stDevOutliers,
                       most_common,
                       least_common,
                       column.analysis.unique]
                header = column.header.rsplit(' ', 2)
                header = header[0] + "<br>" + header[1] + " " + header[2]
                row = [header] #puts column number on next line on header label on report
                for stats in math_stats:
                    if not stats == 'N/A':
                        row.append(stats)
                    else:
                        row.append(stats)
                        #causes problems if some columns have different stats to others of same type
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
                rows += self.row_creator(row,rowNo,'N')
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                        column.analysis.mode,
                        column.most_common[:5],
                        column.least_common[:5],
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
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
                       column.analysis.mode,
                       column.most_common[:5],
                       column.least_common[:5],
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
