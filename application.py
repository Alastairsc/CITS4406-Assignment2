"""Main execution body for Assignment2 project.
"""

import sys
import argparse
import textwrap

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
    if args.t != None:
        if len(args.t) == 1:
            for name in args.filenames:
                main(name, args.t[0])
        else:
            for i in range(0, len(args.filenames)):
                main(args.filenames[i], args.t[i])
    else:
        for name in args.filenames:
            main(name)
