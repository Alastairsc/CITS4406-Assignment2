"""Main execution body for program.
"""

import sys
import argparse
import textwrap
import pandas as pd
import os
#from pympler import classtracker

try:
	from .data import *
	from .report import *
	from .template_reader import *
except SystemError:
	from data import *
	from report import *
	from template_reader import *

def main(*args):
    """
    Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report).
    
        Keyword Arguments:
            args -- Arguments provided to the program at runtime.
    """
    #tr = classtracker.ClassTracker()
    #tr.track_class(Data)
    #tr.create_snapshot()
    filename = args[0]
    print("[Step 1/7] Processing file: ",filename)
    print("[Step 2/7] Reading data")
    if len(args) > 1:
        temp = Template(args[1])
        data = Data(filename, temp)
    else:
        data = Data(filename)
    data.remove_invalid()
    data.create_columns()
    #tr.create_snapshot()
    data.clean()
    print("[Step 3/7] Running pre-analysis")
    data.pre_analysis()
    #tr.create_snapshot()
    print("[Step 4/7] Finding Errors")
    data.find_errors()
    #tr.create_snapshot()
    print("[Step 5/7] Running Analysis")
    data.analysis()
    #tr.create_snapshot()
    report = Report(data)
    str_report = report.html_report()
    print("[Step 6/7] Generating report")
    report.gen_html(str_report)
    #returns string of html, also generates html report for debugging purposes
    print("[Step 7/7] Report Successfully Generated")
    print("Completed analysis for: ",filename)
    #tr.create_snapshot()
    #tr.stats.print_summary()
            
def get_file_dir(location):
    """Returns the directory of the file with the file name
    
    Keyword arguments:
        location -- A file path.
    """
    return location.rpartition('\\')
    
if __name__ == '__main__':
    """If the program is run with application.py as the argument to the command line
    execution begins here. This will process all the command line arguments before 
    proceeding.
    """             
    pathname = os.path.dirname(sys.argv[0])        
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
    filenames = []
    for file in args.filenames:
        print(file)
        name_ext = os.path.splitext(file)
        #TODO handle empty sheets
        if name_ext[1] == '.xls' or name_ext[1] == '.xlsx':
            print("[Step 0/7] Converting to csv file")
            xls=pd.ExcelFile(file)
            sheet_names = xls.sheet_names
            if len(sheet_names) == 1:
                    df = xls.parse(sheet_names[0], index_col=None, na_values=['NA'])
                    new_name = os.path.splitext(file)[0] + ".csv"
                    df.to_csv(new_name, index=False) 
                    filenames.append(new_name)
            else:
                file_dir = os.path.abspath(pathname)
                if not os.path.exists(os.path.join(file_dir, "csv_copies")):
                    os.makedirs(os.path.join(file_dir, "csv_copies"))
                    #makes new directory to store new csv files
                for sheet in sheet_names:
                    df = xls.parse(sheet, index_col=None, na_values=['NA'])
                    new_name = os.path.join(file_dir, "csv_copies" , \
                        os.path.splitext(os.path.split(file)[1])[0] + "_" + sheet + ".csv")
                    df.to_csv(new_name, index=False)
                    filenames.append(new_name)
        elif os.path.isdir(file):
            for dir_files in os.listdir(file):
                if dir_files.endswith(".csv"):
                    filenames.append(os.path.join(file, dir_files))
        else:
            filenames.append(file)   
    if args.t != None:
        if len(args.t) == 1:
            for name in filenames:
                main(name, args.t[0])
        else:
            num_templates = len(args.t)
            num_files = len(filenames)
            if(num_templates == num_files):
                for i in range(0, num_files):
                    main(filenames[i], args.t[i])
            else:
                #TODO keep functionality when excel files have multiple sheets
                print("Error, different number of files and templates")
    else:
        for name in filenames:
            main(name)
