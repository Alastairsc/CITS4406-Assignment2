__author__ = 'Liam'
"""Main execution body for Assignment2 project.
"""

import sys
from data import *
from report import *


def main():
    """Create Data and Report objects, providing necessary information for them 
    to run analysis and create desired outputs (i.e. HTML report).

    """
    file = sys.argv[1]
    data = Data(file)
    data.clean()
    data.analyse()
    report = Report(data, file)
    report.html_report()


if __name__ == '__main__':
    main()
