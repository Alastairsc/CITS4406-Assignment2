"""Main execution body for Assignment2 project.
"""

import sys
import argparse

from data import *
from report import *
from editor import *

def main(*args):
    """Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report).

    """
    file = args[0]
    if len(args) > 1:
        temp = Template(args[1])
        data = Data(file, temp)
    else:
        data = Data(file)
    data.clean()
  #  editor = Editor(data)
    data.analyse()
  #  editor.make_corrected(file)
    report = Report(data, file)
    report.html_report()
            
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Processes Csv files.')
    parser.add_argument('filenames', nargs='+',\
        help='one or more filenames for the processor to analyse')
    parser.add_argument('-t', metavar='template', default='',help='a template for the given files')
    args = parser.parse_args()
    print (args)
    if args.t != '':
        for name in args.filenames:
            main(name, args.t)
    else:
        for name in args.filenames:
            main(name)
