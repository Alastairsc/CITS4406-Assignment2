__author__ = 'Liam'

from template import *


class Report(object):
    def __init__(self, data, file):
        self.data = data
        self.file_name = file
    
    def empty_columns(self):
        return [column.header for column in self.data.columns if column.empty]
    
    def html_report(self):
        html = base_template.format(
            header=self.file_name, 
            len_invalid_rows=len(self.data.invalid_rows),
            invalid_rows=self.list_creator(self.data.invalid_rows), 
            empty_columns=self.list_creator(self.empty_columns()),
            len_empty_columns=len(self.empty_columns()),
            numerical_analysis=self.numerical_analysis(),
            string_analysis=self.string_analysis(),
            enum_analysis=self.enum_analysis()
            )
        html_file = open("{}_report.html".format(self.file_name), "w")
        html_file.write(html)
        html_file.close()
        
    def list_creator(self, list_items):
        html_list = '<ul>'
        if list_items:
            for item in list_items:
                html_list += '<li>' + str(item) + '</li>'
        else:
            html_list += '<li>' + 'Empty' + '</li>'
        html_list += '</ul>'
        return html_list
        
    def row_creator(self, row_items):
        html_row = '<tr>'
        for item in row_items:
            html_row += '<td>' + str(item) + '</td>'
        html_row += '</tr>'
        return html_row
        
    def numerical_analysis(self):
        rows = ''
        for column in self.data.columns:
            if column.type == 'Float' or column.type == 'Integer':
                row = []
                row.append(column.header)
                row.append(column.analysis.min)
                row.append(column.analysis.max)
                row.append(column.analysis.mode)
                row.append(column.analysis.mean)
                row.append(column.analysis.median_low)
                row.append(column.analysis.median)
                row.append(column.analysis.median_high)
                rows += self.row_creator(row)
        return rows
        
    def string_analysis(self):
        rows = ''
        for column in self.data.columns:
            if column.type == 'String':
                row = []
                row.append(column.header)
                row.append(column.analysis.mode)
                row.append(column.most_common[:5])
                rows += self.row_creator(row)
        return rows
        
    def enum_analysis(self):
        rows = ''
        for column in self.data.columns:
            if column.type == 'Enum':
                row = []
                row.append(column.header)
                row.append(column.analysis.mode)
                row.append(column.most_common[:5])
                rows += self.row_creator(row)
        return rows