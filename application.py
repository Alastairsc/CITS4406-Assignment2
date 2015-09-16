"""Main execution body for Assignment2 project.
"""

import sys
import argparse
import textwrap
import pandas as pd
import os

from data import *
from report import *
from editor import *


def main(*args):
    """Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report).
    """

    filename = args[0]
    if len(args) > 1:
        temp = Template(args[1])
        data = Data(filename, temp)
    else:
        data = Data(filename)
    data.clean()
  #  editor = Editor(data)
    data.pre_analysis()
    data.find_errors()
    data.analysis()
  #  editor.make_corrected(file)
    report = Report(data, filename)
    report.html_report()
            
def get_file_dir(location):
    """Returns the directory of the file with the file name"""
    return location.rpartition('\\')
    
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,\
        description=textwrap.dedent('''\
                Processes Csv files.
        ----------------------------------
        Can process one or more csv files. Can specify template to describe
        data further. Templates can be used to describe one or more csv files.
        If using multiple templates for multiple files list templates in the 
        same order as the files they correspond to.
    '''))
    parser.add_argument('filenames', nargs='+',\
        help='one or more filenames for the processor to analyse')
    parser.add_argument('-t', nargs='+', metavar='template', help='a template for the given files')
    args = parser.parse_args()
    print(args)
    filenames = []
    for file in args.filenames:
        name_ext = os.path.splitext(file)
        print(name_ext)
        if name_ext[1] == '.xls' or name_ext[1] == '.xlsx':
            xls=pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            if len(sheet_names) == 1:
                    df = xls.parse(sheet_names[0], index_col=None, na_values=['NA'])
                    new_name = os.path.splitext(file)[0] + ".csv"
                    df.to_csv(new_name, index=False) 
                    filenames.append(new_name)
            else:
                file_dir = get_file_dir(file)
                if not os.path.exists(file_dir[0] + "\csv_copies"):
                    os.makedirs(file_dir[0] + "\csv_copies")
                    #makes new directory to store new csv files
                for sheet in sheet_names:
                    df = xls.parse(sheet, index_col=None, na_values=['NA'])
                    new_name = file_dir[0] + "\csv_copies\\" + os.path.splitext(file_dir[2])[0] \
                    + "_" + sheet + ".csv"
                    df.to_csv(new_name, index=False)
                    filenames.append(new_name)
        elif(len(args.filenames)<2):
            filenames.append(args.filenames[0])        
    print(args.t)     
    if args.t != None:
        if len(args.t) == 1:
            for name in filenames:
                main(name, args.t[0])
        else:
            for i in range(0, len(filenames)):
                main(filenames[i], args.t[i])
                #TODO keep functionality when files have multiple sheets
    else:
        for name in filenames:
            main(name)
